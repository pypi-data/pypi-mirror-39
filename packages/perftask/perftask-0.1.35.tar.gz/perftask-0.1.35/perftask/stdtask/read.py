# -*- coding: utf-8 -*-

"""builtin task module."""

# TODO: divide builtins into mgmt and standard

from __future__ import unicode_literals

from ..task import StandardTask

class ReadTask(StandardTask):

    def perform(self):
        print("Task, 'read', is not supported yet.")

        return 0
