'''Implements EWrapper hook to handle currentTime().'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import threading as _threading
import tws.EClientErrors as _EClientErrors


class HookCurrentTime(object):
    '''Installs hook to handle EWrapper.currentTime() events.

       To install construct an instance passing the wrapper object to hook.

       After installation, your wrapper object will begin handling the
       EWrapper.currentTime event. At any time you may call the method
       <wrapper>.get_current_time() to obtain the current server time as
       reported by the TWS application.
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)
        assert hasattr(wrapper,"client")

        self._wrapper = wrapper
        self._current_time = -1
        self._condition = _threading.Condition()

        wrapper.currentTime = self.currentTime
        wrapper.get_current_time = self.get_current_time


    def currentTime(self, time):
        '''Handler for EWrapper.currentTime event.

           Installed using tws.helper.HookCurrentTime(wrapper)
        '''
        with (self._condition):
            try:
                self._current_time = time
            finally:
                self._condition.notifyAll()


    def get_current_time(self):
        '''Current IB server time.

           This method returns the current system time as reported by the
           TWS application. TWS reports time as an integer number of seconds
           since the epoch (January 1st, 1970 at one minute after midnight)
           in the standard Unix fashion. You can convert it to more useful
           time values using the time module (ctime(), gmtime(), localtime())
           or the datetime module.
           
           Ex: time.strftime('%c',time.localtime(wrapper.get_current_time()))

           Installed using tws.helper.HookCurrentTime(wrapper)
        '''
        if not self._wrapper.client.isConnected():
            raise _EClientErrors.NOT_CONNECTED
        with (self._condition):
            self._wrapper.client.reqCurrentTime()
            self._condition.wait()
            return self._current_time
