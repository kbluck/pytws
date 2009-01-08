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
        self.client.eConnect(0)
        self.assertTrue(self.client.isConnected())
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(len(self.wrapper.calldata), 0)

    def test_eDisconnect(self):
        # Method is stubbed for now.
        self.assertFalse(self.client.isConnected())
        self.client.eConnect(0)
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
        self.client.eConnect(0)
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
        self.client.eConnect(0)

    def _check_min_server(self, version, id, method, *args, **kwds):
        self.client._server_version = (version - 1)
        self.assertTrue(self.client.serverVersion() < version)

        calldata_count = len(self.wrapper.calldata)
        error_count = len(self.wrapper.errors)
        method(*args, **kwds)

        self.assertEqual(len(self.wrapper.calldata), calldata_count)
        self.assertEqual(len(self.wrapper.errors), error_count + 1)
        self.assertEqual(self.wrapper.errors[-1][:2], (id, EClientErrors.UPDATE_TWS.code()))

        self.client._server_version = version

    def _check_error_raised(self, error, id, method, *args, **kwds):
        error_count = len(self.wrapper.errors)
        old_send = self.client._send
        self.client._send = None    # Forces exception
        method(*args, **kwds)
        self.client._send = old_send

        self.assertEqual(len(self.wrapper.errors), error_count + 1)
        self.assertEqual(self.wrapper.errors[-1][:2], (id, error.code()))

    def test_requestmethod_decorator(self):
        from tws._EClientSocket import _requestmethod

        @_requestmethod(min_server=2000, min_server_error_suffix="Test2000")
        def test_call(self):
            self._wrapper.test_call()

        @_requestmethod(generic_error=EClientErrors.UNKNOWN_ID, generic_error_suffix="Test123")
        def test_raise_no_ticker(self):
            raise Exception()

        @_requestmethod(generic_error=EClientErrors.UNKNOWN_ID, has_id=True)
        def test_raise_with_ticker(self, id):
            assert type(id) == int
            raise Exception()

        self._check_connection_required(test_call, self.client)

        self._check_min_server(2000, EClientErrors.NO_VALID_ID, test_call, self.client)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. Test2000")

        # Check exception raised for no ticker method
        self._check_error_raised(EClientErrors.UNKNOWN_ID, -1, test_raise_no_ticker, self.client)
        self.assertEqual(self.wrapper.errors[-1][2], "Fatal Error: Unknown message id. Test123")

        # Check exception raised for ticker method, both positional and keyword
        test_raise_with_ticker(self.client, 123)
        test_raise_with_ticker(self.client, id=321)
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
        if __debug__:
           self.assertRaises(AssertionError, self.client.reqContractDetails, "",tws.Contract())
           self.assertRaises(AssertionError, self.client.reqContractDetails, 1,"")

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

    def test_cancelMktData(self):
        self._check_connection_required(self.client.cancelMktData, 0)
        self._check_error_raised(EClientErrors.FAIL_SEND_CANMKT, 2,
                                 self.client.cancelMktData, 2)

        self.client.cancelMktData(3)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.CANCEL_MKT_DATA,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.cancelMktData, "")


    def test_cancelMktDepth(self):
        self._check_connection_required(self.client.cancelMktDepth, 0)
        self._check_min_server(6, 1, self.client.cancelMktDepth, 1)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support market depth.")
        self._check_error_raised(EClientErrors.FAIL_SEND_CANMKTDEPTH, 2,
                                 self.client.cancelMktDepth, 2)

        self.client.cancelMktDepth(3)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.CANCEL_MKT_DEPTH,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.cancelMktDepth, "")

    def test_exerciseOptions(self):
        self._check_connection_required(self.client.exerciseOptions, 0, tws.Contract(),0,0,"",0)
        self._check_min_server(21, 1, self.client.exerciseOptions, 1, tws.Contract(),0,0,"",0)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support options exercise from the API.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQMKT, 2, # Error type per Java, IB bug?
                                 self.client.exerciseOptions, 2, tws.Contract(),0,0,"",0)

        contract = tws.Contract(con_id=1, symbol="A1", sec_type="B2", expiry="C3", strike=2.5,
                                right="D4", multiplier="E5", exchange="F6", currency="G7",
                                local_symbol="H8", primary_exch="I9", include_expired=True)

        self.client.exerciseOptions(3, contract, 4, 5, "A1", 7)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x003\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x00H8\x004\x005\x00A1\x007\x00" %
                         self.client.EXERCISE_OPTIONS,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.exerciseOptions, "",tws.Contract(),0,0,"",0)
            self.assertRaises(AssertionError, self.client.exerciseOptions, 0,"",0,0,"",0)
            self.assertRaises(AssertionError, self.client.exerciseOptions, 0,tws.Contract(),"",0,"",0)
            self.assertRaises(AssertionError, self.client.exerciseOptions, 0,tws.Contract(),0,"","",0)
            self.assertRaises(AssertionError, self.client.exerciseOptions, 0,tws.Contract(),0,0,0,0)
            self.assertRaises(AssertionError, self.client.exerciseOptions, 0,tws.Contract(),0,0,"","")

    def test_placeOrder(self):
        self.client._server_version = 41
        self._check_connection_required(self.client.placeOrder, 1, tws.Contract(), tws.Order())
        self._check_error_raised(EClientErrors.FAIL_SEND_ORDER, 2,
                                 self.client.placeOrder, 2, tws.Contract(), tws.Order())

        contract = tws.Contract()
        order = tws.Order()

        order.m_scaleInitLevelSize = 1.5
        order.m_scalePriceIncrement = order._DOUBLE_MAX_VALUE
        self._check_min_server(self.client.MIN_SERVER_VER_SCALE_ORDERS, 3, self.client.placeOrder,
                               3, contract, order)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support Scale orders.")

        order.m_scaleInitLevelSize = order._DOUBLE_MAX_VALUE
        order.m_scalePriceIncrement = 2.5
        self._check_min_server(self.client.MIN_SERVER_VER_SCALE_ORDERS, 3, self.client.placeOrder,
                               3, contract, order)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support Scale orders.")
        order = tws.Order()

        contract.m_comboLegs = [tws.ComboLeg(short_sale_slot=1)]
        self._check_min_server(self.client.MIN_SERVER_VER_SSHORT_COMBO_LEGS, 3, self.client.placeOrder,
                               3, contract, order)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support SSHORT flag for combo legs.")

        order.m_whatIf = True
        self._check_min_server(self.client.MIN_SERVER_VER_WHAT_IF_ORDERS, 3, self.client.placeOrder,
                               3, contract, order)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support what-if orders.")

        contract.m_underComp.m_conId = 1
        self._check_min_server(self.client.MIN_SERVER_VER_UNDER_COMP, 3, self.client.placeOrder,
                               3, contract, order)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support delta-neutral orders.")
        contract.m_underComp = tws.UnderComp()

        order.m_scaleSubsLevelSize = 1
        self._check_min_server(self.client.MIN_SERVER_VER_SCALE_ORDERS2, 3, self.client.placeOrder,
                               3, contract, order)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support Subsequent Level Size for Scale orders.")

        order.m_algoStrategy = "Test"
        self._check_min_server(self.client.MIN_SERVER_VER_ALGO_ORDERS, 3, self.client.placeOrder,
                               3, contract, order)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support algo orders.")

        order = tws.Order()
        order.m_orderId = 1; order.m_clientId = 2; order.m_permId = 3; order.m_action = 'a1'
        order.m_totalQuantity = 4; order.m_orderType = 'b2'; order.m_lmtPrice = 1.5
        order.m_auxPrice = 2.5; order.m_tif = 'c3'; order.m_ocaGroup = 'd4'
        order.m_ocaType = 5; order.m_orderRef = 'e5'; order.m_transmit = False
        order.m_parentId = 6; order.m_blockOrder = True; order.m_sweepToFill = True
        order.m_displaySize = 7; order.m_triggerMethod = 8; order.m_outsideRth = True
        order.m_hidden = True; order.m_goodAfterTime = 'f7'; order.m_goodTillDate = 'g8'
        order.m_overridePercentageConstraints = True; order.m_rule80A = 'h9'
        order.m_allOrNone = True; order.m_minQty = 9; order.m_percentOffset = 3.5
        order.m_trailStopPrice = 4.5; order.m_faGroup = 'i1'; order.m_faProfile = 'j2'
        order.m_faMethod = 'k3'; order.m_faPercentage = 'l4'; order.m_openClose = "1"
        order.m_origin = tws.Order.FIRM; order.m_shortSaleSlot = 10;
        order.m_designatedLocation = 'm5'; order.m_discretionaryAmt = 5.5
        order.m_eTradeOnly = True; order.m_firmQuoteOnly = True; order.m_nbboPriceCap = 6.5
        order.m_auctionStrategy = 11; order.m_startingPrice = 7.5; order.m_stockRefPrice = 8.5
        order.m_delta = 9.5; order.m_stockRangeLower = 10.5; order.m_stockRangeUpper = 11.5
        order.m_volatility = 12.5; order.m_volatilityType = 12; order.m_continuousUpdate = 13
        order.m_referencePriceType = 14; order.m_deltaNeutralOrderType = 'n6';
        order.m_deltaNeutralAuxPrice = 13.5; order.m_basisPoints = 14.5;
        order.m_basisPointsType = 15; order.m_account = 'o7'; order.m_settlingFirm = 'p8';
        order.m_clearingAccount = 'q9'; order.m_clearingIntent = 'r1';
        order.m_algoParams = ['t3','u4'];
        contract = tws.Contract(con_id=18, symbol="v5", sec_type="w6", expiry="x7", strike=19.5,
                                right="y8", multiplier="z9", exchange="a2", currency="b3",
                                local_symbol="c4", primary_exch="d5", include_expired=True,
                                combo_legs=[tws.ComboLeg(3, 4, "J1", "K2", 5, 0, ""),
                                            tws.ComboLeg(7, 8, "M4", "N5", 9, 0, "")])

        self.assertEqual(len(self.wrapper.errors), 9)

        self.client._server_version = 2
        self.assertEqual(self.client.serverVersion(), 2)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 4
        self.assertEqual(self.client.serverVersion(), 4)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 5
        self.assertEqual(self.client.serverVersion(), 5)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 7
        self.assertEqual(self.client.serverVersion(), 7)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 8
        self.assertEqual(self.client.serverVersion(), 8)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        contract.m_secType = self.client.BAG_SEC_TYPE
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00BAG\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x002\x003\x004\x00J1\x00K2\x005\x007\x008\x00M4\x00N5\x009\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())
        contract.m_secType = "w6"

        self.client._server_version = 9
        self.assertEqual(self.client.serverVersion(), 9)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 10
        self.assertEqual(self.client.serverVersion(), 10)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 11
        self.assertEqual(self.client.serverVersion(), 11)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 12
        self.assertEqual(self.client.serverVersion(), 12)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 13
        self.assertEqual(self.client.serverVersion(), 13)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 14
        self.assertEqual(self.client.serverVersion(), 14)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 15
        self.assertEqual(self.client.serverVersion(), 15)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 18
        self.assertEqual(self.client.serverVersion(), 18)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 19
        self.assertEqual(self.client.serverVersion(), 19)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 22
        self.assertEqual(self.client.serverVersion(), 22)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 26
        self.assertEqual(self.client.serverVersion(), 26)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00false\x0013\x00\x00\x0014\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        order.m_orderType = "VOL"
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00VOL\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x00\x00\x001\x0012.5\x0012\x00false\x0013\x0010.5\x0011.5\x0014\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 27
        self.assertEqual(self.client.serverVersion(), 27)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00VOL\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00false\x0013\x00\x00\x0014\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())
        order.m_orderType = "b2"

        self.client._server_version = 28
        self.assertEqual(self.client.serverVersion(), 28)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00n6\x0013.5\x0013\x00\x00\x0014\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 30
        self.assertEqual(self.client.serverVersion(), 30)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00n6\x0013.5\x0013\x00\x00\x0014\x004.5\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        order.m_scaleInitLevelSize = 20.5
        order.m_scalePriceIncrement = 21.5
        self.client._server_version = 35
        self.assertEqual(self.client.serverVersion(), 35)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00n6\x0013.5\x0013\x00\x00\x0014\x004.5\x00\x0020.5\x0021.5\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        order.m_whatIf = True
        self.client._server_version = 36
        self.assertEqual(self.client.serverVersion(), 36)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x000\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x000\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00n6\x0013.5\x0013\x00\x00\x0014\x004.5\x00\x0020.5\x0021.5\x001\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        self.client._server_version = 38
        self.assertEqual(self.client.serverVersion(), 38)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x001\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00n6\x0013.5\x0013\x00\x00\x0014\x004.5\x00\x0020.5\x0021.5\x001\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        contract.m_underComp.m_conId = 22
        order.m_scaleSubsLevelSize = 23.5
        self.client._server_version = 40
        self.assertEqual(self.client.serverVersion(), 40)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x001\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00n6\x0013.5\x0013\x00\x00\x0014\x004.5\x0020.5\x0023.5\x0021.5\x00q9\x00r1\x001\x0022\x000.0\x000.0\x001\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())

        order.m_algoStrategy = "v5"
        order.m_algoParams = [tws.TagValue('t3','u4'),tws.TagValue('v5','w6')]
        self.client._server_version = 41
        self.assertEqual(self.client.serverVersion(), 41)
        self.stream.truncate(0)
        self.client.placeOrder(1, contract, order)
        self.assertEqual(len(self.wrapper.errors), 9)
        self.assertEqual("%s\x0027\x001\x00v5\x00w6\x00x7\x0019.5\x00y8\x00z9\x00a2\x00d5\x00b3\x00c4\x00a1\x004\x00b2\x001.5\x002.5\x00c3\x00d4\x00o7\x001\x001\x00e5\x000\x006\x001\x001\x007\x008\x001\x001\x00\x005.5\x00f7\x00g8\x00i1\x00k3\x00l4\x00j2\x0010\x00m5\x005\x00h9\x00p8\x001\x009\x003.5\x001\x001\x006.5\x0011\x007.5\x008.5\x009.5\x0010.5\x0011.5\x001\x0012.5\x0012\x00n6\x0013.5\x0013\x00\x00\x0014\x004.5\x0020.5\x0023.5\x0021.5\x00q9\x00r1\x001\x0022\x000.0\x000.0\x00v5\x002\x00t3\x00u4\x00v5\x00w6\x001\x00" %
                         self.client.PLACE_ORDER,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.placeOrder, "",tws.Contract(),tws.Order())
            self.assertRaises(AssertionError, self.client.placeOrder, 0,"",tws.Order())
            self.assertRaises(AssertionError, self.client.placeOrder, 0,tws.Contract(),"")

    def test_reqAccountUpdates(self):
        self._check_connection_required(self.client.reqAccountUpdates, True, "")
        self._check_error_raised(EClientErrors.FAIL_SEND_ACCT, EClientErrors.NO_VALID_ID,
                                 self.client.reqAccountUpdates, True, "")

        self.assertTrue(self.client.serverVersion() < 9)
        self.stream.truncate(0)
        self.client.reqAccountUpdates(True, "A1")
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x002\x001\x00" %
                         self.client.REQ_ACCOUNT_DATA,
                         self.stream.getvalue())

        self.client._server_version = 9
        self.assertEqual(self.client.serverVersion(), 9)
        self.stream.truncate(0)
        self.client.reqAccountUpdates(True, "A1")
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x002\x001\x00A1\x00" %
                         self.client.REQ_ACCOUNT_DATA,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.reqAccountUpdates, "", "")
            self.assertRaises(AssertionError, self.client.reqAccountUpdates, "", True)

    def test_reqExecutions(self):
        self._check_connection_required(self.client.reqExecutions, 2, tws.ExecutionFilter())
        self._check_error_raised(EClientErrors.FAIL_SEND_EXEC, EClientErrors.NO_VALID_ID,
                                 self.client.reqExecutions, 3, tws.ExecutionFilter())

        filter = tws.ExecutionFilter(1, "ab", "cd", "ef", "gh", "ij", "kl")

        self.assertTrue(self.client.serverVersion() < self.client.MIN_SERVER_VER_EXECUTION_DATA_CHAIN)
        self.stream.truncate(0)
        self.client.reqExecutions(4, filter)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x003\x00" %
                         self.client.REQ_EXECUTIONS,
                         self.stream.getvalue())

        self.client._server_version = 9
        self.assertEqual(self.client.serverVersion(), 9)
        self.stream.truncate(0)
        self.client.reqExecutions(4, filter)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x003\x001\x00ab\x00cd\x00ef\x00gh\x00ij\x00kl\x00" %
                         self.client.REQ_EXECUTIONS,
                         self.stream.getvalue())

        self.client._server_version = self.client.MIN_SERVER_VER_EXECUTION_DATA_CHAIN
        self.assertEqual(self.client.serverVersion(), self.client.MIN_SERVER_VER_EXECUTION_DATA_CHAIN)
        self.stream.truncate(0)
        self.client.reqExecutions(4, filter)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x003\x004\x001\x00ab\x00cd\x00ef\x00gh\x00ij\x00kl\x00" %
                         self.client.REQ_EXECUTIONS,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.reqAccountUpdates, "", tws.ExecutionFilter())
            self.assertRaises(AssertionError, self.client.reqAccountUpdates, 0, "")

    def test_cancelOrder(self):
        self._check_connection_required(self.client.cancelOrder, 1)
        self._check_error_raised(EClientErrors.FAIL_SEND_CORDER, 2,
                                 self.client.cancelOrder, 2)

        self.stream.truncate(0)
        self.client.cancelOrder(3)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.CANCEL_ORDER,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.cancelOrder, "")

    def test_reqOpenOrders(self):
        self._check_connection_required(self.client.reqOpenOrders)
        self._check_error_raised(EClientErrors.FAIL_SEND_OORDER, EClientErrors.NO_VALID_ID,
                                 self.client.reqOpenOrders)

        self.stream.truncate(0)
        self.client.reqOpenOrders()
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x00" %
                         self.client.REQ_OPEN_ORDERS,
                         self.stream.getvalue())

    def test_reqIds(self):
        self._check_connection_required(self.client.reqIds, 1)
        self._check_error_raised(EClientErrors.FAIL_SEND_CORDER, EClientErrors.NO_VALID_ID,
                                 self.client.reqIds, 2)

        self.stream.truncate(0)
        self.client.reqIds(3)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.REQ_IDS,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.reqIds, "")

    def test_reqNewsBulletins(self):
        self._check_connection_required(self.client.reqNewsBulletins, True)
        self._check_error_raised(EClientErrors.FAIL_SEND_CORDER, EClientErrors.NO_VALID_ID,
                                 self.client.reqNewsBulletins, True)

        self.stream.truncate(0)
        self.client.reqNewsBulletins(True)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x001\x00" %
                         self.client.REQ_NEWS_BULLETINS,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.reqNewsBulletins, "")

    def test_cancelNewsBulletins(self):
        self._check_connection_required(self.client.cancelNewsBulletins)
        self._check_error_raised(EClientErrors.FAIL_SEND_CORDER, EClientErrors.NO_VALID_ID,
                                 self.client.cancelNewsBulletins)

        self.stream.truncate(0)
        self.client.cancelNewsBulletins()
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x00" %
                         self.client.CANCEL_NEWS_BULLETINS,
                         self.stream.getvalue())

    def test_setServerLogLevel(self):
        self._check_connection_required(self.client.setServerLogLevel, 1)
        self._check_error_raised(EClientErrors.FAIL_SEND_SERVER_LOG_LEVEL, EClientErrors.NO_VALID_ID,
                                 self.client.setServerLogLevel, 2)

        self.stream.truncate(0)
        self.client.setServerLogLevel(3)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x003\x00" %
                         self.client.SET_SERVER_LOGLEVEL,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.setServerLogLevel, "")

    def test_reqAutoOpenOrders(self):
        self._check_connection_required(self.client.reqAutoOpenOrders, True)
        self._check_error_raised(EClientErrors.FAIL_SEND_OORDER, EClientErrors.NO_VALID_ID,
                                 self.client.reqAutoOpenOrders, True)

        self.stream.truncate(0)
        self.client.reqAutoOpenOrders(True)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x001\x00" %
                         self.client.REQ_AUTO_OPEN_ORDERS,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.reqAutoOpenOrders, "")

    def test_reqAllOpenOrders(self):
        self._check_connection_required(self.client.reqAllOpenOrders)
        self._check_error_raised(EClientErrors.FAIL_SEND_OORDER, EClientErrors.NO_VALID_ID,
                                 self.client.reqAllOpenOrders)

        self.stream.truncate(0)
        self.client.reqAllOpenOrders()
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x00" %
                         self.client.REQ_ALL_OPEN_ORDERS,
                         self.stream.getvalue())

    def test_reqManagedAccts(self):
        self._check_connection_required(self.client.reqManagedAccts)
        self._check_error_raised(EClientErrors.FAIL_SEND_OORDER, EClientErrors.NO_VALID_ID,
                                 self.client.reqManagedAccts)

        self.stream.truncate(0)
        self.client.reqManagedAccts()
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual("%s\x001\x00" %
                         self.client.REQ_MANAGED_ACCTS,
                         self.stream.getvalue())

    def test_requestFA(self):
        self._check_connection_required(self.client.requestFA, 1)
        self._check_min_server(13, EClientErrors.NO_VALID_ID, self.client.requestFA, 2)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support FA request.")
        self._check_error_raised(EClientErrors.FAIL_SEND_FA_REQUEST, EClientErrors.NO_VALID_ID,
                                 self.client.requestFA, 3)

        self.stream.truncate(0)
        self.client.requestFA(4)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x004\x00" %
                         self.client.REQ_FA,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.requestFA, "")

    def test_replaceFA(self):
        self._check_connection_required(self.client.replaceFA, 1, "")
        self._check_min_server(13, EClientErrors.NO_VALID_ID, self.client.replaceFA, 2, "")
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support FA request.")
        self._check_error_raised(EClientErrors.FAIL_SEND_FA_REPLACE, EClientErrors.NO_VALID_ID,
                                 self.client.replaceFA, 3, "")

        self.stream.truncate(0)
        self.client.replaceFA(4, "A1")
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x004\x00A1\x00" %
                         self.client.REPLACE_FA,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.replaceFA, "", "")
            self.assertRaises(AssertionError, self.client.replaceFA, 0, 0)

    def test_reqCurrentTime(self):
        self._check_connection_required(self.client.reqCurrentTime)
        self._check_min_server(33, EClientErrors.NO_VALID_ID, self.client.reqCurrentTime)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support current time requests.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQCURRTIME, EClientErrors.NO_VALID_ID,
                                 self.client.reqCurrentTime)

        self.stream.truncate(0)
        self.client.reqCurrentTime()
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x00" %
                         self.client.REQ_CURRENT_TIME,
                         self.stream.getvalue())

    def test_reqFundamentalData(self):
        self._check_connection_required(self.client.reqFundamentalData, 1, tws.Contract(), "")
        self._check_min_server(self.client.MIN_SERVER_VER_FUNDAMENTAL_DATA, 2, self.client.reqFundamentalData, 2, tws.Contract(), "")
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support fundamental data requests.")
        self._check_error_raised(EClientErrors.FAIL_SEND_REQFUNDDATA, 3,
                                 self.client.reqFundamentalData, 3, tws.Contract(), "")

        contract = tws.Contract(con_id=18, symbol="v5", sec_type="w6", expiry="x7", strike=19.5,
                                right="y8", multiplier="z9", exchange="a2", currency="b3",
                                local_symbol="c4", primary_exch="d5", include_expired=True)

        self.stream.truncate(0)
        self.client.reqFundamentalData(4, contract, "A1")
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x004\x00v5\x00w6\x00a2\x00d5\x00b3\x00c4\x00A1\x00" %
                         self.client.REQ_FUNDAMENTAL_DATA,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.reqFundamentalData, "", tws.Contract(), "")
            self.assertRaises(AssertionError, self.client.reqFundamentalData, 0, "", "")
            self.assertRaises(AssertionError, self.client.reqFundamentalData, 0, tws.Contract(), 0)

    def test_cancelFundamentalData(self):
        self._check_connection_required(self.client.cancelFundamentalData, 1)
        self._check_min_server(self.client.MIN_SERVER_VER_FUNDAMENTAL_DATA, 2, self.client.cancelFundamentalData, 2)
        self.assertEqual(self.wrapper.errors[-1][2], "The TWS is out of date and must be upgraded. It does not support fundamental data requests.")
        self._check_error_raised(EClientErrors.FAIL_SEND_CANFUNDDATA, 3,
                                 self.client.cancelFundamentalData, 3)

        self.stream.truncate(0)
        self.client.cancelFundamentalData(4)
        self.assertEqual(len(self.wrapper.errors), 3)
        self.assertEqual("%s\x001\x004\x00" %
                         self.client.CANCEL_FUNDAMENTAL_DATA,
                         self.stream.getvalue())
        if __debug__:
            self.assertRaises(AssertionError, self.client.cancelFundamentalData, "")
