'''Main connection to TWS client.

   Defines the EClientSocket class, which implements a socket connection to
   the TWS socket server, through which the entire API operates.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import tws.EClientErrors as _EClientErrors
from tws import synchronized


def requestmethod(has_id=False, min_server=0, 
                  min_server_error_suffix="",
                  generic_error=_EClientErrors.TwsError(),
                  generic_error_suffix=""):
    '''Socket request-method decorator.

       Eliminates repetitive error-checking boilerplate from request methods.   
    '''
    assert type(has_id) == bool
    assert type(min_server) == int
    assert type(min_server_error_suffix) == str
    assert isinstance(generic_error, _EClientErrors.TwsError)
    assert type(generic_error_suffix) == str

    def _decorator(method):
        assert  (__import__("inspect").getargspec(method)[0][0] == "self")
        assert  (not has_id) or (__import__("inspect").getargspec(method)[0][1] == "id")

        def _decorated(self, *args, **kwds):
            assert type(self) == EClientSocket

            try:
                # Socket client must be connected.
                if not self._connected:
                    self._error(_EClientErrors.NOT_CONNECTED)
                    return
                # Enforce minimum server version, if any.
                if self._server_version < min_server:
                    self._error(_EClientErrors.TwsError(
                                id=kwds.get("id", args[0] if args else _EClientErrors.NO_VALID_ID) 
                                    if has_id else _EClientErrors.NO_VALID_ID,
                                source=_EClientErrors.UPDATE_TWS,
                                msg=min_server_error_suffix or None))
                    return
                # Call wrapped method, ensuring stream gets flushed.
                result = method(self, *args, **kwds)
                self._stream.flush()
                return result
            # Reraise assertion errors.
            except AssertionError: raise
            # Any other exception report generic error instance to EWrapper._error()
            except:
                self._error(_EClientErrors.TwsError(
                                source=generic_error,
                                id=kwds.get("id", args[0] if args else _EClientErrors.NO_VALID_ID) 
                                    if has_id else _EClientErrors.NO_VALID_ID,
                                msg=generic_error_suffix or method.__name__))

        return _decorated
    return _decorator


class EClientSocket(object):
    '''Socket client which connects to the TWS socket server.
    '''

    def __init__(self, wrapper, socket_factory=__import__("socket").socket):
        assert issubclass(type(wrapper), __import__("tws").EWrapper)  
        assert callable(socket_factory)

        self._wrapper = wrapper
        self._reader = None
        self._connected = False
        self._server_version = 0
        self._tws_time = 0
        self._socket_factory = socket_factory


    @synchronized
    def _close(self):
        self.eDisconnect()
        self.wrapper().connectionClosed()


    def _send(self, data):
        if type(data) in (str, int, long, float):
            self._stream.write(str(data))
        elif type(data) == bool:
            self._stream.write("1" if data else "0")
        elif data is None:
            pass
        else:
            raise ValueError("Unknown data type for EClientSocket._send(): %s", type(data))
        self._stream.write(self.EOL)


    def _sendMax(self, data):
        if type(data) == int:
            self._send(data) if data != self._INT_MAX_VALUE else self._send(None)
        elif type(data) == float:
            self._send(data) if data != self._DOUBLE_MAX_VALUE else self._send(None)
        else:
            raise ValueError("Unknown data type for EClientSocket._sendMax(): %s", type(data))


    @synchronized
    def _error(self, e):
        self._wrapper.error(e)


    @classmethod
    def faMsgTypeName(cls, faDataType):
        if faDataType == cls.GROUPS:
            return "GROUPS"
        elif faDataType == cls.PROFILES:
            return "PROFILES"
        elif faDataType == cls.ALIASES:
            return "ALIASES"

        # Should never get here.
        assert False
        return ""


    # General constants
    CLIENT_VERSION = 42
    SERVER_VERSION = 38
    EOL = "\x00"
    BAG_SEC_TYPE = "BAG"


    # API tag constants
    REQ_MKT_DATA = 1
    CANCEL_MKT_DATA = 2
    PLACE_ORDER = 3
    CANCEL_ORDER = 4
    REQ_OPEN_ORDERS = 5
    REQ_ACCOUNT_DATA = 6
    REQ_EXECUTIONS = 7
    REQ_IDS = 8
    REQ_CONTRACT_DATA = 9
    REQ_MKT_DEPTH = 10
    CANCEL_MKT_DEPTH = 11
    REQ_NEWS_BULLETINS = 12
    CANCEL_NEWS_BULLETINS = 13
    SET_SERVER_LOGLEVEL = 14
    REQ_AUTO_OPEN_ORDERS = 15
    REQ_ALL_OPEN_ORDERS = 16
    REQ_MANAGED_ACCTS = 17
    REQ_FA = 18
    REPLACE_FA = 19
    REQ_HISTORICAL_DATA = 20
    EXERCISE_OPTIONS = 21
    REQ_SCANNER_SUBSCRIPTION = 22
    CANCEL_SCANNER_SUBSCRIPTION = 23
    REQ_SCANNER_PARAMETERS = 24
    CANCEL_HISTORICAL_DATA = 25
    REQ_CURRENT_TIME = 49
    REQ_REAL_TIME_BARS = 50
    CANCEL_REAL_TIME_BARS = 51
    REQ_FUNDAMENTAL_DATA = 52
    CANCEL_FUNDAMENTAL_DATA = 53
    MIN_SERVER_VER_REAL_TIME_BARS = 34
    MIN_SERVER_VER_SCALE_ORDERS = 35
    MIN_SERVER_VER_SNAPSHOT_MKT_DATA = 35
    MIN_SERVER_VER_SSHORT_COMBO_LEGS = 35
    MIN_SERVER_VER_WHAT_IF_ORDERS = 36
    MIN_SERVER_VER_CONTRACT_CONID = 37
    MIN_SERVER_VER_PTA_ORDERS = 39
    MIN_SERVER_VER_FUNDAMENTAL_DATA = 40
    MIN_SERVER_VER_UNDER_COMP = 40
    MIN_SERVER_VER_CONTRACT_DATA_CHAIN = 40
    MIN_SERVER_VER_SCALE_ORDERS2 = 40
    MIN_SERVER_VER_ALGO_ORDERS = 41
    MIN_SERVER_VER_EXECUTION_DATA_CHAIN = 42


    # Message Type name constants
    GROUPS = 1
    PROFILES = 2
    ALIASES = 3


    # Private class imports
    from tws._Util import _INT_MAX_VALUE
    from tws._Util import _DOUBLE_MAX_VALUE


    def wrapper(self):
        return self._wrapper


    def reader(self):
        return self._reader


    def isConnected(self):
        return self._connected


    def serverVersion(self):
        return self._server_version


    def TwsConnectionTime(self):
        return self._tws_time


    def checkConnected(self, host):
        assert issubclass(type(host), str) or (host == None)  

        if self._connected:
            self._wrapper.error(_EClientErrors.ALREADY_CONNECTED)
            return None
        return host if host else "127.0.0.1"


    def connectionError(self):
        self._wrapper.error(_EClientErrors.CONNECT_FAIL)
        self.m_reader = None


    def createReader(self, connection, input_stream):
        assert issubclass(type(connection), type(self))
        assert hasattr(input_stream, "read")

        return __import__("tws").EReader(connection, input_stream)


    @synchronized
    def eConnect(self):
        # Trivial stub for now.
        self._connected = True


    @synchronized
    def eDisconnect(self):
        # Trivial stub for now.
        self._connected = False


    @synchronized
    @requestmethod(has_id=True, min_server=24,
                   min_server_error_suffix="It does not support API scanner subscription.",
                   generic_error=_EClientErrors.FAIL_SEND_CANSCANNER)
    def cancelScannerSubscription(self, id):
        assert type(id) is int
        VERSION = 1

        self._send(self.CANCEL_SCANNER_SUBSCRIPTION)
        self._send(VERSION)
        self._send(id)


    @synchronized
    @requestmethod(min_server=24,
                   min_server_error_suffix="It does not support API scanner subscription.",
                   generic_error=_EClientErrors.FAIL_SEND_REQSCANNERPARAMETERS)
    def reqScannerParameters(self):
        VERSION = 1

        self._send(self.REQ_SCANNER_PARAMETERS)
        self._send(VERSION)


    @synchronized
    @requestmethod(has_id=True, min_server=24,
                   min_server_error_suffix="It does not support API scanner subscription.",
                   generic_error=_EClientErrors.FAIL_SEND_REQSCANNER)
    def reqScannerSubscription(self, id, subscription):
        assert type(id) == int
        assert type(subscription) == __import__("tws").ScannerSubscription
        VERSION = 3

        self._send(self.REQ_SCANNER_SUBSCRIPTION)
        self._send(VERSION)
        self._send(id)
        self._sendMax(subscription.numberOfRows())
        self._send(subscription.instrument())
        self._send(subscription.locationCode())
        self._send(subscription.scanCode())
        self._sendMax(subscription.abovePrice())
        self._sendMax(subscription.belowPrice())
        self._sendMax(subscription.aboveVolume())
        self._sendMax(subscription.marketCapAbove())
        self._sendMax(subscription.marketCapBelow())
        self._send(subscription.moodyRatingAbove())
        self._send(subscription.moodyRatingBelow())
        self._send(subscription.spRatingAbove())
        self._send(subscription.spRatingBelow())
        self._send(subscription.maturityDateAbove())
        self._send(subscription.maturityDateBelow())
        self._sendMax(subscription.couponRateAbove())
        self._sendMax(subscription.couponRateBelow())
        self._send(subscription.excludeConvertible())
        if self._server_version >= 25:
            self._send(subscription.averageOptionVolumeAbove())
            self._send(subscription.scannerSettingPairs())
        if self._server_version >= 27:
            self._send(subscription.stockTypeFilter())


    @synchronized
    @requestmethod(has_id=True,
                   generic_error=_EClientErrors.FAIL_SEND_REQMKT)
    def reqMktData(self, id, contract, generic_tick_list, snapshot):
        assert type(id) == int
        assert type(contract) == __import__("tws").Contract
        assert type(generic_tick_list) == str
        assert type(snapshot) == bool
        VERSION = 8

        if contract.m_underComp and (self._server_version < self.MIN_SERVER_VER_UNDER_COMP):
            self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                            id=id,
                            msg="It does not support delta-neutral orders."))
            return
        if snapshot and (self._server_version < self.MIN_SERVER_VER_SNAPSHOT_MKT_DATA):
            self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                            id=id,
                            msg="It does not support snapshot market data requests."))
            return

        self._send(self.REQ_MKT_DATA)
        self._send(VERSION)
        self._send(id)
        self._send(contract.m_symbol)
        self._send(contract.m_secType)
        self._send(contract.m_expiry)
        self._send(contract.m_strike)
        self._send(contract.m_right)
        if self._server_version >= 15:
            self._send(contract.m_multiplier)
        self._send(contract.m_exchange)
        if self._server_version >= 14:
            self._send(contract.m_primaryExch)
        self._send(contract.m_currency)
        if self._server_version >= 2:
            self._send(contract.m_localSymbol)
        if (self._server_version >= 8):
            if self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                self._send(len(contract.m_comboLegs))
                for leg in contract.m_comboLegs:
                    self._send(leg.m_conId)
                    self._send(leg.m_ratio)
                    self._send(leg.m_action)
                    self._send(leg.m_exchange)
        if self._server_version >= self.MIN_SERVER_VER_UNDER_COMP:
            self._send(bool(contract.m_underComp))
            if contract.m_underComp:
                self._send(contract.m_underComp.m_conId)
                self._send(contract.m_underComp.m_delta)
                self._send(contract.m_underComp.m_price)
        if self._server_version >= 31:
            self._send(generic_tick_list)
        if self._server_version >= self.MIN_SERVER_VER_SNAPSHOT_MKT_DATA:
            self._send(snapshot)


    @synchronized
    @requestmethod(has_id=True, min_server=24,
                   min_server_error_suffix="It does not support historical data query cancellation.",
                   generic_error=_EClientErrors.FAIL_SEND_CANHISTDATA)
    def cancelHistoricalData(self, id):
        assert type(id) == int
        VERSION = 1

        self._send(self.CANCEL_HISTORICAL_DATA)
        self._send(VERSION)
        self._send(id)


    @synchronized
    @requestmethod(has_id=True, min_server=MIN_SERVER_VER_REAL_TIME_BARS,
                   min_server_error_suffix="It does not support realtime bar data query cancellation.",
                   generic_error=_EClientErrors.FAIL_SEND_CANRTBARS)
    def cancelRealTimeBars(self, id):
        assert type(id) == int
        VERSION = 1

        self._send(self.CANCEL_REAL_TIME_BARS)
        self._send(VERSION)
        self._send(id)


    @synchronized
    @requestmethod(has_id=True, min_server=16,
                   min_server_error_suffix="It does not support historical data backfill.",
                   generic_error=_EClientErrors.FAIL_SEND_REQHISTDATA)
    def reqHistoricalData(self, id, contract, end_date_time, duration_str,
                          bar_size_setting, what_to_show, use_RTH, format_date):
        assert type(id) == int
        assert type(contract) == __import__("tws").Contract
        assert type(end_date_time) == str
        assert type(duration_str) == str
        assert type(bar_size_setting) == str
        assert type(what_to_show) == str
        assert type(use_RTH) == int
        assert type(format_date) == int
        VERSION = 4

        self._send(self.REQ_HISTORICAL_DATA)
        self._send(VERSION)
        self._send(id)
        self._send(contract.m_symbol)
        self._send(contract.m_secType)
        self._send(contract.m_expiry)
        self._send(contract.m_strike)
        self._send(contract.m_right)
        self._send(contract.m_multiplier)
        self._send(contract.m_exchange)
        self._send(contract.m_primaryExch)
        self._send(contract.m_currency)
        self._send(contract.m_localSymbol)
        if self._server_version >= 31:
            self._send(bool(contract.m_includeExpired))
        if self._server_version >= 20:
            self._send(end_date_time)
            self._send(bar_size_setting)
        self._send(duration_str)
        self._send(use_RTH)
        self._send(what_to_show)
        if self._server_version >= 17:
            self._send(format_date)
        if self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
            self._send(len(contract.m_comboLegs))
            for leg in contract.m_comboLegs:
                self._send(leg.m_conId)
                self._send(leg.m_ratio)
                self._send(leg.m_action)
                self._send(leg.m_exchange)


    @synchronized
    @requestmethod(has_id=True, min_server=MIN_SERVER_VER_REAL_TIME_BARS,
                   min_server_error_suffix="It does not support real time bars.",
                   generic_error=_EClientErrors.FAIL_SEND_REQRTBARS)
    def reqRealTimeBars(self, id, contract, bar_size, what_to_show, use_RTH):
        assert type(id) == int
        assert type(contract) == __import__("tws").Contract
        assert type(bar_size) == str
        assert type(what_to_show) == str
        assert type(use_RTH) == int
        VERSION = 1

        self._send(self.REQ_REAL_TIME_BARS)
        self._send(VERSION)
        self._send(id)
        self._send(contract.m_symbol)
        self._send(contract.m_secType)
        self._send(contract.m_expiry)
        self._send(contract.m_strike)
        self._send(contract.m_right)
        self._send(contract.m_multiplier)
        self._send(contract.m_exchange)
        self._send(contract.m_primaryExch)
        self._send(contract.m_currency)
        self._send(contract.m_localSymbol)
        self._send(bar_size)
        self._send(what_to_show)
        self._send(use_RTH)


    @synchronized
    @requestmethod(min_server=4, min_server_error_suffix="It does not support contract details.",
                   generic_error=_EClientErrors.FAIL_SEND_REQCONTRACT)
    def reqContractDetails(self, req_id, contract):
        assert type(req_id) == int
        assert type(contract) == __import__("tws").Contract
        VERSION = 5

        self._send(self.REQ_CONTRACT_DATA)
        self._send(VERSION)
        if self._server_version >= self.MIN_SERVER_VER_CONTRACT_DATA_CHAIN:
            self._send(req_id)
        if self._server_version >= self.MIN_SERVER_VER_CONTRACT_CONID:
            self._send(contract.m_conId)
        self._send(contract.m_symbol)
        self._send(contract.m_secType)
        self._send(contract.m_expiry)
        self._send(contract.m_strike)
        self._send(contract.m_right)
        if self._server_version >= 15:
            self._send(contract.m_multiplier)
        self._send(contract.m_exchange)
        self._send(contract.m_currency)
        self._send(contract.m_localSymbol)
        if self._server_version >= 31:
            self._send(contract.m_includeExpired)


    @synchronized
    @requestmethod(has_id=True, min_server=6,
                   min_server_error_suffix="It does not support market depth.",
                   generic_error=_EClientErrors.FAIL_SEND_REQMKTDEPTH)
    def reqMktDepth(self, id, contract, num_rows):
        assert type(id) == int
        assert type(contract) == __import__("tws").Contract
        assert type(num_rows) == int
        VERSION = 3

        self._send(self.REQ_MKT_DEPTH)
        self._send(VERSION)
        self._send(id)
        self._send(contract.m_symbol)
        self._send(contract.m_secType)
        self._send(contract.m_expiry)
        self._send(contract.m_strike)
        self._send(contract.m_right)
        if self._server_version >= 15:
            self._send(contract.m_multiplier)
        self._send(contract.m_exchange)
        self._send(contract.m_currency)
        self._send(contract.m_localSymbol)
        if self._server_version >= 19:
            self._send(num_rows)


    @synchronized
    @requestmethod(has_id=True, 
                   generic_error=_EClientErrors.FAIL_SEND_CANMKT)
    def cancelMktData(self, id):
        assert type(id) == int
        VERSION = 1

        self._send(self.CANCEL_MKT_DATA)
        self._send(VERSION)
        self._send(id)


    @synchronized
    @requestmethod(has_id=True, min_server=6,
                   min_server_error_suffix="It does not support market depth.",
                   generic_error=_EClientErrors.FAIL_SEND_CANMKTDEPTH)
    def cancelMktDepth(self, id):
        assert type(id) == int
        VERSION = 1

        self._send(self.CANCEL_MKT_DEPTH)
        self._send(VERSION)
        self._send(id)


    @synchronized
    @requestmethod(has_id=True, min_server=21,
                   min_server_error_suffix="It does not support options exercise from the API.",
                   generic_error=_EClientErrors.FAIL_SEND_REQMKT)  # Error type per Java, IB bug?
    def exerciseOptions(self, id, contract, exercise_action,
                        exercise_quantity, account, override):
        assert type(id) == int
        assert type(contract) == __import__("tws").Contract
        assert type(exercise_action) == int
        assert type(exercise_quantity) == int
        assert type(account) == str
        assert type(override) == int
        VERSION = 1

        self._send(self.EXERCISE_OPTIONS)
        self._send(VERSION)
        self._send(id)
        self._send(contract.m_symbol)
        self._send(contract.m_secType)
        self._send(contract.m_expiry)
        self._send(contract.m_strike)
        self._send(contract.m_right)
        self._send(contract.m_multiplier)
        self._send(contract.m_exchange)
        self._send(contract.m_currency)
        self._send(contract.m_localSymbol)
        self._send(exercise_action)
        self._send(exercise_quantity)
        self._send(account)
        self._send(override)


    @synchronized
    @requestmethod(has_id=True, 
                   generic_error=_EClientErrors.FAIL_SEND_ORDER)
    def placeOrder(self, id, contract, order):
        assert type(id) == int
        assert type(contract) == __import__("tws").Contract
        assert type(order) == __import__("tws").Order
        VERSION = 27

        if self._server_version < self.MIN_SERVER_VER_SCALE_ORDERS:
            if (order.m_scaleInitLevelSize < order._DOUBLE_MAX_VALUE) or (order.m_scalePriceIncrement < order._DOUBLE_MAX_VALUE):
                self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                                id=id,
                                msg="It does not support Scale orders."))
                return
        if self._server_version < self.MIN_SERVER_VER_SSHORT_COMBO_LEGS:
            for leg in contract.m_comboLegs:
                if leg.m_shortSaleSlot or leg.m_designatedLocation:
                    self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                                    id=id,
                                    msg="It does not support SSHORT flag for combo legs."))
                    return
        if self._server_version < self.MIN_SERVER_VER_WHAT_IF_ORDERS:
            if order.m_whatIf:
                self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                                id=id,
                                msg="It does not support what-if orders."))
                return
        if self._server_version < self.MIN_SERVER_VER_UNDER_COMP:
            if contract.m_underComp:
                self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                                id=id,
                                msg="It does not support delta-neutral orders."))
                return
        if self._server_version < self.MIN_SERVER_VER_SCALE_ORDERS2:
            if (order.m_scaleSubsLevelSize < order._DOUBLE_MAX_VALUE):
                self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                                id=id,
                                msg="It does not support Subsequent Level Size for Scale orders."))
                return
        if self._server_version < self.MIN_SERVER_VER_ALGO_ORDERS:
            if order.m_algoStrategy:
                self._error(_EClientErrors.TwsError( source=_EClientErrors.UPDATE_TWS,
                                id=id,
                                msg="It does not support algo orders."))
                return

        self._send(self.PLACE_ORDER)
        self._send(VERSION)
        self._send(id)
        self._send(contract.m_symbol)
        self._send(contract.m_secType)
        self._send(contract.m_expiry)
        self._send(contract.m_strike)
        self._send(contract.m_right)
        if self._server_version >= 15:
            self._send(contract.m_multiplier)
        self._send(contract.m_exchange)
        if self._server_version >= 14:
            self._send(contract.m_primaryExch)
        self._send(contract.m_currency)
        if self._server_version >= 2:
            self._send(contract.m_localSymbol)
        self._send(order.m_action)
        self._send(order.m_totalQuantity)
        self._send(order.m_orderType)
        self._send(order.m_lmtPrice)
        self._send(order.m_auxPrice)
        self._send(order.m_tif)
        self._send(order.m_ocaGroup)
        self._send(order.m_account)
        self._send(order.m_openClose)
        self._send(order.m_origin)
        self._send(order.m_orderRef)
        self._send(order.m_transmit)
        if self._server_version >= 4:
            self._send(order.m_parentId)
        if self._server_version >= 5:
            self._send(order.m_blockOrder)
            self._send(order.m_sweepToFill)
            self._send(order.m_displaySize)
            self._send(order.m_triggerMethod)
            self._send(True if (self._server_version >= 38) and order.m_outsideRth else False)
        if self._server_version >= 7:
            self._send(order.m_hidden)
        if self._server_version >= 8:
            if self.BAG_SEC_TYPE.lower() == contract.m_secType.lower():
                self._send(len(contract.m_comboLegs))
                for leg in contract.m_comboLegs:
                    self._send(leg.m_conId)
                    self._send(leg.m_ratio)
                    self._send(leg.m_action)
                    self._send(leg.m_exchange)
                    self._send(leg.m_openClose)
                    if self._server_version >= self.MIN_SERVER_VER_SSHORT_COMBO_LEGS:
                        self._send(leg.m_shortSaleSlot)
                        self._send(leg.m_designatedLocation)
        if self._server_version >= 9:
            self._send("")
        if self._server_version >= 10:
            self._send(order.m_discretionaryAmt)
        if self._server_version >= 11:
            self._send(order.m_goodAfterTime)
        if self._server_version >= 12:
            self._send(order.m_goodTillDate)
        if self._server_version >= 13:
            self._send(order.m_faGroup)
            self._send(order.m_faMethod)
            self._send(order.m_faPercentage)
            self._send(order.m_faProfile)
        if self._server_version >= 18:
            self._send(order.m_shortSaleSlot)
            self._send(order.m_designatedLocation)
        if self._server_version >= 19:
            self._send(order.m_ocaType)
            if self._server_version < 38:
                self._send(False)
            self._send(order.m_rule80A)
            self._send(order.m_settlingFirm)
            self._send(order.m_allOrNone)
            self._sendMax(order.m_minQty)
            self._sendMax(order.m_percentOffset)
            self._send(order.m_eTradeOnly)
            self._send(order.m_firmQuoteOnly)
            self._sendMax(order.m_nbboPriceCap)
            self._sendMax(order.m_auctionStrategy)
            self._sendMax(order.m_startingPrice)
            self._sendMax(order.m_stockRefPrice)
            self._sendMax(order.m_delta)
            self._sendMax(order._DOUBLE_MAX_VALUE if (self._server_version == 26) and order.m_orderType == "VOL" else order.m_stockRangeLower)
            self._sendMax(order._DOUBLE_MAX_VALUE if (self._server_version == 26) and order.m_orderType == "VOL" else order.m_stockRangeUpper)
        if self._server_version >= 22:
            self._send(order.m_overridePercentageConstraints)
        if self._server_version >= 26:
            self._sendMax(order.m_volatility)
            self._sendMax(order.m_volatilityType)
            if self._server_version < 28:
                self._send("true" if order.m_deltaNeutralOrderType.upper() == "MKT" else "false")
            else:
                self._send(order.m_deltaNeutralOrderType)
                self._sendMax(order.m_deltaNeutralAuxPrice)
            self._send(order.m_continuousUpdate)
            self._sendMax(order.m_stockRangeLower if (self._server_version == 26) and order.m_orderType == "VOL" else order._DOUBLE_MAX_VALUE)
            self._sendMax(order.m_stockRangeUpper if (self._server_version == 26) and order.m_orderType == "VOL" else order._DOUBLE_MAX_VALUE)
            self._sendMax(order.m_referencePriceType)
        if self._server_version >= 30:
            self._sendMax(order.m_trailStopPrice)
        if self._server_version >= self.MIN_SERVER_VER_SCALE_ORDERS:
            if self._server_version >= self.MIN_SERVER_VER_SCALE_ORDERS2:
                self._sendMax(order.m_scaleInitLevelSize)
                self._sendMax(order.m_scaleSubsLevelSize)
            else:
                self._send("")
                self._sendMax(order.m_scaleInitLevelSize)
            self._sendMax(order.m_scalePriceIncrement)
        if self._server_version >= self.MIN_SERVER_VER_PTA_ORDERS:
            self._send(order.m_clearingAccount)
            self._send(order.m_clearingIntent)
        if self._server_version >= self.MIN_SERVER_VER_UNDER_COMP:
            self._send(bool(contract.m_underComp))
            if contract.m_underComp:
                self._send(contract.m_underComp.m_conId)
                self._send(contract.m_underComp.m_delta)
                self._send(contract.m_underComp.m_price)
        if self._server_version >= self.MIN_SERVER_VER_ALGO_ORDERS:
            self._send(order.m_algoStrategy)
            if order.m_algoStrategy:
                self._send(len(order.m_algoParams))
                for tagvalue in order.m_algoParams:
                    self._send(tagvalue.m_tag)
                    self._send(tagvalue.m_value)
        if self._server_version >= self.MIN_SERVER_VER_WHAT_IF_ORDERS:
            self._send(order.m_whatIf)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_ACCT)
    def reqAccountUpdates(self, subscribe, acct_code):
        assert type(subscribe) == bool
        assert type(acct_code) == str
        VERSION = 2

        self._send(self.REQ_ACCOUNT_DATA)
        self._send(VERSION)
        self._send(subscribe)
        if self._server_version >= 9:
            self._send(acct_code)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_EXEC)
    def reqExecutions(self, id, filter):
        assert type(id) == int
        assert type(filter) == __import__("tws").ExecutionFilter
        VERSION = 3

        self._send(self.REQ_EXECUTIONS)
        self._send(VERSION)
        if self._server_version >= self.MIN_SERVER_VER_EXECUTION_DATA_CHAIN:
            self._send(id)
        if self._server_version >= 9:
            self._send(filter.m_clientId)
            self._send(filter.m_acctCode)
            self._send(filter.m_time)
            self._send(filter.m_symbol)
            self._send(filter.m_secType)
            self._send(filter.m_exchange)
            self._send(filter.m_side)


    @synchronized
    @requestmethod(has_id=True,
                   generic_error=_EClientErrors.FAIL_SEND_CORDER)
    def cancelOrder(self, id):
        assert type(id) == int
        VERSION = 1

        self._send(self.CANCEL_ORDER)
        self._send(VERSION)
        self._send(id)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_OORDER)
    def reqOpenOrders(self):
        VERSION = 1

        self._send(self.REQ_OPEN_ORDERS)
        self._send(VERSION)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_CORDER)   # Error type per Java, IB bug?
    def reqIds(self, num_ids):
        assert type(num_ids) == int
        VERSION = 1

        self._send(self.REQ_IDS)
        self._send(VERSION)
        self._send(num_ids)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_CORDER)   # Error type per Java, IB bug?
    def reqNewsBulletins(self, all_msgs):
        assert type(all_msgs) == bool
        VERSION = 1

        self._send(self.REQ_NEWS_BULLETINS)
        self._send(VERSION)
        self._send(all_msgs)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_CORDER)   # Error type per Java, IB bug?
    def cancelNewsBulletins(self):
        VERSION = 1

        self._send(self.CANCEL_NEWS_BULLETINS)
        self._send(VERSION)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_SERVER_LOG_LEVEL)
    def setServerLogLevel(self, log_level):
        assert type(log_level) == int
        VERSION = 1

        self._send(self.SET_SERVER_LOGLEVEL)
        self._send(VERSION)
        self._send(log_level)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_OORDER)  # Error type per Java, IB bug?
    def reqAutoOpenOrders(self, auto_bind):
        assert type(auto_bind) == bool
        VERSION = 1

        self._send(self.REQ_AUTO_OPEN_ORDERS)
        self._send(VERSION)
        self._send(auto_bind)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_OORDER)  # Error type per Java, IB bug?
    def reqAllOpenOrders(self):
        VERSION = 1

        self._send(self.REQ_ALL_OPEN_ORDERS)
        self._send(VERSION)


    @synchronized
    @requestmethod(generic_error=_EClientErrors.FAIL_SEND_OORDER)  # Error type per Java, IB bug?
    def reqManagedAccts(self):
        VERSION = 1

        self._send(self.REQ_MANAGED_ACCTS)
        self._send(VERSION)

    @synchronized
    @requestmethod(min_server=13,
                   min_server_error_suffix="It does not support FA request.",
                   generic_error=_EClientErrors.FAIL_SEND_FA_REQUEST)  # Error type per Java, IB bug?
    def requestFA(self, fa_data_type):
        assert type(fa_data_type) == int
        VERSION = 1

        self._send(self.REQ_FA)
        self._send(VERSION)
        self._send(fa_data_type)


    @synchronized
    @requestmethod(min_server=13,
                   min_server_error_suffix="It does not support FA request.",
                   generic_error=_EClientErrors.FAIL_SEND_FA_REPLACE)  # Error type per Java, IB bug?
    def replaceFA(self, fa_data_type, xml):
        assert type(fa_data_type) == int
        assert type(xml) == str
        VERSION = 1

        self._send(self.REPLACE_FA)
        self._send(VERSION)
        self._send(fa_data_type)
        self._send(xml)


    @synchronized
    @requestmethod(min_server=33,
                   min_server_error_suffix="It does not support current time requests.",
                   generic_error=_EClientErrors.FAIL_SEND_REQCURRTIME)  # Error type per Java, IB bug?
    def reqCurrentTime(self):
        VERSION = 1

        self._send(self.REQ_CURRENT_TIME)
        self._send(VERSION)


# Clean up unneeded symbols.
_requestmethod = requestmethod
del requestmethod
del synchronized
