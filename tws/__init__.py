'''Python API for Interactive Brokers' Trader Workstation API.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Module imports. Backfill sys.modules for each
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys

import _EClientErrors as EClientErrors
sys.modules.setdefault("tws.EClientErrors", EClientErrors)

import _TickType as TickType
sys.modules.setdefault("tws.TickType", TickType)

import _Util as Util
sys.modules.setdefault("tws.Util", Util)

# Release unneeded references.
del sys


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Class imports.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from tws._ComboLeg import ComboLeg
from tws._Contract import Contract
from tws._EClientSocket import EClientSocket
from tws._EReader import EReader
from tws._Execution import Execution
from tws._ExecutionFilter import ExecutionFilter
from tws._OrderState import OrderState
from tws._TagValue import TagValue
from tws._UnderComp import UnderComp
from tws._EWrapper import EWrapper


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Utility stuff to support package
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def synchronized():
    '''Thread mutex-locking decorator.'''
    def wrapper(callable):
        def inner(*args, **kwds):
            _mutex.acquire()
            try:
                return callable(*args, **kwds)
            finally:
                _mutex.release()
        return inner
    return wrapper

_mutex = __import__("threading").RLock()
