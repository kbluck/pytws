'''Unit test package for module "tws._EClientSocket".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import socket
from StringIO import StringIO
from tws import EClientErrors, EClientSocket, EReader, EWrapper


# Local classes required to test EClientSocket
class _wrapper(EWrapper):

    def __init__(self):
        self.errors = []
    
    def error(self, id, code, text):
        self.errors.append((id, code, text))
        
class _fake_socket(object):

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


class test_EClientSocket(unittest.TestCase):
    '''Test class "tws.EClientSocket"'''
    
    def setUp(self):
        self.wrapper = _wrapper()
        self.client = EClientSocket(self.wrapper)

    def test_init(self):
        self.assertTrue(EClientSocket(_wrapper()))

        if __debug__:
            self.assertRaises(AssertionError, EClientSocket, 0)


    def test_api_versions(self):
        # Want to make sure to notice version changes.
        self.assertEqual(EClientSocket.CLIENT_VERSION, 42)
        self.assertEqual(EClientSocket.SERVER_VERSION, 38)

    def test_checkConnected(self):
        self.client._connected = True
        self.assertEqual(0, len(self.wrapper.errors))
        self.assertEqual(self.client.checkConnected(None), None)
        self.assertEqual(1, len(self.wrapper.errors))
        self.assertEqual(self.wrapper.errors[0],
                         (EClientErrors.NO_VALID_ID, 
                          EClientErrors.ALREADY_CONNECTED.code(),
                          EClientErrors.ALREADY_CONNECTED.msg()))
        
        self.client._connected = False
        self.assertEqual(self.client.checkConnected(None), "127.0.0.1")
        self.assertEqual(self.client.checkConnected("1.2.3.4"), "1.2.3.4")
        self.assertEqual(1, len(self.wrapper.errors))
        
        if __debug__:
            self.assertRaises(AssertionError, self.client.checkConnected, 0)
            
    def test_connectionError(self):
        self.assertEqual(0, len(self.wrapper.errors))
        self.client.connectionError()
        self.assertEqual(1, len(self.wrapper.errors))
        self.assertEqual(self.wrapper.errors[0],
                         (EClientErrors.NO_VALID_ID, 
                          EClientErrors.CONNECT_FAIL.code(),
                          EClientErrors.CONNECT_FAIL.msg()))

    def test_getters(self):
        self.assertEqual(self.client.wrapper(), self.wrapper)
        self.assertEqual(self.client.reader(), None)
        self.assertEqual(self.client.isConnected(), False)
        self.assertEqual(self.client.serverVersion(), "")
        self.assertEqual(self.client.TwsConnectionTime(), "")

    def test_MsgTypeName(self):
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.GROUPS), "GROUPS")
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.PROFILES), "PROFILES")
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.ALIASES), "ALIASES")

        if __debug__:
            self.assertRaises(AssertionError, EClientSocket.faMsgTypeName, 0)
            self.assertRaises(AssertionError, EClientSocket.faMsgTypeName, 4)
