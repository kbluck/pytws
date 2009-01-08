'''ContractDetails data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from tws import Contract as _contract_factory


class ContractDetails(object):
    '''Data structure with attributes used to describe contract details,
       including bond information.
    '''

    def __init__(self, summary=_contract_factory(), market_name="", trading_class="",
                 min_tick=0.0, order_types="", valid_exchanges="", under_con_id=0):
        self.m_summary = summary
        self.m_marketName = market_name
        self.m_tradingClass = trading_class
        self.m_minTick = min_tick
        self.m_orderTypes = order_types
        self.m_validExchanges = valid_exchanges
        self.m_underConId = under_con_id

        # Non-parameterized
        self.m_cusip = ""
        self.m_ratings = ""
        self.m_descAppend = ""
        self.m_bondType = ""
        self.m_couponType = ""
        self.m_callable = False
        self.m_putable = False
        self.m_coupon = 0
        self.m_convertible = False
        self.m_maturity = ""
        self.m_issueDate = ""
        self.m_nextOptionDate = ""
        self.m_nextOptionType = ""
        self.m_nextOptionPartial = False
        self.m_notes = ""


    def __eq__(self, other):  # Not in Java source. IB bug?
        if not isinstance(other, self.__class__): return False
        return True if (
            (self.m_summary == other.m_summary) and
            (self.m_marketName == other.m_marketName) and
            (self.m_tradingClass == other.m_tradingClass) and
            (self.m_minTick == other.m_minTick) and
            (self.m_orderTypes == other.m_orderTypes) and
            (self.m_validExchanges == other.m_validExchanges) and
            (self.m_underConId == other.m_underConId) and
            (self.m_cusip == other.m_cusip) and
            (self.m_ratings == other.m_ratings) and
            (self.m_descAppend == other.m_descAppend) and
            (self.m_bondType == other.m_bondType) and
            (self.m_couponType == other.m_couponType) and
            (self.m_callable == other.m_callable) and
            (self.m_putable == other.m_putable) and
            (self.m_coupon == other.m_coupon) and
            (self.m_convertible == other.m_convertible) and
            (self.m_maturity == other.m_maturity) and
            (self.m_issueDate == other.m_issueDate) and
            (self.m_nextOptionDate == other.m_nextOptionDate) and
            (self.m_nextOptionType == other.m_nextOptionType) and
            (self.m_nextOptionPartial == other.m_nextOptionPartial) and
            (self.m_notes == other.m_notes)
        ) else False
