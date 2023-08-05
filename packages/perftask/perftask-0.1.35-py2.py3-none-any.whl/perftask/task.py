# -*- coding: utf-8 -*-

"""help module."""

from __future__ import unicode_literals

import sys
import os
import re
import abc
import ast
import itertools
import collections
import argparse
import zipfile
import tempfile
import shutil
import toml
import copy
import shlex
import logging

from .message import ParentProxy, ClientProxy, ManagerProxy, parent_proxies, config_home
from .graph import Graph
from .error import PTInternalError, PTUsageError, PTTestError, PTNormalExit, PTNameError
from .util import (name_match, perftask_import, extract_zipfile, urlparse,
        stack_floc, urlopen, HTTPError, URLError, split_taskname, BytesIO,
        StringIO, perftask_print, load_pymod)

# {[0]},  {[1:3]}, {[:2]}, {[":2"]}
_re_slice = re.compile('{\\s*\\[\\s*(?P<slice>["\']?[\\s:\\d]+["\']?)\\s*\\]\\s*}', re.I)

_re_name = re.compile("name\\s['\"](?P<name>\\w+)['\"]\\sis\\snot\\sdefined")

_perftask_arguments = ("evaluate", "autoimport")

def _is_managed(task_loc):
    relpath = os.path.relpath(task_loc, config_home)
    return os.path.join(config_home, relpath) == task_loc
    
def locate_tasks(argv, manager, tempdir, search_pipfile):
    """locate task and search virtual environment setup

    A task could be downloaded from online and unzip if necessary
    """

    if not argv:
        raise PTInternalError("Blank argument!")

    argv_group = [list(group) for k, group in itertools.groupby(argv,
                  lambda x: x == "--") if not k]

    pipfile = None

    group_idx = 0
    search_depth = 0
    max_tasks = manager.get_task("max_tasks")
    max_search = manager.get_task("max_search")

    while group_idx < len(argv_group):

        if len(argv_group) > max_tasks:
            manager.error_exit("The number of tasks exceeds limit.")

        if search_depth > max_search:
            manager.error_exit("The number task search exceeds iteration limit.")

        search_depth += 1

        # recover aliased command if necessary
        task_argv = argv_group[group_idx]
        task_loc, fragment = split_taskname(task_argv[0])

        if not os.path.exists(task_loc) and task_loc in manager.get_task("aliases", keysonly=True):

            alias_def = manager.get_task("aliases", task_loc)

            if not alias_def:
                raise PTInternalError("'{0}' is not aliased name.".format())

            alias_tasks = alias_def["tasks"]

            # NOTE: assumes that task_argv does not contain any optional argument

            new_alias_group = []
            for alias_argv in alias_tasks:
                new_argv = [alias_argv[0]]
                for alias_idx in range(1, len(alias_argv)):
                    match = _re_slice.match(alias_argv[alias_idx])
                    # TODO: supports findall
                    if match:
                        try:
                            mstr = match.group("slice")
                            targv = alias_argv[alias_idx][:match.start()]
                            if mstr[0] in ('"', "'") and mstr[0] == mstr[-1]:
                                if mstr[1:-1].isdigit():
                                    mlist = eval("[task_argv[1:]["+mstr[1:-1]+"]]")
                                else:
                                    mlist = eval("task_argv[1:]["+mstr[1:-1]+"]")
                                targv += " "
                                q = '"' if mstr[0] == "'" else "'"
                                targv += " ".join([ '%s%s%s'%(q, mstr[0] + m + mstr[0], q) for m in mlist])
                            else:
                                if mstr.isdigit():
                                    mlist = eval("[task_argv[1:]["+mstr+"]]")
                                else:
                                    mlist = eval("task_argv[1:]["+mstr+"]")
                                targv += " "
                                targv += " ".join(['"%s"'%m for m in mlist])
                            targv += alias_argv[alias_idx][match.end():]
                            new_argv.extend(shlex.split(targv))
                        except IndexError:
                            manager.error_exit("Aliasing input seems not provided.",
                                               error_class=PTUsageError)
                    else:
                        new_argv.append(alias_argv[alias_idx])
                if "--log-all" in argv:
                    new_argv.append("--log")
                elif "--log" in argv:
                    new_argv.append("--log")
                    argv.remove("--log")
                new_alias_group.append(new_argv)
            argv_group = argv_group[:max(0, group_idx-1)] + new_alias_group + \
                         argv_group[min(len(argv_group), group_idx+1):]
            continue

        # download a task if necessary
        task_argv = argv_group[group_idx]
        task_loc, fragment = split_taskname(task_argv[0])

        url = urlparse(task_loc)

        if url.netloc:

            try:

                with urlopen(task_loc) as fnet:

                    if tempdir is None:
                        tempdir = tempfile.mkdtemp()
                    task_path = os.path.join(tempdir, os.path.basename(url.path))

                    rdata = fnet.read()
                    with open(task_path, 'wb') as floc:
                        floc.write(rdata)

                    fragment_str = "#" + fragment if fragment else ""
                    task_argv[0] = task_path + fragment_str

            except (HTTPError, URLError) as e:
                manager.error_exit(str(e))


        # locate task
        task_argv = argv_group[group_idx]
        task_loc, fragment = split_taskname(task_argv[0])

        taskdir = None

        # unzip a package if necessary
        if zipfile.is_zipfile(task_loc):

            if tempdir is None:
                tempdir = tempfile.mkdtemp()

            taskdir = os.path.join(tempdir, str(group_idx))
            os.makedirs(taskdir)

            extract_zipfile(task_loc, outdir=taskdir)

            task_path = os.path.join(taskdir, "PERFTASK")
            if os.path.isfile(task_path):
                fragment_str = "#" + fragment if fragment else ""
                task_argv[0] = task_path + fragment_str
            else:
                shutil.rmtree(tempdir)
                raise PTUsageError("The zipfile is not a perftask package.")

        elif os.path.isfile(task_loc) and not _is_managed(task_loc):
            taskdir = os.path.dirname(task_loc)

        elif os.path.isdir(task_loc) and not _is_managed(task_loc):
            taskdir = os.path.abspath(os.path.join(task_loc, ".."))

        # locate installed task if necessary
        elif manager.has_task("installed", task_loc):

            task_root = manager.get_task("task_root")
            rel_path = manager.get_task("installed", task_loc, "path")
            task_path = os.path.join(task_root, rel_path)
            taskdir = os.path.dirname(task_path)
            if os.path.exists(task_path):
                fragment_str = "#" + fragment if fragment else ""
                task_argv[0] = task_path + fragment_str
            else:
                manager.error_exit("task does not exist: {0}.".format(task_path))

        if group_idx == 0 and search_pipfile and taskdir:
            pipfile_path = os.path.join(taskdir, "Pipfile")
            if os.path.isfile(pipfile_path):
                pipfile = pipfile_path

        group_idx += 1

    return argv_group, tempdir, pipfile

