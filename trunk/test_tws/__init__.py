'''Unit test package for package "tws".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import socket
import logging
import tws

def test_import():
    '''Verify successful import of top-level "tws" package'''
    import tws
    assert tws

class mock_logger(logging.Logger):
    def __init__(self):
        logging.Logger.__init__(self, "mock")
        self.setLevel(logging.DEBUG)
        self.logs = []

    def _log(self, level, msg, args):
        self.logs.append((level, msg, args))

class mock_wrapper(tws.EWrapper):

    def __init__(self, logger=mock_logger()):
        tws.EWrapper.__init__(self, logger)
        self.calldata = []
        self.errors = []

    def error(self, e):
        if hasattr(e, 'id'):
            self.errors.append((e.id(), e.code(), e.msg()))
        else:
            self.errors.append((-1,type(e),e.args))

    def connectionClosed(self):
        # Override to log invocation to calldata.
        self.calldata.append(("connectionClosed", (), {}))

    def __getattr__(self, name):
        # Any arbitrary unknown attribute is mapped to a function call which is
        # recorded into self.calldata.
        return lambda *args, **kwds: self.calldata.append((name, args, kwds))


class mock_socket(object):

    def __init__(self):
        self._peer = ()

    def connect(self, peer, error=False):
        if error: raise socket.error()
        self._peer = peer

    def getpeername(self):
        if not self._peer: raise socket.error()
        return self._peer

    def makefile(self, mode):
        return StringIO()
