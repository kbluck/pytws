'''Unit test package for module "tws._EReader".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from StringIO import StringIO
from tws import EClientSocket, EReader, Util
from test_tws import mock_wrapper


class test_EReader(unittest.TestCase):
    '''Test class "tws.EReader"'''
    
    def setUp(self):
        self.wrapper = mock_wrapper()
        self.parent = EClientSocket(self.wrapper)
        self.stream = StringIO()
        self.reader = self.parent.createReader(self.parent, self.stream)

    def test_init(self):
        self.assertTrue(EReader(self.parent, StringIO()))

        if __debug__:
            self.assertRaises(AssertionError, EReader, 1, self.stream)
            self.assertRaises(AssertionError, EReader, self.parent, 1)

    def test_readStr(self):
        self.stream.write('test1\x00test2\x00\x00test3\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readStr(), 'test1')
        self.assertEqual(self.reader._readStr(), 'test2')
        self.assertEqual(self.reader._readStr(), None)
        self.assertEqual(self.reader._readStr(), 'test3')

    def test_readInt(self):
        self.stream.write('123\x00456\x00\x001b3\x00789\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readInt(), 123)
        self.assertEqual(self.reader._readInt(), 456)
        self.assertEqual(self.reader._readInt(), 0)
        self.assertRaises(ValueError, self.reader._readInt)
        self.assertEqual(self.reader._readInt(), 789)

    def test_readIntMax(self):
        self.stream.write('123\x00456\x00\x001b3\x00789\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readIntMax(), 123)
        self.assertEqual(self.reader._readIntMax(), 456)
        self.assertEqual(self.reader._readIntMax(), Util._INT_MAX_VALUE)
        self.assertRaises(ValueError, self.reader._readIntMax)
        self.assertEqual(self.reader._readIntMax(), 789)

    def test_readLong(self):
        self.stream.write('123\x00456\x00\x001b3\x00789\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readLong(), long(123))
        self.assertEqual(self.reader._readLong(), long(456))
        self.assertEqual(self.reader._readLong(), long(0))
        self.assertRaises(ValueError, self.reader._readLong)
        self.assertEqual(self.reader._readLong(), long(789))

    def test_readDouble(self):
        self.stream.write('1.25\x00456\x00\x001b3\x00789.\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readDouble(), 1.25)
        self.assertEqual(self.reader._readDouble(), 456.0)
        self.assertEqual(self.reader._readDouble(), 0.0)
        self.assertRaises(ValueError, self.reader._readDouble)
        self.assertEqual(self.reader._readDouble(), 789.0)
