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


    def _readTickPrice(self):
        version = self._readInt()
        ticker_id = self._readInt()
        price_tick_type = self._readInt()
        price = self._readDouble()
        size = self._readInt() if version >= 2 else 0
        can_auto_execute = self._readInt() if version >= 3 else 0
        self._wrapper.tickPrice(ticker_id, price_tick_type, price, can_auto_execute)
        if version >= 2:
            size_tick_type = _TickType.BID_SIZE  if price_tick_type == _TickType.BID  else \
                             _TickType.ASK_SIZE  if price_tick_type == _TickType.ASK  else \
                             _TickType.LAST_SIZE if price_tick_type == _TickType.LAST else -1 
            if (size_tick_type != -1):
                self._wrapper.tickSize(ticker_id, size_tick_type, size)


    def _readTickSize(self):
        version = self._readInt()
        ticker_id = self._readInt()
        tick_type = self._readInt()
        size = self._readInt()
        self._wrapper.tickSize(ticker_id, tick_type, size)


    def _readTickOptionComputation(self):
        version = self._readInt()
        ticker_id = self._readInt()
        tick_type = self._readInt()
        implied_vol = self._readDouble()
        delta = self._readDouble()
        if (tick_type == _TickType.MODEL_OPTION):
            model_price = self._readDouble()
            pv_dividend = self._readDouble()
        else:
            model_price = pv_dividend = self._DOUBLE_MAX_VALUE

        self._wrapper.tickOptionComputation(ticker_id, tick_type, 
                                            implied_vol if implied_vol >= 0.0 else self._DOUBLE_MAX_VALUE,
                                            delta if abs(delta) <= 1.0 else self._DOUBLE_MAX_VALUE,
                                            model_price, pv_dividend)


    def _readTickGeneric(self):
        version = self._readInt()
        ticker_id = self._readInt()
        tick_type = self._readInt()
        value = self._readDouble()
        self._wrapper.tickGeneric(ticker_id, tick_type, value)


    def _readTickString(self):
        version = self._readInt()
        ticker_id = self._readInt()
        tick_type = self._readInt()
        value = self._readStr()
        self._wrapper.tickString(ticker_id, tick_type, value)


    def _readTickEFP(self):
        version = self._readInt()
        ticker_id = self._readInt()
        tick_type = self._readInt()
        basis_points = self._readDouble()
        formatted_basis_points = self._readStr()
        implied_futures_price = self._readDouble()
        hold_days = self._readInt()
        future_expiry = self._readStr()
        dividend_impact = self._readDouble()
        dividends_to_expiry = self._readDouble()
        self._wrapper.tickEFP(ticker_id, tick_type, basis_points, formatted_basis_points, implied_futures_price,
                              hold_days, future_expiry, dividend_impact, dividends_to_expiry)


    def _readOrderStatus(self):
        version = self._readInt()
        id = self._readInt()
        status = self._readStr()
        filled = self._readInt()
        remaining = self._readInt()
        avg_fill_price = self._readDouble()
        perm_id = self._readInt() if version >= 2 else 0
        parent_id = self._readInt() if version >= 3 else 0
        last_fill_price = self._readDouble() if version >= 4 else 0
        client_id = self._readInt() if version >= 5 else 0
        why_held = self._readStr() if version >= 6 else None
        self._wrapper.orderStatus(id, status, filled, remaining, avg_fill_price, perm_id,
                                  parent_id, last_fill_price, client_id, why_held)

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
