# -*- coding: utf-8 -*-

"""entry module."""

from __future__ import unicode_literals

import sys
import os
import copy
import shutil

from .builtin import mgmt_tasks, flowcontrol_tasks
from .task import locate_tasks, ShellTask
from .message import ManagerProxy
from .util import (perftask_decode, has_envvar, get_envvar, set_envvar,
                   del_envvar, split_taskname, is_taskpath)
from .help import (short_help, perftask_version)
from .error import PTUsageError, PTInternalError, PTNormalExit, PTTestError, PTNameError

# TODO: taskid triple : static task id, session task id, local task id, (hidden argv id)
# TODO: launch std task for dynamic loading
# TODO: resource per locale?
# TODO: decide where to pup Pipenv and .env when a task without pre-set Pipenv
# TODO: github project, stackoverflow teams in docs ???
# TODO: group tasks are just regular tasks having sub tasks

def _handle_nontask_options(argv):
    """handle command-line options that are not related to a particular task

    """
    retval = False

    if len(argv) == 0:
        print("\n".join(short_help()))
        retval = True

    elif argv[0] == "--version":
        print("perftask version "+perftask_version())
        retval = True

    elif argv[0] == "--help":
        del argv[:]
        argv.append("help")

    return retval

def _handle_venv_options(manager, argv, pipfile):

    venv = False
    no_venv = False

    if "--venv" in argv:
        argv.remove("--venv")
        venv = True

    if "--no-venv" in argv:
        argv.remove("--no-venv")
        no_venv = True

    if venv and no_venv:
        os.parent.error_exit()
        manager.log_critical("'--venv' and '--no-venv' options can not be used simultaneously.")
        sys.exit(-1)

    if venv:
        if pipfile is None or not os.path.exists(pipfile):
            pipfile = True
    elif no_venv:
        if pipfile is not None and os.path.exists(pipfile):
            pipfile = None

    return pipfile

