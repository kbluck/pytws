'''Unit test package for module "tws._ContractDetails".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import ContractDetails, Contract


class test_ContractDetails(unittest.TestCase):
    '''Test type "tws.ContractDetails"'''

    def test_init(self):
        test1 = ContractDetails()
        test2 = ContractDetails(Contract(), "ab", "cd", 1.5, "ef", "gh", 2)

        self.assertEqual(test1.m_summary, Contract())
        self.assertEqual(test1.m_marketName, "")
        self.assertEqual(test1.m_tradingClass, "")
        self.assertEqual(test1.m_minTick, 0.0)
        self.assertEqual(test1.m_orderTypes, "")
        self.assertEqual(test1.m_validExchanges, "")
        self.assertEqual(test1.m_underConId, 0)
        self.assertEqual(test1.m_cusip, "")
        self.assertEqual(test1.m_ratings, "")
        self.assertEqual(test1.m_descAppend, "")
        self.assertEqual(test1.m_bondType, "")
        self.assertEqual(test1.m_couponType, "")
        self.assertEqual(test1.m_callable, False)
        self.assertEqual(test1.m_putable, False)
        self.assertEqual(test1.m_coupon, 0)
        self.assertEqual(test1.m_convertible, False)
        self.assertEqual(test1.m_maturity, "")
        self.assertEqual(test1.m_issueDate, "")
        self.assertEqual(test1.m_nextOptionDate, "")
        self.assertEqual(test1.m_nextOptionType, "")
        self.assertEqual(test1.m_nextOptionPartial, False)
        self.assertEqual(test1.m_notes, "")

        self.assertEqual(test2.m_summary, Contract())
        self.assertEqual(test2.m_marketName, "ab")
        self.assertEqual(test2.m_tradingClass, "cd")
        self.assertEqual(test2.m_minTick, 1.5)
        self.assertEqual(test2.m_orderTypes, "ef")
        self.assertEqual(test2.m_validExchanges, "gh")
        self.assertEqual(test2.m_underConId, 2)
        self.assertEqual(test2.m_cusip, "")
        self.assertEqual(test2.m_ratings, "")
        self.assertEqual(test2.m_descAppend, "")
        self.assertEqual(test2.m_bondType, "")
        self.assertEqual(test2.m_couponType, "")
        self.assertEqual(test2.m_callable, False)
        self.assertEqual(test2.m_putable, False)
        self.assertEqual(test2.m_coupon, 0)
        self.assertEqual(test2.m_convertible, False)
        self.assertEqual(test2.m_maturity, "")
        self.assertEqual(test2.m_issueDate, "")
        self.assertEqual(test2.m_nextOptionDate, "")
        self.assertEqual(test2.m_nextOptionType, "")
        self.assertEqual(test2.m_nextOptionPartial, False)
        self.assertEqual(test2.m_notes, "")

    def test_fields(self):
        test = ContractDetails()

        test.m_summary = Contract()
        test.m_marketName = "ab"
        test.m_tradingClass = "cd"
        test.m_minTick = 1.5
        test.m_orderTypes = "ef"
        test.m_validExchanges = "gh"
        test.m_underConId = 2
        test.m_cusip = "ij"
        test.m_ratings = "kl"
        test.m_descAppend = "mn"
        test.m_bondType = "op"
        test.m_couponType = "qr"
        test.m_callable = True
        test.m_putable = True
        test.m_coupon = 3
        test.m_convertible = True
        test.m_maturity = "st"
        test.m_issueDate = "uv"
        test.m_nextOptionDate = "wx"
        test.m_nextOptionType = "yz"
        test.m_nextOptionPartial = True
        test.m_notes = "az"

        self.assertEqual(test.m_summary, Contract())
        self.assertEqual(test.m_marketName, "ab")
        self.assertEqual(test.m_tradingClass, "cd")
        self.assertEqual(test.m_minTick, 1.5)
        self.assertEqual(test.m_orderTypes, "ef")
        self.assertEqual(test.m_validExchanges, "gh")
        self.assertEqual(test.m_underConId, 2)
        self.assertEqual(test.m_cusip, "ij")
        self.assertEqual(test.m_ratings, "kl")
        self.assertEqual(test.m_descAppend, "mn")
        self.assertEqual(test.m_bondType, "op")
        self.assertEqual(test.m_couponType, "qr")
        self.assertEqual(test.m_callable, True)
        self.assertEqual(test.m_putable, True)
        self.assertEqual(test.m_coupon, 3)
        self.assertEqual(test.m_convertible, True)
        self.assertEqual(test.m_maturity, "st")
        self.assertEqual(test.m_issueDate, "uv")
        self.assertEqual(test.m_nextOptionDate, "wx")
        self.assertEqual(test.m_nextOptionType, "yz")
        self.assertEqual(test.m_nextOptionPartial, True)
        self.assertEqual(test.m_notes, "az")

    def test_equals(self):
        test1 = ContractDetails()
        test2 = ContractDetails()
        test3 = ContractDetails(Contract(), "ab", "cd", 1.5, "ef", "gh", 2)

        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)
