'''Unit test package for module "tws.helper._synchronizedwrapper".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import EWrapper
from tws.helper import SynchronizedWrapper


class test_SynchronizedWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = SynchronizedWrapper() 

    def test_init(self):
        self.assertTrue(isinstance(SynchronizedWrapper(), EWrapper))
