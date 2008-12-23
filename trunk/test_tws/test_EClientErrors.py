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

        self.assertEqual(test1.id(), 3)
        self.assertEqual(test2.id(), 4)
        self.assertEqual(test1.code(), 1)
        self.assertEqual(test2.code(), 2)
        self.assertEqual(test1.msg(), "Test1")
        self.assertEqual(test2.msg(), "Test2")
        self.assertEqual(test1.args, ((3, 1, 'Test1'),))
        self.assertEqual(test2.args, ((4, 2, 'Test2'),))
        self.assertEqual(test1.message, "1: Test1 (Id: 3)")
        self.assertEqual(test2.message, "2: Test2 (Id: 4)")

        if __debug__:
            self.assertRaises(AssertionError, CodeMsgPair, id=None)
            self.assertRaises(AssertionError, CodeMsgPair, [])
            self.assertRaises(AssertionError, CodeMsgPair, 1,2,3)
            self.assertRaises(AssertionError, CodeMsgPair, 1, "","")
