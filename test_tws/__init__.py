'''Unit test package for package "tws".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import socket
from tws import EWrapper


def test_import():
    '''Verify successful import of top-level "tws" package'''
    import tws
    assert tws


class mock_wrapper(EWrapper):

    def __init__(self):
        self.calldata = []
        self.errors = []
    
    def error(self, e):
        if hasattr(e, 'id'):
            self.errors.append((e.id(), e.code(), e.msg()))
        else:
            self.errors.append((-1,type(e),e.args))

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



