'''Unit test package for module "tws._TagValue".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import TagValue


class test_TagValue(unittest.TestCase):
    '''Test type "tws.TagValue"'''

    def test_init(self):
        test1 = TagValue()
        test2 = TagValue("AB","CD")
        self.assertEqual(test1.m_tag, "")
        self.assertEqual(test1.m_value, "")
        self.assertEqual(test2.m_tag, "AB")
        self.assertEqual(test2.m_value, "CD")

    def test_fields(self):
        test = TagValue()
        test.m_tag = "ab"
        test.m_value = "cd"
        self.assertEqual(test.m_tag, "ab")
        self.assertEqual(test.m_value, "cd")

    def test_equals(self):
        test1 = TagValue()
        test2 = TagValue()
        test3 = TagValue("AB","CD")

        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertNotEqual(test1, test3)
