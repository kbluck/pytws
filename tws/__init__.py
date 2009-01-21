'''Python API for Interactive Brokers" Trader Workstation API.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Utility stuff to support package
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def synchronized(f):
    '''Thread mutex-locking decorator.'''

    assert  (__import__("inspect").getargspec(f)[0][0] == "self")

    def _synchronized_call(self, *args, **kwds):
        assert hasattr(self, "_mutex")
        
        self._mutex.acquire()
        try:
            return f(self, *args, **kwds)
        finally:
            self._mutex.release()

    return _synchronized_call


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
from tws._ContractDetails import ContractDetails
from tws._EClientSocket import EClientSocket
from tws._EReader import EReader
from tws._Execution import Execution
from tws._ExecutionFilter import ExecutionFilter
from tws._Order import Order
from tws._OrderState import OrderState
from tws._ScannerSubscription import ScannerSubscription
from tws._TagValue import TagValue
from tws._UnderComp import UnderComp
from tws._EWrapper import EWrapper
