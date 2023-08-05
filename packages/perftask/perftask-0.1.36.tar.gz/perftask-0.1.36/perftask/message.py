# -*- coding: utf-8 -*-

"""message module."""

from __future__ import unicode_literals

import os
import toml
import copy
import logging
import logging.handlers
import time
import re
from functools import partial
from threading import Lock

from .help import perftask_version
from .util import perftask_print, print_error, stack_floc
from .error import PTInternalError, PTUsageError

if "PERFTASK_CONFIG_HOME" in os.environ:
    config_home = os.path.abspath(os.environ["PERFTASK_CONFIG_HOME"])
else:
    config_home = os.path.abspath(os.path.join(os.path.expanduser("~"), ".perftask"))

_task_dir = os.path.join(config_home, "task")

# TODO: specify (read, write permissions)

cfg_default = {
    "perftask": {
        "version": perftask_version()
    },
    "general": {
        "user": {
            "name": None,
            "email": None,
            "perftask_username": None,
        },
        "last_accessed": None,
        "logging": {
            "path": None
        },
    },
    "history": {
        "list": [],
        "max_items": 1000,
        "max_display": 30,
    },
    "task": {
        "task_root": _task_dir,
        "installed": {},
        "aliases": {},
        "groups": {},
        "max_tasks": 100,
        "max_search": 1000,
    }
}

class Config(object):

    defaultfile = "DEFAULTS"
    metafile = "METAFILE"
    histfile = "HISTFILE"

    def __init__(self):

        # home directory
        if not os.path.isdir(config_home):
            os.makedirs(config_home)

        # defaults
        defaults = os.path.join(config_home, self.defaultfile)
        if not os.path.isfile(defaults):
            with open(defaults, 'w') as f:
                toml.dump(cfg_default, f)
        with open(defaults, 'r') as f:
            self.defaults = toml.load(f)
        self.perftask = self.defaults["perftask"]

        # general config
        metafile = os.path.join(config_home, self.metafile)
        if not os.path.isfile(metafile):
            with open(metafile, 'w') as f:
                toml.dump({}, f)
        self.general = self.defaults["general"]
        with open(metafile, 'r') as f:
            self.general.update(toml.load(f))

        # task directory
        if not os.path.isdir(_task_dir):
            os.makedirs(_task_dir)

        # task config
        metafile = os.path.join(_task_dir, self.metafile)
        if not os.path.isfile(metafile):
            with open(metafile, 'w') as f:
                toml.dump({}, f)
        self.task = self.defaults["task"]
        with open(metafile, 'r') as f:
            self.task.update(toml.load(f))

        histfile = os.path.join(config_home, self.histfile)
        if not os.path.isfile(histfile):
            with open(histfile, 'w') as f:
                toml.dump({}, f)
        self.history = self.defaults["history"]
        with open(histfile, 'r') as f:
            self.history.update(toml.load(f))

    def _cfg(self, *items, **kwargs):

        action = kwargs.get("action", None)
        config = kwargs.get("config", None)
        keysonly = kwargs.get("keysonly", False)
        slicing = kwargs.get("slicing", False)

        cfg = getattr(self, config)

        if action in ("set") and len(items) > 1:
            path = items[:-2]
            target = items[-2]
            value = items[-1]
        elif action == "get":
            if keysonly:
                path = items
            else:
                path = items[:-1]
                target = items[-1]
        elif action in ("add", "del", "len", "has"):
            path = items[:-1]
            target = items[-1]
        name = cfg
        for p in path:
            try:
                name = name[p]
            except KeyError as err:
                raise PTInternalError(str(err))

        if action == "set":
            name[target] = value
        elif action == "get":
            if keysonly:
                if isinstance(name, dict):
                    if slicing:
                        return copy.deepcopy(list(name.keys()[slicing]))
                    else:
                        return copy.deepcopy(list(name.keys()))
                else:
                    return []
            else:
                try:
                    if slicing:
                        return copy.deepcopy(name[target][slicing])
                    else:
                        return copy.deepcopy(name[target])
                except:
                    return []
        elif action == "add" and isinstance(name, list):
            name.append(target)
        elif action == "del":
            try:
                del name[target]
            except:
                pass
        elif action == "has":
            return target in name
        elif action == "len":
            if isinstance(name[target], (list, dict)):
                return len(name[target])
            else:
                return None
        else:
            raise PTInternalError("Config access failed: %s"%str(items))

    def __getattr__(self, name):
        action_types = ("get_", "set_", "add_", "del_", "len_", "has_")
        if len(name) > 4 and name[:4] in action_types:
            if name[4:] in ("general", "task", "history", "perftask"):
                return partial(self._cfg, action=name[:3], config=name[4:])
        raise AttributeError("'Config' object has no attribute '%s'"%name)

    def dump_config(self):

        with open(os.path.join(config_home, self.metafile), 'w') as f:
            toml.dump(self.general, f)

        with open(os.path.join(config_home, "task", self.metafile), 'w') as f:
            toml.dump(self.task, f)

        with open(os.path.join(config_home, self.histfile), 'w') as f:
            toml.dump(self.history, f)

