'''Unit test package for module "tws._EClientErrors".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws.EClientErrors as EClientErrors
from tws.EClientErrors import CodeMsgPair


class test_EClientErrors(unittest.TestCase):
    '''Test module "tws.EClientErrors"'''

    def test_CodeMsgPair(self):
        test1 = CodeMsgPair(id=3, code=1, msg="Test1")
        test2 = CodeMsgPair(id=4, code=2, msg="Test2")
        test3 = CodeMsgPair(source=test1, id=5, code=3, msg="Test3")
        test4 = CodeMsgPair(source=test2, id=6)

        self.assertEqual(test1.id(), 3)
        self.assertEqual(test2.id(), 4)
        self.assertEqual(test3.id(), 5)
        self.assertEqual(test4.id(), 6)
        self.assertEqual(test1.code(), 1)
        self.assertEqual(test2.code(), 2)
        self.assertEqual(test3.code(), 1)
        self.assertEqual(test4.code(), 2)
        self.assertEqual(test1.msg(), "Test1")
        self.assertEqual(test2.msg(), "Test2")
        self.assertEqual(test3.msg(), test1.msg() + ": Test3")
        self.assertEqual(test4.msg(), test2.msg())
        self.assertEqual(test1.args, ((3, 1, 'Test1', None),))
        self.assertEqual(test2.args, ((4, 2, 'Test2', None),))
        self.assertEqual(test3.args, ((5, 3,  "Test3", test1),))
        self.assertEqual(test4.args, ((6, None, None, test2),))
        self.assertEqual(test1.message, "1: Test1 (Ticker ID: 3)")
        self.assertEqual(test2.message, "2: Test2 (Ticker ID: 4)")
        self.assertEqual(test3.message, "1: Test1: Test3 (Ticker ID: 5)")
        self.assertEqual(test4.message, "2: Test2 (Ticker ID: 6)")

        if __debug__:
            self.assertRaises(AssertionError, CodeMsgPair, id=None)
            self.assertRaises(AssertionError, CodeMsgPair, [])
            self.assertRaises(AssertionError, CodeMsgPair, 1,2,3)
            self.assertRaises(AssertionError, CodeMsgPair, 1, "","")
