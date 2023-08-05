# -*- coding: utf-8 -*-

"""builtin task module."""

from __future__ import unicode_literals

import os
import pydoc
import tempfile
import zipfile
import shutil
import shlex
import subprocess

from .package import pack_task
from .task import MgmtTask, ShellTask
from .help import long_help
from .util import (perftask_print, urlparse, unparse_argument, extract_zipfile,
                   set_envvar, del_envvar, configparser, perftask_decode,
                   runcmd, perftask_import)
from .error import PTUsageError, PTTestError

def _mgmt_tasks():

    lines = ["management tasks"]
    lines.append("----------------")
    for task in sorted(mgmt_tasks):
        docs = mgmt_tasks[task].__doc__
        if docs:
            lines.append("{0:10} : {1}".format(task, pydoc.splitdoc(docs)[0]))
        else:
            lines.append("{0:10} : {0}".format(task))
    return lines

def _flowcontrol_tasks():

    lines = ["folw-control tasks"]
    lines.append("------------------")
    for task in sorted(flowcontrol_tasks):
        docs = flowcontrol_tasks[task].__doc__
        if docs:
            lines.append("{0:10} : {1}".format(task, pydoc.splitdoc(docs)[0]))
        else:
            lines.append("{0:10} : {0}".format(task))
    return lines

def _standard_tasks():

    lines = ["standard tasks"]
    lines.append("--------------")
    for task in sorted(std_tasks):
        docs = std_tasks[task].__doc__
        if docs:
            lines.append("{0:10} : {1}".format(task, pydoc.splitdoc(docs)[0]))
        else:
            lines.append("{0:10} : {0}".format(task))
    return lines

class AliasTask(MgmtTask):
    """create a task alias on a local system
    """
    def __init__(self, argv):

        # TODO: need to support input to subtask mapping

        self.add_data_argument('alias_name', nargs="?", help='alias name.')
        self.add_option_argument('-d', '--desc',
            help='short description of this alias.')

    def perform(self, targs):

        alias_name = targs.alias_name

        if alias_name:

            if self.parent.has_task("aliases", alias_name):
                self.parent.error_exit("Alias, '{0}', already exists.".format(
                                       alias_name), error_class=PTUsageError)

            if targs.desc:
                desc = targs.desc.vargs[0]
            else:
                desc = alias_name

            tasks = []
            for task_argv in self.argv_group:
                if os.path.exists(task_argv[0]):
                    task_argv[0] = os.path.abspath(task_argv[0])
                elif task_argv[0] not in builtin_tasks:
                    self.parent.error_exit("Aliasing requires a local task"\
                        " or builtin task, but found '%s'"%str(task_argv),
                        error_class=PTUsageError)
                if "--log" in task_argv:
                    task_argv.remove("--log")
            alias_def = {"desc": desc, "tasks": self.argv_group}

            self.parent.set_task("aliases", alias_name, alias_def)

        else:

            tasks = self.parent.get_task("aliases")

            if tasks:
                perftask_print("")
                perftask_print("alias task(s)")
                perftask_print("-------------")
                for task, task_def in tasks.items():
                    desc = task_def.get("desc", None)
                    if desc:
                        perftask_print("{0} : {1}".format(task, desc))
                    else:
                        perftask_print("{0} : {0}".format(task))
            else:
                perftask_print("")
                perftask_print("No aliased task")
                perftask_print("---------------")

        return 0

class UnaliasTask(MgmtTask):
    """remove task aliases from a local system
    """

    def __init__(self, argv):

        self.add_data_argument('alias_name', nargs='+', help='alias name.')

    def perform(self, targs):

        for alias_name in targs.alias_name:

            if self.parent.has_task("aliases", alias_name):
                self.parent.del_task("aliases", alias_name)
            else:
                self.parent.error_exit("'{0}' does not exist.".format(alias_name))

        return 0

