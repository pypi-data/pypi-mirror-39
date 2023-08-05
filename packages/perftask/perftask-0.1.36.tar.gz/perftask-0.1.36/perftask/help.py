# -*- coding: utf-8 -*-

"""help module."""

from __future__ import unicode_literals

__version__ = "0.1.36"

def short_help():

    lines = []

    # TODO: may use textwrap dedent
    lines.append("perftask version "+perftask_version())
    lines.append("usage: perform [task] [task-arg...] "
                 "[-- <task> [task-arg...]]...")

    return lines

def short_desc():

    desc = """"perftask" is a Python library and command-line tool
for creation, execution, combination, packaging, and
sharing of the highly configurable Python programs, or tasks."""

    return desc

def long_desc():

    return "instant task infrastructure"

def license():
    return "MIT License"

def long_help():
    lines = short_help()
    lines.append("")

    lines.append(short_desc())

    return lines

def perftask_version():
    return __version__

