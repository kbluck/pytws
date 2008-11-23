'''Unit test package for module "tws._EClientSocket".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import EClientSocket


class test_EClientSocket(unittest.TestCase):
    '''Test class "tws.EClientSocket"'''

    def test_init(self):
        self.assertTrue(EClientSocket())
