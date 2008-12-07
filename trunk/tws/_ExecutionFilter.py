'''ExecutionFilter data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class ExecutionFilter(object):
    '''Data structure containing attributes to describe execution filter
       criteria.
    '''

    def __init__(self, client_id=0, acct_code="", time="", symbol="", 
                       sec_type="", exchange="", side=""):
        self.m_clientId = client_id
        self.m_acctCode = acct_code
        self.m_time = time
        self.m_symbol = symbol
        self.m_secType = sec_type
        self.m_exchange = exchange
        self.m_side = side


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        return True if (
            (self.m_clientId == other.m_clientId) and 
            (self.m_acctCode.lower() == other.m_acctCode.lower()) and
            (self.m_time.lower() == other.m_time.lower()) and
            (self.m_symbol.lower() == other.m_symbol.lower()) and
            (self.m_secType.lower() == other.m_secType.lower()) and
            (self.m_exchange.lower() == other.m_exchange.lower()) and
            (self.m_side.lower() == other.m_side.lower())
        ) else False
