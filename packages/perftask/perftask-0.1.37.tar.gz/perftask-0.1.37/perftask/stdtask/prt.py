# -*- coding: utf-8 -*-

"""print standard task module."""

from __future__ import unicode_literals

import re
import pprint

from ..util import perftask_print
from ..task import StandardTask

_re_unicode = re.compile("u'[^']*'")

class PrintTask(StandardTask):
    """show content of data
    """

    def __init__(self, parent, tid, path, fragment, argv):

        self.add_data_argument('data', nargs="*", evaluate=True, autoimport=True, help='input data.')

        self.add_option_argument('-s', '--str', metavar='object', action='append', help='run str() function.')
        self.add_option_argument('--version', action='version', version='print task version 0.1.0')

    def _repl(self, match):
        return '"{0}"'.format(self.teval(match.group(0)))

    def _print(self, text):
        substr = _re_unicode.sub(self._repl, text, re.I)
        perftask_print(substr)

    def perform(self, targs):

        printed = False

        if targs.str:
            for option in targs.str:
                for varg in option.vargs:
                    self._print("{0}".format(self.teval(varg)))
                    printed = True

        if not printed:
            if targs.data:
                pprint.pprint(targs.data)
            elif isinstance(self.env["D"], (list, tuple)):
                if self.env["D"]:
                    pprint.pprint(self.env["D"])
                else:
                    print("No data to print.")
            elif self.env["D"] is not None:
                pprint.pprint(self.env["D"])
            else:
                print("No data to print.")

        return 0