class Manager(object):
    """perftask manager"""

    def __init__(self):

        self.config = Config()
        self.logger = None

    def __getattr__(self, name):

        return getattr(self.config, name)

    def error_exit(self, msg, error_class=PTInternalError):
        raise error_class(msg, **stack_floc(depth=3))

    def turn_logging_on(self, name, level=logging.DEBUG,
            format="%(levelname)-8s [%(fname)s:%(lnum)s@%(ts)d] %(message)s"):

            self.logger = logging.getLogger(name)
            self.logger.propagate = False
            self.logger.setLevel(logging.DEBUG)
            path = self.config.get_general("logging", "path")
            if path:
                fh = logging.handlers.RotatingFileHandler("%s/%s.log"%(path, name),
                        maxBytes=int(1E6), backupCount=10)
            else:
                fh = logging.handlers.RotatingFileHandler("%s.log"%name,
                        maxBytes=int(1E6), backupCount=10)
            fh.setLevel(level)
            #"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            fh.setFormatter(logging.Formatter(format))
            self.logger.addHandler(fh)
            self.log_info("Start logging")

    def turn_logging_off(self):
        if self.logger is not None:
            self.log_info("Stop logging")
            logging.shutdown()
            self.logger = None

    def is_logging_on(self):
        return self.logger is None

    def log(self, level, msg, args, kwargs):

        if level >= logging.ERROR:
            print_error(msg)

        if self.logger is not None:
            c = stack_floc(depth=3)
            fname = os.path.basename(kwargs.pop("filename", c["filename"]))
            lnum = kwargs.pop("lineno", c["lineno"])
            ts = kwargs.pop("ts", int(time.time()))
            extra = {"fname": fname, "lnum": lnum, "ts":ts}
            self.logger.log(level, msg, *args, extra=extra, **kwargs)

    def log_debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, args, kwargs)

    def log_info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, args, kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self.log(logging.WARNING, msg, args, kwargs)

    def log_error(self, msg, *args, **kwargs):
        self.log(logging.ERROR, msg, args, kwargs)

    def log_critical(self, msg, *args, **kwargs):
        self.log(logging.CRITICAL, msg, args, kwargs)

    def log_exception(self, msg, *args, **kwargs):
        if self.logger is not None:
            self.logger.exception(msg, args, kwargs)

    def shutdown(self):
        self.turn_logging_off()

_manager = Manager()

def _threadsafe_wrapper(*vargs, **kwargs):

    func = kwargs.pop("_original_function", None)
    if func is None:
        raise Exception("Manager could not find the original function.")
    with Lock():
        return func(*vargs, **kwargs)

