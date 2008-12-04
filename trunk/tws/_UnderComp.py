'''UnderComp data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class UnderComp(object):
    '''Data structure with information about a delta-neutral combination of contracts.'''
    def __init__(self):
        self.m_conId = 0
        self.m_delta = 0.0
        self.m_price = 0.0


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        if (self.m_conId != other.m_conId): return False
        if (self.m_delta != other.m_delta): return False
        if (self.m_price != other.m_price): return False
        return True
