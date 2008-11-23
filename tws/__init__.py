'''Python API for Interactive Brokers' Trader Workstation API.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import sys


from tws import _EClientErrors as EClientErrors
sys.modules.setdefault("tws.EClientErrors", EClientErrors)

from tws import _Util as Util
sys.modules.setdefault("tws.Util", Util)


del sys
