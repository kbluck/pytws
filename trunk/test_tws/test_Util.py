'''Unit test package for module "tws._Util".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws.Util as Util


class test_Util(unittest.TestCase):
    '''Test free functions in module "tws.Util"'''

    def test_StringIsEmpty(self):
        self.assertTrue(Util.StringIsEmpty(""))
        self.assertTrue(Util.StringIsEmpty(None))
        self.assertFalse(Util.StringIsEmpty("0"))

        if __debug__:
            self.assertRaises(AssertionError, Util.StringIsEmpty, 0)

    def test_NormalizeString(self):
        self.assertEqual("", Util.NormalizeString(None))
        self.assertEqual("", Util.NormalizeString(""))
        self.assertEqual("123", Util.NormalizeString("123"))

        if __debug__:
            self.assertRaises(AssertionError, Util.NormalizeString, 0)

    def test_StringCompare(self):
        self.assertTrue(Util.StringCompare(None, None))
        self.assertTrue(Util.StringCompare("", None))
        self.assertTrue(Util.StringCompare(None,""))
        self.assertTrue(Util.StringCompare("123","123"))
        self.assertTrue(Util.StringCompare("ABC","ABC"))
        self.assertTrue(Util.StringCompare("xyz","xyz"))

        self.assertFalse(Util.StringCompare("123", None))
        self.assertFalse(Util.StringCompare(None, "123"))
        self.assertFalse(Util.StringCompare("123", ""))
        self.assertFalse(Util.StringCompare("", "123"))
        self.assertFalse(Util.StringCompare("123", "321"))
        self.assertFalse(Util.StringCompare("321", "123"))
        self.assertFalse(Util.StringCompare("ABC","abc"))
        self.assertFalse(Util.StringCompare("abc","ABC"))

        if __debug__:
            self.assertRaises(AssertionError, Util.StringCompare, 0, "")
            self.assertRaises(AssertionError, Util.StringCompare, "", 0)
            self.assertRaises(AssertionError, Util.StringCompare, 0, 0)

    def test_StringCompareIgnCase(self):
        self.assertTrue(Util.StringCompareIgnCase(None, None))
        self.assertTrue(Util.StringCompareIgnCase("", None))
        self.assertTrue(Util.StringCompareIgnCase(None,""))
        self.assertTrue(Util.StringCompareIgnCase("123","123"))
        self.assertTrue(Util.StringCompareIgnCase("ABC","ABC"))
        self.assertTrue(Util.StringCompareIgnCase("xyz","xyz"))
        self.assertTrue(Util.StringCompareIgnCase("ABC","abc"))
        self.assertTrue(Util.StringCompareIgnCase("abc","ABC"))

        self.assertFalse(Util.StringCompareIgnCase("123", None))
        self.assertFalse(Util.StringCompareIgnCase(None, "123"))
        self.assertFalse(Util.StringCompareIgnCase("123", ""))
        self.assertFalse(Util.StringCompareIgnCase("", "123"))
        self.assertFalse(Util.StringCompareIgnCase("123", "321"))
        self.assertFalse(Util.StringCompareIgnCase("321", "123"))

        if __debug__:
            self.assertRaises(AssertionError, Util.StringCompare, 0, "")
            self.assertRaises(AssertionError, Util.StringCompare, "", 0)
            self.assertRaises(AssertionError, Util.StringCompare, 0, 0)

    def test_VectorEqualsUnordered(self):
        self.assertTrue(Util.VectorEqualsUnordered([0,1,2], [0,1,2]))
        self.assertTrue(Util.VectorEqualsUnordered([0,1,2], [2,1,0]))
        self.assertTrue(Util.VectorEqualsUnordered([2,1,0], [0,1,2]))
        self.assertTrue(Util.VectorEqualsUnordered([1,2,0], [0,1,2]))

        self.assertFalse(Util.VectorEqualsUnordered([0,1,2], [0,1,1]))
        self.assertFalse(Util.VectorEqualsUnordered([0,1,2], [0,1]))
        self.assertFalse(Util.VectorEqualsUnordered([0,1,2], [0,1,2,3]))

        if __debug__:
            self.assertRaises(AssertionError, Util.VectorEqualsUnordered, "", "")
            self.assertRaises(AssertionError, Util.VectorEqualsUnordered, [], "")
            self.assertRaises(AssertionError, Util.VectorEqualsUnordered, "", [])

    def test_IntMaxString(self):
        self.assertEqual("0", Util.IntMaxString(0))
        self.assertEqual("1", Util.IntMaxString(1))
        self.assertEqual("-1", Util.IntMaxString(-1))
        self.assertEqual("", Util.IntMaxString(Util._INT_MAX_VALUE))

        if __debug__:
            self.assertRaises(AssertionError, Util.IntMaxString, "0")
            self.assertRaises(AssertionError, Util.IntMaxString, 0.0)

    def test_DoubleMaxString(self):
        self.assertEqual("0.0", Util.DoubleMaxString(0.0))
        self.assertEqual("1.0", Util.DoubleMaxString(1.0))
        self.assertEqual("-1.0", Util.DoubleMaxString(-1.0))
        self.assertEqual("", Util.DoubleMaxString(Util._DOUBLE_MAX_VALUE))

        if __debug__:
            self.assertRaises(AssertionError, Util.DoubleMaxString, "0")
            self.assertRaises(AssertionError, Util.DoubleMaxString, 0)
