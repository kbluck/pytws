'''TagValue data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class TagValue(object):
    '''Tag/Value pair data structure.
    
       Used to pass parameters for Algo orders.
    '''

    def __init__(self, tag="", value=""):
        self.m_tag = tag
        self.m_value = value


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        return True if (
            (self.m_tag == other.m_tag) and
            (self.m_value == other.m_value)
        ) else False
