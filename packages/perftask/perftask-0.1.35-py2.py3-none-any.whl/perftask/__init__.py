# -*- coding: utf-8 -*-
"""Top-level package for perftask."""

name = "perftask"
__author__ = """Youngsung Kim"""
__email__ = 'grnydawn@gmail.com'

from .task import Task              # noqa: F401
from .help import perftask_version  # noqa: F401
from .util import perftask_encode   # noqa: F401
from .util import perftask_decode   # noqa: F401

__version__ = perftask_version()

