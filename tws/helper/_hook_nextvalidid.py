'''Implements EWrapper hook to handle nextValidId().'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from time import sleep as _sleep
import tws.EClientErrors as _EClientErrors


class HookNextValidId(object):
    '''Installs hook to handle EWrapper.nextValidId() events.

       To install construct an instance passing the wrapper object to hook. 
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)

        self._next_valid_id = _EClientErrors.NO_VALID_ID
        self._wrapper = wrapper
        wrapper.nextValidId = self.nextValidId
        wrapper.get_next_id = self.get_next_id


    def nextValidId(self, id):
        '''Handler for EWrapper.nextValidId event.'''
        with (self._wrapper.client.mutex):
            self._next_valid_id = id


    def get_next_id(self):
        '''Next valid order ID.

           This property contains the current next valid order ID as reported
           by the TWS application. Naturally, TWS has no knowledge of any IDs
           that may be in use by as-yet unsubmitted Order objects. 
        '''
        while True:
            with (self._wrapper.client.mutex):
                id =  self._next_valid_id
                if id != _EClientErrors.NO_VALID_ID:
                    self._next_valid_id = _EClientErrors.NO_VALID_ID
                    self._wrapper.client.reqIds(1)
                    return id
            if not self._wrapper.client.isConnected():
                raise _EClientErrors.NOT_CONNECTED
            _sleep(0.001)
