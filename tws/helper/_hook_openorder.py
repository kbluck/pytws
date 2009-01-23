'''Implements EWrapper hook to handle openOrder() and and openOrderEnd().'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import threading as _threading


class HookOpenOrder(object):
    '''Installs hook to handle EWrapper.openOrder() events.

       To install construct an instance passing the wrapper object to hook.

       After installation, your wrapper object will begin handling the
       EWrapper.openOrder and openOrderEnd events. At any time you may
       call the method <wrapper>.get_open_orders() to obtain a dict of
       the currently open orders as reported by TWS.
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)
        assert hasattr(wrapper,"client")

        self._wrapper = wrapper
        self._condition = _threading.Condition()
        self._open_orders = None

        wrapper.openOrder = self.openOrder
        wrapper.openOrderEnd = self.openOrderEnd
        wrapper.get_open_orders = self.get_open_orders


    def openOrder(self, order_id, contract, order, order_state):
        '''Handler for EWrapper.openOrder event.

           Installed using tws.helper.HookOpenOrder(wrapper)
        '''
        with (self._condition):
            if self._open_orders != None:
                self._open_orders[order_id] = (contract, order, order_state)


    def openOrderEnd(self):
        '''Handler for EWrapper.openOrderEnd event.

           Installed using tws.helper.HookOpenOrder(wrapper)
        '''
        with (self._condition):
            if self._open_orders != None:
                self._condition.notifyAll()


    def get_open_orders(self):
        '''Get set of currently open orders.

           This method returns a dict containing the current set of open
           orders as reported by TWS. The dict is indexed by Order ID and
           each entry's value is a tuple of the associated Contract, Order,
           and OrderState objects.

           Note that TWS will not report an order as "open" until it has
           finished transmitting and received confirmation of the order from
           IB, so if you call get_open_orders() immediately after calling
           placeOrder(), you probably won't see the order you just placed
           right away. If you wait a bit, it will show up once TWS confirms
           it as opened.

           Installed using tws.helper.HookOpenOrder(wrapper)
        '''
        if not self._wrapper.client.isConnected():
            raise _EClientErrors.NOT_CONNECTED
        with (self._condition):
            assert self._open_orders is None

            self._open_orders = {}
            self._wrapper.client.reqOpenOrders()
            self._condition.wait()
            result = self._open_orders
            self._open_orders = None
            return result
