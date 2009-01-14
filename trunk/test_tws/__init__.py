'''Unit test package for package "tws".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import socket
import threading
import tws


def test_import():
    '''Verify successful import of top-level "tws" package'''
    import tws
    assert tws


class mock_wrapper(tws.EWrapper):

    def __init__(self, logger=None):
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


class test_synchronized(unittest.TestCase):
    '''Test decorator "tws.synchronized"'''

    def setUp(self):
        self._mutex = threading.Lock()
        self._old_mutex = tws._mutex
        tws._mutex = self._mutex

    def tearDown(self):
        tws._mutex = self._old_mutex

    @tws.synchronized
    def mock_function(self, *args, **kwds):
        self.assertTrue(self._mutex.locked())
        return (args, kwds)

    @tws.synchronized
    def throws(self):
        self.assertTrue(self._mutex.locked())
        raise Exception()

    def test_decorator(self):
        self.assertFalse(self._mutex.locked())
        self.assertEqual(self.mock_function(1, "B", c="C"),
                        ((1,"B"),{"c":"C"}))
        self.assertFalse(self._mutex.locked())
        self.assertRaises(Exception, self.throws)
        self.assertFalse(self._mutex.locked())
