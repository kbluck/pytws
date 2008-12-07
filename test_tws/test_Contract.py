'''Unit test package for module "tws._Contract".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import Contract, ComboLeg, UnderComp


class test_Contract(unittest.TestCase):
    '''Test type "tws.Contract"'''

    def test_init(self):
        test1 = Contract()
        test2 = Contract(1, "ab", "cd", "ef", 2.5, "gh", "ij", "kl",
                         "mn", "op", [ComboLeg()], "qr", True)
    
        self.assertEqual(test1.m_conId, 0)
        self.assertEqual(test1.m_symbol, "")
        self.assertEqual(test1.m_secType, "")
        self.assertEqual(test1.m_expiry, "")
        self.assertEqual(test1.m_strike, 0.0)
        self.assertEqual(test1.m_right, "")
        self.assertEqual(test1.m_multiplier, "")
        self.assertEqual(test1.m_exchange, "")
        self.assertEqual(test1.m_currency, "")
        self.assertEqual(test1.m_localSymbol, "")
        self.assertEqual(test1.m_comboLegs, [])
        self.assertEqual(test1.m_primaryExch, "")
        self.assertEqual(test1.m_includeExpired, False)
        self.assertEqual(test1.m_comboLegsDescrip, "")
        self.assertEqual(test1.m_underComp, UnderComp())

        self.assertEqual(test2.m_conId, 1)
        self.assertEqual(test2.m_symbol, "ab")
        self.assertEqual(test2.m_secType, "cd")
        self.assertEqual(test2.m_expiry, "ef")
        self.assertEqual(test2.m_strike, 2.5)
        self.assertEqual(test2.m_right, "gh")
        self.assertEqual(test2.m_multiplier, "ij")
        self.assertEqual(test2.m_exchange, "kl")
        self.assertEqual(test2.m_currency, "mn")
        self.assertEqual(test2.m_localSymbol, "op")
        self.assertEqual(test2.m_comboLegs, [ComboLeg()])
        self.assertEqual(test2.m_primaryExch, "qr")
        self.assertEqual(test1.m_comboLegsDescrip, "")
        self.assertEqual(test1.m_underComp, UnderComp())

    def test_fields(self):
        test = Contract()

        test.m_conId = 1
        test.m_symbol = "ab"
        test.m_secType = "cd"
        test.m_expiry = "ef"
        test.m_strike = 2.5
        test.m_right = "gh"
        test.m_multiplier = "ij"
        test.m_exchange = "kl"
        test.m_currency = "mn"
        test.m_localSymbol = "op"
        test.m_comboLegs = [ComboLeg()]
        test.m_primaryExch = "qr"
        test.m_comboLegsDescrip = "st"
        test.m_underComp = UnderComp()

        self.assertEqual(test.m_conId, 1)
        self.assertEqual(test.m_symbol, "ab")
        self.assertEqual(test.m_secType, "cd")
        self.assertEqual(test.m_expiry, "ef")
        self.assertEqual(test.m_strike, 2.5)
        self.assertEqual(test.m_right, "gh")
        self.assertEqual(test.m_multiplier, "ij")
        self.assertEqual(test.m_exchange, "kl")
        self.assertEqual(test.m_currency, "mn")
        self.assertEqual(test.m_localSymbol, "op")
        self.assertEqual(test.m_comboLegs, [ComboLeg()])
        self.assertEqual(test.m_primaryExch, "qr")
        self.assertEqual(test.m_comboLegsDescrip, "st")
        self.assertEqual(test.m_underComp, UnderComp())

    def test_equals(self):
        test1 = Contract()
        test2 = Contract()
        test3 = Contract(1, "ab", "cd", "ef", 2.5, "gh", "ij", "kl",
                         "mn", "op", [ComboLeg()], "qr", True)
        
        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)
