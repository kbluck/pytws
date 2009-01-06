'''Unit test package for module "tws._EClientSocket".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from StringIO import StringIO
import tws
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

    def _check_min_server(self, version, ticker_id, method, *args, **kwds):
        self.client._server_version = (version - 1)
        self.assertTrue(self.client.serverVersion() < version)

        calldata_count = len(self.wrapper.calldata)
        error_count = len(self.wrapper.errors)
        method(*args, **kwds)

        self.assertEqual(len(self.wrapper.calldata), calldata_count)
        self.assertEqual(len(self.wrapper.errors), error_count + 1)
        self.assertEqual(self.wrapper.errors[-1][:2], (ticker_id, EClientErrors.UPDATE_TWS.code()))

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

        @_requestmethod(min_server=2000, min_server_error_suffix="Test2000")        
        def test_call(self):
            self._wrapper.test_call()
        
        @_requestmethod(generic_error=EClientErrors.UNKNOWN_ID, generic_error_suffix="Test123")        
        def test_raise_no_ticker(self):
            raise Exception()

        @_requestmethod(generic_error=EClientErrors.UNKNOWN_ID, has_ticker=True)        
        def test_raise_with_ticker(self, ticker_id):
            assert type(ticker_id) == int
            raise Exception()

        self._check_connection_required(test_call, self.client)

        self._check_min_server(2000, EClientErrors.NO_VALID_ID, test_call, self.client)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. Test2000")

        # Check exception raised for no ticker method
        self._check_error_raised(EClientErrors.UNKNOWN_ID, -1, test_raise_no_ticker, self.client)
        self.assertEqual(self.wrapper.errors[-1][2], "Fatal Error: Unknown message id. Test123")

        # Check exception raised for ticker method, both positional and keyword
        test_raise_with_ticker(self.client, 123)
        test_raise_with_ticker(self.client, ticker_id=321)
        self.assertEqual(len(self.wrapper.calldata), 0)
        self.assertEqual(len(self.wrapper.errors), 5)
        self.assertEqual(self.wrapper.errors[3][:2], (123, 505))
        self.assertEqual(self.wrapper.errors[4][:2], (321, 505))
        self.assertEqual(self.wrapper.errors[3][2], "Fatal Error: Unknown message id. test_raise_with_ticker")

        # Check assertion is not caught by wrapper
        if __debug__:
            self.assertRaises(AssertionError, test_raise_with_ticker, self.client, None)

        # Check successful call
        test_call(self.client)
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 5)
        self.assertEqual(self.wrapper.calldata[0][0], "test_call")

    def test_cancelScannerSubscription(self):
        self._check_connection_required(self.client.cancelScannerSubscription, 0)
        self._check_min_server(24, 1, self.client.cancelScannerSubscription, 1)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support API scanner subscription.")
        self._check_error_raised(EClientErrors.FAIL_SEND_CANSCANNER, 2,
                                 self.client.cancelScannerSubscription, 2)

        self.client.cancelScannerSubscription(3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.CANCEL_SCANNER_SUBSCRIPTION,
                         self.stream.getvalue())

        if __debug__:
            self.assertRaises(AssertionError, self.client.cancelScannerSubscription, 3.5)

    def test_reqScannerParameters(self):
        self._check_connection_required(self.client.cancelScannerSubscription)
        self._check_min_server(24, EClientErrors.NO_VALID_ID, self.client.cancelScannerSubscription)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support API scanner subscription.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQSCANNERPARAMETERS,
                                 EClientErrors.NO_VALID_ID,
                                 self.client.reqScannerParameters)

        self.client.reqScannerParameters()
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x00" %
                         self.client.REQ_SCANNER_PARAMETERS,
                         self.stream.getvalue())


    def test_reqScannerSubscription(self):
        subscription = tws.ScannerSubscription()
        
        self._check_connection_required(self.client.reqScannerSubscription, 1, subscription)
        self._check_min_server(24, 2, self.client.reqScannerSubscription, 2, subscription)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support API scanner subscription.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQSCANNER, 3,
                                 self.client.reqScannerSubscription,
                                 3, subscription)

        self.assertEqual(self.client.serverVersion(), 24)
        self.client.reqScannerSubscription(4, subscription)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x003\x004\x00-1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" %
                         self.client.REQ_SCANNER_SUBSCRIPTION,
                         self.stream.getvalue())
        
        subscription.numberOfRows(1)
        subscription.instrument("A1")
        subscription.locationCode("B2")
        subscription.scanCode("C3")
        subscription.abovePrice(1.5)
        subscription.belowPrice(2.5)
        subscription.aboveVolume(3)
        subscription.averageOptionVolumeAbove(4)
        subscription.marketCapAbove(5.5)
        subscription.marketCapBelow(6.5)
        subscription.moodyRatingAbove("D4")
        subscription.moodyRatingBelow("E5")
        subscription.spRatingAbove("F6")
        subscription.spRatingBelow("G7")
        subscription.maturityDateAbove("H8")
        subscription.maturityDateBelow("I9")
        subscription.couponRateAbove(7.5)
        subscription.couponRateBelow(8.5)
        subscription.excludeConvertible("J1")
        subscription.scannerSettingPairs("K2")
        subscription.stockTypeFilter("L3")

        self.assertEqual(self.client.serverVersion(), 24)
        self.stream.truncate(0)
        self.client.reqScannerSubscription(5, subscription)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x003\x005\x001\x00A1\x00B2\x00C3\x001.5\x002.5\x003\x005.5\x006.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x007.5\x008.5\x00J1\x00" %
                         self.client.REQ_SCANNER_SUBSCRIPTION,
                         self.stream.getvalue())

        self.client._server_version = 25
        self.assertEqual(self.client.serverVersion(), 25)
        self.stream.truncate(0)
        self.client.reqScannerSubscription(6, subscription)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x003\x006\x001\x00A1\x00B2\x00C3\x001.5\x002.5\x003\x005.5\x006.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x007.5\x008.5\x00J1\x004\x00K2\x00" %
                         self.client.REQ_SCANNER_SUBSCRIPTION,
                         self.stream.getvalue())

        self.client._server_version = 27
        self.assertEqual(self.client.serverVersion(), 27)
        self.stream.truncate(0)
        self.client.reqScannerSubscription(7, subscription)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x003\x007\x001\x00A1\x00B2\x00C3\x001.5\x002.5\x003\x005.5\x006.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x007.5\x008.5\x00J1\x004\x00K2\x00L3\x00" %
                         self.client.REQ_SCANNER_SUBSCRIPTION,
                         self.stream.getvalue())

        if __debug__:
            self.assertRaises(AssertionError, self.client.reqScannerSubscription, 3.5, subscription)
            self.assertRaises(AssertionError, self.client.reqScannerSubscription, 3, None)

    def test_reqMktData(self):
        self._check_connection_required(self.client.reqMktData, 0, tws.Contract(), "", False)
        self._check_error_raised(EClientErrors.FAIL_SEND_REQMKT, 1,
                                 self.client.reqMktData, 1, tws.Contract(), "", False)

        contract = tws.Contract()
        contract.m_underComp.m_conId = 1 
        self._check_min_server(self.client.MIN_SERVER_VER_UNDER_COMP, 1, self.client.reqMktData,
                               1, contract, "", False)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support delta-neutral orders.")
        
        self._check_min_server(self.client.MIN_SERVER_VER_SNAPSHOT_MKT_DATA, 2, self.client.reqMktData,
                               2, tws.Contract(), "", True)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support snapshot market data requests.")

        contract = tws.Contract(con_id=1, symbol="A1", sec_type="B2", expiry="C3", strike=2.5,
                                right="D4", multiplier="E5", exchange="F6", currency="G7",
                                local_symbol="H8", primary_exch="I9", include_expired=True,
                                combo_legs=[tws.ComboLeg(3, 4, "J1", "K2", 5, 6, "L3"),
                                            tws.ComboLeg(7, 8, "M4", "N5", 9, 10, "O6")])

        self.client._server_version = 1
        self.assertEqual(self.client.serverVersion(), 1)
        self.stream.truncate(0)
        self.client.reqMktData(11, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0011\x00A1\x00B2\x00C3\x002.5\x00D4\x00F6\x00G7\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        self.client._server_version = 2
        self.assertEqual(self.client.serverVersion(), 2)
        self.stream.truncate(0)
        self.client.reqMktData(12, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0012\x00A1\x00B2\x00C3\x002.5\x00D4\x00F6\x00G7\x00H8\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        self.client._server_version = 8
        self.assertEqual(self.client.serverVersion(), 8)
        self.stream.truncate(0)
        self.client.reqMktData(13, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0013\x00A1\x00B2\x00C3\x002.5\x00D4\x00F6\x00G7\x00H8\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        legs = contract.m_comboLegs
        contract.m_comboLegs = []
        contract.m_secType = self.client.BAG_SEC_TYPE        
        self.stream.truncate(0)
        self.client.reqMktData(14, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0014\x00A1\x00BAG\x00C3\x002.5\x00D4\x00F6\x00G7\x00H8\x000\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        contract.m_comboLegs = legs
        self.stream.truncate(0)
        self.client.reqMktData(15, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0015\x00A1\x00BAG\x00C3\x002.5\x00D4\x00F6\x00G7\x00H8\x002\x003\x004\x00J1\x00K2\x007\x008\x00M4\x00N5\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())
        contract.m_secType = "B2"

        self.client._server_version = 14
        self.assertEqual(self.client.serverVersion(), 14)
        self.stream.truncate(0)
        self.client.reqMktData(16, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0016\x00A1\x00B2\x00C3\x002.5\x00D4\x00F6\x00I9\x00G7\x00H8\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        self.client._server_version = 15
        self.assertEqual(self.client.serverVersion(), 15)
        self.stream.truncate(0)
        self.client.reqMktData(17, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0017\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        self.client._server_version = 31
        self.assertEqual(self.client.serverVersion(), 31)
        self.stream.truncate(0)
        self.client.reqMktData(18, contract, "P7", False)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0018\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x00P7\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        self.client._server_version = self.client.MIN_SERVER_VER_SNAPSHOT_MKT_DATA
        self.assertEqual(self.client.serverVersion(), self.client.MIN_SERVER_VER_SNAPSHOT_MKT_DATA)
        self.stream.truncate(0)
        self.client.reqMktData(19, contract, "P7", True)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x00P7\x001\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())


        self.client._server_version = self.client.MIN_SERVER_VER_UNDER_COMP
        self.assertEqual(self.client.serverVersion(), self.client.MIN_SERVER_VER_UNDER_COMP)
        self.stream.truncate(0)
        self.client.reqMktData(20, contract, "P7", True)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0020\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x000\x00P7\x001\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        contract.m_underComp.m_conId = 100
        contract.m_underComp.m_delta = 200.5
        contract.m_underComp.m_price = 300.5
        self.assertEqual(self.client.serverVersion(), self.client.MIN_SERVER_VER_UNDER_COMP)
        self.stream.truncate(0)
        self.client.reqMktData(20, contract, "P7", True)
        self.assertEqual(len(self.wrapper.errors), 4)
        self.assertEqual("%s\x008\x0020\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x001\x00100\x00200.5\x00300.5\x00P7\x001\x00" %
                         self.client.REQ_MKT_DATA,
                         self.stream.getvalue())

        if __debug__:
           self.assertRaises(AssertionError, self.client.reqMktData, 1.5, tws.Contract(), "", False)
           self.assertRaises(AssertionError, self.client.reqMktData, 1, None, "", False)
           self.assertRaises(AssertionError, self.client.reqMktData, 1, tws.Contract(), None, False)
           self.assertRaises(AssertionError, self.client.reqMktData, 1, tws.Contract(), "", None)

    def test_cancelHistoricalData(self):
        self._check_connection_required(self.client.cancelHistoricalData, 0)
        self._check_min_server(24, 1, self.client.cancelHistoricalData, 1)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support historical data query cancellation.")
        self._check_error_raised(EClientErrors.FAIL_SEND_CANHISTDATA, 2,
                                 self.client.cancelHistoricalData, 2)

        self.client.cancelHistoricalData(3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.CANCEL_HISTORICAL_DATA,
                         self.stream.getvalue())

        if __debug__:
            self.assertRaises(AssertionError, self.client.cancelHistoricalData, 3.5)

    def test_cancelRealTimeBars(self):
        self._check_connection_required(self.client.cancelRealTimeBars, 0)
        self._check_min_server(self.client.MIN_SERVER_VER_REAL_TIME_BARS, 1, self.client.cancelRealTimeBars, 1)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support realtime bar data query cancellation.")
        self._check_error_raised(EClientErrors.FAIL_SEND_CANRTBARS, 2,
                                 self.client.cancelRealTimeBars, 2)

        self.client.cancelRealTimeBars(3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.CANCEL_REAL_TIME_BARS,
                         self.stream.getvalue())

        if __debug__:
            self.assertRaises(AssertionError, self.client.cancelRealTimeBars, 3.5)

    def test_reqHistoricalData(self):
        self._check_connection_required(self.client.reqHistoricalData, 0, tws.Contract(),"","","","",0,0)
        self._check_min_server(16, 1, self.client.reqHistoricalData, 1, tws.Contract(),"","","","",0,0)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support historical data backfill.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQHISTDATA, 2,
                                 self.client.reqHistoricalData, 2, tws.Contract(),"","","","",0,0)

        contract = tws.Contract(con_id=1, symbol="A1", sec_type="B2", expiry="C3", strike=2.5,
                                right="D4", multiplier="E5", exchange="F6", currency="G7",
                                local_symbol="H8", primary_exch="I9", include_expired=True,
                                combo_legs=[tws.ComboLeg(3, 4, "J1", "K2", 5, 6, "L3"),
                                            tws.ComboLeg(7, 8, "M4", "N5", 9, 10, "O6")])

        self.client._server_version = 16
        self.assertEqual(self.client.serverVersion(), 16)
        self.stream.truncate(0)
        self.client.reqHistoricalData(14, contract, "P7", "Q8", "R9", "S1", 11, 12)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x004\x0014\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x00Q8\x0011\x00S1\x00" %
                         self.client.REQ_HISTORICAL_DATA,
                         self.stream.getvalue())

        self.client._server_version = 17
        self.assertEqual(self.client.serverVersion(), 17)
        self.stream.truncate(0)
        self.client.reqHistoricalData(15, contract, "P7", "Q8", "R9", "S1", 11, 12)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x004\x0015\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x00Q8\x0011\x00S1\x0012\x00" %
                         self.client.REQ_HISTORICAL_DATA,
                         self.stream.getvalue())

        self.client._server_version = 20
        self.assertEqual(self.client.serverVersion(), 20)
        self.stream.truncate(0)
        self.client.reqHistoricalData(16, contract, "P7", "Q8", "R9", "S1", 11, 12)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x004\x0016\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x00P7\x00R9\x00Q8\x0011\x00S1\x0012\x00" %
                         self.client.REQ_HISTORICAL_DATA,
                         self.stream.getvalue())

        self.client._server_version = 31
        self.assertEqual(self.client.serverVersion(), 31)
        self.stream.truncate(0)
        self.client.reqHistoricalData(17, contract, "P7", "Q8", "R9", "S1", 11, 12)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x004\x0017\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x001\x00P7\x00R9\x00Q8\x0011\x00S1\x0012\x00" %
                         self.client.REQ_HISTORICAL_DATA,
                         self.stream.getvalue())
       
        contract.m_secType = self.client.BAG_SEC_TYPE        
        self.stream.truncate(0)
        self.client.reqHistoricalData(17, contract, "P7", "Q8", "R9", "S1", 11, 12)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x004\x0017\x00A1\x00BAG\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x001\x00P7\x00R9\x00Q8\x0011\x00S1\x0012\x002\x003\x004\x00J1\x00K2\x007\x008\x00M4\x00N5\x00" %
                         self.client.REQ_HISTORICAL_DATA,
                         self.stream.getvalue())

        if __debug__:
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1.5,tws.Contract(),"","","","",0,0)
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1, "","","","","",0,0)
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1,tws.Contract(),1,"","","",0,0)
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1,tws.Contract(),"",1,"","",0,0)
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1,tws.Contract(),"","",1,"",0,0)
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1,tws.Contract(),"","","",1,0,0)
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1,tws.Contract(),"","","","","",0)
           self.assertRaises(AssertionError, self.client.reqHistoricalData, 1,tws.Contract(),"","","","",0,"")

    def test_reqRealTimeBars(self):
        self._check_connection_required(self.client.reqRealTimeBars, 0, tws.Contract(),"","",0)
        self._check_min_server(self.client.MIN_SERVER_VER_REAL_TIME_BARS, 1, self.client.reqRealTimeBars, 1, tws.Contract(),"","",0)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support real time bars.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQRTBARS, 2,
                                 self.client.reqRealTimeBars, 2, tws.Contract(),"","",0)

        contract = tws.Contract(con_id=1, symbol="A1", sec_type="B2", expiry="C3", strike=2.5,
                                right="D4", multiplier="E5", exchange="F6", currency="G7",
                                local_symbol="H8", primary_exch="I9", include_expired=True)

        self.client._server_version = self.client.MIN_SERVER_VER_REAL_TIME_BARS
        self.assertEqual(self.client.serverVersion(), self.client.MIN_SERVER_VER_REAL_TIME_BARS)
        self.stream.truncate(0)
        self.client.reqRealTimeBars(4, contract, "P7", "Q8", 11)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x004\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00I9\x00G7\x00H8\x00P7\x00Q8\x0011\x00" %
                         self.client.REQ_REAL_TIME_BARS,
                         self.stream.getvalue())

        if __debug__:
           self.assertRaises(AssertionError, self.client.reqRealTimeBars, 1.5,tws.Contract(),"","",0)
           self.assertRaises(AssertionError, self.client.reqRealTimeBars, 1, "","","",0)
           self.assertRaises(AssertionError, self.client.reqRealTimeBars, 1,tws.Contract(),1,"",0)
           self.assertRaises(AssertionError, self.client.reqRealTimeBars, 1,tws.Contract(),"",1,0)
           self.assertRaises(AssertionError, self.client.reqRealTimeBars, 1,tws.Contract(),"","","")

    def test_reqContractDetails(self):
        self._check_connection_required(self.client.reqContractDetails, 0, tws.Contract())
        self._check_min_server(4, EClientErrors.NO_VALID_ID, self.client.reqContractDetails, 1, tws.Contract())
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support contract details.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQCONTRACT, EClientErrors.NO_VALID_ID,
                                 self.client.reqContractDetails, 2, tws.Contract())

        contract = tws.Contract(con_id=1, symbol="A1", sec_type="B2", expiry="C3", strike=2.5,
                                right="D4", multiplier="E5", exchange="F6", currency="G7",
                                local_symbol="H8", primary_exch="I9", include_expired=True)

        self.client._server_version = 4
        self.assertEqual(self.client.serverVersion(), 4)
        self.stream.truncate(0)
        self.client.reqContractDetails(4, contract)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x005\x00A1\x00B2\x00C3\x002.5\x00D4\x00F6\x00G7\x00H8\x00" %
                         self.client.REQ_CONTRACT_DATA,
                         self.stream.getvalue())

        self.client._server_version = 15
        self.assertEqual(self.client.serverVersion(), 15)
        self.stream.truncate(0)
        self.client.reqContractDetails(5, contract)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x005\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00" %
                         self.client.REQ_CONTRACT_DATA,
                         self.stream.getvalue())

        self.client._server_version = 31
        self.assertEqual(self.client.serverVersion(), 31)
        self.stream.truncate(0)
        self.client.reqContractDetails(6, contract)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x005\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x00H8\x001\x00" %
                         self.client.REQ_CONTRACT_DATA,
                         self.stream.getvalue())

        self.client._server_version = self.client.MIN_SERVER_VER_CONTRACT_CONID
        self.assertEqual(self.client.serverVersion(), self.client.MIN_SERVER_VER_CONTRACT_CONID)
        self.stream.truncate(0)
        self.client.reqContractDetails(4, contract)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x005\x001\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x00H8\x001\x00" %
                         self.client.REQ_CONTRACT_DATA,
                         self.stream.getvalue())

        self.client._server_version = self.client.MIN_SERVER_VER_CONTRACT_DATA_CHAIN
        self.assertEqual(self.client.serverVersion(), self.client.MIN_SERVER_VER_CONTRACT_DATA_CHAIN)
        self.stream.truncate(0)
        self.client.reqContractDetails(4, contract)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x005\x004\x001\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x00H8\x001\x00" %
                         self.client.REQ_CONTRACT_DATA,
                         self.stream.getvalue())

    def test_reqMktDepth(self):
        self._check_connection_required(self.client.reqMktDepth, 0, tws.Contract(), 0)
        self._check_min_server(6, 1, self.client.reqMktDepth, 1, tws.Contract(), 0)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support market depth.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQMKTDEPTH, 2,
                                 self.client.reqMktDepth, 2, tws.Contract(), 0)

        contract = tws.Contract(con_id=1, symbol="A1", sec_type="B2", expiry="C3", strike=2.5,
                                right="D4", multiplier="E5", exchange="F6", currency="G7",
                                local_symbol="H8", primary_exch="I9", include_expired=True)

        self.client._server_version = 6
        self.assertEqual(self.client.serverVersion(), 6)
        self.stream.truncate(0)
        self.client.reqMktDepth(4, contract, 3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x003\x004\x00A1\x00B2\x00C3\x002.5\x00D4\x00F6\x00G7\x00H8\x00" %
                         self.client.REQ_MKT_DEPTH,
                         self.stream.getvalue())

        self.client._server_version = 15
        self.assertEqual(self.client.serverVersion(), 15)
        self.stream.truncate(0)
        self.client.reqMktDepth(5, contract, 3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x003\x005\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00" %
                         self.client.REQ_MKT_DEPTH,
                         self.stream.getvalue())

        self.client._server_version = 19
        self.assertEqual(self.client.serverVersion(), 19)
        self.stream.truncate(0)
        self.client.reqMktDepth(6, contract, 3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x003\x006\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x00H8\x003\x00" %
                         self.client.REQ_MKT_DEPTH,
                         self.stream.getvalue())

        if __debug__:
           self.assertRaises(AssertionError, self.client.reqMktDepth, "",tws.Contract(),0)
           self.assertRaises(AssertionError, self.client.reqMktDepth, 1,"",0)
           self.assertRaises(AssertionError, self.client.reqMktDepth, 1,tws.Contract(),"")
