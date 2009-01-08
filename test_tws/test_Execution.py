'''Unit test package for module "tws._Execution".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import Execution


class test_Execution(unittest.TestCase):
    '''Test type "tws.Execution"'''

    def test_init(self):
        test1 = Execution()
        test2 = Execution(1, 2, "ab", "cd", "ef", "gh", "ij", 3, 3.5, 4, 5, 6, 7.5)

        self.assertEqual(test1.m_orderId, 0)
        self.assertEqual(test1.m_clientId, 0)
        self.assertEqual(test1.m_execId, "")
        self.assertEqual(test1.m_time, "")
        self.assertEqual(test1.m_acctNumber, "")
        self.assertEqual(test1.m_exchange, "")
        self.assertEqual(test1.m_side, "")
        self.assertEqual(test1.m_shares, 0)
        self.assertEqual(test1.m_price, 0.0)
        self.assertEqual(test1.m_permId, 0)
        self.assertEqual(test1.m_liquidation, 0)
        self.assertEqual(test1.m_cumQty, 0)
        self.assertEqual(test1.m_avgPrice, 0.0)

        self.assertEqual(test2.m_orderId, 1)
        self.assertEqual(test2.m_clientId, 2)
        self.assertEqual(test2.m_execId, "ab")
        self.assertEqual(test2.m_time, "cd")
        self.assertEqual(test2.m_acctNumber, "ef")
        self.assertEqual(test2.m_exchange, "gh")
        self.assertEqual(test2.m_side, "ij")
        self.assertEqual(test2.m_shares, 3)
        self.assertEqual(test2.m_price, 3.5)
        self.assertEqual(test2.m_permId, 4)
        self.assertEqual(test2.m_liquidation, 5)
        self.assertEqual(test2.m_cumQty, 6)
        self.assertEqual(test2.m_avgPrice, 7.5)

    def test_fields(self):
        test = Execution()

        test.m_orderId = 1
        test.m_clientId = 2
        test.m_execId = "ab"
        test.m_time = "cd"
        test.m_acctNumber = "ef"
        test.m_exchange = "gh"
        test.m_side = "ij"
        test.m_shares = 3
        test.m_price = 3.0
        test.m_permId = 4
        test.m_liquidation = 5
        test.m_cumQty = 6
        test.m_avgPrice = 7.5

        self.assertEqual(test.m_orderId, 1)
        self.assertEqual(test.m_clientId, 2)
        self.assertEqual(test.m_execId, "ab")
        self.assertEqual(test.m_time, "cd")
        self.assertEqual(test.m_acctNumber, "ef")
        self.assertEqual(test.m_exchange, "gh")
        self.assertEqual(test.m_side, "ij")
        self.assertEqual(test.m_shares, 3)
        self.assertEqual(test.m_price, 3.0)
        self.assertEqual(test.m_permId, 4)
        self.assertEqual(test.m_liquidation, 5)
        self.assertEqual(test.m_cumQty, 6)
        self.assertEqual(test.m_avgPrice, 7.5)

    def test_equals(self):
        test1 = Execution()
        test2 = Execution()
        test3 = Execution(1, 2, "ab")

        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)