def main():
    """entry for perform command

    """

    retval = 0
    prog = sys.argv[0]

    # convert to unicode if necessary
    argv =  [perftask_decode(sys.argv[idx]) for idx in range(1, len(sys.argv))]


    # TODO: support nested task syntax
    #     print 1 -- [ repeat 3 -- print 2 -- print 3 ] -- print 4

    # handles --help, --version, and no option
    if not _handle_nontask_options(argv):

        try:

            manager = ManagerProxy()

            # handling exclamation mark
            histnum = None
            if argv[0].startswith("!"):
                histnum = -1
                num = argv[0][1:]
                if num:
                    argv.insert(1, num)

                if len(argv) > 1:
                    try:
                        histnum = int(argv[1])
                    except ValueError:
                        pass
                argv[0] = "history"

            argvcopy = copy.deepcopy(argv)

            # handling history expansion
            if isinstance(histnum, int):
                hist = manager.get_history("list", histnum)
                if hist:
                    argv = [eval(a) for a in hist]
                else:
                    manager.log_critical("ERROR: no history item of %d"%histnum)
                    sys.exit(-1)

            # locate tasks from alias, installed, zipped, downloeded, ...
            if has_envvar("PERFTASK_PIPENV_RUN"):
                argv_group, tempdir, pipfile = locate_tasks(argv, manager, None, False)
            else:
                argv_group, tempdir, pipfile = locate_tasks(argv, manager, None, True)
                pipfile = _handle_venv_options(manager, argv_group[0], pipfile)

            cwd = os.getcwd()

            # launch a task
            if pipfile and not has_envvar("PERFTASK_PIPENV_RUN"):

                set_envvar("PIPENV_IGNORE_VIRTUALENVS")
                set_envvar("PIPENV_VENV_IN_PROJECT")
                set_envvar("PIPENV_HIDE_EMOJIS")
                if not isinstance(pipfile, bool) and os.path.exists(pipfile):
                    set_envvar("PIPENV_PIPFILE", pipfile)

                set_envvar("PERFTASK_PIPENV_RUN")
                set_envvar("PERFTASK_PIPENV_CMDDIR", cwd)

                venvdir = os.path.dirname(pipfile)
                #if tempdir:
                    #set_envvar("PERFTASK_PIPENV_TMPDIR", tempdir)
                #    os.chdir(tempdir)
                os.chdir(venvdir)

                quoteargv = ['"{0}"'.format(a) for aa in argv_group for a in aa]
                os.system("pipenv --bare run -- perform {0}".format(" ".join(quoteargv)))

                #if tempdir:
                    #os.chdir(cwd)
                #    shutil.rmtree(tempdir)
                os.chdir(cwd)

            else:

                if has_envvar("PERFTASK_PIPENV_CMDDIR"):
                    os.chdir(get_envvar("PERFTASK_PIPENV_CMDDIR"))

                entry_task = argv_group[0][0]
                shell_argv = []

                if "--log-all" in argv_group[0]:
                    idx = argv_group[0].index("--log-all")
                    argv_group[0][idx] = "--log"
                    for idx in range(1, len(argv_group)):
                        if "--log" not in argv_group[idx]:
                            argv_group[idx].append("--log")
                    shell_argv.append("--log")
                    manager.turn_logging_on("perftask")
                elif any("--log" in g for g in argv_group):
                    manager.turn_logging_on("perftask")

                task_path, fragment = split_taskname(entry_task)

                if is_taskpath(task_path):

                    task_instance = ShellTask(argv_group, proxy=manager,
                            shell_argv=shell_argv)

                elif task_path in mgmt_tasks:

                    task_instance = mgmt_tasks[task_path](argv_group[0])
                    task_instance.argv = argv_group[0][1:]
                    task_instance.set_argv_group(argv_group[1:])

                elif task_path in flowcontrol_tasks:

                    task_instance = flowcontrol_tasks[task_path](manager, -1, entry_task,
                                    None, argv_group[0][1:])
                    task_instance.set_argv_group(argv_group[1:])

                else:

                    task_instance = ShellTask(argv_group, proxy=manager,
                            shell_argv=shell_argv)

                retval, forward, promote = task_instance.run({}, {})

                #if has_envvar("PERFTASK_PIPENV_TMPDIR"):
                #    del_envvar("PERFTASK_PIPENV_TMPDIR")

                del_envvar("PERFTASK_PIPENV_CMDDIR")
                del_envvar("PERFTASK_PIPENV_RUN")
                del_envvar("PIPENV_PIPFILE")
                del_envvar("PIPENV_HIDE_EMOJIS")
                del_envvar("PIPENV_IGNORE_VIRTUALENVS")
                del_envvar("PIPENV_VENV_IN_PROJECT")

            if tempdir is not None and os.path.isdir(tempdir):
                shutil.rmtree(tempdir)

            if argvcopy[0] != "history":
                quoteargv = ['"{0}"'.format(a) for a in argvcopy]
                lasthist = manager.get_history("list", -1)
                if not lasthist or lasthist != quoteargv:
                    manager.add_history("list", quoteargv)

            manager.dump_config()

        except PTUsageError as err:

            manager.log_critical("Usage error occured: %s"%str(err),
                filename=err.filename, lineno=err.lineno)
            retval = -1

        except PTInternalError as err:

            manager.log_critical("Internal error occured: %s"%str(err),
                filename=err.filename, lineno=err.lineno)
            retval = -1

        except PTTestError as err:

            manager.log_critical("Test failed: %s"%str(err),
                filename=err.filename, lineno=err.lineno)
            retval = -1

        except PTNameError as err:

            manager.log_critical("Unknown name: %s"%str(err),
                filename=err.filename, lineno=err.lineno)
            retval = -1

        except PTNormalExit:

            manager.dump_config()

        finally:

            manager.shutdown()


    try:
        if not sys.stdout.closed:
            sys.stdout.flush()
            #sys.stdout.close()
        if not sys.stderr.closed:
            sys.stderr.flush()
            #sys.stderr.close()
    except:
        pass
    finally:
        return retval

