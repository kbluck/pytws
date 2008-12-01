'''Reader for client socket.

   Defines the EReader class, which defines the interface for a type that
   is responsible for reading data from the client socket.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from tws import _TickType


class EReader(object):
    """Type which reads and reacts to EClientSocket data.

       Reads data from client socket and fires events in the application-defined
       EWrapper-derived object provided to EClientSocket.
    """

    def __init__(self, connection, input_stream):
        assert issubclass(type(connection), __import__("tws").EClientSocket)
        assert hasattr(input_stream, "read")

        self._connection = connection
        self._wrapper = connection._wrapper
        self._stream = input_stream


    def _readTickPrice(self):
        version = self._readInt()
        tickerId = self._readInt()
        tickType = self._readInt()
        price = self._readDouble()
        size = self._readInt() if version >= 2 else 0
        canAutoExecute = self._readInt() if version >= 3 else 0
        self._wrapper.tickPrice(tickerId, tickType, price, canAutoExecute)
        if version >= 2:
            sizeTickType = _TickType.BID_SIZE  if tickType == _TickType.BID  else \
                           _TickType.ASK_SIZE  if tickType == _TickType.ASK  else \
                           _TickType.LAST_SIZE if tickType == _TickType.LAST else -1 
            if (sizeTickType != -1):
                self._wrapper.tickSize(tickerId, sizeTickType, size)


    def _readTickSize(self):
        version = self._readInt()
        tickerId = self._readInt()
        tickType = self._readInt()
        size = self._readInt()
        self._wrapper.tickSize(tickerId, tickType, size)


    ## Raw base data stream reader functions ##

    def _readStr(self):
        buffer = self._buffer_factory()
        while True:
            char = self._stream.read(1)
            if char == '\x00': break
            buffer.write(char)
        result = buffer.getvalue()
        return result if result else None


    def _readInt(self, default=0):
        strval = self._readStr()
        return int(strval) if strval else default


    def _readIntMax(self):
        return self._readInt(default=self._INT_MAX_VALUE)


    def _readBoolFromInt(self):
        return bool(self._readInt())


    def _readLong(self):
        strval = self._readStr()
        return long(strval) if strval else long(0)


    def _readDouble(self, default=0.0):
        strval = self._readStr()
        return float(strval) if strval else default


    def _readDoubleMax(self):
        return self._readDouble(default=self._DOUBLE_MAX_VALUE)


    ## Tag constants ##

    TICK_PRICE = 1
    TICK_SIZE = 2
    ORDER_STATUS = 3
    ERR_MSG = 4
    OPEN_ORDER = 5
    ACCT_VALUE = 6
    PORTFOLIO_VALUE = 7
    ACCT_UPDATE_TIME = 8
    NEXT_VALID_ID = 9
    CONTRACT_DATA = 10
    EXECUTION_DATA = 11
    MARKET_DEPTH = 12
    MARKET_DEPTH_L2 = 13
    NEWS_BULLETINS = 14
    MANAGED_ACCTS = 15
    RECEIVE_FA = 16
    HISTORICAL_DATA = 17
    BOND_CONTRACT_DATA = 18
    SCANNER_PARAMETERS = 19
    SCANNER_DATA = 20
    TICK_OPTION_COMPUTATION = 21
    TICK_GENERIC = 45
    TICK_STRING = 46
    TICK_EFP = 47
    CURRENT_TIME = 49
    REAL_TIME_BARS = 50
    FUNDAMENTAL_DATA = 51
    CONTRACT_DATA_END = 52
    OPEN_ORDER_END = 53
    ACCT_DOWNLOAD_END = 54
    EXECUTION_DATA_END = 55
    DELTA_NEUTRAL_VALIDATION = 56


    ## Private class imports ##

    from cStringIO import StringIO as _buffer_factory
    from tws._Util import _INT_MAX_VALUE
    from tws._Util import _DOUBLE_MAX_VALUE
