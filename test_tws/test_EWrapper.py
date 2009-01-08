'''Unit test package for module "tws._EWrapper".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import EWrapper


# Local classes required to test EWrapper
class _wrapper(EWrapper):
    pass


class test_EWrapper(unittest.TestCase):
    '''Test class "tws.EWrapper"'''

    def setUp(self):
        self.wrapper = _wrapper()
