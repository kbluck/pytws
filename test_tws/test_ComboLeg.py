'''Unit test package for module "tws._ComboLeg".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import ComboLeg


class test_ComboLeg(unittest.TestCase):
    '''Test type "tws.ComboLeg"'''

    m_conId = 0
    m_ratio = 0
    m_action = ""
    m_exchange = ""
    m_openClose = 0
    m_shortSaleSlot = 0
    m_designatedLocation = ""

    def test_init(self):
        test1 = ComboLeg()
        test2 = ComboLeg(1, 2, "ab", "cd", 3, 4, "ef")

        self.assertEqual(test1.m_conId, 0)
        self.assertEqual(test1.m_ratio, 0)
        self.assertEqual(test1.m_action, "")
        self.assertEqual(test1.m_exchange, "")
        self.assertEqual(test1.m_openClose, 0)
        self.assertEqual(test1.m_shortSaleSlot, 0)
        self.assertEqual(test1.m_designatedLocation, "")

        self.assertEqual(test2.m_conId, 1)
        self.assertEqual(test2.m_ratio, 2)
        self.assertEqual(test2.m_action, "ab")
        self.assertEqual(test2.m_exchange, "cd")
        self.assertEqual(test2.m_openClose, 3)
        self.assertEqual(test2.m_shortSaleSlot, 4)
        self.assertEqual(test2.m_designatedLocation, "ef")

    def test_fields(self):
        test = ComboLeg()

        test.m_conId = 1
        test.m_ratio = 2
        test.m_action = "ab"
        test.m_exchange = "cd"
        test.m_openClose = 3
        test.m_shortSaleSlot = 4
        test.m_designatedLocation = "ef"

        self.assertEqual(test.m_conId, 1)
        self.assertEqual(test.m_ratio, 2)
        self.assertEqual(test.m_action, "ab")
        self.assertEqual(test.m_exchange, "cd")
        self.assertEqual(test.m_openClose, 3)
        self.assertEqual(test.m_shortSaleSlot, 4)
        self.assertEqual(test.m_designatedLocation, "ef")

    def test_equals(self):
        test1 = ComboLeg()
        test2 = ComboLeg()
        test3 = ComboLeg(1, 2, "ab", "cd", 3, 4, "ef")

        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)

    def test_constants(self):
         self.assertEqual(ComboLeg.SAME, 0)
         self.assertEqual(ComboLeg.OPEN, 1)
         self.assertEqual(ComboLeg.CLOSE, 2)
         self.assertEqual(ComboLeg.UNKNOWN, 3)
