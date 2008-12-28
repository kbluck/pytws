'''Unit test package for module "tws._EClientSocket".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from StringIO import StringIO
from tws import EClientSocket, EClientErrors, EReader
from test_tws import mock_wrapper, mock_socket


# Local classes required to test EClientSocket
class test_EClientSocket(unittest.TestCase):
    '''Test class "tws.EClientSocket"'''

    def setUp(self):
        self.wrapper = mock_wrapper()
        self.client = EClientSocket(self.wrapper)

    def test_init(self):
        self.assertTrue(EClientSocket(mock_wrapper()))
        self.assertTrue(EClientSocket(mock_wrapper(), mock_socket))

        if __debug__:
            self.assertRaises(AssertionError, EClientSocket, 0)
            self.assertRaises(AssertionError, EClientSocket, self.wrapper, 0)

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

    def test_createReader(self):
        self.assertTrue(issubclass(type(
            self.client.createReader(self.client, StringIO())), EReader))

        if __debug__:
            self.assertRaises(AssertionError, self.client.createReader, 1, StringIO())
            self.assertRaises(AssertionError, self.client.createReader, self.client, 1)

    def test_getters(self):
        self.assertEqual(self.client.wrapper(), self.wrapper)
        self.assertEqual(self.client.reader(), None)
        self.assertEqual(self.client.isConnected(), False)
        self.assertEqual(self.client.serverVersion(), 0)
        self.assertEqual(self.client.TwsConnectionTime(), 0)

    def test_MsgTypeName(self):
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.GROUPS), "GROUPS")
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.PROFILES), "PROFILES")
        self.assertEqual(EClientSocket.faMsgTypeName(EClientSocket.ALIASES), "ALIASES")

        if __debug__:
            self.assertRaises(AssertionError, EClientSocket.faMsgTypeName, 0)
            self.assertRaises(AssertionError, EClientSocket.faMsgTypeName, 4)

    def test_eConnect(self):
        # Method is stubbed for now.
        self.assertFalse(self.client.isConnected())
        self.client.eConnect()
        self.assertTrue(self.client.isConnected())
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(len(self.wrapper.calldata), 0)

    def test_eDisconnect(self):
        # Method is stubbed for now.
        self.assertFalse(self.client.isConnected())
        self.client.eConnect()
        self.assertTrue(self.client.isConnected())
        self.client.eDisconnect()
        self.assertFalse(self.client.isConnected())
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(len(self.wrapper.calldata), 0)

    def test_send(self):
        self.client._stream = StringIO() #Inject mock stream

        self.client._send("ABC")
        self.client._send(123)
        self.client._send(1234.5)
        self.client._send(123456789012345)
        self.client._send(True)
        self.client._send(False)
        self.client._send(None)

        self.assertEqual("ABC\x00123\x001234.5\x00123456789012345\x001\x000\x00\x00",
                         self.client._stream.getvalue())

        self.assertRaises(ValueError, self.client._send, object())

    def test_sendMax(self):
        self.client._stream = StringIO() #Inject mock stream

        self.client._sendMax(123)
        self.client._sendMax(1234.5)
        self.client._sendMax(self.client._INT_MAX_VALUE)
        self.client._sendMax(self.client._DOUBLE_MAX_VALUE)

        self.assertEqual("123\x001234.5\x00\x00\x00",
                         self.client._stream.getvalue())

        self.assertRaises(ValueError, self.client._sendMax, "")

    def test_error(self):
        self.client._error(Exception())
        self.assertEqual(len(self.wrapper.calldata), 0)
        self.assertEqual(len(self.wrapper.errors), 1)
        self.assertEqual(self.wrapper.errors[0], (-1, Exception, ()))

    def test_close(self):
        self.client.eConnect()
        self.assertTrue(self.client.isConnected())
        self.client._close()
        self.assertFalse(self.client.isConnected())

        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(self.wrapper.calldata[0], ('connectionClosed', (), {}))