def load_task(tid, argv, parent_proxy, task_proxy):

    if len(argv) == 0:
        parent_proxy.error_exit("Task argument is wrong: %s"%str(argv))

#    def load_mod(head, base):
#        sys.path.insert(0, head)
#        m = perftask_import(base)
#        sys.path.pop(0)
#        return m

    taskpath, fragment = split_taskname(argv[0])

    task_class = None

    if os.path.exists(taskpath):

        npath = os.path.abspath(os.path.realpath(taskpath))

        mods = []

        head, base = os.path.split(taskpath)

        if base == "PERFTASK":
            with open(taskpath) as f:
                meta = toml.load(f)
                taskpath = os.path.join(head, meta['tasks'][meta['entry']])
                fragment = meta.get('fragment', fragment)

        if os.path.isfile(taskpath):
            head, base = os.path.split(taskpath)
            if base.endswith(".py"):
                mods.append(load_pymod(head, base[:-3]))
        elif os.path.isdir(taskpath):
            if os.path.isfile(os.path.join(taskpath, "__init__.py")):
                head, base = os.path.split(taskpath)
                mods.append(load_pymod(head, base))

        candidates = {}
        for mod in mods:
            for name in dir(mod):
                if not name.startswith("_"):
                    obj = getattr(mod, name)
                    if (type(obj) == type(TaskBase) and
                        issubclass(obj, TaskBase) and
                        obj not in (TaskBase, Task, GroupTaskBase)):
                        candidates[name] = obj

        if candidates:
            if fragment:
                task_class = candidates.get(fragment, None)
                if task_class is None:
                    parent_proxy.error_exit("No task is found."\
                                            " Please check the name of task class.")
            elif len(candidates) == 1:
                task_class = candidates.popitem()[1]
            else:
                parent_proxy.error_exit("More than one frame are found."\
                                  "Please add fragment to select one: %s"%\
                                  list(candidates.keys()))

            if task_class is not None:
                task_instance = task_class(task_proxy, tid, taskpath, fragment, argv[1:])
                task_instance.argv = argv[1:]
                return task_instance

    else:

        # TODO : add group task's own argument handling

        task = parent_proxy.get_task("groups", taskpath)

        if task:

            argv_group = task['tasks']

            gtask = GroupTaskBase(parent_proxy, -1, taskpath, fragment, argv[1:])

            prev_task = None
            for tid, task_argv in enumerate(argv_group):
                prev_task = gtask.add_task(tid, task_argv, prev_task, task_proxy.__class__)

            return gtask

        else:
            from .builtin import flowcontrol_tasks, std_tasks

            task_names = name_match(taskpath, flowcontrol_tasks)
            if len(task_names) == 1:
                task_class = flowcontrol_tasks.get(task_names[0], None)
            elif len(task_names) > 1:
                parent.error_exit("Given task name, '{0}', matches multiple tasks: {1}"\
                                  .format(taskpath, str(task_names)))
            else:
                task_names = name_match(taskpath, std_tasks)
                if len(task_names) == 1:
                    task_class = std_tasks.get(task_names[0], None)
                elif len(task_names) > 1:
                    parent.error_exit("Given task name, '{0}', matches multiple tasks: {1}"\
                                      .format(taskpath, str(task_names)))

            if task_class is not None:
                task_instance = task_class(task_proxy, tid, taskpath, fragment, argv[1:])
                task_instance.argv = argv[1:]
                return task_instance

    return None

