'''Implements EWrapper hook to handle nextValidId().'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import threading as _threading
import tws.EClientErrors as _EClientErrors


class HookNextValidId(object):
    '''Installs hook to handle EWrapper.nextValidId() events.

       To install construct an instance passing the wrapper object to hook.

       After installation, your wrapper object will begin handling the
       EWrapper.nextValidId event. At any time you may call the method
       <wrapper>.get_next_id() to obtain the next valid order id as
       reported by the TWS application.
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)
        assert hasattr(wrapper,"client")

        self._wrapper = wrapper
        self._next_valid_id = _EClientErrors.NO_VALID_ID
        self._condition = _threading.Condition()

        wrapper.nextValidId = self.nextValidId
        wrapper.get_next_id = self.get_next_id


    def nextValidId(self, id):
        '''Handler for EWrapper.nextValidId event.

           Installed using tws.helper.HookNextValidId(wrapper)
        '''
        with (self._condition):
            try:
                self._next_valid_id = id
            finally:
                self._condition.notifyAll()


    def get_next_id(self):
        '''Next valid order ID.

           This method returns the current next valid order ID as reported
           by the TWS application. Naturally, TWS has no knowledge of any IDs
           that may be in use by as-yet unsubmitted Order objects.

           Installed using tws.helper.HookNextValidId(wrapper)
        '''
        if not self._wrapper.client.isConnected():
            raise _EClientErrors.NOT_CONNECTED
        with (self._condition):
            if self._next_valid_id == _EClientErrors.NO_VALID_ID:
                self._condition.wait()
            id = self._next_valid_id
            self._next_valid_id = _EClientErrors.NO_VALID_ID
            self._wrapper.client.reqIds(1)
            return id
