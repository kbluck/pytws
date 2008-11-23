'''Unit test package for module "tws.EClientErrors".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws.EClientErrors as EClientErrors
from tws.EClientErrors import CodeMsgPair


class test_EClientErrors(unittest.TestCase):
    '''Test module "tws.EClientErrors"'''

    def test_CodeMsgPair(self):
        test1 = CodeMsgPair((1,"Test1"))
        test2 = CodeMsgPair((2,"Test2"))

        self.assertEqual(test1.code(), 1)
        self.assertEqual(test2.code(), 2)
        self.assertEqual(test1.msg(), "Test1")
        self.assertEqual(test2.msg(), "Test2")

        if __debug__:
            self.assertRaises(TypeError, CodeMsgPair, 1)
            self.assertRaises(AssertionError, CodeMsgPair, [])
            self.assertRaises(AssertionError, CodeMsgPair, (1,2,3))
            self.assertRaises(AssertionError, CodeMsgPair, ("",""))
            self.assertRaises(AssertionError, CodeMsgPair, (1,2))
