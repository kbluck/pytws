'''Unit test package for module "tws.helper._hook_accountupdates".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
from tws.helper import HookAccountUpdates


class test_helper_HookAccountUpdates(unittest.TestCase):
    '''Test type "tws.helper.HookAccountUpdates"'''

    def setUp(self):
        self.wrapper = tws.EWrapper()

    def test_init(self):
        self.assertTrue(HookAccountUpdates(tws.EWrapper()))

    def test_hook(self):
        self.assertFalse(self.wrapper.__dict__.get("updateAccountValue", None))
        self.assertFalse(self.wrapper.__dict__.get("updatePortfolio", None))
        self.assertFalse(self.wrapper.__dict__.get("updateAccountTime", None))
        self.assertFalse(self.wrapper.__dict__.get("accountDownloadEnd", None))
        self.assertFalse(self.wrapper.__dict__.get("get_account_values", None))
        self.assertFalse(self.wrapper.__dict__.get("get_portfolio", None))
        self.assertFalse(self.wrapper.__dict__.get("get_account_update_time", None))
        HookAccountUpdates(self.wrapper)
        self.assertTrue(self.wrapper.__dict__.get("updateAccountValue", None))
        self.assertTrue(self.wrapper.__dict__.get("updatePortfolio", None))
        self.assertTrue(self.wrapper.__dict__.get("updateAccountTime", None))
        self.assertTrue(self.wrapper.__dict__.get("accountDownloadEnd", None))
        self.assertTrue(self.wrapper.__dict__.get("get_account_values", None))
        self.assertTrue(self.wrapper.__dict__.get("get_portfolio", None))
        self.assertTrue(self.wrapper.__dict__.get("get_account_update_time", None))