class CLIAppTask(MgmtTask):
    """convert a task to a command-line application development project
    """

    def __init__(self, argv):

        self.add_data_argument("app_name", help="appication name.")

        self.add_option_argument("-o", "--output", metavar="path", help="path to create a project")

    def perform(self, targs):

        # TODO: generate a dev setup of the app
        # TODO: some explanation what to do next

        if targs.output:
            output = targs.output
        else:
            output = os.path.join(os.getcwd(), targs.app_name)

        if os.path.exists(output):
            self.parent.error_exit("'%s' already exists."%output)
        else:
            os.makedirs(output)

        # docs

        # examples

        # init git or svn ...

        # LICENSE

        # Makefile

        # package of this app

        # README.rs

        # requirements.txt

        # setup.cfg

        # setup.py

        # tests

class ConfigTask(MgmtTask):
    """manage perftask configuration
    """

    def __init__(self, argv):
        # Name syntax: a.b.c...
        self.add_data_argument('names', nargs="*", help='show config item')
        self.add_option_argument('-d', '--delete', action="store_true", help='delete config item')
        self.add_option_argument('-t', '--type', default="general", help='configuration type')

    def _getmethod(self, acttype, cfgtype):
        method = acttype+"_"+cfgtype
        if hasattr(self.parent, method):
            return getattr(self.parent, method)
        else:
            self.parent.error_exit("Unknown config method: %s"%method)

    def perform(self, targs):

        if targs.names:
            for name in targs.names:
                cfgtype = targs.type.vargs[0]
                s = name.split("=")
                if len(s)==2:
                    if targs.delete:
                        self.parent.error_exit("Assignment argument can not be used with '--delete' option.")
                    method = self._getmethod("set", cfgtype)
                    method(*(s[0].split(".")+ [s[1]]))
                elif targs.delete:
                    method = self._getmethod("del", cfgtype)
                    method(*(s[0].split(".")))
                else:
                    method = self._getmethod("get", cfgtype)
                    config = method(*(s[0].split(".")))
                    if config:
                        perftask_print(config)
        else:
            cfg = self.parent.get_general(keysonly=True)
            perftask_print("config items: {0}".format(" ".join(cfg)))

# TODO : support for user to add new optional arguments for the group task

class GroupingTask(MgmtTask):
    """create a group task of multiple tasks on a local system
    """
    def __init__(self, argv):

        self.add_data_argument('group_name', nargs="?", help='group name.')
        self.add_option_argument('-d', '--desc',
            help='short description of this group.')

    def perform(self, targs):

        group_name = targs.group_name

        if group_name:

            if self.parent.has_task("groups", group_name):
                self.parent.error_exit("Group, '{0}', already exists.".format(
                                       group_name), error_class=PTUsageError)

            if targs.desc:
                desc = targs.desc.vargs[0]
            else:
                desc = group_name

            tasks = []
            for task_argv in self.argv_group:
                if os.path.exists(task_argv[0]):
                    task_argv[0] = os.path.abspath(task_argv[0])
                elif all(task_argv[0] not in t for t in (std_tasks, flowcontrol_tasks)):
                    self.parent.error_exit("Grouping requires a local task, "\
                        "standard task, or flowcontrol task, but found '%s'"%str(task_argv),
                        error_class=PTUsageError)
            group_def = {"desc": desc, "tasks": self.argv_group}

            self.parent.set_task("groups", group_name, group_def)

        else:

            tasks = self.parent.get_task("groups")

            if tasks:
                perftask_print("")
                perftask_print("group task(s)")
                perftask_print("-------------")
                for task, task_def in tasks.items():
                    desc = task_def.get("desc", None)
                    if desc:
                        perftask_print("{0} : {1}".format(task, desc))
                    else:
                        perftask_print("{0} : {0}".format(task))
            else:
                perftask_print("")
                perftask_print("No grouped task")
                perftask_print("---------------")

        return 0

class UngroupingTask(MgmtTask):
    """remove group tasks from a local system
    """

    def __init__(self, argv):

        self.add_data_argument('group_name', nargs='+', help='group name.')

    def perform(self, targs):

        for group_name in targs.group_name:

            if self.parent.has_task("groups", group_name):
                self.parent.del_task("groups", group_name)
            else:
                self.parent.error_exit("'{0}' does not exist.".format(group_name))

        return 0

