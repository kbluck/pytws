'''Unit test package for module "tws._OrderState".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import OrderState


class test_OrderState(unittest.TestCase):
    '''Test type "tws.OrderState"'''

    def test_init(self):
        test1 = OrderState()
        test2 = OrderState("ab", "cd", "ef", "gh", 3.5, 4.5, 5.5, "ij", "kl")
    
        self.assertEqual(test1.m_status, "")
        self.assertEqual(test1.m_initMargin, "")
        self.assertEqual(test1.m_maintMargin, "")
        self.assertEqual(test1.m_equityWithLoan, "")
        self.assertEqual(test1.m_commission, 0.0)
        self.assertEqual(test1.m_minCommission, 0.0)
        self.assertEqual(test1.m_maxCommission, 0.0)
        self.assertEqual(test1.m_commissionCurrency, "")
        self.assertEqual(test1.m_warningText, "")

        self.assertEqual(test2.m_status, "ab")
        self.assertEqual(test2.m_initMargin, "cd")
        self.assertEqual(test2.m_maintMargin, "ef")
        self.assertEqual(test2.m_equityWithLoan, "gh")
        self.assertEqual(test2.m_commission, 3.5)
        self.assertEqual(test2.m_minCommission, 4.5)
        self.assertEqual(test2.m_maxCommission, 5.5)
        self.assertEqual(test2.m_commissionCurrency, "ij")
        self.assertEqual(test2.m_warningText, "kl")

    def test_fields(self):
        test = OrderState()

        test.m_status = "ab"
        test.m_initMargin = "cd"
        test.m_maintMargin = "ef"
        test.m_equityWithLoan = "gh"
        test.m_commission = 3.5
        test.m_minCommission = 4.5
        test.m_maxCommission = 5.5
        test.m_commissionCurrency = "ij"
        test.m_warningText = "kl"

        self.assertEqual(test.m_status, "ab")
        self.assertEqual(test.m_initMargin, "cd")
        self.assertEqual(test.m_maintMargin, "ef")
        self.assertEqual(test.m_equityWithLoan, "gh")
        self.assertEqual(test.m_commission, 3.5)
        self.assertEqual(test.m_minCommission, 4.5)
        self.assertEqual(test.m_maxCommission, 5.5)
        self.assertEqual(test.m_commissionCurrency, "ij")
        self.assertEqual(test.m_warningText, "kl")

    def test_equals(self):
        test1 = OrderState()
        test2 = OrderState()
        test3 = OrderState("ab", "cd", "ef", "gh", 3.5, 4.5, 5.5, "ij", "kl")
        
        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)
        