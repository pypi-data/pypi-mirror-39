# -*- coding: utf-8 -*-

"""Repeating task module."""

from __future__ import unicode_literals

from ..error import PTUsageError
from ..task import FlowcontrolTaskBase, ParentProxy, load_task


class RepeatTask(FlowcontrolTaskBase):
    """launch tasks multiple times in sequence
    """

    def __init__(self, parent, tid, path, fragment, argv):

        self.add_data_argument('loopctr', help='loop control, an integer or any expression can be used in "for" or "while" statement.')

        self.add_option_argument('-t', '--take', metavar='expr', action='append', help='data from last subtask')
        self.add_option_argument('-f', '--feed', metavar='expr', evaluate=True, autoimport=True, action='append', help='data to first subtask.')

    def _run(self, forward, promote):

        for task in self.subtasks:
            retval, forward, promote = task.run(forward, promote)

        return retval, forward, promote

    def _load_subtasks(self):

        self.subtasks = []

        for tid, task_argv in enumerate(self.argv_group):

            if not task_argv:
                continue

            task_instance = load_task(tid, task_argv, self.parent, ParentProxy(self))
            if task_instance:
                self.subtasks.append(task_instance)

        if len(self.subtasks) == 0:
            self.parent.error_exit("No subtask is found.")

    def perform(self, targs):

        if not isinstance(self.argv_group, list) or len(self.argv_group) == 0:
            self.parent.warn("No subtask is found to repeat. "\
                             "Skipping repeat task.")
            return -1

        self._load_subtasks()

        loopseq  = None
        loopcond = None

        if targs.loopctr.isdigit():
            loopidx = int(eval(targs.loopctr, None, self.env))
            loopseq = range(loopidx)
        else:
            try:
                _tmp  = eval(targs.loopctr, None, self.env)
                [t for t in _tmp]
                loopseq = _tmp
            except (TypeError, NameError):
                pass

        forward = {}
        promote = {}

        if targs.feed:
            for opt in targs.feed:
                forward.update(opt.kwargs)

        if loopseq:

            for cnt, val in enumerate(loopseq):

                forward.update({'cnt': cnt, 'val': val})
                retval, forward, promote = self._run(forward, promote)
        else:
            try:
                cnt = 0
                while eval(targs.loopctr, {'cnt': cnt, 'val': None}, self.env):

                    forward.update({'cnt': cnt, 'val': None})
                    retval, forward, promote = self._run(forward, promote)
                    cnt += 1

            except Exception as err:
                self.parent.error_exit(str(err), error_class=PTUsageError)


        if targs.take:
            forward.update(promote)
            for opt in targs.take:
                for k, v in opt.kwargs.items():
                    try:
                        self.env[k] = eval(v, None, forward)
                    except:
                        pass

        return 0

