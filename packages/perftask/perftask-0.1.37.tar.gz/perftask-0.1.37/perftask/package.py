# -*- coding: utf-8 -*-

"""package module."""

from __future__ import unicode_literals

import sys
import os
import tempfile
import zipfile
import toml
import ast
import shutil
import pipenv

from .util import (iterpath, perftask_import, set_envvar, del_envvar)
from .error import PTUsageError

class CollectModule(ast.NodeVisitor):

    def __init__(self, modules, cache):
        self.modules = modules
        self.cache = cache

    def _collect_modules(self, name):

        if name in self.cache:
            return

        head = None
        modname = None

        if '.' in name:
            head = name.split(".")[0]
            if not head.startswith("_"):
                modename = head
        elif not name.startswith("_"):
            modname = name

        if modname:
            if modname in sys.modules:
                self.modules[modname] = None
            else:
                try:
                    mod = perftask_import(modname)
                    self.modules[modname] = None
                except:
                    pass

        if head is not None:
            self.cache[head] = None
        self.cache[name] = None

    def visit_Import(self, node):

        for alias in node.names:
            self._collect_modules(alias.name)

    def visit_ImportFrom(self, node):

        if node.level > 0:
            pass
        elif node.module:
            self._collect_modules(node.module)
        else:
            raise Exception("Internal error: unknown ImportFrom syntax: {}".format(str(node)))

def addToZip(zf, path, zippath):
    if os.path.isfile(path):
        zf.write(path, zippath, zipfile.ZIP_DEFLATED)
    elif os.path.isdir(path):
        if zippath:
            zf.write(path, zippath)
        for nm in os.listdir(path):
            addToZip(zf, os.path.join(path, nm), os.path.join(zippath, nm))
    # else: ignore

def gen_setup(workdir, kwargs):
    script = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

"The setup script."

from setuptools import setup, find_packages

setup(
    name='{name}',
    version='{version}',
    py_modules=[{py_modules}],
    packages=[{packages}],
    data_files=[{data_files}],
    install_requires=[{install_requires}],
)

""".format(**kwargs)

    py_setup = os.path.join(workdir, "setup.py")
    with open(py_setup, "w") as f:
        f.write(script)
    return py_setup

def collect_modules(path, modules, cache={}):

    path = os.path.abspath(os.path.realpath(path))

    if path in cache:
        return

    if os.path.isdir(path):
        cache[path] = None

    for pysrc in iterpath(path):
        if pysrc not in cache:
            cache[pysrc] = None
            try:
                with open(pysrc, 'rb') as f:
                    tree = ast.parse(f.read(), filename=pysrc)
                collector = CollectModule(modules, cache)
                collector.visit(tree)
            except SyntaxError:
                pass

def pack_task(name, version, paths, output, metafiles, compress, venv):
    try:

        setup_kwargs = {
            "name": name,
            "version": version,
            "packages": "",
            "py_modules": "",
            "data_files": "",
            "install_requires": "",
        }

        workdir = tempfile.mkdtemp()

        modules = {}
        packages = set()
        py_modules = set()

        for task_path in paths:

            head, base = os.path.split(task_path)

            if os.path.isdir(task_path):
                if os.path.isfile(os.path.join(task_path, "__init__.py")):
                    packages.add(base)
                    shutil.copytree(task_path, workdir)
                else:
                    raise PTUsageError("'{}' is not Python package.".format(task_path))
            elif os.path.isfile(task_path):
                if base.endswith(".py"):
                    py_modules.add(base[:-3])
                    shutil.copy(task_path, workdir)
                else:
                    raise PTUsageError("'{}' is not Python source file.".format(task_path))
            else:
                raise PTUsageError("'{}' does not exist.".format(task_path))

            work_path = os.path.join(workdir, base)

            collect_modules(work_path, modules)

        setup_kwargs["packages"] = ",".join(["'{}'".format(base) for base in packages])
        setup_kwargs["py_modules"] = ",".join(["'{}'".format(base) for base in py_modules])

        install_requires = []
        for modname, modver in modules.items():
            if modver is not None:
                install_requires.append("'{0}=={1}'".format(modname, modver))
            else:
                install_requires.append("'{}'".format(modname))
        setup_kwargs["install_requires"] = ", ".join(install_requires)

        data_files = list(metafiles.keys())
        if venv:
            data_files.append("Pipfile")
            data_files.append("Pipfile.lock")
        data_files_str = ", ".join(["'{}'".format(k) for k in data_files])
        setup_kwargs["data_files"] = "('.', [{}])".format(data_files_str)

        for metafile, metadata in metafiles.items():
            with open(os.path.join(workdir, metafile), "w") as f:
                toml.dump(metadata, f)

        # generate setup.py (app vs. package)
        py_setup = gen_setup(workdir, setup_kwargs)

        cwd_save = os.getcwd()
        os.chdir(workdir)

        if venv:

            import click
            click.disable_unicode_literals_warning = True

            set_envvar("PIPENV_IGNORE_VIRTUALENVS")
            set_envvar("PIPENV_VENV_IN_PROJECT")
            set_envvar("PIPENV_HIDE_EMOJIS")

            try:
                os.system("pipenv --bare install -e "+workdir)
                shutil.rmtree(os.path.join(workdir, ".venv"))
            except SystemExit as err:
                pass

            del_envvar("PIPENV_HIDE_EMOJIS")
            del_envvar("PIPENV_VENV_IN_PROJECT")
            del_envvar("PIPENV_IGNORE_VIRTUALENVS")

        if compress:

            with zipfile.ZipFile(output, 'w') as zf:
                for path in list(packages) + [m+".py" for m in py_modules] + \
                    data_files + ["setup.py", "Pipfile.lock"]:
                    zippath = os.path.basename(path)
                    if not zippath:
                        zippath = os.path.basename(os.path.dirname(path))
                    if zippath in ('', os.curdir, os.pardir):
                        zippath = ''
                    addToZip(zf, path, zippath)
        else:
            shutil.copytree(workdir, output)

        os.chdir(cwd_save)

        # generate sdist and bdist
        #script_args = ["sdist", "--formats=zip", "--dist-dir=."]
        #sdist = distutils.core.run_setup("setup.py", script_args=script_args, stop_after="run")


    #except SyntaxError as err:
    #    import pdb; pdb.set_trace()
    #except UnicodeError as err:
    #    import pdb; pdb.set_trace()
    #except IOError as err:
    #    import pdb; pdb.set_trace()
        #msg = sys.exc_info()[1]
    #except Exception as err:
    #    import pdb; pdb.set_trace()
    finally:
        if os.path.isdir(workdir):
            shutil.rmtree(workdir)

