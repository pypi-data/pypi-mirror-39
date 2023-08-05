# -*- coding: utf-8 -*-

"""shell standard task module."""

from __future__ import unicode_literals

import os
import shlex

from ..task import StandardTask
from ..util import runcmd, perftask_print

class ShellCmdTask(StandardTask):
    """invoke an shell commands
    """

    def __init__(self, parent, tid, path, fragment, argv):
    
        self.add_data_argument('cmds', nargs="*", help='shell commands')
    
        self.add_option_argument('--cwd', metavar='path', help='working directory')
        self.add_option_argument('--shell', metavar='path', help='shell to use')

        # TODO: support | pipe, > rediction ...

    def perform(self, targs):

        retval = 0

        if targs.cmds:

            for cmd in targs.cmds:

                retval, stdout, stderr = runcmd(cmd, cwd=targs.cwd, shell=targs.shell)
               
                if retval != 0:
                    perftask_print("return value = %d"%retval)

                if stdout:
                    perftask_print("[stdout]\n%s"%stdout)

                if stderr:
                    perftask_print("[stderr]\n%s"%stderr)

        else:
            perftask_print(os.environ["SHELL"])

        return retval
