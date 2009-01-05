'''Main connection to TWS client.

   Defines the EClientSocket class, which implements a socket connection to
   the TWS socket server, through which the entire API operates.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import tws.EClientErrors as _EClientErrors
from tws import synchronized


def requestmethod(min_server=0, has_ticker=False,
                  generic_error=_EClientErrors.TwsError(),
                  error_suffix=""):
    '''Socket request-method decorator.

       Eliminates repetitive error-checking boilerplate from request methods.   
    '''
    assert type(min_server) == int
    assert type(has_ticker) == bool
    assert isinstance(generic_error, _EClientErrors.TwsError)
    assert type(error_suffix) == str

    def _decorator(method):
        assert  (__import__("inspect").getargspec(method)[0][0] == "self")
        assert  (not has_ticker) or (__import__("inspect").getargspec(method)[0][1] == "ticker_id")

        def _decorated(self, *args, **kwds):
            assert type(self) == EClientSocket

            try:
                # Socket client must be connected.
                if not self._connected:
                    self._error(_EClientErrors.NOT_CONNECTED)
                    return
                # Enforce minimum server version, if any.
                if self._server_version < min_server:
                    self._error(_EClientErrors.UPDATE_TWS)
                    return
                # Call wrapped method
                return method(self, *args, **kwds)
            # On exception, report generic error instance to EWrapper._error()
            except:
                self._error(_EClientErrors.TwsError(
                                source=generic_error,
                                id=kwds.get("ticker_id", args[0] if args else None) 
                                    if has_ticker else _EClientErrors.NO_VALID_ID,
                                msg=error_suffix or method.__name__))

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
    @requestmethod(min_server=24, has_ticker=True,
                   generic_error=_EClientErrors.FAIL_SEND_CANSCANNER)
    def cancelScannerSubscription(self, ticker_id):
        VERSION = 1
        self._send(self.CANCEL_SCANNER_SUBSCRIPTION)
        self._send(VERSION)
        self._send(ticker_id)


    @synchronized
    @requestmethod(min_server=24,
                   generic_error=_EClientErrors.FAIL_SEND_REQSCANNERPARAMETERS)
    def reqScannerParameters(self):
        VERSION = 1
        self._send(self.REQ_SCANNER_PARAMETERS)
        self._send(VERSION)


    @synchronized
    @requestmethod(min_server=24, has_ticker=True,
                   generic_error=_EClientErrors.FAIL_SEND_REQSCANNER)
    def reqScannerSubscription(self, ticker_id, subscription):
        VERSION = 3
        self._send(self.REQ_SCANNER_SUBSCRIPTION)
        self._send(VERSION)
        self._send(ticker_id)
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


# Clean up unneeded symbols.
_requestmethod = requestmethod
del requestmethod
del synchronized
