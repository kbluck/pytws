'''Implements EWrapper hook to handle orderStatus().'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import threading as _threading
import tws.EClientErrors as _EClientErrors


class HookOrderStatus(object):
    '''Installs hook to handle EWrapper.orderStatus() events.

       To install construct an instance passing the wrapper object to hook.
       
       After installation, your wrapper object will begin handling the 
       EWrapper.orderStatus event. At any time you may call the method
       <wrapper>.get_order_status() to obtain the current order status
       as reported by the TWS application. 
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)
        assert hasattr(wrapper,"client")

        self._wrapper = wrapper
        self._order_status = {}
        self._condition = _threading.Condition()

        wrapper.orderStatus = self.orderStatus
        wrapper.get_order_status = self.get_order_status


    def orderStatus(self, order_id, status, filled, remaining, avg_fill_price,
                    perm_id, parent_id, last_fill_price, client_id, why_held):
        '''Handler for EWrapper.orderStatus event.

           Installed using tws.helper.HookOrderStatus(wrapper)
        '''
        with (self._condition):
            try:
                self._order_status[order_id] = (order_id, status, filled,
                           remaining, avg_fill_price, perm_id, parent_id,
                           last_fill_price, client_id, why_held)
            finally:
                self._condition.notifyAll()


    def get_order_status(self, wait_until_changed=None, timeout=None):
        '''Gets current order status.

           This method returns the the current order status as reported by
           the TWS application. It returns a dict keyed by order ID and
           with values being tuples containing the same values as the
           arguments that would be passed to the EWrapper.orderStatus()
           method.
           
           It is often the case that you will want to wait for the order
           status to change. To do this, pass in the the wait_until_changed
           param the dict of order statuses which you consider current.
           The method will block until it received an update from TWS with
           an updated order status. Be careful! By default it will wait
           forever for an update, so you should not wait unless you are
           certain that TWS will deliver an order status update within a
           reasonable amount of time. If you like, you may pass in a float
           timeout value for the maximum seconds it should wait before
           returning the current order status dict regardless of whether
           there was an update from TWS.
           
           If you do not pass a dict to the wait_until_changed param, the
           method will not block, and the timeout param is ignored.

           Installed using tws.helper.HookOrderStatus(wrapper)
        '''
        assert isinstance(wait_until_changed, dict) or (wait_until_changed is None)
        assert (timeout >= 0) or (timeout is None)

        if not self._wrapper.client.isConnected():
            raise _EClientErrors.NOT_CONNECTED
        with (self._condition):
            if wait_until_changed != None:
                if self._order_status == wait_until_changed:
                    self._condition.wait(timeout)
            return self._order_status.copy()
