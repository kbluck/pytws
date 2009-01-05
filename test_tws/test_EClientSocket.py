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
        self.stream = StringIO()
        self.client._stream = self.stream

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
        self.client._send("ABC")
        self.client._send(123)
        self.client._send(1234.5)
        self.client._send(123456789012345)
        self.client._send(True)
        self.client._send(False)
        self.client._send(None)

        self.assertEqual("ABC\x00123\x001234.5\x00123456789012345\x001\x000\x00\x00",
                         self.stream.getvalue())

        self.assertRaises(ValueError, self.client._send, object())

    def test_sendMax(self):
        self.client._sendMax(123)
        self.client._sendMax(1234.5)
        self.client._sendMax(self.client._INT_MAX_VALUE)
        self.client._sendMax(self.client._DOUBLE_MAX_VALUE)

        self.assertEqual("123\x001234.5\x00\x00\x00",
                         self.stream.getvalue())

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

    def _check_connection_required(self, method, *args, **kwds):
        self.assertFalse(self.client.isConnected())

        calldata_count = len(self.wrapper.calldata)
        error_count = len(self.wrapper.errors)
        method(*args, **kwds)

        self.assertEqual(len(self.wrapper.calldata), calldata_count)
        self.assertEqual(len(self.wrapper.errors), error_count + 1)
        self.assertEqual(self.wrapper.errors[-1][:2], (EClientErrors.NO_VALID_ID, EClientErrors.NOT_CONNECTED.code()))
        self.client.eConnect()

    def _check_min_server(self, version, method, *args, **kwds):
        self.assertTrue(self.client.serverVersion() < version)

        calldata_count = len(self.wrapper.calldata)
        error_count = len(self.wrapper.errors)
        method(*args, **kwds)

        self.assertEqual(len(self.wrapper.calldata), calldata_count)
        self.assertEqual(len(self.wrapper.errors), error_count + 1)
        self.assertEqual(self.wrapper.errors[-1][:2], (EClientErrors.NO_VALID_ID, EClientErrors.UPDATE_TWS.code()))

        self.client._server_version = version

    def _check_error_raised(self, error, ticker_id, method, *args, **kwds):
        error_count = len(self.wrapper.errors)
        old_send = self.client._send
        self.client._send = None    # Forces exception
        method(*args, **kwds)
        self.client._send = old_send

        self.assertEqual(len(self.wrapper.errors), error_count + 1)
        self.assertEqual(self.wrapper.errors[-1][:2], (ticker_id, error.code()))

    def test_requestmethod_decorator(self):
        from tws._EClientSocket import _requestmethod

        @_requestmethod(min_server=2000)        
        def test_call(self):
            self._wrapper.test_call()
        
        @_requestmethod(generic_error=EClientErrors.UNKNOWN_ID, error_suffix="Test123")        
        def test_raise_no_ticker(self):
            raise Exception()

        @_requestmethod(generic_error=EClientErrors.UNKNOWN_ID, has_ticker=True)        
        def test_raise_with_ticker(self, ticker_id):
            raise Exception()

        self._check_connection_required(test_call, self.client)
        self._check_min_server(2000, test_call, self.client)

        # Check exception raised for no ticker method
        self._check_error_raised(EClientErrors.UNKNOWN_ID, -1, test_raise_no_ticker, self.client)
        self.assertEqual(self.wrapper.errors[-1][2], "Fatal Error: Unknown message id.: Test123")

        # Check exception raised for ticker method, both positional and keyword
        test_raise_with_ticker(self.client, 123)
        test_raise_with_ticker(self.client, ticker_id=321)
        self.assertEqual(len(self.wrapper.calldata), 0)
        self.assertEqual(len(self.wrapper.errors), 5)
        self.assertEqual(self.wrapper.errors[3][:2], (123, 505))
        self.assertEqual(self.wrapper.errors[4][:2], (321, 505))
        self.assertEqual(self.wrapper.errors[3][2], "Fatal Error: Unknown message id.: test_raise_with_ticker")

        # Check successful call
        test_call(self.client)
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 5)
        self.assertEqual(self.wrapper.calldata[0][0], "test_call")

    def test_cancelScannerSubscription(self):
        self._check_connection_required(self.client.cancelScannerSubscription, 0)
        self._check_min_server(24, self.client.cancelScannerSubscription, 1)
        self._check_error_raised(EClientErrors.FAIL_SEND_CANSCANNER, 2,
                                 self.client.cancelScannerSubscription, 2)

        self.client.cancelScannerSubscription(3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.CANCEL_SCANNER_SUBSCRIPTION,
                         self.stream.getvalue())

    def test_reqScannerParameters(self):
        self._check_connection_required(self.client.cancelScannerSubscription)
        self._check_min_server(24, self.client.cancelScannerSubscription)
        self._check_error_raised(EClientErrors.FAIL_SEND_REQSCANNERPARAMETERS,
                                 EClientErrors.NO_VALID_ID,
                                 self.client.reqScannerParameters)

        self.client.reqScannerParameters()
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x00" %
                         self.client.REQ_SCANNER_PARAMETERS,
                         self.stream.getvalue())