class ManagerProxy(object):

    def __init__(self):

        self._manager = _manager

    def __getattr__(self, name):

        try:
            attr = getattr(self._manager, name)
            if not callable(attr):
                raise AttributeError()
            return partial(_threadsafe_wrapper, _original_function=attr)
        except AttributeError as err:
            raise AttributeError("'Manager' object has no attribute '%s'"%name)

    def log(self, level, msg, args, kwargs):
        c = None
        if "filename" not in kwargs:
            c = stack_floc(depth=3)
            kwargs["filename"] = c["filename"]
        if "lineno" not in kwargs:
            if c is None:
                c = stack_floc(depth=3)
            kwargs["lineno"] = c["lineno"]
        if self._manager is not None:
            self._manager.log(level, msg, args, kwargs)

    def log_debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, args, kwargs)

    def log_info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, args, kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self.log(logging.WARNING, msg, args, kwargs)

    def log_error(self, msg, *args, **kwargs):
        self.log(logging.ERROR, msg, args, kwargs)

    def log_critical(self, msg, *args, **kwargs):
        self.log(logging.CRITICAL, msg, args, kwargs)

class TaskProxy(object):
    """base proxy class for task classes
    """

    def __init__(self, task):

        if not task:
            raise PTInternalError("Proxy can not support None task.")

        self.task = task

class ParentProxy(TaskProxy):

    def __getattr__(self, attr):

        try:
            return getattr(self.task.parent, attr)
        except:
            raise PTUsageError(
                "'ParentProxy' object has no attribute '%s'"%attr)

    def log(self, level, msg, args, kwargs):
        c = None
        if "filename" not in kwargs:
            c = stack_floc(depth=3)
            kwargs["filename"] = c["filename"]
        if "lineno" not in kwargs:
            if c is None:
                c = stack_floc(depth=3)
            kwargs["lineno"] = c["lineno"]
        if self.task.parent is not None:
            self.task.parent.log(level, msg, args, kwargs)

    def log_debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, args, kwargs)

    def log_info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, args, kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self.log(logging.WARNING, msg, args, kwargs)

    def log_error(self, msg, *args, **kwargs):
        self.log(logging.ERROR, msg, args, kwargs)

    def log_critical(self, msg, *args, **kwargs):
        self.log(logging.CRITICAL, msg, args, kwargs)

class RemoteProxy(object):
    (_MP_MSG_FINISHED, _MP_MSG_TERMINATE, _MP_MSG_CLIENTPROXY, _MP_MSG_ARGV,
     _MP_MSG_ERROR, _MP_MSG_PUSH, _MP_MSG_PULL) = range(7)

class ServerProxy(RemoteProxy):

    def __init__(self, parent, pid, pipe, share, argv_group):
        self.parent = parent
        self.pid = pid
        self.pipe = pipe
        self.share = share
        self.argv_group = argv_group
        self.forward = {}
        self.pending_msgs = []

    def handle_message(self):

        msgid = None

        try:
            if self.pipe.poll():
                self.pending_msgs.append(self.pipe.recv())

            if self.pending_msgs:
                sender_pid, msgid, item = self.pending_msgs.pop(0)

                if sender_pid != self.pid:
                    self.parent.log_error("from SUBTASK %d: pid mismatch != %d"%(self.pid, sender_pid))
                    msgid = None
                self.parent.log_debug("from SUBTASK %d: msgid=%d, item=%s"%(self.pid, msgid, item))

                if msgid == self._MP_MSG_ARGV:
                    self.pipe.send((self.pid, ClientProxy._MP_MSG_ARGV, self.argv_group))

                elif msgid == self._MP_MSG_CLIENTPROXY:
                    proxycall = item.pop("__proxycall__", None)
                    if proxycall:
                        vargs = item.pop("__vargs__", [])
                        values = getattr(self.parent, proxycall)(*vargs, **item)
                        self.pipe.send((self.pid, self._MP_MSG_CLIENTPROXY, values))
                    else:
                        msgid = self._MP_MSG_ERROR

                elif msgid == self._MP_MSG_FINISHED:
                    self.forward = item
                    self.pipe.send((self.pid, self._MP_MSG_FINISHED, True))

                elif msgid == self._MP_MSG_PUSH:
                    for var, value in item.items():
                        if var in self.share:
                            if isinstance(self.share, dict):
                                if self.pid in self.share[var]:
                                    # other subtask's variable
                                    self.log_error("Dupulicated subtask variable : %s"%var)
                                else:
                                    self.share[var][self.pid] = value
                            else:
                                # parent variables
                                self.log_error("Dupulicated parent task variable : %s"%var)
                        else:
                            self.share[var] = {}
                            self.share[var][self.pid] = value

                elif msgid == self._MP_MSG_PULL:
                    values = {}
                    share = self.share.copy()
                    share["pid"] = self.pid
                    try:
                        for opt in item:
                            for arg in opt.vargs:
                                values[arg] = eval(arg, share)
                            for v, e in opt.kwargs.items():
                                values[v] = eval(e, share)
                        self.pipe.send((self.pid, self._MP_MSG_PULL, values))
                    except KeyError as err:
                        self.pending_msgs.append((sender_pid, msgid, item))

                elif msgid == self._MP_MSG_TERMINATE:
                    self.pipe.send((self.pid, self._MP_MSG_TERMINATE, None))

                elif msgid == self._MP_MSG_ERROR:
                    self.parent.log_error("from SUBTASK %d: %s"%(self.pid, item))
                    msgid = self._MP_MSG_TERMINATE

                else:
                    self.parent.log_error("from SUBTASK %d: Unknown message id of %d"%(self.pid, msgid))
                    msgid = self._MP_MSG_TERMINATE

        except EOFError as err:

            self.parent.log_error("from SUBTASK %d: End of File Error"%self.pid)
            msgid = self._MP_MSG_TERMINATE
    
        return msgid

    def get_forward(self):
        return self.forward

