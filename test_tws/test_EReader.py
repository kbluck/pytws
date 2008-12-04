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
        self.calldata = []

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

    def test_readBoolFromInt(self):
        self.stream.write('0\x001\x00\x00-1\x001b3\x00123\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readBoolFromInt(), False)
        self.assertEqual(self.reader._readBoolFromInt(), True)
        self.assertEqual(self.reader._readBoolFromInt(), False)
        self.assertEqual(self.reader._readBoolFromInt(), True)
        self.assertRaises(ValueError, self.reader._readBoolFromInt)
        self.assertEqual(self.reader._readBoolFromInt(), True)

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

    def test_readDoubleMax(self):
        self.stream.write('1.25\x00456\x00\x001b3\x00789.\x00')
        self.stream.seek(0)
        self.assertEqual(self.reader._readDoubleMax(), 1.25)
        self.assertEqual(self.reader._readDoubleMax(), 456.0)
        self.assertEqual(self.reader._readDoubleMax(), Util._DOUBLE_MAX_VALUE)
        self.assertRaises(ValueError, self.reader._readDoubleMax)
        self.assertEqual(self.reader._readDoubleMax(), 789.0)

    def test_readTickPrice_v1(self):
        self.stream.write('1\x002\x004\x001.5\x00')
        self.stream.seek(0)
        self.reader._readTickPrice()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickPrice', (2,4,1.5,0), {}))

    def test_readTickPrice_v2(self):
        self.stream.write('2\x002\x001\x001.5\x006\x00')
        self.stream.write('2\x002\x002\x001.5\x006\x00')
        self.stream.write('2\x002\x004\x001.5\x006\x00')
        self.stream.write('2\x002\x005\x001.5\x006\x00')
        self.stream.seek(0)
        self.reader._readTickPrice()
        self.reader._readTickPrice()
        self.reader._readTickPrice()
        self.reader._readTickPrice()
        self.assertEqual(len(self.wrapper.calldata), 7)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickPrice', (2,1,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[1], ('tickSize',  (2,0,6), {}))
        self.assertEqual(self.wrapper.calldata[2], ('tickPrice', (2,2,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[3], ('tickSize',  (2,3,6), {}))
        self.assertEqual(self.wrapper.calldata[4], ('tickPrice', (2,4,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[5], ('tickSize',  (2,5,6), {}))
        self.assertEqual(self.wrapper.calldata[6], ('tickPrice', (2,5,1.5,0), {}))

    def test_readTickPrice_v3(self):
        self.stream.write('3\x002\x001\x001.5\x006\x001\x00')
        self.stream.write('3\x002\x002\x001.5\x006\x000\x00')
        self.stream.write('3\x002\x004\x001.5\x006\x001\x00')
        self.stream.write('3\x002\x005\x001.5\x006\x000\x00')
        self.stream.seek(0)
        self.reader._readTickPrice()
        self.reader._readTickPrice()
        self.reader._readTickPrice()
        self.reader._readTickPrice()
        self.assertEqual(len(self.wrapper.calldata), 7)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickPrice', (2,1,1.5,1), {}))
        self.assertEqual(self.wrapper.calldata[1], ('tickSize',  (2,0,6), {}))
        self.assertEqual(self.wrapper.calldata[2], ('tickPrice', (2,2,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[3], ('tickSize',  (2,3,6), {}))
        self.assertEqual(self.wrapper.calldata[4], ('tickPrice', (2,4,1.5,1), {}))
        self.assertEqual(self.wrapper.calldata[5], ('tickSize',  (2,5,6), {}))
        self.assertEqual(self.wrapper.calldata[6], ('tickPrice', (2,5,1.5,0), {}))

    def test_readTickSize(self):
        self.stream.write('3\x009\x001\x008\x00')
        self.stream.seek(0)
        self.reader._readTickSize()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickSize', (9,1,8), {}))

    def test_readTickOptionComputation(self):
        self.stream.write('3\x009\x0013\x00.25\x00.5\x00.125\x001.5\x00')
        self.stream.write('3\x009\x0013\x00-.25\x00.5\x00.125\x001.5\x00')
        self.stream.write('3\x009\x0013\x00.25\x001.5\x00.125\x001.5\x00')
        self.stream.write('3\x009\x0013\x00.25\x00-1.5\x00.125\x001.5\x00')
        self.stream.write('3\x009\x001\x00.25\x00.5\x00')
        self.stream.seek(0)
        self.reader._readTickOptionComputation()
        self.reader._readTickOptionComputation()
        self.reader._readTickOptionComputation()
        self.reader._readTickOptionComputation()
        self.reader._readTickOptionComputation()
        self.assertEqual(len(self.wrapper.calldata), 5)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickOptionComputation', (9, 13, 0.25, 0.5, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[1], ('tickOptionComputation', (9, 13, Util._DOUBLE_MAX_VALUE, 0.5, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[2], ('tickOptionComputation', (9, 13, 0.25, Util._DOUBLE_MAX_VALUE, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[3], ('tickOptionComputation', (9, 13, 0.25, Util._DOUBLE_MAX_VALUE, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[4], ('tickOptionComputation', (9, 1, 0.25, 0.5, Util._DOUBLE_MAX_VALUE, Util._DOUBLE_MAX_VALUE), {}))

    def test_readTickGeneric(self):
        self.stream.write('3\x009\x001\x001.25\x00')
        self.stream.seek(0)
        self.reader._readTickGeneric()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickGeneric', (9,1,1.25), {}))

    def test_readTickString(self):
        self.stream.write('3\x009\x001\x00ABC123\x00')
        self.stream.seek(0)
        self.reader._readTickString()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickString', (9,1,'ABC123'), {}))

    def test_readTickEFP(self):
        self.stream.write('3\x002\x001\x001.5\x00ABC\x002.5\x003\x00XYZ\x004.5\x005.5\x00')
        self.stream.seek(0)
        self.reader._readTickEFP()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ('tickEFP', (2,1,1.5,'ABC',2.5,3,'XYZ',4.5,5.5), {}))
