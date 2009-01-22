'''Unit test package for module "tws.helper._hook_nextvalidid".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
from tws.helper import HookNextValidId


class test_helper_HookNextValidId(unittest.TestCase):
    '''Test type "tws.helper.HookNextValidId"'''

    def setUp(self):
        self.wrapper = tws.EWrapper()

    def test_init(self):
        self.assertTrue(HookNextValidId(tws.EWrapper()))

    def test_hook(self):         
        self.assertFalse(self.wrapper.__dict__.get("nextValidId", None))
        self.assertFalse(self.wrapper.__dict__.get("get_next_id", None))
        HookNextValidId(self.wrapper)
        self.assertTrue(self.wrapper.__dict__.get("nextValidId", None))
        self.assertTrue(self.wrapper.__dict__.get("get_next_id", None))
