'''Useful EWrapper subclasses.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from Queue import Queue
from tws import EWrapper


class QueueWrapper(Queue, EWrapper):

    _queue_type = Queue

    def __init__(self):
        super(QueueWrapper, self).__init__()


    def _put_wrapper_call(self, method_name, *args, **kwds):
        QueueWrapper._queue_type.put(self, item=(method_name, args, kwds),
                                     block=False, timeout=None)


    def put(self, *args, **kwds):
        '''Superclass method 'put' is not implemented.'''
        raise NotImplementedError

    
    def put_nowait(self, *args, **kwds):
        '''Superclass method 'put_nowait' is not implemented.'''
        raise NotImplementedError


class SynchronizedWrapper(EWrapper):
    pass


del EWrapper
del Queue
