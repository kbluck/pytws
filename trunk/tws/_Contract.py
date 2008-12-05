'''Contract data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from tws import Util as _Util


class Contract(object):
    '''Data structure with attributes to describe a tradeable contract.
    '''

    def __init__(self, con_id=0, symbol='', sec_type='', expiry='', strike=0.0,
                       right='', multiplier='', exchange='', currency='',
                       local_symbol="", combo_legs=[], primary_exch="",
                       include_expired=False):
        self.m_conId = con_id
        self.m_symbol = symbol
        self.m_secType = sec_type
        self.m_expiry = expiry
        self.m_strike = strike
        self.m_right = right
        self.m_multiplier = multiplier
        self.m_exchange = exchange
        self.m_currency = currency
        self.m_localSymbol = local_symbol
        self.m_primaryExch = primary_exch
        self.m_includeExpired = include_expired

        # Combos
        self.m_comboLegs = combo_legs
        self.m_comboLegsDescrip = ''
    
        # delta neutrals
        self.m_underComp = self._undercomp_factory();


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        if (
            (self.m_conId != other.m_conId) or
            (self.m_secType != other.m_secType) or
            (self.m_symbol != other.m_symbol) or
            (self.m_exchange != other.m_exchange) or
            (self.m_primaryExch != other.m_primaryExch) or
            (self.m_currency != other.m_currency)):
            return False
        if self.m_secType != "BOND":
            if (
                (self.m_strike != other.m_strike) or
                (self.m_expiry != other.m_expiry) or
                (self.m_right != other.m_right) or
                (self.m_multiplier != other.m_multiplier) or
                (self.m_localSymbol != other.m_localSymbol)):
                return False
        if not (self.m_underComp == other.m_underComp):
            return False
        if not _Util.VectorEqualsUnordered(self.m_comboLegs, other.m_comboLegs):
            return False
        return True


    from tws._UnderComp import UnderComp as _undercomp_factory
