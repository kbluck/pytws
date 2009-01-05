'''Unit test package for module "tws._UnderComp".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import UnderComp


class test_UnderComp(unittest.TestCase):
    '''Test class "tws.UnderComp"'''

    def test_init(self):
        test = UnderComp()
        self.assertEqual(test.m_conId, 0)
        self.assertEqual(test.m_delta, 0.0)
        self.assertEqual(test.m_price, 0.0)

    def test_fields(self):
        test = UnderComp()
        test.m_conId = 1
        test.m_delta = 2.5
        test.m_price = 3.0
        self.assertEqual(test.m_conId, 1)
        self.assertEqual(test.m_delta, 2.5)
        self.assertEqual(test.m_price, 3.0)

    def test_equals(self):
        test1 = UnderComp()
        test2 = UnderComp()
        test3 = UnderComp()
        test4 = UnderComp()
        test3.m_conId = 1
        test3.m_delta = 2.5
        test3.m_price = 3.0
        
        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)

    def test_nonzero(self):
        test1 = UnderComp()
        test2 = UnderComp()
        test2.m_conId = 1
        test2.m_delta = 2.5
        test2.m_price = 3.0
        self.assertFalse(test1)
        self.assertTrue(test2)
        