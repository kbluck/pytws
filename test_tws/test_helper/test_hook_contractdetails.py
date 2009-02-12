'''Unit test package for module "tws.helper._hook_contractdetails".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
from tws.helper import HookContractDetails


class test_helper_HookContractDetails(unittest.TestCase):
    '''Test type "tws.helper.HookContractDetails"'''

    def setUp(self):
        self.wrapper = tws.EWrapper()

    def test_init(self):
        self.assertTrue(HookContractDetails(tws.EWrapper()))

    def test_hook(self):
        self.assertFalse(self.wrapper.__dict__.get("contractDetails", None))
        self.assertFalse(self.wrapper.__dict__.get("contractDetailsEnd", None))
        self.assertFalse(self.wrapper.__dict__.get("get_contract_details", None))
        HookContractDetails(self.wrapper)
        self.assertTrue(self.wrapper.__dict__.get("contractDetails", None))
        self.assertTrue(self.wrapper.__dict__.get("contractDetailsEnd", None))
        self.assertTrue(self.wrapper.__dict__.get("get_contract_details", None))
