# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from .common import PY3

if PY3:

    from importlib import __import__ as perftask_import

    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.error import HTTPError, URLError

    import configparser

    from io import StringIO, BytesIO

    def perftask_print(msg, **kwargs):
        if type(msg) == type(b"a"):
            print(msg.decode("utf-8"), **kwargs)
        else:
            print(msg, **kwargs)

    def perftask_mp_set_start_method(method):
        import multiprocessing
        multiprocessing.set_start_method(method)
else:

    perftask_import = __import__

    from urllib2 import urlopen, HTTPError, URLError
    from urlparse import urlparse

    import ConfigParser as configparser

    from StringIO import StringIO
    from cStringIO import StringIO as BytesIO

    def perftask_print(msg, **kwargs):
        if type(msg) == type(u"A"):
            print(msg.encode("utf-8"), **kwargs)
        else:
            print(msg, **kwargs)

    def perftask_mp_set_start_method(method):
        pass
