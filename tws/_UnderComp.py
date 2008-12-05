'''UnderComp data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class UnderComp(object):
    '''Data structure with information to help build a delta-neutral
       combination of contracts.
    '''

    def __init__(self):
        self.m_conId = 0
        self.m_delta = 0.0
        self.m_price = 0.0


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        return True if (
            (self.m_conId == other.m_conId) and
            (self.m_delta == other.m_delta) and
            (self.m_price == other.m_price)
        ) else False