class Option(object):

    def __str__(self):
        out = []
        ctx = []
        for c in self.context:
            ctx.append(c + "@")
        for v in self.vargs:
            out.append(v)
        for k, v in self.kwargs.items():
            out.append(k+"="+v)
        return "".join(ctx)+",".join(out)

class TaskBase(object):

    def __new__(cls, parent_proxy, tid, path, fragment, argv):
        """task constructor

        Arguments:

            `parent` argument represents a direct upper-level task of this
            task. Most likely, this task was generated and invoked by `parent`.
            `parent` is not an actual task, but a proxy of parent task. Please
            see :ref:`task_organization` for details. Generally,`parent`
            provides mgmtistration services like configuration data access.

            `path` is a resolved location of this task. This path could be
            different from what user specified in command-line.

            `argv` is a resolved command-line arguments of this taks. This
            argv again could be different from original input by user.

        In addition to usual initialization work in this method, user
        can several task-specific work using arguments of this method.

        Using `self.add_data_argument`, user can specify its own positional
        arguments to get user input through command line. The syntax is
        the same to Python `argparse`'s `add_argument` method plus two additional
        keyword arguments: : `evaluate` and `autoimport`. With `evalute=True`,
        perftask invokes `eval` Python built-in function to convert string
        arguments to Python objects. `autoimport` enables to automatically
        import Python module in case of NameError.
        """

        obj = super(TaskBase, cls).__new__(cls)

        obj.parent = parent_proxy
        obj.tid = tid
        obj.path = path
        obj.taskname = os.path.basename(path)
        obj.fragment = fragment
        obj.argv = argv

        obj._targs = None
        obj._help = None
        obj._args_temp = {"dargs": [], "kargs": [], "cargs": []}
        obj.env = {"__builtins__": __builtins__, "tid": tid}
        obj.forward = {}
        obj.promote = {}

        def add_common_argument(*vargs, **kwargs):
            obj._args_temp['cargs'].append((vargs, kwargs))

        # TODO : support this
        #add_common_argument('--name', metavar='name',
        #    help="define human-readable name of this task")

        add_common_argument('--import-function', metavar='function',
            action='append', help="import Python function into a task's namespace")
        add_common_argument('--import-module', metavar='module',
            action='append', help="import Python module into a task's namespace")
        
        add_common_argument('--calc', metavar='assignment', evaluate=True,
            action='append', help='python code for generating a variable.')
        add_common_argument('--print', metavar='variable', dest='printvar',
            action='append', help='show content of a variable.')

        add_common_argument('--assert-input', metavar='boolexpr',
            action='append', help='unittest before performing task.')
        add_common_argument('--assert-output', metavar='boolexpr',
            action='append', help='unittest after performing task.')
        add_common_argument('--assert-forward', metavar='boolexpr',
            action='append', help='unittest for forward data.')
        add_common_argument('--assert-promote', metavar='boolexpr',
            action='append', help='unittest for promote data.')
        add_common_argument('--assert-stdout', metavar='boolexpr',
            action='append', help='unittest for standard output.')
        add_common_argument('--assert-stderr', metavar='boolexpr',
            action='append', help='unittest for standard error.')

        add_common_argument('--log', action='store_true',
            help='turn on logging')

        if not issubclass(cls, MgmtTask):
            add_common_argument('--forward', metavar='variable', action='append',
                help='forward local variable to next task.')
            add_common_argument('--promote', metavar='variable', action='append',
                help='promote local variable to upper level.')
            add_common_argument('--venv', action='store_true',
                help='run task using virtualenv')
            add_common_argument('--no-venv', action='store_true',
                help='run task without virtualenv')

        #if issubclass(cls, FlowcontrolTask):
        #    add_common_argument('--group', metavar='group_name',
        #        help='define a group name of the task.')

        if any(isinstance(p, ClientProxy) for p in parent_proxies(parent_proxy)):
            add_common_argument('--push', metavar='data', action='append',
                help='put data for sharing.')
            add_common_argument('--pull', metavar='variable', action='append',
                help='get data from the other task.')

        obj.log_info("Task '%s' is created."%obj.taskname)

        return obj

    def __getnewargs__(self):
        return self.parent, self.tid, self.path, self.fragment, self.argv

    @abc.abstractmethod
    def perform(self, targs):
        """primary place to implement task.

        All **Task-class** should implement this method. To define task,
        user writes Python code inside of this method.

        `perftask` provides several services that help to build task.

        `targs` argument holds all parsed command-line arguments. There
        are several command-line arguments that are available to all tasks.
        Please see :ref:`task_commandline_argument` for details. User also
        can add its own command-line arguments using `add_data_argument`
        and/or `add_option_argument` methods inside of `__init__`
        function. Please read below for details on `__init__` method.

        All **Task-class** maintains its own namespace in `self.tenv`.
        By having this namespace, user can process information seperatly
        from the namespace where the code itself lives in. To support
        this independant information processing, `perftask` provides a
        task version of Python built-in function of `eval` as `self.teval`.
        `perftask` considers Python code in this method as incomplete.
        Rather, Python code in this method is treated as a skeleton of final
        task code. The final task code is completed when user provides
        task configuration through command-line arguments. `self.teval`
        methods is a fundamental tool to convert user-provided command-
        line arguments to executable Python code in this method.

        Return value of this function is important to share information
        between tasks. The syntax of return statement is following.

        .. code-block:: python

            # four possible return statements of perform method

            return None
            return int
            return int, dict1
            return int, dict1, dict2

        First return argument is used to return value to invoking shell when
        the task is invoked as a command-line program. Second return
        argument of `dict1` is a Python dictionary or None. If it is Python
        dictionary, it should have a form of { string: any Python object, ...}.
        All the Python object in the dictionary will be available to `self.tenv`
        of next task that is linked after this task in the name of the `string`
        keys.  This way of data sharing is called `forwarding` in perftask.
        Third return argument of `dict2` is a Python dictionary or None.
        Similar to dict1, the content of `dict2` is available to `self.tenv` of
        next task.  Different to dict1, the content of `dict2` will be avilable
        beyond next task among all the tasks under the same parent task.
        This is called `promoting` in perftask.
        """
        pass

    def teval(self, expr, **kwargs):

        def _teval(_expr, _env, _autoimport, _kwargs):
            trynext = True
            while trynext:
                trynext = False
                try:
                    return eval(_expr, _env, _kwargs)
                except SyntaxError as err:
                    self.parent.error_exit('SYNTAX: near "{0}"'.format(_expr))
                except TypeError as err:
                    self.parent.error_exit('TYPE: %s from %s'%(str(err), _expr))
                except NameError as err:
                    if _autoimport:
                        match = _re_name.match(str(err))
                        if match:
                            name = match.group('name')
                            try:
                                mod = perftask_import(match.group('name'))
                                if mod:
                                    _env[name] = mod
                                    trynext = True
                                else:
                                    self.parent.error_exit(str(err),
                                            error_class=PTNameError)
                            except ImportError as err:
                                self.parent.error_exit(str(err),
                                        error_class=PTNameError)
                    else:
                        self.parent.error_exit(str(err), error_class=PTNameError)

        autoimport = kwargs.get("autoimport", False)
        env = dict((k,v) for k,v in self.env.items())

        retval = None

        if type(expr) == type(u"A"):
            retval = _teval(expr, env, autoimport, kwargs)
        elif isinstance(expr, list):
            retval = []
            for _e in expr:
                retval.append(_teval(_e, env, autoimport, kwargs))
        elif isinstance(expr, dict):
            retval = {}
            for k, _e in expr.items():
                retval[k] = _teval(_e, env, autoimport, kwargs)

        return retval

    def teval_option(self, val, evaluate, autoimport):

        def _p(*argv, **kw_str):
            return list(argv), kw_str

        obj = Option()

        if isinstance(val, str) or type(val) == type("A"):
            items = [v.strip() for v in val.split("@")]
            setattr(obj, 'context', items[:-1])

            if evaluate:
                eval_out = self.teval('_p({0})'.format(items[-1]), _p=_p, autoimport=autoimport)
                if eval_out:
                    obj.vargs, obj.kwargs = eval_out
                else:
                    self.parent.error_exit("syntax error at '{0}'.".format(str(items[-1])))
            else:
                obj.vargs, obj.kwargs = self.parse_literal_args(items[-1])
        else:
            obj.context = []
            obj.vargs = [val]
            obj.kwargs = {}

        return obj

    def parse_literal_args(self, expr):

        lv = []
        lk = {}

        expr_items = expr.split(",")
        text = ""
        while expr_items:

            if text:
                text = text + "," + expr_items.pop(0)
            else:
                text = expr_items.pop(0)
            if not text:
                continue

            try:
                tree = ast.parse("func({0})".format(text))
                args = tree.body[0].value.args
                keywords = tree.body[0].value.keywords
                if len(args) > 0 and len(keywords):
                     self.error_exit("Both of args and keywords are found during argument parsing.")

                if len(args) > 0:
                    lv.append(text.strip())
                elif len(keywords) > 0:
                    key, val = text.strip().split("=", 1)
                    if val:
                        lk[key] = val
                text = ""

            except Exception as err:
                pass

        if not lv and not lk:
            lv.append(expr)

        return lv, lk


    def run(self, forward, promote):

        if promote:
            self.env.update(promote)
        if forward:
            self.env.update(forward)

        if "-h" in self.argv or "--help" in self.argv:

            if self._help is None:

                help_parser = argparse.ArgumentParser(prog="", add_help=False)
                for cvargs, ckwargs in self._args_temp['cargs']:
                    ckwargs = dict((k,v) for k,v in ckwargs.items() if k not in (
                                "evaluate", "autoimport"))
                    help_parser.add_argument(*cvargs, **ckwargs)

                _help = help_parser.format_help()
                pos = _help.find("optional arguments:\n")
                if not isinstance(self, MgmtTask) and pos > 0:
                    common_option_help = "common arguments:\n" + _help[pos+20:]
                else:
                    common_option_help = ""


                dummy_parser = argparse.ArgumentParser(prog="perform "+self.taskname,
                               formatter_class=argparse.RawTextHelpFormatter,
                               epilog=common_option_help)

                dummy_args = self._args_temp['dargs'] + self._args_temp['kargs']
                for dvargs, dkwargs in dummy_args:
                    dkwargs = dict((k,v) for k,v in dkwargs.items() if k not in (
                                "evaluate", "autoimport"))
                    dummy_parser.add_argument(*dvargs, **dkwargs)

                if not isinstance(self, MgmtTask):
                    dummy_parser.add_argument("--common-argument", metavar="",
                        help='task common arguments. See below.')

                #dummy_parser.parse_args(["-h"])
                self._help = dummy_parser.format_help()

            perftask_print(self._help)
            raise PTNormalExit()

        parser = argparse.ArgumentParser(prog="perform "+self.taskname, add_help=False)

        if not self._args_temp['dargs'] and not isinstance(self, MgmtTask):
            self.add_data_argument("D", metavar='<input>', autoimport=False,
                                   nargs="*", help='input data')

        datainputs = collections.OrderedDict()

        for vargs, kwargs in self._args_temp['dargs']:
            data_evaluate = kwargs.get("evaluate", False)
            data_autoimport = kwargs.get("autoimport", False)
            _kwargs = dict((k,v) for k,v in kwargs.items() if k not in
                      _perftask_arguments)
            parser.add_argument(*vargs, **_kwargs)
            data_dest = parser._actions[-1].dest
            data_type = parser._actions[-1].type
            datainputs[data_dest] = (data_evaluate, data_autoimport, data_type)

        options = collections.OrderedDict()
        opt_args = self._args_temp['kargs'] + self._args_temp['cargs']
        for vargs, kwargs in opt_args:
            opt_evaluate = kwargs.get("evaluate", False)
            opt_autoimport = kwargs.get("autoimport", False)
            _kwargs = dict((k,v) for k,v in kwargs.items() if k not in
                      _perftask_arguments)
            parser.add_argument(*vargs, **_kwargs)
            opt_dest = parser._actions[-1].dest
            opt_type = parser._actions[-1].type
            options[opt_dest] = (opt_evaluate, opt_autoimport, opt_type)

        if "version" not in options:
            parser.add_argument('--version', action='version',
                version="'{0}' generic version 0.1.0".format(self.taskname))

        self._targs = parser.parse_args(self.argv)

        self.log_info("Begin task '%s'"%self.taskname)

        if self._targs.import_module:
            for modpath in self._targs.import_module:
                if os.path.exists(modpath):
                    head, base = os.path.split(modpath)
                    modname, ext = os.path.splitext(base)
                    if ext == ".py":
                        sys.path.insert(0, head)
                        mod = perftask_import(modname)
                        sys.path.pop(0)
                        if mod:
                            self.env[modname] = mod
                else:
                    try:
                        mod = perftask_import(modpath)
                        if mod:
                            self.env[modpath] = mod
                    except ImportError as err:
                        self.parent.log_critical("WARNING: module, '{}', is not imported.".
                                       format(modname))

        if self._targs.import_function:
            for modname_funcs in self._targs.import_function:
                opt = self.teval_option(modname_funcs, False, False)
                if os.path.exists(opt.context[0]):
                    head, base = os.path.split(opt.context[0])
                    modname, ext = os.path.splitext(base)
                    if ext == ".py":
                        sys.path.insert(0, head)
                        mod = perftask_import(modname)
                        sys.path.pop(0)
                        if mod:
                            for func in opt.vargs:
                                fobj = getattr(mod, func, None)
                                if callable(fobj):
                                    self.env[func] = fobj
                else:
                    self.parent.log_critical("WARNING: function import failed: {}".
                                   format(modname_funcs))

        # end of self._targs check

        D = []

        for data_dest, (data_evaluate, data_autoimport, data_type) in \
            datainputs.items():

            val = getattr(self._targs, data_dest, None)

            if val:
                if data_type in (None, str) and (data_evaluate is True or \
                   data_evaluate in ("yes", "true")):

                    if isinstance(val, (list, tuple)):
                        for idx1, val2 in enumerate(val):
                            if val2:
                                if isinstance(val2, (list, tuple)):
                                    for idx2 in range(len(val2)):
                                        val2[idx2] = self.teval(val2[idx2],
                                                     autoimport=data_autoimport)
                                        D.append(val2[idx2])
                                else:
                                    val[idx1] = self.teval(val2,
                                                autoimport=data_autoimport)
                                    D.append(val[idx1])
                    else:
                        setattr(self._targs, data_dest, self.teval(val,
                                autoimport=data_autoimport))
                        D.append(getattr(self._targs, data_dest))
                else:
                    if isinstance(val, (list, tuple)):
                        D.extend(val)
                    else:
                        D.append(val)

        if D:
            self.env["D"] = D
        elif "D" not in self.env:
            self.env["D"] = []

        if self._targs.calc:
            for calc in self._targs.calc:
                obj = self.teval_option(calc, True, False)
                self.env.update(obj.kwargs)

        for opt_dest, (opt_evaluate, opt_autoimport, opt_type) in \
            options.items():

            if opt_dest in ("import_module", "import_function", "calc", "log"):
                continue

            val = getattr(self._targs, opt_dest, None)

            if val:
                if opt_type in (None, str):
                    if isinstance(val, (list, tuple)):
                        for idx1, val2 in enumerate(val):
                            if val2:
                                if isinstance(val2, (list, tuple)):
                                    for idx2 in range(len(val2)):
                                        if opt_evaluate is True or \
                                           opt_evaluate in ("yes", "true"):
                                            obj = self.teval_option(val2[idx2],
                                                  True, opt_autoimport)
                                        else:

                                            obj = self.teval_option(val2[idx2],
                                                  False, opt_autoimport)
                                        val2[idx2] = obj
                                elif opt_evaluate is True or opt_evaluate in \
                                     ("yes", "true"):
                                    obj = self.teval_option(val2, True,
                                          opt_autoimport)
                                else:
                                    obj = self.teval_option(val2, False,
                                          opt_autoimport)
                                val[idx1] = obj
                    else:
                        if opt_evaluate is True or opt_evaluate in \
                           ("yes", "true"):
                            obj = self.teval_option(val, True, opt_autoimport)
                        else:
                            obj = self.teval_option(val, False, opt_autoimport)
                        setattr(self._targs, opt_dest, obj)
                else:
                    obj = self.teval_option(val, False, opt_autoimport)
                    setattr(self._targs, opt_dest, obj)

        if self._targs.assert_input:
            for boolexpr in self._targs.assert_input:
                for varg in boolexpr.vargs:
                    try:
                        assert_result = self.teval(varg)
                        if assert_result is not True:
                            self.parent.error_exit("'%s' => not True"%varg, error_class=PTTestError)
                    except Exception as err:
                        self.parent.error_exit("Exception occured from '%s'"%varg, error_class=PTTestError)


        if hasattr(self._targs, "pull") and self._targs.pull:
            pull_values = self.parent.pull_data(self._targs.pull)
            for key, value in pull_values.items():
                self.env[key] = value

        if self._targs.assert_stdout:
            old_stdout = sys.stdout
            old_stdout.flush()
            new_stdout = StringIO()
            sys.stdout = new_stdout

        if self._targs.assert_stderr:
            old_stderr = sys.stderr
            old_stderr.flush()
            new_stderr = StringIO()
            sys.stderr = new_stderr

        if isinstance(self, GroupTaskBase):
            out = self.group_perform(self._targs)
        else:
            out = self.perform(self._targs)

        if self._targs.printvar:
            _D = []
            _f = {'D': _D}
            for opt in self._targs.printvar:
                for varg in opt.vargs:
                    _D.append(self.teval(varg))
            print_task = load_task(0, ['print'], self.parent, ParentProxy(self))
            print_task.run(_f, {})

        if self._targs.assert_stdout:
            sys.stdout = old_stdout

        if self._targs.assert_stderr:
            sys.stderr = old_stderr

        if hasattr(self._targs, "push") and self._targs.push:
            push_dict = {}
            for opt in self._targs.push:
                for arg in opt.vargs:
                    push_dict[arg] = self.teval(arg)
                for v, e in opt.kwargs.items():
                    push_dict[v] = self.teval(e)
            self.parent.push_data(push_dict)

        if self._targs.assert_output:
            for boolexpr in self._targs.assert_output:
                for varg in boolexpr.vargs:
                    try:
                        assert_result = self.teval(varg)
                        if assert_result is not True:
                            self.parent.error_exit("'%s' => not True"%varg, error_class=PTTestError)
                    except Exception as err:
                        self.parent.error_exit("Exception occured from '%s'"%varg, error_class=PTTestError)

        if out is None:
            retval, _forward, _promote = 0, {}, {}
        elif isinstance(out, int):
            retval, _forward, _promote = out, {}, {}
        elif isinstance(out, tuple):
            if len(out) == 1:
                retval, _forward, _promote = out[0], {}, {}
            elif len(out) == 2:
                retval, _forward, _promote = out[0], out[1], {}
            elif len(out) == 3:
                retval, _forward, _promote = out[0], out[1], out[2]
            else:
                self.parent.error_exit(
                "perform returned wrong number of return vaules.: %s"%str(out))
        else:
            self.parent.error_exit("perform returned wrong type.: %s"%type(out))

        promote.update(_promote)

        if hasattr(self._targs, "promote") and self._targs.promote:
            for opt in self._targs.promote:
                for k, v in opt.kwargs.items():
                    promote[k] = self.teval(v)

        forward = {}
        forward.update(_forward)

        if hasattr(self._targs, "forward") and self._targs.forward:
            D = []
            F = {}
            for opt in self._targs.forward:
                for varg in opt.vargs:
                    D.append(self.teval(varg))
                for k, v in opt.kwargs.items():
                    val = self.teval(v)
                    if k == "D":
                        if isinstance(k, (list, tuple)):
                            D.extend(val)
                        else:
                            D.append(val)
                    else:
                        F[k] = val
            if D:
                forward["D"] = D
            forward.update(F)

        if self._targs.assert_stdout:
            for boolexpr in self._targs.assert_stdout:
                for varg in boolexpr.vargs:
                    try:
                        env = {"stdout": new_stdout.getvalue()}
                        env.update(self.env)
                        assert_result = eval(varg, env)
                        if assert_result is not True:
                            self.parent.error_exit("'%s' => not True"%varg, error_class=PTTestError)
                    except Exception as err:
                        self.parent.error_exit("Exception occured from '%s'"%varg, error_class=PTTestError)

        if self._targs.assert_stderr:
            for boolexpr in self._targs.assert_stderr:
                for varg in boolexpr.vargs:
                    try:
                        env = {"stderr": new_stderr.getvalue()}
                        env.update(self.env)
                        assert_result = eval(varg, env)
                        if assert_result is not True:
                            self.parent.error_exit("'%s' => not True"%varg, error_class=PTTestError)
                    except Exception as err:
                        self.parent.error_exit("Exception occured from '%s'"%varg, error_class=PTTestError)

        if self._targs.assert_forward:
            for boolexpr in self._targs.assert_forward:
                for varg in boolexpr.vargs:
                    try:
                        assert_result = eval(varg, forward)
                        if assert_result is not True:
                            self.parent.error_exit("'%s' => not True"%varg, error_class=PTTestError)
                    except Exception as err:
                        self.parent.error_exit("Exception occured from '%s'"%varg, error_class=PTTestError)

        if self._targs.assert_promote:
            for boolexpr in self._targs.assert_promote:
                for varg in boolexpr.vargs:
                    try:
                        assert_result = eval(varg, promote)
                        if assert_result is not True:
                            self.parent.error_exit("'%s' => not True"%varg, error_class=PTTestError)
                    except Exception as err:
                        self.parent.error_exit("Exception occured from '%s'"%varg, error_class=PTTestError)

        self.log_info("End task '%s'"%self.taskname)

        return retval, forward, promote

    def add_data_argument(self, *vargs, **kwargs):
        self._args_temp['dargs'].append((vargs, kwargs))

    def add_option_argument(self, *vargs, **kwargs):
        self._args_temp['kargs'].append((vargs, kwargs))

    def log(self, level, msg, args, kwargs):
        if self._targs is not None and self._targs.log is True:
            c = stack_floc(depth=3)
            if "filename" not in kwargs:
                kwargs["filename"] = c["filename"]
            if "lineno" not in kwargs:
                kwargs["lineno"] = c["lineno"]
            return self.parent.log(level, msg, args, kwargs)

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

