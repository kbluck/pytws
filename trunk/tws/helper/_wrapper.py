'''Useful EWrapper subclasses.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from tws import EWrapper

class QueueWrapper(EWrapper):
    pass


class SynchronizedWrapper(EWrapper):
    pass


del EWrapper