def _client_wrapper(*vargs, **kwargs):

    func = kwargs.pop("_original_function", None)
    if func is None:
        raise Exception("ClientProxy could not find the original function.")

    pipe = kwargs.pop("_message_pipe", None)
    if pipe is None:
        raise Exception("ClientProxy has no message pipe.")

    msgid = kwargs.pop("_proxy_msg_id", None)
    pid = kwargs.pop("_proxy_pid", None)

    kwargs["__proxycall__"] = func
    kwargs["__vargs__"] = vargs
    pipe.send((pid, msgid, kwargs))
    pid_from, msgid, values = pipe.recv()
    return values

class ClientProxy(RemoteProxy):

    def __init__(self, pid, pipe):

        self.pid = pid
        self.pipe = pipe

    def __getattr__(self, attr):

        try:
            return partial(_client_wrapper, _original_function=attr,
                           _message_pipe=self.pipe, _proxy_msg_id=
                           self._MP_MSG_CLIENTPROXY, _proxy_pid=self.pid)
        except Exception as err:
            raise AttributeError(
                "'ParentProxy' object has no attribute '%s'"%attr)

    def terminate(self, forward):
        self.pipe.send((self.pid, self._MP_MSG_FINISHED, forward))
        pid_from, msgid, argv_group = self.pipe.recv()
        self.pipe.send((self.pid, self._MP_MSG_TERMINATE, None))
        pid_from, msgid, argv_group = self.pipe.recv()

    def pull_data(self, pulls):
        # pulls : variable assignments
        self.pipe.send((self.pid, self._MP_MSG_PULL, pulls))
        pid_from, msgid, pulled = self.pipe.recv()
        if pid_from == self.pid and msgid == self._MP_MSG_PULL:
            return pulled
        elif pid_from != self.pid:
            self.log_warn("pid mismatch: %d != %d"%(pid_from, pid))
        else:
            self.log_warn("message id mismatch: %d != %d"%(msgid, self._MP_MSG_PULL))

    def push_data(self, pushes):
        # pushes : dict of values
        self.pipe.send((self.pid, self._MP_MSG_PUSH, pushes))

    def error_exit(self, msg, error_class=PTInternalError):
        self.pipe.send((self.pid, self._MP_MSG_ERROR, (msg, error_class)))

def parent_proxies(proxy):

    while proxy:
        if hasattr(proxy, "task") and hasattr(proxy.task, "parent") and \
            isinstance(proxy.task.parent, (TaskProxy, RemoteProxy)):
            proxy = proxy.task.parent
            yield proxy
        else:
            proxy = None
