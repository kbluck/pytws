'''Unit test package for module "tws.helper._hook_orderstatus".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
from tws.helper import HookOrderStatus


class test_helper_HookOrderStatus(unittest.TestCase):
    '''Test type "tws.helper.HookOrderStatus"'''

    def setUp(self):
        self.wrapper = tws.EWrapper()

    def test_init(self):
        self.assertTrue(HookOrderStatus(tws.EWrapper()))

    def test_hook(self):         
        self.assertFalse(self.wrapper.__dict__.get("orderStatus", None))
        self.assertFalse(self.wrapper.__dict__.get("get_order_status", None))
        HookOrderStatus(self.wrapper)
        self.assertTrue(self.wrapper.__dict__.get("orderStatus", None))
        self.assertTrue(self.wrapper.__dict__.get("get_order_status", None))
