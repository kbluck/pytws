'''Implements EWrapper subclass QueueWrapper.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from Queue import Queue
from tws import EWrapper


class QueueWrapper(Queue, EWrapper):

    def __init__(self):
        super(QueueWrapper, self).__init__()


    if __debug__: # Assert structure of items put into Queue
        _queue_type = Queue

        def _put(self, item):
            assert type(item) == tuple
            assert len(item) == 2
            assert type(item[0]) == str
            assert type(item[1]) == dict

            QueueWrapper._queue_type._put(self, item)


    def _put_wrapper_call(self, method_name, **kwds):
        self.put(item=(method_name, kwds), block=False, timeout=None)


    def error(self, e):
        self._put_wrapper_call("error", e=e)


    def connectionClosed(self):
        self._put_wrapper_call("connectionClosed")


del EWrapper
del Queue
