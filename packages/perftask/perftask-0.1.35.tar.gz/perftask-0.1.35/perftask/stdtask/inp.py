# -*- coding: utf-8 -*-

"""input standard task module."""

from __future__ import unicode_literals

from ..task import StandardTask

class InputTask(StandardTask):
    """transform input data to another
    """

    def __init__(self, parent, tid, path, fragment, argv):

        self.add_data_argument('data', nargs="*", evaluate=True, autoimport=True, help='input data.')

        self.add_option_argument('-a', '--assign', metavar='formula', evaluate=True, action='append', help='assignment statement.')

        # TODO: add more complex structure such as for loop and if block
        # --for --if --elif --else --while --with --try --except --finally 
        # [contextname @] expr
        # perform calc [1,2,3] -a 

    def perform(self, targs):

        if targs.assign:
            for assign in targs.assign:
                self.env.update(assign.kwargs)

        return 0
