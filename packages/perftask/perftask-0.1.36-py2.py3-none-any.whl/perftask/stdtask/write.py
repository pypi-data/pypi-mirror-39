# -*- coding: utf-8 -*-

"""builtin task module."""

# TODO: divide builtins into mgmt and standard

from __future__ import unicode_literals

from ..task import StandardTask

class WriteTask(StandardTask):

    def perform(self):
        print("Task, 'write', is not supported yet.")

        return 0