class MgmtTask(TaskBase):
    """parent task of mgmt tasks
    """

    def __new__(cls, argv):

        proxy = ManagerProxy()

        obj = super(MgmtTask, cls).__new__(cls, proxy, -1, argv[0], None, argv[1:])

        obj.argv_group = None

        return obj

    def set_argv_group(self, argv_group):

        self.argv_group = argv_group

class FlowcontrolTaskBase(TaskBase):
    """parent task of flow-control tasks
    """

    def __new__(cls, proxy, tid, path, fragment, argv):

        obj = super(FlowcontrolTaskBase, cls).__new__(cls, proxy, -1, path, fragment, argv)

        obj.argv_group = None

        return obj

    def set_argv_group(self, argv_group):

        self.argv_group = argv_group

class StandardTask(TaskBase):
    """parent task of standard tasks
    """
    pass

class GroupTaskBase(TaskBase):
    """parent class of group tasks
    """

    def __new__(cls, parent, tid, path, fragment, argv):

        obj = super(GroupTaskBase, cls).__new__(cls, parent, -1, path, fragment, argv)

        obj.graph = Graph()

        return obj

    def init_group(self):
        pass

    def fini_group(self):
        pass

    def pre_task(self, task):
        pass

    def post_task(self, task):
        pass

    def group_perform(self, targs):

        self.init_group()

        out = self.perform(targs)

        if out is None:
            retval, forward, promote = 0, {}, {}
        elif isinstance(out, int):
            retval, forward, promote = out, {}, {}
        elif isinstance(out, tuple):
            if len(out) == 1:
                retval, forward, promote = out[0], {}, {}
            elif len(out) == 2:
                retval, forward, promote = out[0], out[1], {}
            elif len(out) == 3:
                retval, forward, promote = out[0], out[1], out[2]
            else:
                self.parent.error_exit(
                "group_perform returned wrong number of return vaules.: %s"%str(out))
        else:
            self.parent.error_exit("group_perform returned wrong type.: %s"%type(out))

        self.fini_group()

        return retval, forward, promote

    def run_subtasks(self):

        def _push(stack, tasks, f, p):

            if tasks:
                stack.append((tasks[0], f, p))
                for task in tasks[1:]:
                    _f = copy.deepcopy(f)
                    _p = copy.deepcopy(p)
                    stack.append((task, _f, _p))

        retval = 0
        forward = copy.deepcopy(self.forward)
        promote = copy.deepcopy(self.promote)

        task_stack = []

        tasks = self.graph.get_entrynodes()
        _push(task_stack, tasks, forward, promote)

        while task_stack:
            task, forward, promote = task_stack.pop()
            self.pre_task(task)
            retval, forward, promote = task.run(forward, promote)
            self.post_task(task)
            tasks = self.graph.get_nextnodes(task)
            _push(task_stack, tasks, forward, promote)

        return retval, forward, promote

    def add_task(self, tid, task, prev_task, proxy_class):

        if not task:
            return None

        if prev_task not in self.graph:
            self.parent.error_exit("Previous task is not in graph.")

        if isinstance(task, TaskBase):
            task.parent.task = self
            task_instance = task
        else:
            task_instance = load_task(tid, task, self.parent, proxy_class(self))

        if isinstance(task_instance, TaskBase):
            self.graph.add(task_instance, prev_task)
        else:
            self.parent.error_exit("unrecognized task: '{0}'.".format(
                str(task[0])), error_class=PTUsageError)

        return task_instance