class HelpTask(MgmtTask):
    """show information of a task"""

    def __init__(self, argv):

        self.add_data_argument('task', nargs="?", help='task location.')

    def perform(self, targs):

        if targs.task:

            # TODO: improve help message for a task
            name = targs.task

            taskname = urlparse(name).path
            if len(taskname) > 20:
                taskname = taskname[:3] + "..." + taskname[-15:]

            if taskname in builtin_tasks:
                docs = builtin_tasks[taskname].__doc__
                if docs:
                    perftask_print(pydoc.splitdoc(docs)[0])
                else:
                    perftask_print(taskname)
            elif self.parent.has_task("installed", taskname):
                task_def = self.parent.get_task("installed", taskname)
                perftask_print(task_def["desc"])
            elif self.parent.get_task("aliases", taskname) :
                alias_def = self.parent.get_task("aliases", taskname)
                perftask_print(alias_def["desc"])
            elif os.path.exists(taskname):
                # TODO: implement this
                pass
            else:
                perftask_print("Help message is not found.")
        else:

            perftask_print("\n".join(long_help()))

            perftask_print("")
            perftask_print('Builtin-tasks are listed below. To see a full list of tasks')
            perftask_print('available in this system, please run "perform list" command.')

            perftask_print("")
            for line in _standard_tasks():
                perftask_print(line)

            perftask_print("")
            for line in _flowcontrol_tasks():
                perftask_print(line)

            perftask_print("")
            for line in _mgmt_tasks():
                perftask_print(line)


        return 0

class HistoryTask(MgmtTask):
    """list or invoke perftask commands
    """

    def perform(self, targs):

        max_display = self.parent.get_history("max_display")
        len_history = self.parent.len_history("list")
        start = max(0, len_history-int(max_display))
        stop  = min(len_history, start+len_history)
        hist = self.parent.get_history("list", slicing=slice(start, stop))

        for idx, item in enumerate(hist):
            if item:
                lines = [item.pop(0)]
                for i in item:
                    if len(lines[-1]) > 80:
                        lines.append(i)
                    else:
                        lines[-1] += " " + i
                perftask_print(" {0:d}  {1}".format(idx+start,
                               lines.pop(0)))
                indent = " "*(len(str(idx))+3)
                for line in lines:
                    perftask_print(indent+line)

        return 0

class InstallTask(MgmtTask):
    """install a task on a local system
    """
    def __init__(self, argv):

        self.add_data_argument('name', nargs="?", help='package name.')
        self.add_data_argument('path', nargs="?", help='task location.')

        self.add_option_argument('--task-version', default='0.0.0', help='specifying a task version.')
        self.add_option_argument('-d', '--desc', help='installed task description.')
        self.add_option_argument('--no-venv', action='store_true', help='not using virtualenv')

    def perform(self, targs):

        if targs.name and targs.path:

            task_root = self.parent.get_task("task_root")
            task_name = targs.name
            task_version = unparse_argument(targs.task_version)
            task_dir = os.path.join(task_root, task_name, task_version)
            basename = os.path.basename(targs.path)

            if os.path.exists(task_dir):
                self.parent.error_exit("'{0} version {1}' already exists.".format(task_name, task_version))

            if zipfile.is_zipfile(targs.path):
                _tmpdir = tempfile.mkdtemp()
                extract_zipfile(targs.path, outdir=_tmpdir)
                meta = os.path.join(_tmpdir, "PERFTASK")
                if os.path.isfile(meta):
                    basename = "PERFTASK"
                    if targs.no_venv and targs.no_venv.vargs[0]:
                        pipfile = os.path.join(_tmpdir, "Pipfile")
                        piplock = os.path.join(_tmpdir, "Pipfile.lock")
                        if os.path.exists(pipfile): os.remove(pipfile)
                        if os.path.exists(piplock): os.remove(piplock)
                    shutil.copytree(_tmpdir, task_dir)
                    shutil.rmtree(_tmpdir)
                else:
                    shutil.rmtree(_tmpdir)
                    self.parent.error_exit("'{}' is not Python package file.".format(task_dir))

            else:
                basename = os.path.basename(targs.path)

                metafiles = {
                    "PERFTASK": {
                        "entry": targs.name,
                        "tasks": {
                            targs.name: basename
                        },
                    },
                }

                pack_task(task_name, task_version, [targs.path], task_dir, metafiles, False, not targs.no_venv)

            pipfile = os.path.join(task_dir, "Pipfile")
            if os.path.isfile(pipfile):

                cwd = os.getcwd()
                os.chdir(task_dir)

                import click
                click.disable_unicode_literals_warning = True

                set_envvar("PIPENV_IGNORE_VIRTUALENVS")
                set_envvar("PIPENV_VENV_IN_PROJECT")
                set_envvar("PIPENV_HIDE_EMOJIS")
                set_envvar("PIPENV_PIPFILE", pipfile)

                try:
                    os.system("pipenv --bare sync")
                except SystemExit as err:
                    pass

                del_envvar("PIPENV_PIPFILE")
                del_envvar("PIPENV_HIDE_EMOJIS")
                del_envvar("PIPENV_VENV_IN_PROJECT")
                del_envvar("PIPENV_IGNORE_VIRTUALENVS")

                os.chdir(cwd)

            # TODO: let installed path a list so that multiple versions co-exist
            if targs.desc:
                task_desc = unparse_argument(targs.desc)
            else:
                task_desc = task_name

            install_def = {"desc": task_desc, "path": os.path.join(task_name,
                           task_version, basename)}
            self.parent.set_task("installed", task_name, install_def)

        else:

            tasks = self.parent.get_task("installed")

            if tasks:
                perftask_print("")
                perftask_print("installed task(s)")
                perftask_print("-----------------")
                for task, task_def in tasks.items():
                    desc = task_def.get("desc", None)
                    if desc:
                        perftask_print("{0} : {1}".format(task, desc))
                    else:
                        perftask_print("{0} : {0}".format(task))
            else:
                perftask_print("")
                perftask_print("No installed task")
                perftask_print("-----------------")

        return 0

