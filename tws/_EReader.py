'''Reader for client socket.

   Defines the EReader class, which defines the interface for a type that
   is responsible for reading data from the client socket.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from tws import EClientErrors as _EClientErrors
from tws import TickType as _TickType
from threading import Thread as _thread_type
from threading import currentThread as _current_thread


class EReader(_thread_type):
    '''Type which reads and reacts to EClientSocket data.

       Reads data from client socket and fires events in the application-defined
       EWrapper-derived object provided to EClientSocket.

       Note carefully: EReader reads socket data in a separate thread, and the
       calls it makes to the EClientSocket's EWrapper object's methods will
       also be made in the context of that thread. EWrapper objects must take
       appropriate measures to synchronize these calls as appropriate to the
       application at hand.
    '''

    def __init__(self, connection, input_stream, name=None):
        assert issubclass(type(connection), __import__("tws").EClientSocket)
        assert hasattr(input_stream, "read")

        _thread_type.__init__(self, name=name)
        self.setDaemon(True)

        self._connection = connection
        self._wrapper = connection._wrapper
        self._stream = input_stream
        self._interrupted = False


    def interrupt(self):
        self._stream.close()

        # Wait only a second for thread to terminate.
        if self.isAlive() and self != _current_thread():
            self.join(1.0)


    def run(self):
        try:
            while not self._stream.closed and self._readNextMessage():
                pass
        except Exception:
            assert False  # Should never happen.

        try:
            if self._connection.isConnected():
                self._connection._close()
        except Exception, e:
            try:
                self._wrapper.error(e)
            except: pass


    def _readNextMessage(self):
        try:
            try:
                message_id = self._readInt()
                if (message_id == -1): return False

                reader_method = self._reader_map.get(message_id, None)
                if not reader_method:
                    raise _EClientErrors.TwsError(source=_EClientErrors.UNKNOWN_ID,
                                                  msg="Message ID: %d" % message_id)
                reader_method(self)

            except Exception, e:
                assert hasattr(self._wrapper, "error")
                try:
                    self._wrapper.error(e)
                except: pass
                return False

            return True

        except:
            assert False # Should never get here.
            return False


    def _readStr(self):
        buffer = self._buffer_factory()
        while True:
            char = self._stream.read(1)
            if char == "\x00": break
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
        if implied_vol < 0: #-1 is the "not yet computed" indicator
		implied_vol = self._DOUBLE_MAX_VALUE 
        delta = self._readDouble()
        if abs(delta) > 1: #-2 is the "not yet computed" indicator
		    delta = self._DOUBLE_MAX_VALUE
        opt_price = self._DOUBLE_MAX_VALUE
        pv_dividend = self._DOUBLE_MAX_VALUE
        gamma = self._DOUBLE_MAX_VALUE
        vega = self._DOUBLE_MAX_VALUE
        theta = self._DOUBLE_MAX_VALUE
        und_price = self._DOUBLE_MAX_VALUE
        if (version >= 6) or (tick_type == _TickType.MODEL_OPTION):
		    opt_price = self._readDouble()
        if opt_price < 0: 
            opt_price = self._DOUBLE_MAX_VALUE #-1 is the "not yet computed" indicator
        pv_dividend = self._readDouble()
        if pv_dividend < 0:
            pv_dividend = self._DOUBLE_MAX_VALUE #-1 is the "not yet computed" indicator
        if version >= 6:
            gamma = self._readDouble()
        if abs(gamma) > 1:
            gamma = self._DOUBLE_MAX_VALUE # -2 is the "not yet computed" indicator
        vega = self._readDouble()
        if abs(vega) > 1:
            vega = self._DOUBLE_MAX_VALUE # -2 is the "not yet computed" indicato
        theta = self._readDouble()
        if abs(theta) > 1:
            theta = self._DOUBLE_MAX_VALUE # -2 is the "not yet computed" indicator		
        und_price = self._readDouble()
        if und_price < 0:
            und_price = self._DOUBLE_MAX_VALUE #-1 is the "not yet computed" indicator
	    self._wrapper.tickOptionComputation(ticker_id, tick_type, implied_vol, delta, opt_price, pv_dividend, 
						gamma, vega, theta, und_price)

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

    def _readUpdateAccountValue(self):
        version = self._readInt()
        key = self._readStr()
        val = self._readStr()
        cur = self._readStr()
        account_name = self._readStr() if version >= 2 else None
        self._wrapper.updateAccountValue(key, val, cur, account_name)

    def _readUpdatePortfolio(self):
        version = self._readInt()

        contract = self._contract_factory()
        if version >= 6:
            contract.m_conId = self._readInt()
        contract.m_symbol = self._readStr()
        contract.m_secType = self._readStr()
        contract.m_expiry = self._readStr()
        contract.m_strike = self._readDouble()
        contract.m_right = self._readStr()
        if version >= 7:
            contract.m_multiplier = self._readStr()
            contract.m_primaryExch = self._readStr()
        contract.m_currency = self._readStr()
        if version >= 2:
            contract.m_localSymbol = self._readStr()

        position = self._readInt()
        market_price = self._readDouble()
        market_value = self._readDouble()

        average_cost = self._readDouble() if version >= 3 else 0.0
        unrealized_PNL = self._readDouble() if version >= 3 else 0.0
        realized_PNL = self._readDouble() if version >= 3 else 0.0
        account_name = self._readStr() if version >= 4 else ""

        if (version == 6) and (self._connection.serverVersion() == 39):
            contract.m_primaryExch = self._readStr()

        self._wrapper.updatePortfolio(contract, position, market_price, market_value, average_cost,
                                      unrealized_PNL, realized_PNL, account_name)

    def _readUpdateAccountTime(self):
        version = self._readInt()
        timestamp = self._readStr()
        self._wrapper.updateAccountTime(timestamp)


    def _readError(self):
        version = self._readInt()
        id = self._readInt() if version >= 2 else _EClientErrors.NO_VALID_ID
        code = self._readInt() if version >= 2 else _EClientErrors.UNKNOWN_ID.code()
        msg = self._readStr()
        self._wrapper.error(_EClientErrors.TwsError(id, code, msg))


    def _readOpenOrder(self):
        version = self._readInt()
        order = self._order_factory()
        order.m_orderId = self._readInt()
        contract = self._contract_factory()
        if version >= 17:
            contract.m_conId = self._readInt()
        contract.m_symbol = self._readStr()
        contract.m_secType = self._readStr()
        contract.m_expiry = self._readStr()
        contract.m_strike = self._readDouble()
        contract.m_right = self._readStr()
        contract.m_exchange = self._readStr()
        contract.m_currency = self._readStr()
        if version >= 2:
            contract.m_localSymbol = self._readStr()
        order.m_action = self._readStr()
        order.m_totalQuantity = self._readInt()
        order.m_orderType = self._readStr()
        order.m_lmtPrice = self._readDouble()
        order.m_auxPrice = self._readDouble()
        order.m_tif = self._readStr()
        order.m_ocaGroup = self._readStr()
        order.m_account = self._readStr()
        order.m_openClose = self._readStr()
        order.m_origin = self._readInt()
        order.m_orderRef = self._readStr()
        if version >= 3:
            order.m_clientId = self._readInt()
        if version >= 4:
            order.m_permId = self._readInt()
            if version < 18:
                self._readBoolFromInt()
            else:
                order.m_outsideRth = self._readBoolFromInt()
            order.m_hidden = (self._readInt() == 1)
            order.m_discretionaryAmt = self._readDouble()
        if version >= 5:
            order.m_goodAfterTime = self._readStr()
        if version >= 6: #skip deprecated sharesAllocation field
            self._readStr()
        if version >= 7:
            order.m_faGroup = self._readStr()
            order.m_faMethod = self._readStr()
            order.m_faPercentage = self._readStr()
            order.m_faProfile = self._readStr()
        if version >= 8:
            order.m_goodTillDate = self._readStr()
        if version >= 9:
            order.m_rule80A = self._readStr()
            order.m_percentOffset = self._readDouble()
            order.m_settlingFirm = self._readStr()
            order.m_shortSaleSlot = self._readInt()
            order.m_designatedLocation = self._readStr()
	    if (self._connection.serverVersion() == 51):
		self._readInd() #exemptCode
            if (version >= 23):
		order.m_exemptCode = self._readInt()
	    order.m_auctionStrategy = self._readInt()
            order.m_startingPrice = self._readDouble()
            order.m_stockRefPrice = self._readDouble()
            order.m_delta = self._readDouble()
            order.m_stockRangeLower = self._readDouble()
            order.m_stockRangeUpper = self._readDouble()
            order.m_displaySize = self._readInt()
            if version < 18:
                self._readBoolFromInt()
            order.m_blockOrder = self._readBoolFromInt()
            order.m_sweepToFill = self._readBoolFromInt()
            order.m_allOrNone = self._readBoolFromInt()
            order.m_minQty = self._readInt()
            order.m_ocaType = self._readInt()
            order.m_eTradeOnly = self._readBoolFromInt()
            order.m_firmQuoteOnly = self._readBoolFromInt()
            order.m_nbboPriceCap = self._readDouble()
        if version >= 10:
            order.m_parentId = self._readInt()
            order.m_triggerMethod = self._readInt()
        if version >= 11:
            order.m_volatility = self._readDouble()
            order.m_volatilityType = self._readInt()
            if (version == 11):
                receivedInt = self._readInt()
                order.m_deltaNeutralOrderType = "NONE" if (receivedInt == 0) else "MKT"
            else:
                order.m_deltaNeutralOrderType = self._readStr()
                order.m_deltaNeutralAuxPrice = self._readDouble()
            order.m_continuousUpdate = self._readInt()
            if (self._connection.serverVersion() == 26):
                order.m_stockRangeLower = self._readDouble()
                order.m_stockRangeUpper = self._readDouble()
            order.m_referencePriceType = self._readInt()
        if version >= 13:
            order.m_trailStopPrice = self._readDouble()
        if version >= 14:
            order.m_basisPoints = self._readDouble()
            order.m_basisPointsType = self._readInt()
            contract.m_comboLegsDescrip = self._readStr()
        if version >= 15:
            if version >= 20:
                order.m_scaleInitLevelSize = self._readIntMax()
                order.m_scaleSubsLevelSize = self._readIntMax()
            else:
                self._readIntMax()
                order.m_scaleInitLevelSize = self._readIntMax()
            order.m_scalePriceIncrement = self._readDoubleMax()
        if version >= 19:
            order.m_clearingAccount = self._readStr()
            order.m_clearingIntent = self._readStr()
	if version >= 22:
	    order.m_notHeld = self._readBoolFromInt()
        if version >= 20:
            if self._readBoolFromInt():
                undercomp = self._undercomp_factory()
                undercomp.m_conId = self._readInt()
                undercomp.m_delta = self._readDouble()
                undercomp.m_price = self._readDouble()
                contract.m_underComp = undercomp
        if version >= 21:
            order.m_algoStrategy = self._readStr()
            if order.m_algoStrategy:
                algoParamsCount = self._readInt()
                if algoParamsCount > 0:
                    order.m_algoParams = []
                    for i in xrange(algoParamsCount):
                        order.m_algoParams.append(
                            self._tag_value_factory(self._readStr(),
                                                    self._readStr()))
        orderState = self._order_state_factory()
        if version >= 16:
            order.m_whatIf = self._readBoolFromInt()
            orderState.m_status = self._readStr()
            orderState.m_initMargin = self._readStr()
            orderState.m_maintMargin = self._readStr()
            orderState.m_equityWithLoan = self._readStr()
            orderState.m_commission = self._readDoubleMax()
            orderState.m_minCommission = self._readDoubleMax()
            orderState.m_maxCommission = self._readDoubleMax()
            orderState.m_commissionCurrency = self._readStr()
            orderState.m_warningText = self._readStr()
        self._wrapper.openOrder(order.m_orderId, contract, order, orderState)


    def _readNextValidId(self):
        version = self._readInt()
        order_id = self._readInt()
        self._wrapper.nextValidId(order_id)


    def _readScannerData(self):
        version = self._readInt()
        ticker_id = self._readInt()
	number_of_elements = self._readInt()
        for i in xrange(number_of_elements):
            contract = self._contract_details_factory()
            rank = self._readInt()
            if version >= 3:
                contract.m_summary.m_conId = self._readInt()
            contract.m_summary.m_symbol = self._readStr()
            contract.m_summary.m_secType = self._readStr()
            contract.m_summary.m_expiry = self._readStr()
            contract.m_summary.m_strike = self._readDouble()
            contract.m_summary.m_right = self._readStr()
            contract.m_summary.m_exchange = self._readStr()
            contract.m_summary.m_currency = self._readStr()
            contract.m_summary.m_localSymbol = self._readStr()
            contract.m_marketName = self._readStr()
            contract.m_tradingClass = self._readStr()
            distance = self._readStr()
            benchmark = self._readStr()
            projection = self._readStr()
            legs = self._readStr() if version >= 2 else None
            self._wrapper.scannerData(ticker_id, rank, contract, distance, benchmark, projection, legs)
        self._wrapper.scannerDataEnd(ticker_id)


    def _readContractDetails(self):
        version = self._readInt()
        req_id = self._readInt() if version >= 3 else -1
        contract = self._contract_details_factory()
        contract.m_summary.m_symbol = self._readStr()
        contract.m_summary.m_secType = self._readStr()
        contract.m_summary.m_expiry = self._readStr()
        contract.m_summary.m_strike = self._readDouble()
        contract.m_summary.m_right = self._readStr()
        contract.m_summary.m_exchange = self._readStr()
        contract.m_summary.m_currency = self._readStr()
        contract.m_summary.m_localSymbol = self._readStr()
        contract.m_marketName = self._readStr()
        contract.m_tradingClass = self._readStr()
        contract.m_summary.m_conId = self._readInt()
        contract.m_minTick = self._readDouble()
        contract.m_summary.m_multiplier = self._readStr()
        contract.m_orderTypes = self._readStr()
        contract.m_validExchanges = self._readStr()
        if version >= 2:
            contract.m_priceMagnifier = self._readInt()
        if version >= 4:
            contract.m_underConId = self._readInt()
	if version >= 5: 
	    contract.m_longName = self._readStr()
	    contract.m_summary.m_primaryExch = self._readStr()
	if version >= 6: 
	    contract.m_contractMonth = self._readStr()
	    contract.m_industry = self._readStr()
	    contract.m_category = self._readStr()
	    contract.m_subcategory = self._readStr()
	    contract.m_timeZoneId = self._readStr()
	    contract.m_tradingHours = self._readStr()
	    contract.m_liquidHours = self._readStr()
        self._wrapper.contractDetails(req_id, contract)


    def _readBondContractDetails(self):
        version = self._readInt()
        req_id = self._readInt() if version >= 3 else -1
        contract = self._contract_details_factory()
        contract.m_summary.m_symbol = self._readStr()
        contract.m_summary.m_secType = self._readStr()
        contract.m_cusip = self._readStr()
        contract.m_coupon = self._readDouble()
        contract.m_maturity = self._readStr()
        contract.m_issueDate = self._readStr()
        contract.m_ratings = self._readStr()
        contract.m_bondType = self._readStr()
        contract.m_couponType = self._readStr()
        contract.m_convertible = self._readBoolFromInt()
        contract.m_callable = self._readBoolFromInt()
        contract.m_putable = self._readBoolFromInt()
        contract.m_descAppend = self._readStr()
        contract.m_summary.m_exchange = self._readStr()
        contract.m_summary.m_currency = self._readStr()
        contract.m_marketName = self._readStr()
        contract.m_tradingClass = self._readStr()
        contract.m_summary.m_conId = self._readInt()
        contract.m_minTick = self._readDouble()
        contract.m_orderTypes = self._readStr()
        contract.m_validExchanges = self._readStr()
        if version >= 2:
            contract.m_nextOptionDate = self._readStr()
            contract.m_nextOptionType = self._readStr()
            contract.m_nextOptionPartial = self._readBoolFromInt()
            contract.m_notes = self._readStr()
	if version >= 4:
	    contract.m_longName = self._readStr()
        self._wrapper.bondContractDetails(req_id, contract)


    def _readExecDetails(self):
        version = self._readInt()
        req_id = self._readInt() if version >= 7 else -1
        order_id = self._readInt()
        contract = self._contract_factory()
        if version >= 5:
            contract.m_conId = self._readInt()
        contract.m_symbol = self._readStr()
        contract.m_secType = self._readStr()
        contract.m_expiry = self._readStr()
        contract.m_strike = self._readDouble()
        contract.m_right = self._readStr()
        contract.m_exchange = self._readStr()
        contract.m_currency = self._readStr()
        contract.m_localSymbol = self._readStr()
        execution = self._execution_factory()
        execution.m_orderId = order_id
        execution.m_execId = self._readStr()
        execution.m_time = self._readStr()
        execution.m_acctNumber = self._readStr()
        execution.m_exchange = self._readStr()
        execution.m_side = self._readStr()
        execution.m_shares = self._readInt()
        execution.m_price = self._readDouble()
        if version >= 2:
            execution.m_permId = self._readInt()
        if version >= 3:
            execution.m_clientId = self._readInt()
        if version >= 4:
            execution.m_liquidation = self._readInt()
        if version >= 6:
            execution.m_cumQty = self._readInt()
            execution.m_avgPrice = self._readDouble()
        self._wrapper.execDetails(req_id, contract, execution)


    def _readUpdateMktDepth(self):
        version = self._readInt()
        id = self._readInt()
        position = self._readInt()
        operation = self._readInt()
        side = self._readInt()
        price = self._readDouble()
        size = self._readInt()
        self._wrapper.updateMktDepth(id, position, operation, side, price, size)


    def _readUpdateMktDepthL2(self):
        version = self._readInt()
        id = self._readInt()
        position = self._readInt()
        market_maker = self._readStr()
        operation = self._readInt()
        side = self._readInt()
        price = self._readDouble()
        size = self._readInt()
        self._wrapper.updateMktDepthL2(id, position, market_maker, operation, side, price, size)


    def _readUpdateNewsBulletin(self):
        version = self._readInt()
        news_msg_id = self._readInt()
        news_msg_type = self._readInt()
        news_message = self._readStr()
        originating_exch = self._readStr()
        self._wrapper.updateNewsBulletin(news_msg_id, news_msg_type, news_message, originating_exch)


    def _readManagedAccounts(self):
        version = self._readInt()
        accounts_list = self._readStr()
        self._wrapper.managedAccounts(accounts_list)


    def _readReceiveFA(self):
        version = self._readInt()
        fa_data_type = self._readInt()
        xml = self._readStr()
        self._wrapper.receiveFA(fa_data_type, xml)


    def _readHistoricalData(self):
        version = self._readInt()
        req_id = self._readInt()
        finish_token = "finished"
        if version >= 2:
            finish_token += '-%s-%s' % (self._readStr(), self._readStr())
        item_count = self._readInt()
        for i in xrange(item_count):
            date = self._readStr()
            open = self._readDouble()
            high = self._readDouble()
            low = self._readDouble()
            close = self._readDouble()
            volume = self._readInt()
            wap = self._readDouble()
            has_gaps = (str(self._readStr()).upper() == "TRUE")
            bar_count = self._readInt() if version >= 3 else -1
            self._wrapper.historicalData(req_id, date, open, high, low, close, volume, bar_count, wap, has_gaps)
        self._wrapper.historicalData(req_id, finish_token, -1, -1, -1, -1, -1, -1, -1, False)


    def _readScannerParameters(self):
        version = self._readInt()
        xml = self._readStr()
        self._wrapper.scannerParameters(xml)


    def _readCurrentTime(self):
        self._readInt()
        time = self._readLong()
        self._wrapper.currentTime(time)


    def _readRealtimeBar(self):
        self._readInt()
        req_id = self._readInt()
        time = self._readLong()
        open = self._readDouble()
        high = self._readDouble()
        low = self._readDouble()
        close = self._readDouble()
        volume = self._readLong()
        wap = self._readDouble()
        count = self._readInt()
        self._wrapper.realtimeBar(req_id, time, open, high, low, close, volume, wap, count)


    def _readFundamentalData(self):
        self._readInt()
        req_id = self._readInt()
        data = self._readStr()
        self._wrapper.fundamentalData(req_id, data)


    def _readContractDetailsEnd(self):
        self._readInt()
        req_id = self._readInt()
        self._wrapper.contractDetailsEnd(req_id)


    def _readOpenOrderEnd(self):
        self._readInt()
        self._wrapper.openOrderEnd()


    def _readAccountDownloadEnd(self):
        self._readInt()
        account_name = self._readStr()
        self._wrapper.accountDownloadEnd(account_name)


    def _readExecDetailsEnd(self):
        self._readInt()
        req_id = self._readInt()
        self._wrapper.execDetailsEnd(req_id)


    def _readDeltaNeutralValidation(self):
        self._readInt()
        req_id = self._readInt()
        undercomp = self._undercomp_factory()
        undercomp.m_conId = self._readInt()
        undercomp.m_delta = self._readDouble()
        undercomp.m_price = self._readDouble()
        self._wrapper.deltaNeutralValidation(req_id, undercomp)

    def _tickSnapshotEnd(self):
	self._readInt()
	req_id = self.readInt()
	self._wrapper.tickSnapshotEnd(req_id)
 

    ## incoming msg id's##
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
    TICK_SNAPSHOT_END = 57

    ## Tag-method dispatch rules ##
    _reader_map = {
        TICK_PRICE: _readTickPrice,
        TICK_SIZE: _readTickSize,
        TICK_OPTION_COMPUTATION: _readTickOptionComputation,
        TICK_GENERIC: _readTickGeneric,
        TICK_STRING: _readTickString,
        TICK_EFP: _readTickEFP,
        ORDER_STATUS: _readOrderStatus,
        ACCT_VALUE: _readUpdateAccountValue,
        PORTFOLIO_VALUE: _readUpdatePortfolio,
        ACCT_UPDATE_TIME: _readUpdateAccountTime,
        ERR_MSG: _readError,
        OPEN_ORDER: _readOpenOrder,
        NEXT_VALID_ID: _readNextValidId,
        SCANNER_DATA: _readScannerData,
        CONTRACT_DATA: _readContractDetails,
        BOND_CONTRACT_DATA: _readBondContractDetails,
        EXECUTION_DATA: _readExecDetails,
        MARKET_DEPTH: _readUpdateMktDepth,
        MARKET_DEPTH_L2: _readUpdateMktDepthL2,
        NEWS_BULLETINS: _readUpdateNewsBulletin,
        MANAGED_ACCTS: _readManagedAccounts,
        RECEIVE_FA: _readReceiveFA,
        HISTORICAL_DATA:_readHistoricalData,
        SCANNER_PARAMETERS: _readScannerParameters,
        CURRENT_TIME: _readCurrentTime,
        REAL_TIME_BARS: _readRealtimeBar,
        FUNDAMENTAL_DATA: _readFundamentalData,
        CONTRACT_DATA_END: _readContractDetailsEnd,
        OPEN_ORDER_END: _readOpenOrderEnd,
        ACCT_DOWNLOAD_END: _readAccountDownloadEnd,
        EXECUTION_DATA_END: _readExecDetailsEnd,
        DELTA_NEUTRAL_VALIDATION: _readDeltaNeutralValidation,
	TICK_SNAPSHOT_END: _tickSnapshotEnd
    }


    ## Private class imports ##
    from cStringIO import StringIO as _buffer_factory
    from tws._Contract import Contract as _contract_factory
    from tws._ContractDetails import ContractDetails as _contract_details_factory
    from tws._Execution import Execution as _execution_factory
    from tws._Order import Order as _order_factory
    from tws._OrderState import OrderState as _order_state_factory
    from tws._TagValue import TagValue as _tag_value_factory
    from tws._UnderComp import UnderComp as _undercomp_factory
    from tws._Util import _INT_MAX_VALUE
    from tws._Util import _DOUBLE_MAX_VALUE
