'''Unit test package for module "tws.helper._hook_currenttime".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
from tws.helper import HookCurrentTime


class test_helper_HookCurrentTime(unittest.TestCase):
    '''Test type "tws.helper.HookCurrentTime"'''

    def setUp(self):
        self.wrapper = tws.EWrapper()

    def test_init(self):
        self.assertTrue(HookCurrentTime(tws.EWrapper()))

    def test_hook(self):
        self.assertFalse(self.wrapper.__dict__.get("currentTime", None))
        self.assertFalse(self.wrapper.__dict__.get("get_current_time", None))
        HookCurrentTime(self.wrapper)
        self.assertTrue(self.wrapper.__dict__.get("currentTime", None))
        self.assertTrue(self.wrapper.__dict__.get("get_current_time", None))
