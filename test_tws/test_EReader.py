'''Unit test package for module "tws._EReader".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import EReader


# Local classes required to test EReader
class _reader(EReader):
    pass


class test_EReader(unittest.TestCase):
    '''Test class "tws.EReader"'''
    
    def setUp(self):
        self.reader = _reader()
