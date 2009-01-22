'''Unit test package for module "tws.helper._hook_openorder".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
from tws.helper import HookOpenOrder


class test_helper_HookOpenOrder(unittest.TestCase):
    '''Test type "tws.helper.HookOpenOrder"'''

    def setUp(self):
        self.wrapper = tws.EWrapper()

    def test_init(self):
        self.assertTrue(HookOpenOrder(tws.EWrapper()))

    def test_hook(self):         
        self.assertFalse(self.wrapper.__dict__.get("openOrder", None))
        self.assertFalse(self.wrapper.__dict__.get("openOrderEnd", None))
        self.assertFalse(self.wrapper.__dict__.get("get_open_orders", None))
        HookOpenOrder(self.wrapper)
        self.assertTrue(self.wrapper.__dict__.get("openOrder", None))
        self.assertTrue(self.wrapper.__dict__.get("openOrderEnd", None))
        self.assertTrue(self.wrapper.__dict__.get("get_open_orders", None))
