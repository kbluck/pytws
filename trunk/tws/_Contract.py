'''Contract data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from tws import Util as _Util


class Contract(object):
    '''Data structure with attributes to describe a tradeable contract.
    '''

    def __init__(self, con_id=0, symbol="", sec_type="", expiry="", strike=0.0,
                       right="", multiplier="", exchange="", currency="",
                       local_symbol="", combo_legs=[], primary_exch="",
                       include_expired=False, sec_id_type="", sec_id=""):
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
        self.m_primaryExch = primary_exch #pick a non-aggregate (ie not the SMART exchange) exchange that the contract trades on.  DO NOT SET TO SMART.
        self.m_includeExpired = include_expired #can not be set to true for orders.
	self.m_secIdType = sec_id_type #CUSIP;SEDOL;ISIN;RIC
	self.m_secId = sec_id

        # Combos
        self.m_comboLegs = combo_legs
        self.m_comboLegsDescrip = "" #received in open order version 14 and up for all combos

        # delta neutrals
        self.m_underComp = None;


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        if (
            (self.m_conId != other.m_conId) or
            (self.m_secType.lower() != other.m_secType.lower()) or
            (self.m_symbol.lower() != other.m_symbol.lower()) or
            (self.m_exchange.lower() != other.m_exchange.lower()) or
            (self.m_primaryExch.lower() != other.m_primaryExch.lower()) or
            (self.m_currency.lower() != other.m_currency.lower())):
            return False
        if self.m_secType != "BOND":
            if (
                (self.m_strike != other.m_strike) or
                (self.m_expiry.lower() != other.m_expiry.lower()) or
                (self.m_right.lower() != other.m_right.lower()) or
                (self.m_multiplier.lower() != other.m_multiplier.lower()) or
                (self.m_localSymbol.lower() != other.m_localSymbol.lower()) or
		(self.m_secIdType.lower() != other.m_secIdType.lower()) or
		(self.m_secId.lower() != other.m_secId.lower())):
                return False
        if not (self.m_underComp == other.m_underComp):
            return False
        if not _Util.VectorEqualsUnordered(self.m_comboLegs, other.m_comboLegs):
            return False
        return True


    def __hash__(self):
        return hash(self.m_symbol)
