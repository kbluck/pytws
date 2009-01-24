'''Implements EWrapper hook to handle tick*().'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import threading as _threading
import tws.EClientErrors as _EClientErrors


class HookTicks(object):
    '''Installs hook to handle EWrapper.tick*() events.

       To install construct an instance passing the wrapper object to hook.

       After installation, your wrapper object will begin handling all the
       EWrapper.tick* events. At any time you may call the method
       <wrapper>.get_ticks() to obtain the current ticks as reported by
       the TWS application.
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)
        assert hasattr(wrapper,"client")

        self._wrapper = wrapper
        self._ticks = {}
        self._condition = _threading.Condition()

        wrapper.tickPrice = self.tickPrice
        wrapper.tickSize = self.tickSize
        wrapper.tickOptionComputation = self.tickOptionComputation
        wrapper.tickGeneric = self.tickGeneric
        wrapper.tickString = self.tickString
        wrapper.tickEFP = self.tickEFP
        wrapper.get_ticks = self.get_ticks


    def tickPrice(self, ticker_id, field, price, can_auto_execute):
        '''Handler for EWrapper.tickPrice() events.

           Installed using tws.helper.HookTicks(wrapper)
        '''
        assert isinstance(ticker_id, int)
        assert isinstance(field, int)
        assert isinstance(price, float)
        assert isinstance(can_auto_execute, int)

        with (self._condition):
            try:
                self._ticks.setdefault(ticker_id,dict())[field] = (
                    ticker_id, field, price, can_auto_execute)
            finally:
                self._condition.notifyAll()


    def tickSize(self, ticker_id, field, size):
        '''Handler for EWrapper.tickSize() events.

           Installed using tws.helper.HookTicks(wrapper)
        '''
        assert isinstance(ticker_id, int)
        assert isinstance(field, int)
        assert isinstance(size, int)

        with (self._condition):
            try:
                self._ticks.setdefault(ticker_id,dict())[field] = (
                    ticker_id, field, size)
            finally:
                self._condition.notifyAll()


    def tickOptionComputation(self, ticker_id, field, implied_vol, delta,
                              model_price, pv_dividend):
        '''Handler for EWrapper.tickOptionComputation() events.

           Installed using tws.helper.HookTicks(wrapper)
        '''
        assert isinstance(ticker_id, int)
        assert isinstance(field, int)
        assert isinstance(implied_vol, float)
        assert isinstance(delta, float)
        assert isinstance(model_price, float)
        assert isinstance(pv_dividend, float)

        with (self._condition):
            try:
                self._ticks.setdefault(ticker_id,dict())[field] = (
                    ticker_id, field, implied_vol, delta,
                    model_price, pv_dividend)
            finally:
                self._condition.notifyAll()


    def tickGeneric(self, ticker_id, field, value):
        '''Handler for EWrapper.tickGeneric() events.

           Installed using tws.helper.HookTicks(wrapper)
        '''
        assert isinstance(ticker_id, int)
        assert isinstance(field, int)
        assert isinstance(value, float)

        with (self._condition):
            try:
                self._ticks.setdefault(ticker_id,dict())[field] = (
                    ticker_id, field, value)
            finally:
                self._condition.notifyAll()


    def tickString(self, ticker_id, field, value):
        '''Handler for EWrapper.tickString() events.

           Installed using tws.helper.HookTicks(wrapper)
        '''
        assert isinstance(ticker_id, int)
        assert isinstance(field, int)
        assert isinstance(value, str)

        with (self._condition):
            try:
                self._ticks.setdefault(ticker_id,dict())[field] = (
                    ticker_id, field, value)
            finally:
                self._condition.notifyAll()


    def tickEFP(self, ticker_id, field, basis_points, formatted_basis_points,
                implied_future, hold_days, future_expiry, dividend_impact,
                dividends_to_expiry):
        '''Handler for EWrapper.tickEFP() events.

           Installed using tws.helper.HookTicks(wrapper)
        '''
        assert isinstance(ticker_id, int)
        assert isinstance(field, int)
        assert isinstance(basis_points, float)
        assert isinstance(formatted_basis_points, str)
        assert isinstance(implied_future, float)
        assert isinstance(hold_days, int)
        assert isinstance(future_expiry, str)
        assert isinstance(dividend_impact, float)
        assert isinstance(dividends_to_expiry, float)

        with (self._condition):
            try:
                self._ticks.setdefault(ticker_id,dict())[field] = (
                    ticker_id, field, basis_points, formatted_basis_points,
                    implied_future, hold_days, future_expiry, dividend_impact,
                    dividends_to_expiry)
            finally:
                self._condition.notifyAll()


    def get_ticks(self, wait_until_changed=None, timeout=None):
        '''Gets current ticks.

           This method returns the the current tick values as reported by
           the TWS application. It returns a dict keyed by ticker ID and
           with values also being dicts. Each value dick is keyed by the
           field ID and contains a value which is a tuple containing the
           same values as the arguments that would be passed to the
           EWrapper.tick*() method corresponding to that field. For
           example, a field value of 1 (bid) would have the values passed
           to the tickPrice() method, while field 0 (bid size) would have
           the values passed to the tickSize() method.

           Since the ticks are stored as nested dicts, you should be careful
           when using chained subscript notation. For example, you might
           use "ticks[10][1]" to get the values of the bid tick for ticker
           ID 10. However, you should be aware that if a bid tick has not
           yet arrived for that ticker, you will get a KeyError exception.
           If you don't want to deal with that exception, it would be safer
           to use something like "ticks[10].get(1,0.0)" to return a default
           value if there is no tick instead of raising a KeyError.

           It is often the case that you will want to wait for the next tick
           update. To do this, pass in the the wait_until_changed param the
           dict of ticks which you consider current. The method will block
           until it received an update from TWS with an updated tick. Be
           careful! By default it will wait forever for an update, so you
           should not wait unless you are certain that TWS will deliver a
           tick update update within a reasonable amount of time. You should
           also be aware that the method will unblock on *any* tick update,
           not necessarily the one you happen to be interested in. If you
           like, you may pass in a float timeout value for the maximum
           seconds the method should wait before returning the current tick
           dict regardless of whether there was a tick update from TWS.

           If you do not pass a dict to the wait_until_changed param, the
           method will not block, and the timeout param is ignored.

           Installed using tws.helper.HookTicks(wrapper)
        '''
        assert isinstance(wait_until_changed, dict) or (wait_until_changed is None)
        assert (timeout >= 0) or (timeout is None)

        if not self._wrapper.client.isConnected():
            raise _EClientErrors.NOT_CONNECTED
        with (self._condition):
            if wait_until_changed != None:
                if self._ticks == wait_until_changed:
                    self._condition.wait(timeout)
            return self._ticks.copy()
