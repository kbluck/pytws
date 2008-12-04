'''Unit test package for module "tws._ExecutionFilter".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import ExecutionFilter


class test_ExecutionFilter(unittest.TestCase):
    '''Test type "tws.ExecutionFilter"'''

    def test_init(self):
        test1 = ExecutionFilter()
        test2 = ExecutionFilter(1, 'ab', 'cd', 'ef', 'gh', 'ij', 'kl')
    
        self.assertEqual(test1.m_clientId, 0)
        self.assertEqual(test1.m_acctCode, '')
        self.assertEqual(test1.m_time, '')
        self.assertEqual(test1.m_symbol, '')
        self.assertEqual(test1.m_secType, '')
        self.assertEqual(test1.m_exchange, '')
        self.assertEqual(test1.m_side, '')

        self.assertEqual(test2.m_clientId, 1)
        self.assertEqual(test2.m_acctCode, 'ab')
        self.assertEqual(test2.m_time, 'cd')
        self.assertEqual(test2.m_symbol, 'ef')
        self.assertEqual(test2.m_secType, 'gh')
        self.assertEqual(test2.m_exchange, 'ij')
        self.assertEqual(test2.m_side, 'kl')

    def test_fields(self):
        test = ExecutionFilter()

        test.m_clientId = 1
        test.m_acctCode = 'ab'
        test.m_time = 'cd'
        test.m_symbol = 'ef'
        test.m_secType = 'gh'
        test.m_exchange = 'ij'
        test.m_side = 'kl'

        self.assertEqual(test.m_clientId, 1)
        self.assertEqual(test.m_acctCode, 'ab')
        self.assertEqual(test.m_time, 'cd')
        self.assertEqual(test.m_symbol, 'ef')
        self.assertEqual(test.m_secType, 'gh')
        self.assertEqual(test.m_exchange, 'ij')
        self.assertEqual(test.m_side, 'kl')

    def test_equals(self):
        test1 = ExecutionFilter()
        test2 = ExecutionFilter()
        test3 = ExecutionFilter(1, 'ab', 'cd', 'ef', 'gh', 'ij', 'kl')
        
        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)
