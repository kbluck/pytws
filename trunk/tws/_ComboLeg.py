'''ComboLeg data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class ComboLeg(object):
    '''Data structure containing attributes to describe individual legs of
       combination orders.
    '''

    def __init__(self, con_id=0, ratio=0, action="", exchange="", open_close=0, 
                       short_sale_slot=0, designated_location=""):
        self.m_conId = con_id
        self.m_ratio = ratio
        self.m_action = action
        self.m_exchange = exchange
        self.m_openClose = open_close
        self.m_shortSaleSlot = short_sale_slot
        self.m_designatedLocation = designated_location


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        return True if (
            (self.m_conId == other.m_conId) and
            (self.m_ratio == other.m_ratio) and
            (self.m_action.lower() == other.m_action.lower()) and
            (self.m_exchange.lower() == other.m_exchange.lower()) and
            (self.m_openClose == other.m_openClose) and
            (self.m_shortSaleSlot == other.m_shortSaleSlot) and
            (self.m_designatedLocation.lower() == other.m_designatedLocation.lower())
        ) else False


    # ComboLeg constants
    SAME = 0
    OPEN = 1
    CLOSE = 2
    UNKNOWN = 3
