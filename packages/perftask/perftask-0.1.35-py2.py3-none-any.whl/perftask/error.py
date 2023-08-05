# -*- coding: utf-8 -*-

"""error module."""

from __future__ import unicode_literals

import sys
import os

from .util import stack_floc

class PerftaskError(Exception):
    def __init__(self, msg, **kwargs):

        super(PerftaskError, self).__init__(msg)
 
        c = stack_floc(depth=2)
        self.filename = kwargs.get("filename", c["filename"])
        self.lineno = kwargs.get("lineno", c["lineno"])

class PTNormalExit(PerftaskError):

    def __init__(self):
        super(PTNormalExit, self).__init__("")

class PTUsageError(PerftaskError):
    pass

class PTInternalError(PerftaskError):
    pass

class PTTestError(PerftaskError):
    pass

class PTNameError(PerftaskError):
    pass