class UninstallTask(MgmtTask):
    """uninstall a task from a local system
    """

    def __init__(self, argv):

        self.add_data_argument('taskname', nargs="+", help='task name.')

    def perform(self, targs):

        for taskname in targs.taskname:

            # remove task
            task_root = self.parent.get_task("task_root")
            task_def = self.parent.get_task("installed", taskname)
            task_path = os.path.join(task_root, task_def["path"])
            task_dir = task_path
            if os.path.isfile(task_path):
                task_dir = os.path.abspath(os.path.dirname(task_path))

            if os.path.isdir(task_dir):
                shutil.rmtree(task_dir)
            else:
                self.parent.error_exit("task does not exist: {0}.".format(taskname))

            # update metafile
            self.parent.del_task("installed", taskname)

        return 0


class ListTask(MgmtTask):
    """list tasks on a local system"""

    def perform(self, targs):

        tasks = self.parent.get_task("installed")
        if tasks:
            perftask_print("")
            perftask_print("installed task(s)")
            perftask_print("-----------------")
            for task, task_def in tasks.items():
                desc = task_def.get("desc", task)
                perftask_print("{0:10} : {1}".format(task, desc))
        else:
            perftask_print("")
            perftask_print("No installed task")
            perftask_print("-----------------")

        aliases = self.parent.get_task("aliases")
        if aliases:
            perftask_print("")
            perftask_print("alias task(s)")
            perftask_print("-------------")
            for alias, alias_def in aliases.items():
                desc = alias_def.get("desc", alias)
                perftask_print("{0:10} : {1}".format(alias, desc))
                tasks_str = "\n             ".join([str(l) for l in alias_def['tasks']])
                perftask_print("{0:12} {1}".format("", tasks_str))
        else:
            perftask_print("")
            perftask_print("No aliased task")
            perftask_print("---------------")

        groups = self.parent.get_task("groups")
        if groups:
            perftask_print("")
            perftask_print("group task(s)")
            perftask_print("-------------")
            for group, group_def in groups.items():
                desc = group_def.get("desc", group)
                perftask_print("{0:10} : {1}".format(group, desc))
                tasks_str = "\n             ".join([str(l) for l in group_def['tasks']])
                perftask_print("{0:12} {1}".format("", tasks_str))
        else:
            perftask_print("")
            perftask_print("No grouped task")
            perftask_print("---------------")

        perftask_print("")
        for line in _standard_tasks():
            perftask_print(line)

        perftask_print("")
        for line in _flowcontrol_tasks():
            perftask_print(line)

        perftask_print("")
        for line in _mgmt_tasks():
            perftask_print(line)

        return 0

