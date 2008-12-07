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
