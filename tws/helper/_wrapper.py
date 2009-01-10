'''Useful EWrapper subclasses.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from Queue import Queue
from tws import EWrapper


class QueueWrapper(Queue, EWrapper):

    def __init__(self):
        super(QueueWrapper, self).__init__()


class SynchronizedWrapper(EWrapper):
    pass


del EWrapper
del Queue