class PackTask(MgmtTask):
    """make a shareable ackage of a task
    """

    def __init__(self, argv):

        self.add_data_argument('name', help='package name.')
        self.add_data_argument('path', help='task location.')

        self.add_option_argument('--task-version', default='0.0.0', help='specifying a task version.')
        self.add_option_argument('-o', '--output', help='output path.')

        # may add option for sample input, document, ... anything for sharing

    def perform(self, targs):

        basename = os.path.basename(targs.path)

        metafiles = {
            "PERFTASK": {
                "entry": targs.name,
                "tasks": {
                    targs.name: basename
                },
            },
        }

        if targs.output is None:
            output = os.path.join(os.getcwd(), targs.name+".task")
        else:
            output = os.path.join(targs.output, targs.name+".task")

        # TODO: support aliased task
        pack_task(targs.name, targs.task_version, [targs.path], output, metafiles, True, True)

        return 0

class RegisterTask(MgmtTask):
    """register a task to share"""
    pass

class TestTask(MgmtTask):
    """execute a set of test cases for a task"""

    def __init__(self, argv):

        self.add_data_argument('target', nargs="*", help='test target.')

        self.add_option_argument('--only', action="append", help='specifying tests to run.')
        self.add_option_argument('--except', dest="exc", action="append", help='specifying tests not to run.')

        # TODO: support this
        self.add_option_argument('--shell', help='specifying shell to run.')

    def _parse(self, text):

        items = [v.strip() for v in text.split("@")]
        return items[0], items[1:]

    def _run_test(self, argv):

        test_result = False
        test_errmsg = None

        try:
            retcode, stdout, stderr = runcmd(["perform"]+argv)
            if retcode == 0:
                test_result = True
            else:
                test_errmsg = stdout + "\n" + stderr
        except subprocess.CalledProcessError as err:
            test_errmsg = str(err)

        return test_result, test_errmsg

    def perform(self, targs):
        # target: directory, test_group, task

        test_results = {}

        # execute a test from argv group
        if self.argv_group:
            argv = self.argv_group[0]
            if targs.log:
                if "--log" not in argv and "--log-all" not in argv:
                    argv.append("--log")
            for l in self.argv_group[1:]:
                argv.append("--")
                argv.extend(l)
            out = self._run_test(argv)
            test_results["cmdline"] = (argv, out)

        # collect test groups
        test_groups = []
        for target in targs.target:

            if os.path.isfile(target):
                test_groups.append(os.path.relpath(target))
            elif os.path.isdir(target):
                for root, dirs, files in os.walk(target):
                    for name in files:
                        path = os.path.join(root, name)
                        if os.path.isfile(path):
                            test_groups.append(os.path.relpath(path))

        only_tests = {}
        if targs.only:
            for o in targs.only:
                for t in o.vargs:
                    s = t.split(".")
                    if s[0] not in only_tests:
                        only_tests[s[0]] = None
                    if len(s) == 2:
                        if isinstance(only_tests[s[0]], list):
                            only_tests[s[0]].append(s[1])
                        else:
                            only_tests[s[0]] = [s[1]]
                    else:
                        only_tests[s[0]] = None

        except_tests = {}
        if targs.exc:
            for o in targs.exc:
                for t in o.vargs:
                    s = t.split(".")
                    if s[0] not in except_tests:
                        except_tests[s[0]] = None
                    if len(s) == 2:
                        if isinstance(except_tests[s[0]], list):
                            except_tests[s[0]].append(s[1])
                        else:
                            except_tests[s[0]] = [s[1]]
                    else:
                        except_tests[s[0]] = None

        # executes tests in test groups
        for test_group in test_groups:

            if test_group and os.path.basename(test_group).startswith("."):
                continue

            tg = {}
            test_results[test_group] = tg

            tests = configparser.RawConfigParser(allow_no_value=True)
            tests.optionxform = str
            opened = tests.read(test_group)

            if opened:

                testenv = {}

                # TODO : supports class section

                sec = "import"
                if tests.has_section(sec):
                    for opt in tests.options(sec):
                        imp = tests.get(sec, opt)
                        if os.path.exists(opt):
                            head, base = os.path.split(opt)
                            import pdb; pdb.set_trace()
                        elif imp:
                            if imp.startswith("from "):
                                import pdb; pdb.set_trace()
                            else:
                                self.parent.log_error("Wrong import syntax: %s"%imp)
                        else:
                            mod = perftask_import(opt)
                            testenv[opt] = mod

                sec = "setup"
                if tests.has_section(sec):
                    for opt in tests.options(sec):
                        imp = tests.get(sec, opt)
                        exec("%s = %s"%(opt, imp), None, testenv)
                        if opt not in testenv or not testenv[opt]:
                            self.parent.log_warning("Null test result: %s = %s"%(opt, imp))

                try:

                    for sec in tests.sections():

                        if sec in ("import", "setup", "teardown"):
                            continue

                        if only_tests and sec not in only_tests:
                            continue

                        if except_tests and sec in except_tests and except_tests[sec] is None:
                            continue

                        og = {}
                        tg[sec] = og
                        for opt in tests.options(sec):

                            if except_tests and sec in except_tests and opt in except_tests[sec]:
                                continue

                            cmd = tests.get(sec, opt).format(**testenv)
                            argv = [perftask_decode(a) for a in shlex.split(cmd)]

                            if targs.log:
                                if "--log" not in argv and "--log-all" not in argv:
                                    argv.append("--log")

                            out = self._run_test(argv)
                            og[opt] = cmd, out

                finally:

                    sec = "teardown"
                    if tests.has_section("teardown"):
                        for opt in tests.options(sec):
                            imp = tests.get(sec, opt)
                            exec("%s = %s"%(opt, imp), None, testenv)
                            if opt not in testenv or not testenv[opt]:
                                self.parent.log_warning("Null test result: %s = %s"%(opt, imp))


            else:
                perftask_print("Warning: no test is found at '%s'."%test_group)

        # report tests
        tot_tests = 0
        pass_tests = 0

        for tgname, tg in test_results.items():
            perftask_print("")
            if tgname == "cmdline":
                cmd, (ret, err) = tg
                tot_tests += 1
                pass_tests += 0 if err else 1
                pf = " => PASS" if ret else " => FAIL"
                errmsg = ", %s"%str(err) if err else ""
                perftask_print("TEST: cmdline")
                perftask_print(" "*4+str(cmd)+pf+errmsg)

            else:
                perftask_print("TEST: %s"%tgname)
                for sec, og in tg.items():
                    perftask_print(" "*4+"GROUP: "+sec)
                    for opt, out in og.items():
                        cmd, (ret, err) = out
                        tot_tests += 1
                        pass_tests += 0 if err else 1
                        pf = "=> PASS" if ret else "=> FAIL"
                        errmsg = ", %s"%str(err) if err else ""
                        perftask_print(" "*8+opt+" : "+str(cmd.replace("\n", " ")))
                        perftask_print(" "*12+pf+errmsg)

        perftask_print("")
        perftask_print("Total no. of tests  : %s"%tot_tests)
        perftask_print("No. of passed tests : %s"%pass_tests)

        return 0 if tot_tests == pass_tests else -1

