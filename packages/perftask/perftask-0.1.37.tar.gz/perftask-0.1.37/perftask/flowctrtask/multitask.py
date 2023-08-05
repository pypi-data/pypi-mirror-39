# -*- coding: utf-8 -*-

"""Multitasking module."""

from __future__ import unicode_literals

import multiprocessing
import time
import copy
#import resource

from ..task import TaskBase, FlowcontrolTaskBase, ShellTask, load_task
from ..message import ServerProxy, ClientProxy
from ..graph import Graph
from ..util import perftask_mp_set_start_method
from ..error import PTUsageError

# NOTE: pid: path id, tid : task id

class MultitaskTask(FlowcontrolTaskBase):
    """launch multiple tasks in parallel
    """

    def __init__(self, parent, tid, path, fragment, argv):

        self.add_data_argument('data', nargs="*", evaluate=True, autoimport=True, help='input data.')

        self.add_option_argument('-r', '--reduce', metavar='expression', action='append', help='subtask data reduction.')
        self.add_option_argument('-s', '--share', metavar='data', action='append', help='data for sharing with subtasks.')
        self.add_option_argument('-n', '--nproc', metavar='N', evaluate=True, help='set the number of processes.')
        self.add_option_argument('--spawn', action="store_true", help='use spawn method.')

        self.num_proc = 1

    def perform(self, targs):

        if not isinstance(self.argv_group, list) or len(self.argv_group) == 0:
            self.parent.warn("No subtask is found for multi-tasking. "\
                             "Skipping multi-tasking.")
            return -1

        if targs.nproc:
            self.num_proc = targs.nproc.vargs[-1]

        if targs.spawn:
            perftask_mp_set_start_method("spawn")
    
        # parent share
        mgr_share = {}
        if targs.share:
            for opt in targs.share:
                for v in opt.vargs:
                    mgr_share[v] = {}
                    mgr_share[v] = self.teval(v)
                for k, v in opt.kwargs.items():
                    mgr_share[k] = {}
                    mgr_share[k] = self.teval(v)

        # create subtasks
        subtasks = {}
        subprocs = {}
        for pid in range(self.num_proc):
            parent_conn, child_conn = multiprocessing.Pipe()
            proc = multiprocessing.Process(target=launch_subtask, args=(pid, child_conn))
            proxy = ServerProxy(self.parent, pid, parent_conn, mgr_share,
                    copy.deepcopy(self.argv_group))
            subtasks[pid] = proxy
            proc.start()
            while not proc.is_alive():
                pass
            subprocs[pid] = proc

        # run subtasks
        finished = {}
        while subtasks:
            for pid in list(subtasks.keys()):
                if subprocs[pid].is_alive():
                    subtask = subtasks[pid]
                    message = subtask.handle_message()
                    if message in (ServerProxy._MP_MSG_TERMINATE, ):
                        finished[pid] = subtasks.pop(pid)
                else:
                    subtasks.pop(pid)

        # join subtasks
        for pid, proc in subprocs.items():
            proc.join()

        forwards = {}
        for pid, proxy in finished.items():
            forwards[pid] = proxy.get_forward()

        # collect data from subtasks
        if targs.reduce:
            env = {}
            for pid, varmap in forwards.items():
                for vname, value in varmap.items():
                    if vname not in env:
                        env[vname] = [None for _ in range(self.num_proc)]
                    env[vname][pid] = value

            for opt in targs.reduce:
                for varg in opt.vargs:
                    self.env[varg] = self.teval(varg, **env)
                for key, value in opt.kwargs.items():
                    self.env[key] = self.teval(value, **env)

        return 0

def launch_subtask(pid, pipe):

    # get argv
    pipe.send((pid, ClientProxy._MP_MSG_ARGV, None))
    pid_from, msgid, argv_group = pipe.recv()

    if pid_from != pid:
        perftask_print("SUBTASK %d: pid mismatch != %d"%(pid, pid_from))
        return

    forward, promote = {}, {}

    try:
        instance = ShellTask(argv_group, proxy=ClientProxy(pid, pipe))
        for t in instance.graph:
            t.env["pid"] = pid
        retval, forward, promote = instance.run(forward, promote)
        instance.parent.terminate(forward)
    except Exception as err:
        pipe.send((pid, ClientProxy._MP_MSG_ERROR, str(err)))

    #pipe.send((pid, ClientProxy._MP_MSG_TERMINATE, forward))