class ShellTask(GroupTaskBase):
    """shell task
    """

    def __new__(cls, argv_group, proxy=None, shell_argv=[]):

        if not argv_group:
            raise PTUsageError("No task to perform.")

        if proxy is None:
            proxy = ManagerProxy()

        obj = super(ShellTask, cls).__new__(cls, proxy, -1, "shell", None, shell_argv)

        prev_task = obj.add_task(0, argv_group[0], None, ParentProxy)

        if isinstance(prev_task, GroupTaskBase):

            obj = prev_task
            prev_task = None

            for tid, task_argv in enumerate(argv_group[1:]):
                prev_task = obj.add_task(tid, task_argv, prev_task, ParentProxy)

        elif isinstance(prev_task, FlowcontrolTaskBase):

            prev_task.set_argv_group(argv_group[1:])

        else:

            for tid, task_argv in enumerate(argv_group[1:]):
                prev_task = obj.add_task(tid+1, task_argv, prev_task, ParentProxy)

        return obj

    def perform(self, targs):

        out = self.run_subtasks()
        return out

class Task(TaskBase):
    """Base class for user-defined tasks.

    User defines task by writing Python code inside of `perform` method of
    an inheritant(**Task-class**) of this class.

    An instance of **Task-class** can be invoked as a command-line program under
    `perform` command-line tool that is a part of `perftask` package.
    Or, it can be linked with other **Task-class** to build a larger task.

    User can specify command-line arguments for a task in `__init__` constructor of
    this class. `Task` class provides `add_data_argument` and `add_option_argument`
    methods to specify command-line arguments for positional and keyword
    arguments each.

    For example, following code defines `MyTask` **Task-class** that accept
    zero or more positional arguments and one keyword argument. If any argument
    is provided, the task simply prints the arguments.

    >>> from perftask import Task
    >>> class MyTask(Task):
    ...     "A task example"
    ...     def __init__(self, parent, path, fragment, argv):
    ...         self.add_data_argument('data', nargs="*", evaluate=True, help='input data.')
    ...         self.add_option_argument('-o', '--opt', evaluate=True, help='example option')
    ...     def perform(self, targs):
    ...         if targs.data:
    ...             print(targs.data)
    ...         if targs.opt:
    ...             print(targs.opt)
    ...         return 0

    Following shell command shows how to invoke the task defined above
    assuming that `mytask.py` file contains above code and currrent directory
    is the same where `mytask.py` is.

    .. code-block:: bash

        $ perform mytask.py 1 2 -o 3
        [1, 2]
        3

    `Task` class internally uses `argparse` Python standard library to implement
    `add_data_argument` and `add_option_argument`. The way for `Task` class to
    handle command-line arguments is essentially the same to `argparse`. Two keyword
    arguments are added to `add_argument` of `argparse`: `evaluate` and `autoimport`.
    With `evalute=True`, perftask invokes `eval` Python built-in function to
    convert string arguments to Python objects. `autoimport` enables to automatically
    import Python module in case of NameError. `targs` is an argument of `perform`
    method that holds all command-line arguments. In this example, `targs.data`
    holds a list of two integer values of `[1, 2]` and `targs.opt` holds
    3.
    """
    pass

# TODO : implement this
class GroupTask(GroupTaskBase):
    """Base class for user-defined group tasks.

    """

# TODO : implement this
class FlowcontrolTask(FlowcontrolTaskBase):
    """Base class for user-defined flow-control tasks.

    """
