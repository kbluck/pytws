'''Unit test package for module "tws.helper._hook_ticks".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
from tws.helper import HookTicks


class test_helper_HookTicks(unittest.TestCase):
    '''Test type "tws.helper.HookTicks"'''

    def setUp(self):
        self.wrapper = tws.EWrapper()

    def test_init(self):
        self.assertTrue(HookTicks(tws.EWrapper()))

    def test_hook(self):
        self.assertFalse(self.wrapper.__dict__.get("tickPrice", None))
        self.assertFalse(self.wrapper.__dict__.get("tickSize", None))
        self.assertFalse(self.wrapper.__dict__.get("tickOptionComputation", None))
        self.assertFalse(self.wrapper.__dict__.get("tickGeneric", None))
        self.assertFalse(self.wrapper.__dict__.get("tickString", None))
        self.assertFalse(self.wrapper.__dict__.get("tickEFP", None))
        self.assertFalse(self.wrapper.__dict__.get("get_ticks", None))
        HookTicks(self.wrapper)
        self.assertTrue(self.wrapper.__dict__.get("tickPrice", None))
        self.assertTrue(self.wrapper.__dict__.get("tickSize", None))
        self.assertTrue(self.wrapper.__dict__.get("tickOptionComputation", None))
        self.assertTrue(self.wrapper.__dict__.get("tickGeneric", None))
        self.assertTrue(self.wrapper.__dict__.get("tickString", None))
        self.assertTrue(self.wrapper.__dict__.get("tickEFP", None))
        self.assertTrue(self.wrapper.__dict__.get("get_ticks", None))
