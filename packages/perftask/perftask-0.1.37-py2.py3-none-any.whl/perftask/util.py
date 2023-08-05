# -*- coding: utf-8 -*-

"""util module."""

from __future__ import unicode_literals

import sys
import os
import zipfile
import subprocess
import inspect
import time
import tempfile

from .platform import (perftask_print, perftask_import, urlparse,
                       urlopen, HTTPError, URLError, BytesIO, StringIO,
                       configparser, perftask_mp_set_start_method)

def print_error(msg, **kwargs):
    perftask_print(msg, file=sys.stderr, **kwargs)

# to unicode
def perftask_decode(string):
    outstr = string
    if type(string) != type(u"A"):
        if sys.stdout.encoding:
            outstr = outstr.decode(sys.stdout.encoding)
        else:
            outstr = outstr.decode("utf-8")
    return outstr

# to utf-8
def perftask_encode(string):
    outstr = string
    if type(string) == type(u"A"):
        outstr = outstr.encode("utf-8")
    return outstr

def set_envvar(name, value="1"):
    if name in os.environ:
        os.environ["{}_ORG".format(name)] = os.environ[name]
    os.environ[name] = value

def get_envvar(name):
    return os.environ[name] if name in os.environ else None

def has_envvar(name):
    return name in os.environ

def del_envvar(name):
    if "{}_ORG".format(name) in os.environ:
        os.environ[name] = os.environ["{}_ORG".format(name)]
        del os.environ["{}_ORG".format(name)]
    elif name in os.environ:
        del os.environ[name]

def name_match(pat, names):
    match = []
    p = [x.strip() for x in pat.split(".")]
    for name in names:
        match.append(name)
        n = [x.strip() for x in name.split(".")]
        if len(p) > len(n):
            match.pop()
            break
        for a, b in zip(p, n[:len(p)]):
            if a != b:
                match.pop()
                break
    return match

def iterpath(path):
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(".py"):
                    yield os.path.join(dirpath, filename)
    elif path.endswith(".py"):
        yield path
    else:
        iter([])

def extract_zipfile(path, outdir=None):

    if outdir is None:
        outdir = tempfile.mkdtemp()
    task = zipfile.ZipFile(path)
    task.extractall(path=outdir)

    return outdir

def unparse_argument(opt):
    items = []
    items.append("@".join(opt.context))
    items.append(",".join(opt.vargs))
    items.append(",".join([k+"="+v for k,v in opt.kwargs.items()]))

    output = ""

    if items[0]:
        output += items[0]
        if items[1] or items[2]:
            output += "@"

    if items[1]:
        output += items[1]
        if items[2]:
            output += ","
    if items[2]:
        output += items[2]

    return output

def split_taskname(taskname):

    task_split = taskname.split("#", 1)
    if len(task_split) == 2:
        return tuple(task_split)
    else:
        return taskname, None

def is_taskpath(path):

    taskpath, fragment = split_taskname(path)
    head, base = os.path.split(taskpath)

    if base == "PERFTASK":
        return True

    if os.path.isfile(taskpath):
        head, base = os.path.split(taskpath)
        if base.endswith(".py"):
            return True
    elif os.path.isdir(taskpath):
        if os.path.isfile(os.path.join(taskpath, "__init__.py")):
            return True

    return False

def runcmd(cmd, cwd=None, env=None, shell=False):

    executable = None
    if shell is not False:
        executable = shell
        shell = True

    out = tempfile.TemporaryFile()
    err = tempfile.TemporaryFile()

    popen = subprocess.Popen(cmd, stdout=out, cwd=cwd, env=env,
        stderr=err, universal_newlines=True, shell=shell,
        executable=executable)

    retval = popen.wait()

    out.seek(0)
    err.seek(0)

    stdout = perftask_decode(out.read())
    stderr = perftask_decode(err.read())

    out.close()
    err.close()

    return retval, stdout, stderr

def stack_floc(depth=1):
    c = inspect.getframeinfo(inspect.stack()[depth][0])
    return {"filename": c.filename, "lineno": c.lineno, "ts": int(time.time())}

def load_pymod(head, base):
    sys.path.insert(0, head)
    m = perftask_import(base)
    sys.path.pop(0)
    return m