class WorkflowTask(MgmtTask):
    """monitor and control a workflow of tasks"""
    pass

mgmt_tasks = {
    "alias":        AliasTask,
    "cliapp":       CLIAppTask,
    "config":       ConfigTask,
    "group":        GroupingTask,
    "help":         HelpTask,
    "history":      HistoryTask,
    "install":      InstallTask,
    "list":         ListTask,
    "pack":         PackTask,
    "register":     RegisterTask,
    "test":         TestTask,
    "unalias":      UnaliasTask,
    "ungroup":      UngroupingTask,
    "uninstall":    UninstallTask,
    "workflow":     WorkflowTask,
}

from .stdtask import (InputTask, PrintTask, PythonTask, ReadTask, WriteTask,
                      ShellCmdTask)

std_tasks = {
    "input":        InputTask,
    "print":        PrintTask,
    "python":       PythonTask,
    "read":         ReadTask,
    "shell":        ShellCmdTask,
    "write":        WriteTask,
}

from .flowctrtask import (MultitaskTask, RepeatTask)

flowcontrol_tasks = {
    "multitask":    MultitaskTask,
    "repeat":       RepeatTask,
}

builtin_tasks = mgmt_tasks.copy()
builtin_tasks.update(std_tasks)
builtin_tasks.update(flowcontrol_tasks)
