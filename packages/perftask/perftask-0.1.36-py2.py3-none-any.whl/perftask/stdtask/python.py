# -*- coding: utf-8 -*-

"""python standard task module."""

from __future__ import unicode_literals

import code

from ..task import StandardTask

class PythonTask(StandardTask):
    """launch an interactive python
    """

    def perform(self, targs):

        local_namespace = self.env.copy()

        try:
            import readline
            local_namespace["readline"] = readline
        except ImportError:
            pass

        shell = code.InteractiveConsole(local_namespace)
        shell.interact()

        return 0
