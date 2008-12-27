'''Main connection to TWS client.

   Defines the EClientSocket class, which implements a socket connection to
   the TWS socket server, through which the entire API operates.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import tws._EClientErrors as EClientErrors


class EClientSocket(object):
    '''Socket client which connects to the TWS socket server.
    '''

    def __init__(self, wrapper, socket_factory=__import__("socket").socket):
        assert issubclass(type(wrapper), __import__("tws").EWrapper)  
        assert callable(socket_factory)

        self._wrapper = wrapper
        self._reader = None
        self._connected = False
        self._serverVersion = ""
        self._twsTime = ""
        self._socket_factory = socket_factory


    def wrapper(self):
        return self._wrapper


    def reader(self):
        return self._reader


    def isConnected(self):
        return self._connected


    def serverVersion(self):
        return self._serverVersion


    def TwsConnectionTime(self):
        return self._twsTime


    def checkConnected(self, host):
        assert issubclass(type(host), str) or (host == None)  

        if self._connected:
            self._wrapper.error(EClientErrors.ALREADY_CONNECTED)
            return None
        return host if host else "127.0.0.1"


    def connectionError(self):
        self._wrapper.error(EClientErrors.CONNECT_FAIL)
        self.m_reader = None

    def createReader(self, connection, input_stream):
        assert issubclass(type(connection), type(self))
        assert hasattr(input_stream, "read")

        return __import__("tws").EReader(connection, input_stream)


    def send(self, data):
        if type(data) in (str, int, long, float):
            self._stream.write(str(data))
        elif type(data) == bool:
            self._stream.write("1" if data else "0")
        else:
            raise ValueError("Unknown data type for EClientSocket.send(): %s", type(data))
        self._stream.write(self.EOL)


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
