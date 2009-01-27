'''Implements EWrapper hook to handle account updates.'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import threading as _threading
import tws.EClientErrors as _EClientErrors


class HookAccountUpdates(object):
    '''Installs hook to handle EWrapper account update events.

       To install construct an instance passing the wrapper object to hook.

       After installation, your wrapper object will begin handling all the
       EWrapper account update events. At any time you may call the method
       <wrapper>.get_account_updates() to obtain the current account data
       as reported by the TWS application.
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)
        assert hasattr(wrapper,"client")

        self._wrapper = wrapper
        self._snapshot = {}
        self._values = {}
        self._portfolio = {}
        self._timestamp = ""
        self._condition = _threading.Condition()

        wrapper.updateAccountValue = self.updateAccountValue
        wrapper.updatePortfolio = self.updatePortfolio
        wrapper.updateAccountTime = self.updateAccountTime
        wrapper.accountDownloadEnd = self.accountDownloadEnd
        wrapper.get_account_values = self.get_account_values
        wrapper.get_portfolio = self.get_portfolio
        wrapper.get_account_update_time = self.get_account_update_time


    def updateAccountValue(self, key, value, currency, account):
        '''Handler for EWrapper.updateAccountValue() events.

           Installed using tws.helper.HookAccountUpdates(wrapper)
        '''
        assert isinstance(key, str)
        assert isinstance(value, str)
        assert isinstance(currency, str) or (currency is None)
        assert isinstance(account, str)

        with (self._condition):
            try:
                self._values.setdefault(account,{})[key] = (
                    key, value, currency, account)
            finally:
                self._condition.notifyAll()


    def updatePortfolio(self, contract, position, market_price, market_value,
                        average_cost, unrealized_PNL, realized_PNL, account):
        '''Handler for EWrapper.updatePortfolio() events.

           Installed using tws.helper.HookAccountUpdates(wrapper)
        '''
        assert isinstance(contract, __import__("tws").Contract)
        assert isinstance(position, int)
        assert isinstance(market_price, float)
        assert isinstance(market_value, float)
        assert isinstance(average_cost, float)
        assert isinstance(unrealized_PNL, float)
        assert isinstance(realized_PNL, float)
        assert isinstance(account, str)

        with (self._condition):
            try:
                self._portfolio.setdefault(account,{})[contract] = (
                    contract,position,market_price,market_value,average_cost,
                    unrealized_PNL,realized_PNL,account)
            finally:
                self._condition.notifyAll()


    def updateAccountTime(self, timestamp):
        '''Handler for EWrapper.updateAccountTime() events.

           Installed using tws.helper.HookAccountUpdates(wrapper)
        '''
        assert isinstance(timestamp, str)

        with (self._condition):
            try:
                self._timestamp = timestamp
            finally:
                self._condition.notifyAll()


    def accountDownloadEnd(self, account):
        '''Handler for EWrapper.accountDownloadEnd() events.

           Installed using tws.helper.HookAccountUpdates(wrapper)
        '''
        assert isinstance(account, str)

        with (self._condition):
            try:
                self._values.setdefault(account, {})
                self._portfolio.setdefault(account, {})
                self._snapshot[account] = True
            finally:
                self._condition.notifyAll()


    def get_account_values(self, account, wait_until_changed=None, timeout=None):
        '''Gets current value data for a named account.

           This method returns the current account values as reported by the
           TWS application for the account name you specify. It returns a
           dict keyed by strings describing each type of account value. Each
           value is a tuple containing the same values as the arguments that
           would be passed to the EWrapper.updateAccountValue() method.

           Since TWS distinguishes between different accounts by name, you
           must supply a value for the account parameter which matches the
           account you are interested in. This is true even if you only have
           a single account with IB. Note that TWS does not throw an error if
           you supply an incorrect account name, so you will be waiting
           forever for a snapshot if you do that, even if you provided a
           timeout value.

           It is often the case that you will want to wait for the next value
           update. To do this, pass in the the wait_until_changed param the
           dict of values which you consider current for the account. The
           method will block until it receives an update from TWS with an
           updated value. Be careful! By default it will wait forever for an
           update, so you should not wait unless you are certain that TWS will
           deliver an update within a reasonable amount of time. You should
           also be aware that the method will unblock on *any* value update,
           not necessarily the one you happen to be interested in. If you
           like, you may pass in a float timeout value for the maximum seconds
           the method should wait before returning the current values dict
           regardless of whether there was a values update from TWS.

           If you do not pass a dict to the wait_until_changed param, the
           method will not block, and the timeout param is ignored.

           Installed using tws.helper.HookAccountUpdates(wrapper)
        '''
        assert isinstance(account, str)
        assert isinstance(wait_until_changed, dict) or (wait_until_changed is None)
        assert (timeout >= 0) or (timeout is None)

        with (self._condition):
            self._wait_for_snapshot(account, timeout)
            assert isinstance(self._values[account], dict)

            if wait_until_changed != None:
                while self._values[account] == wait_until_changed:
                    self._condition.wait(timeout)
                    if timeout: break
                    
            return self._values[account]


    def get_portfolio(self, account, wait_until_changed=None, timeout=None):
        '''Gets current portfolio data for a named account.

           This method returns the current portfolio as reported by the TWS
           application for the account name you specify. It returns a dict
           keyed by tws.Contract objects describing each position. Each value
           is a tuple containing the same values as the arguments that would
           be passed to the EWrapper.updatePortfolio() method.

           Since TWS distinguishes between different accounts by name, you
           must supply a value for the account parameter which matches the
           account you are interested in. This is true even if you only have
           a single account with IB. Note that TWS does not throw an error if
           you supply an incorrect account name, so you will be waiting
           forever for a snapshot if you do that, even if you provided a
           timeout value.

           Note carefully that the returned dict is keyed on tws.Contract
           objects. To reference such keys, you must supply a contract object
           which evaluates equal to the key object. This may not be exactly
           what you might expect. The Contract objects used to key your
           portfolio will be completely filled in, including fields you might
           consider "optional", such as conId in particular. If the Contract
           object you use is not "equal" according to TWS rules, which means
           your matching Contract objects must be completely filled out, they
           will not match. It is probably safest to iterate through the list
           of portfolio keys to get the actual, fully specified Contract key
           objects for later use if you want to do dict indexing by key.

           It is often the case that you will want to wait for the next
           portfolio update. To do this, pass in the the wait_until_changed
           param the dict of positions which you consider current for the
           account. The  method will block until it receives an update from
           TWS with an updated position. Be careful! By default it will wait
           forever for an update, so you should not wait unless you are
           certain that TWS will deliver an update within a reasonable amount
           of time. You should also be aware that the method will unblock on
           *any* position update, not necessarily the one you happen to be
           interested in. If you like, you may pass in a float timeout value
           for the maximum seconds the method should wait before returning the
           current portfolio dict regardless of whether there was an update
           from TWS.

           If you do not pass a dict to the wait_until_changed param, the
           method will not block, and the timeout param is ignored.

           Installed using tws.helper.HookAccountUpdates(wrapper)
        '''
        assert isinstance(account, str)
        assert isinstance(wait_until_changed, dict) or (wait_until_changed is None)
        assert (timeout >= 0) or (timeout is None)

        with (self._condition):
            self._wait_for_snapshot(account, timeout)
            assert isinstance(self._portfolio[account], dict)

            if wait_until_changed != None:
                while self._portfolio[account] == wait_until_changed:
                    self._condition.wait(timeout)
                    if timeout: break
                    
            return self._portfolio[account]


    def get_account_update_time(self):
        '''Gets timestamp string of last account update.

           This method returns a string with the formatted timestamp of the
           last account update received by TWS. You must have requested
           account updates for at least one account by the reqAccountUpdates()
           method of EClientSocket before any timestamp updates will occur.
           Unlike the other account methods, it does not take an account name.
           The timestamp returned may reflect any account requested. The
           timestamp may be blank if a complete account snapshot has not
           yet been received.

           Installed using tws.helper.HookAccountUpdates(wrapper)
        '''
        if not self._wrapper.client.isConnected():
            raise _EClientErrors.NOT_CONNECTED
        with (self._condition):
            return self._timestamp


    def _wait_for_snapshot(self, account, timeout):
        assert isinstance(account, str)

        # Waits for the full account snapshot to be downloaded. Assumes that
        # updates for the named account have already been requested, and that
        # condition is already acquired by calling method.
        if not self._wrapper.client.isConnected():
            raise _EClientErrors.NOT_CONNECTED

        while not self._snapshot.setdefault(account, False):
            self._condition.wait(timeout)
