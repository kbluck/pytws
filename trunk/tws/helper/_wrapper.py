'''Useful EWrapper subclasses.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from Queue import Queue
from tws import EWrapper


class QueueWrapper(Queue, EWrapper):
    
    def __init__(self):
        super(QueueWrapper, self).__init__()


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
