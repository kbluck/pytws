'''Unit test package for module "tws._EReader".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from StringIO import StringIO
from tws import Contract, ContractDetails, EClientErrors, EClientSocket, EReader, \
                Execution, Order, OrderState, TagValue, UnderComp, Util
from test_tws import mock_wrapper


class test_EReader(unittest.TestCase):
    '''Test class "tws.EReader"'''
    
    def setUp(self):
        self.wrapper = mock_wrapper()
        self.connection = EClientSocket(self.wrapper)
        self.stream = StringIO()
        self.reader = self.connection.createReader(self.connection, self.stream)
        self.calldata = []

    def test_init(self):
        self.assertTrue(EReader(self.connection, StringIO()))

        if __debug__:
            self.assertRaises(AssertionError, EReader, 1, self.stream)
            self.assertRaises(AssertionError, EReader, self.connection, 1)

    def test_readNextMessage(self):
        self.stream.write("52\x001\x002\x00")
        self.stream.write("123456\x00")
        self.stream.write("53\x001\x00")
        self.stream.write("-1\x00")
        self.stream.write("54\x001\x00A1\x00")
        self.stream.write("654321\x00")
        self.stream.write("654321\x00")

        def _raise(x=1, y=2): raise Exception(654321)
        self.reader._reader_map[654321] = _raise
        
        self.stream.seek(0)
        return_values = []
        for i in xrange(6): return_values.append(self.reader._readNextMessage())

        self.assertEqual(len(return_values), 6)
        self.assertEqual(len(self.wrapper.calldata), 3)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertTrue(return_values[0]) 
        self.assertEqual(self.wrapper.calldata[0], ("contractDetailsEnd", (2,), {}))
        self.assertFalse(return_values[1]) 
        self.assertTrue(return_values[2]) 
        self.assertEqual(self.wrapper.calldata[1], ("openOrderEnd", (), {}))
        self.assertFalse(return_values[3]) 
        self.assertEqual(self.wrapper.errors[0], (123456,
                                                  EClientErrors.UNKNOWN_ID.code(),
                                                  EClientErrors.UNKNOWN_ID.msg()))
        self.assertTrue(return_values[4]) 
        self.assertEqual(self.wrapper.calldata[2], ("accountDownloadEnd", ("A1",), {}))
        self.assertFalse(return_values[5]) 
        self.assertEqual(self.wrapper.errors[1], (-1,Exception,(654321,)))

        self.wrapper.error = _raise
        return_values.append(self.reader._readNextMessage())
        self.assertEqual(len(return_values), 7)
        self.assertEqual(len(self.wrapper.calldata), 3)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertFalse(return_values[6]) 
        

    def test_readStr(self):
        self.stream.write("test1\x00test2\x00\x00test3\x00")
        self.stream.seek(0)
        self.assertEqual(self.reader._readStr(), "test1")
        self.assertEqual(self.reader._readStr(), "test2")
        self.assertEqual(self.reader._readStr(), None)
        self.assertEqual(self.reader._readStr(), "test3")

    def test_readInt(self):
        self.stream.write("123\x00456\x00\x001b3\x00789\x00")
        self.stream.seek(0)
        self.assertEqual(self.reader._readInt(), 123)
        self.assertEqual(self.reader._readInt(), 456)
        self.assertEqual(self.reader._readInt(), 0)
        self.assertRaises(ValueError, self.reader._readInt)
        self.assertEqual(self.reader._readInt(), 789)

    def test_readIntMax(self):
        self.stream.write("123\x00456\x00\x001b3\x00789\x00")
        self.stream.seek(0)
        self.assertEqual(self.reader._readIntMax(), 123)
        self.assertEqual(self.reader._readIntMax(), 456)
        self.assertEqual(self.reader._readIntMax(), Util._INT_MAX_VALUE)
        self.assertRaises(ValueError, self.reader._readIntMax)
        self.assertEqual(self.reader._readIntMax(), 789)

    def test_readBoolFromInt(self):
        self.stream.write("0\x001\x00\x00-1\x001b3\x00123\x00")
        self.stream.seek(0)
        self.assertEqual(self.reader._readBoolFromInt(), False)
        self.assertEqual(self.reader._readBoolFromInt(), True)
        self.assertEqual(self.reader._readBoolFromInt(), False)
        self.assertEqual(self.reader._readBoolFromInt(), True)
        self.assertRaises(ValueError, self.reader._readBoolFromInt)
        self.assertEqual(self.reader._readBoolFromInt(), True)

    def test_readLong(self):
        self.stream.write("123\x00456\x00\x001b3\x00789\x00")
        self.stream.seek(0)
        self.assertEqual(self.reader._readLong(), long(123))
        self.assertEqual(self.reader._readLong(), long(456))
        self.assertEqual(self.reader._readLong(), long(0))
        self.assertRaises(ValueError, self.reader._readLong)
        self.assertEqual(self.reader._readLong(), long(789))

    def test_readDouble(self):
        self.stream.write("1.25\x00456\x00\x001b3\x00789.\x00")
        self.stream.seek(0)
        self.assertEqual(self.reader._readDouble(), 1.25)
        self.assertEqual(self.reader._readDouble(), 456.0)
        self.assertEqual(self.reader._readDouble(), 0.0)
        self.assertRaises(ValueError, self.reader._readDouble)
        self.assertEqual(self.reader._readDouble(), 789.0)

    def test_readDoubleMax(self):
        self.stream.write("1.25\x00456\x00\x001b3\x00789.\x00")
        self.stream.seek(0)
        self.assertEqual(self.reader._readDoubleMax(), 1.25)
        self.assertEqual(self.reader._readDoubleMax(), 456.0)
        self.assertEqual(self.reader._readDoubleMax(), Util._DOUBLE_MAX_VALUE)
        self.assertRaises(ValueError, self.reader._readDoubleMax)
        self.assertEqual(self.reader._readDoubleMax(), 789.0)

    def test_readTickPrice(self):
        self.stream.write("1\x002\x004\x001.5\x00")
        self.stream.write("2\x002\x001\x001.5\x006\x00")
        self.stream.write("2\x002\x002\x001.5\x006\x00")
        self.stream.write("2\x002\x004\x001.5\x006\x00")
        self.stream.write("2\x002\x005\x001.5\x006\x00")
        self.stream.write("3\x002\x001\x001.5\x006\x001\x00")
        self.stream.write("3\x002\x002\x001.5\x006\x000\x00")
        self.stream.write("3\x002\x004\x001.5\x006\x001\x00")
        self.stream.write("3\x002\x005\x001.5\x006\x000\x00")
        self.stream.seek(0)
        for i in xrange(9): self.reader._readTickPrice()
        self.assertEqual(len(self.wrapper.calldata), 15)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0],  ("tickPrice", (2,4,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[1],  ("tickPrice", (2,1,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[2],  ("tickSize",  (2,0,6), {}))
        self.assertEqual(self.wrapper.calldata[3],  ("tickPrice", (2,2,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[4],  ("tickSize",  (2,3,6), {}))
        self.assertEqual(self.wrapper.calldata[5],  ("tickPrice", (2,4,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[6],  ("tickSize",  (2,5,6), {}))
        self.assertEqual(self.wrapper.calldata[7],  ("tickPrice", (2,5,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[8],  ("tickPrice", (2,1,1.5,1), {}))
        self.assertEqual(self.wrapper.calldata[9],  ("tickSize",  (2,0,6), {}))
        self.assertEqual(self.wrapper.calldata[10], ("tickPrice", (2,2,1.5,0), {}))
        self.assertEqual(self.wrapper.calldata[11], ("tickSize",  (2,3,6), {}))
        self.assertEqual(self.wrapper.calldata[12], ("tickPrice", (2,4,1.5,1), {}))
        self.assertEqual(self.wrapper.calldata[13], ("tickSize",  (2,5,6), {}))
        self.assertEqual(self.wrapper.calldata[14], ("tickPrice", (2,5,1.5,0), {}))

    def test_readTickSize(self):
        self.stream.write("3\x009\x001\x008\x00")
        self.stream.seek(0)
        self.reader._readTickSize()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("tickSize", (9,1,8), {}))

    def test_readTickOptionComputation(self):
        self.stream.write("3\x009\x0013\x00.25\x00.5\x00.125\x001.5\x00")
        self.stream.write("3\x009\x0013\x00-.25\x00.5\x00.125\x001.5\x00")
        self.stream.write("3\x009\x0013\x00.25\x001.5\x00.125\x001.5\x00")
        self.stream.write("3\x009\x0013\x00.25\x00-1.5\x00.125\x001.5\x00")
        self.stream.write("3\x009\x001\x00.25\x00.5\x00")
        self.stream.seek(0)
        for i in xrange(5): self.reader._readTickOptionComputation()
        self.assertEqual(len(self.wrapper.calldata), 5)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("tickOptionComputation", (9, 13, 0.25, 0.5, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[1], ("tickOptionComputation", (9, 13, Util._DOUBLE_MAX_VALUE, 0.5, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[2], ("tickOptionComputation", (9, 13, 0.25, Util._DOUBLE_MAX_VALUE, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[3], ("tickOptionComputation", (9, 13, 0.25, Util._DOUBLE_MAX_VALUE, 0.125, 1.5), {}))
        self.assertEqual(self.wrapper.calldata[4], ("tickOptionComputation", (9, 1, 0.25, 0.5, Util._DOUBLE_MAX_VALUE, Util._DOUBLE_MAX_VALUE), {}))

    def test_readTickGeneric(self):
        self.stream.write("3\x009\x001\x001.25\x00")
        self.stream.seek(0)
        self.reader._readTickGeneric()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("tickGeneric", (9,1,1.25), {}))

    def test_readTickString(self):
        self.stream.write("3\x009\x001\x00ABC123\x00")
        self.stream.seek(0)
        self.reader._readTickString()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("tickString", (9,1,"ABC123"), {}))

    def test_readTickEFP(self):
        self.stream.write("3\x002\x001\x001.5\x00ABC\x002.5\x003\x00XYZ\x004.5\x005.5\x00")
        self.stream.seek(0)
        self.reader._readTickEFP()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("tickEFP", (2,1,1.5,"ABC",2.5,3,"XYZ",4.5,5.5), {}))

    def test_readOrderStatus(self):
        self.stream.write("1\x009\x00ABC\x002\x003\x001.5\x00")
        self.stream.write("2\x009\x00ABC\x002\x003\x001.5\x004\x00")
        self.stream.write("3\x009\x00ABC\x002\x003\x001.5\x004\x005\x00")
        self.stream.write("4\x009\x00ABC\x002\x003\x001.5\x004\x005\x002.5\x00")
        self.stream.write("5\x009\x00ABC\x002\x003\x001.5\x004\x005\x002.5\x006\x00")
        self.stream.write("6\x009\x00ABC\x002\x003\x001.5\x004\x005\x002.5\x006\x00DEF\x00")
        self.stream.seek(0)
        for i in xrange(6): self.reader._readOrderStatus()
        self.assertEqual(len(self.wrapper.calldata), 6)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("orderStatus", (9,"ABC",2,3,1.5,0,0,0.0,0,None), {}))
        self.assertEqual(self.wrapper.calldata[1], ("orderStatus", (9,"ABC",2,3,1.5,4,0,0.0,0,None), {}))
        self.assertEqual(self.wrapper.calldata[2], ("orderStatus", (9,"ABC",2,3,1.5,4,5,0.0,0,None), {}))
        self.assertEqual(self.wrapper.calldata[3], ("orderStatus", (9,"ABC",2,3,1.5,4,5,2.5,0,None), {}))
        self.assertEqual(self.wrapper.calldata[4], ("orderStatus", (9,"ABC",2,3,1.5,4,5,2.5,6,None), {}))
        self.assertEqual(self.wrapper.calldata[5], ("orderStatus", (9,"ABC",2,3,1.5,4,5,2.5,6,"DEF"), {}))

    def test_readUpdateAccountValue(self):
        self.stream.write("1\x00AB\x00CD\x00EF\x00")
        self.stream.write("2\x00AB\x00CD\x00EF\x00GH\x00")
        self.stream.seek(0)
        for i in xrange(2): self.reader._readUpdateAccountValue()
        self.assertEqual(len(self.wrapper.calldata), 2)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("updateAccountValue", ("AB","CD","EF",None), {}))
        self.assertEqual(self.wrapper.calldata[1], ("updateAccountValue", ("AB","CD","EF","GH"), {}))

    def test_readUpdatePortfolio(self):
        self.stream.write("1\x00AB\x00CD\x00EF\x001.5\x00GH\x00IJ\x002\x003.5\x004.5\x00")
        self.stream.write("2\x00AB\x00CD\x00EF\x001.5\x00GH\x00IJ\x00KL\x002\x003.5\x004.5\x00")
        self.stream.write("3\x00AB\x00CD\x00EF\x001.5\x00GH\x00IJ\x00KL\x002\x003.5\x004.5\x005.5\x006.5\x007.5\x00")
        self.stream.write("4\x00AB\x00CD\x00EF\x001.5\x00GH\x00IJ\x00KL\x002\x003.5\x004.5\x005.5\x006.5\x007.5\x00MN\x00")
        self.stream.write("6\x008\x00AB\x00CD\x00EF\x001.5\x00GH\x00IJ\x00KL\x002\x003.5\x004.5\x005.5\x006.5\x007.5\x00MN\x00")
        self.stream.write("6\x008\x00AB\x00CD\x00EF\x001.5\x00GH\x00IJ\x00KL\x002\x003.5\x004.5\x005.5\x006.5\x007.5\x00MN\x00ST\x00")
        self.stream.write("7\x008\x00AB\x00CD\x00EF\x001.5\x00GH\x00OP\x00QR\x00IJ\x00KL\x002\x003.5\x004.5\x005.5\x006.5\x007.5\x00MN\x00")
        self.stream.seek(0)
        for i in xrange(5): self.reader._readUpdatePortfolio()
        self.assertEqual(len(self.wrapper.calldata), 5)
        self.assertEqual(len(self.wrapper.errors), 0)

        contract = Contract(symbol="AB", sec_type="CD", expiry="EF", strike=1.5, right="GH", currency="IJ")
        self.assertEqual(self.wrapper.calldata[0], ("updatePortfolio", (contract,2,3.5,4.5,0.0,0.0,0.0,''), {}))
        contract.m_localSymbol = "KL"
        self.assertEqual(self.wrapper.calldata[1], ("updatePortfolio", (contract,2,3.5,4.5,0.0,0.0,0.0,''), {}))
        self.assertEqual(self.wrapper.calldata[2], ("updatePortfolio", (contract,2,3.5,4.5,5.5,6.5,7.5,''), {}))
        self.assertEqual(self.wrapper.calldata[3], ("updatePortfolio", (contract,2,3.5,4.5,5.5,6.5,7.5,'MN'), {}))
        contract.m_conId = 8
        self.assertEqual(self.wrapper.calldata[4], ("updatePortfolio", (contract,2,3.5,4.5,5.5,6.5,7.5,'MN'), {}))

        self.connection._serverVersion = 39
        self.reader._readUpdatePortfolio()
        contract.m_primaryExch = "ST"
        self.assertEqual(self.wrapper.calldata[5], ("updatePortfolio", (contract,2,3.5,4.5,5.5,6.5,7.5,'MN'), {}))

        self.reader._readUpdatePortfolio()
        contract.m_multiplier = "OP"
        contract.m_primaryExch = "QR"
        self.assertEqual(self.wrapper.calldata[6], ("updatePortfolio", (contract,2,3.5,4.5,5.5,6.5,7.5,'MN'), {}))

    def test_readUpdateAccountTime(self):
        self.stream.write("3\x00AB\x00")
        self.stream.seek(0)
        self.reader._readUpdateAccountTime()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("updateAccountTime", ("AB",), {}))

    def test_readError(self):
        self.stream.write("1\x00AB\x00")
        self.stream.write("2\x001\x002\x00CD\x00")
        self.stream.seek(0)
        for i in xrange(2): self.reader._readError()
        self.assertEqual(len(self.wrapper.calldata), 0)
        self.assertEqual(len(self.wrapper.errors), 2)
        self.assertEqual(self.wrapper.errors[0], (EClientErrors.NO_VALID_ID,EClientErrors.UNKNOWN_ID.code(),"AB"))
        self.assertEqual(self.wrapper.errors[1], (1,2,"CD"))

    def test_readOpenOrder(self):
        # This one's huge.
        self.stream.write("1\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x00")
        self.stream.write("2\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x00")
        self.stream.write("3\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x00")
        self.stream.write("4\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00")
        self.stream.write("5\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00")
        self.stream.write("6\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00")
        self.stream.write("7\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00")
        self.stream.write("8\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00")
        self.stream.write("9\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x00")
        self.stream.write("10\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x00")
        self.stream.write("11\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x0015\x001\x0016\x00")
        self.stream.write("11\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x0015\x001\x0015.5\x0016.5\x0016\x00")
        self.stream.write("12\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x00")
        self.stream.write("13\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x00")
        self.stream.write("14\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x00")
        self.stream.write("15\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x001\x0018\x0020.5\x00")
        self.stream.write("16\x002\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x001\x0018\x0020.5\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("17\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x001\x0018\x0020.5\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("18\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x001\x0018\x0020.5\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("19\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x001\x0018\x0020.5\x00F6\x00G7\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("20\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x0020\x0021\x0020.5\x00F6\x00G7\x000\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("20\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x0020\x0021\x0020.5\x00F6\x00G7\x001\x0022\x0024.5\x0025.5\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("21\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x0020\x0021\x0020.5\x00F6\x00G7\x001\x0022\x0024.5\x0025.5\x00\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("21\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x0020\x0021\x0020.5\x00F6\x00G7\x001\x0022\x0024.5\x0025.5\x00H8\x000\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")
        self.stream.write("21\x002\x0019\x00A1\x00B2\x00C3\x002.5\x00D4\x00E5\x00F6\x00N5\x00G7\x003\x00H8\x003.5\x004.5\x00I9\x00J1\x00K2\x00L3\x004\x00M4\x005\x006\x001\x001\x005.5\x00O6\x00\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x006.5\x00V4\x007\x00W5\x008\x007.5\x008.5\x009.5\x0010.5\x0011.5\x009\x001\x001\x001\x0010\x0011\x001\x001\x0012.5\x0012\x0013\x0013.5\x0014\x00X6\x0017.5\x001\x0016\x0018.5\x0019.5\x0017\x00Y7\x0020\x0021\x0020.5\x00F6\x00G7\x001\x0022\x0024.5\x0025.5\x00H8\x002\x00I9\x00J1\x00K2\x00L3\x001\x00Z8\x00A9\x00B1\x00C2\x0021.5\x0022.5\x0023.5\x00D4\x00E5\x00")

        self.stream.seek(0)

        self.connection._serverVersion = -1 # Arbitrary fake value.
        for i in xrange(11): self.reader._readOpenOrder()
        self.connection._serverVersion = 26 # Server version matters on the 12th test call.
        self.reader._readOpenOrder()
        self.connection._serverVersion = -1 # Back to fake server version
        for i in xrange(13): self.reader._readOpenOrder()

        self.assertEqual(len(self.wrapper.calldata), 25)
        self.assertEqual(len(self.wrapper.errors), 0)

        contract = Contract()
        order = Order()
        orderstate = OrderState()

        # V1
        contract.m_symbol = "A1"
        contract.m_secType = "B2"
        contract.m_expiry = "C3"
        contract.m_strike = 2.5
        contract.m_right = "D4"
        contract.m_exchange = "E5"
        contract.m_currency = "F6"
        order.m_orderId = 2
        order.m_action = "G7"
        order.m_totalQuantity = 3
        order.m_orderType = "H8"
        order.m_lmtPrice = 3.5
        order.m_auxPrice = 4.5
        order.m_tif = "I9"
        order.m_ocaGroup = "J1"
        order.m_account = "K2"
        order.m_openClose = "L3"
        order.m_origin = 4
        order.m_orderRef = "M4"
        self.assertEqual(self.wrapper.calldata[0], ("openOrder", (2,contract,order,orderstate), {}))
        # V2
        contract.m_localSymbol = "N5"
        self.assertEqual(self.wrapper.calldata[1], ("openOrder", (2,contract,order,orderstate), {}))
        # V3
        order.m_clientId = 5
        self.assertEqual(self.wrapper.calldata[2], ("openOrder", (2,contract,order,orderstate), {}))
        # V4
        order.m_permId = 6
        order.m_hidden = 1
        order.m_discretionaryAmt = 5.5
        self.assertEqual(self.wrapper.calldata[3], ("openOrder", (2,contract,order,orderstate), {}))
        order.m_permId = 0 # Matching permID will force order to evaluate equal otherwise.
        self.assertEqual(self.wrapper.calldata[3], ("openOrder", (2,contract,order,orderstate), {}))
        # V5
        order.m_goodAfterTime = "O6"
        self.assertEqual(self.wrapper.calldata[4], ("openOrder", (2,contract,order,orderstate), {}))
        # V6
        self.assertEqual(self.wrapper.calldata[5], ("openOrder", (2,contract,order,orderstate), {}))
        # V7
        order.m_faGroup = "P7"
        order.m_faMethod = "Q8"
        order.m_faPercentage = "R9"
        order.m_faProfile = "S1"
        self.assertEqual(self.wrapper.calldata[6], ("openOrder", (2,contract,order,orderstate), {}))
        # V8
        order.m_goodTillDate = "T2"
        self.assertEqual(self.wrapper.calldata[7], ("openOrder", (2,contract,order,orderstate), {}))
        # V9
        order.m_rule80A = "U3"
        order.m_percentOffset = 6.5
        order.m_settlingFirm = "V4"
        order.m_shortSaleSlot = 7
        order.m_designatedLocation = "W5"
        order.m_auctionStrategy = 8
        order.m_startingPrice = 7.5
        order.m_stockRefPrice = 8.5
        order.m_delta = 9.5
        order.m_stockRangeLower = 10.5
        order.m_stockRangeUpper = 11.5
        order.m_displaySize = 9
        order.m_blockOrder = True
        order.m_sweepToFill = True
        order.m_allOrNone = True
        order.m_minQty = 10
        order.m_ocaType = 11
        order.m_eTradeOnly = True
        order.m_firmQuoteOnly = True
        order.m_nbboPriceCap = 12.5
        self.assertEqual(self.wrapper.calldata[8], ("openOrder", (2,contract,order,orderstate), {}))
        # V10
        order.m_parentId = 12
        order.m_triggerMethod = 13
        self.assertEqual(self.wrapper.calldata[9], ("openOrder", (2,contract,order,orderstate), {}))
        # V11 
        order.m_volatility = 13.5
        order.m_volatilityType = 14
        order.m_deltaNeutralOrderType = "MKT"
        order.m_continuousUpdate = 1
        order.m_referencePriceType = 16
        self.assertEqual(self.wrapper.calldata[10], ("openOrder", (2,contract,order,orderstate), {}))
        order.m_stockRangeLower = 15.5
        order.m_stockRangeUpper = 16.5
        self.assertEqual(self.wrapper.calldata[11], ("openOrder", (2,contract,order,orderstate), {}))
        # V12
        order.m_deltaNeutralOrderType = "X6"
        order.m_deltaNeutralAuxPrice = 17.5
        order.m_stockRangeLower = 10.5
        order.m_stockRangeUpper = 11.5
        self.assertEqual(self.wrapper.calldata[12], ("openOrder", (2,contract,order,orderstate), {}))
        # V13
        order.m_trailStopPrice = 18.5
        self.assertEqual(self.wrapper.calldata[13], ("openOrder", (2,contract,order,orderstate), {}))
        # V14
        order.m_basisPoints = 19.5
        order.m_basisPointsType = 17
        contract.m_comboLegsDescrip = "Y7"
        self.assertEqual(self.wrapper.calldata[14], ("openOrder", (2,contract,order,orderstate), {}))
        # V15        
        order.m_scaleInitLevelSize = 18
        order.m_scalePriceIncrement = 20.5
        self.assertEqual(self.wrapper.calldata[15], ("openOrder", (2,contract,order,orderstate), {}))
        # V16
        order.m_whatIf = True
        orderstate.m_status = "Z8"
        orderstate.m_initMargin = "A9"
        orderstate.m_maintMargin = "B1"
        orderstate.m_equityWithLoan = "C2"
        orderstate.m_commission = 21.5
        orderstate.m_minCommission = 22.5
        orderstate.m_maxCommission = 23.5
        orderstate.m_commissionCurrency = "D4"
        orderstate.m_warningText = "E5"
        self.assertEqual(self.wrapper.calldata[16], ("openOrder", (2,contract,order,orderstate), {}))
        # V17
        contract.m_conId = 19
        self.assertEqual(self.wrapper.calldata[17], ("openOrder", (2,contract,order,orderstate), {}))
        # V18
        order.m_outsideRth = True
        self.assertEqual(self.wrapper.calldata[18], ("openOrder", (2,contract,order,orderstate), {}))
        # V19
        order.m_clearingAccount = "F6"
        order.m_clearingIntent = "G7"
        self.assertEqual(self.wrapper.calldata[19], ("openOrder", (2,contract,order,orderstate), {}))
        # V20
        order.m_scaleInitLevelSize = 20
        order.m_scaleSubsLevelSize = 21
        self.assertEqual(self.wrapper.calldata[20], ("openOrder", (2,contract,order,orderstate), {}))
        undercomp = UnderComp()
        undercomp.m_conId = 22
        undercomp.m_delta = 24.5
        undercomp.m_price = 25.5
        contract.m_underComp = undercomp
        self.assertEqual(self.wrapper.calldata[21], ("openOrder", (2,contract,order,orderstate), {}))
        # V21
        order.m_algoStrategy = None
        self.assertEqual(self.wrapper.calldata[22], ("openOrder", (2,contract,order,orderstate), {}))
        order.m_algoStrategy = "H8"
        self.assertEqual(self.wrapper.calldata[23], ("openOrder", (2,contract,order,orderstate), {}))
        order.m_algoParams = [TagValue("I9","J1"),TagValue("K2","L3")]
        self.assertEqual(self.wrapper.calldata[24], ("openOrder", (2,contract,order,orderstate), {}))

    def test_readNextValidId(self):
        self.stream.write("1\x002\x00")
        self.stream.seek(0)
        self.reader._readNextValidId()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("nextValidId", (2,), {}))

    def test_readScannerData(self):
        self.stream.write("1\x003\x002\x004\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x005\x00M4\x00N5\x00O6\x002.5\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x00V4\x00W5\x00X6\x00")
        self.stream.write("2\x003\x002\x004\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x00Y7\x005\x00M4\x00N5\x00O6\x002.5\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x00V4\x00W5\x00X6\x00Z8\x00")
        self.stream.write("3\x003\x002\x004\x006\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x00Y7\x005\x007\x00M4\x00N5\x00O6\x002.5\x00P7\x00Q8\x00R9\x00S1\x00T2\x00U3\x00V4\x00W5\x00X6\x00Z8\x00")
        self.stream.seek(0)
        for i in xrange(3): self.reader._readScannerData()
        self.assertEqual(len(self.wrapper.calldata), 9)
        self.assertEqual(len(self.wrapper.errors), 0)

        contract1 = ContractDetails()
        contract2 = ContractDetails()

        contract1.m_summary.m_symbol = "A1"
        contract1.m_summary.m_secType = "B2"
        contract1.m_summary.m_expiry = "C3"
        contract1.m_summary.m_strike = 1.5
        contract1.m_summary.m_right = "D4"
        contract1.m_summary.m_exchange = "E5"
        contract1.m_summary.m_currency = "F6"
        contract1.m_summary.m_localSymbol = "G7"
        contract1.m_marketName = "H8"
        contract1.m_tradingClass = "I9"

        contract2.m_summary.m_symbol = "M4"
        contract2.m_summary.m_secType = "N5"
        contract2.m_summary.m_expiry = "O6"
        contract2.m_summary.m_strike = 2.5
        contract2.m_summary.m_right = "P7"
        contract2.m_summary.m_exchange = "Q8"
        contract2.m_summary.m_currency = "R9"
        contract2.m_summary.m_localSymbol = "S1"
        contract2.m_marketName = "T2"
        contract2.m_tradingClass = "U3"

        self.assertEqual(self.wrapper.calldata[0], ("scannerData", (3, 4, contract1, "J1", "K2", "L3", None), {}))
        self.assertEqual(self.wrapper.calldata[1], ("scannerData", (3, 5, contract2, "V4", "W5", "X6", None), {}))
        self.assertEqual(self.wrapper.calldata[2], ("scannerDataEnd", (3,), {}))
        self.assertEqual(self.wrapper.calldata[3], ("scannerData", (3, 4, contract1, "J1", "K2", "L3", "Y7"), {}))
        self.assertEqual(self.wrapper.calldata[4], ("scannerData", (3, 5, contract2, "V4", "W5", "X6", "Z8"), {}))
        self.assertEqual(self.wrapper.calldata[5], ("scannerDataEnd", (3,), {}))
        contract1.m_summary.m_conId = 6
        contract2.m_summary.m_conId = 7
        self.assertEqual(self.wrapper.calldata[6], ("scannerData", (3, 4, contract1, "J1", "K2", "L3", "Y7"), {}))
        self.assertEqual(self.wrapper.calldata[7], ("scannerData", (3, 5, contract2, "V4", "W5", "X6", "Z8"), {}))
        self.assertEqual(self.wrapper.calldata[8], ("scannerDataEnd", (3,), {}))


    def test_readContractDetails(self):
        self.stream.write("1\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x002\x002.5\x00J1\x00K2\x00L3\x00")
        self.stream.write("2\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x002\x002.5\x00J1\x00K2\x00L3\x003\x00")
        self.stream.write("3\x004\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x002\x002.5\x00J1\x00K2\x00L3\x003\x00")
        self.stream.write("4\x004\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x002\x002.5\x00J1\x00K2\x00L3\x003\x005\x00")
        self.stream.seek(0)
        for i in xrange(4): self.reader._readContractDetails()
        self.assertEqual(len(self.wrapper.calldata), 4)
        self.assertEqual(len(self.wrapper.errors), 0)

        contract = ContractDetails()
        contract.m_summary.m_symbol = "A1"
        contract.m_summary.m_secType = "B2"
        contract.m_summary.m_expiry = "C3"
        contract.m_summary.m_strike = 1.5
        contract.m_summary.m_right = "D4"
        contract.m_summary.m_exchange = "E5"
        contract.m_summary.m_currency = "F6"
        contract.m_summary.m_localSymbol = "G7"
        contract.m_marketName = "H8"
        contract.m_tradingClass = "I9"
        contract.m_summary.m_conId = 2
        contract.m_minTick = 2.5
        contract.m_summary.m_multiplier = "J1"
        contract.m_orderTypes = "K2"
        contract.m_validExchanges = "L3"
        self.assertEqual(self.wrapper.calldata[0], ("contractDetails", (-1, contract), {}))
        contract.m_priceMagnifier = 3
        self.assertEqual(self.wrapper.calldata[1], ("contractDetails", (-1, contract), {}))
        self.assertEqual(self.wrapper.calldata[2], ("contractDetails", (4, contract), {}))
        contract.m_underConId = 5
        self.assertEqual(self.wrapper.calldata[3], ("contractDetails", (4, contract), {}))


    def test_readBondContractDetails(self):
        self.stream.write("1\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x001\x001\x001\x00I9\x00J1\x00K2\x00L3\x00M4\x002\x002.5\x00N5\x00O6\x00")
        self.stream.write("2\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x001\x001\x001\x00I9\x00J1\x00K2\x00L3\x00M4\x002\x002.5\x00N5\x00O6\x00P7\x00Q8\x001\x00R9\x00")
        self.stream.write("3\x004\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x001\x001\x001\x00I9\x00J1\x00K2\x00L3\x00M4\x002\x002.5\x00N5\x00O6\x00P7\x00Q8\x001\x00R9\x00")
        self.stream.seek(0)
        for i in xrange(3): self.reader._readBondContractDetails()
        self.assertEqual(len(self.wrapper.calldata), 3)
        self.assertEqual(len(self.wrapper.errors), 0)

        contract = ContractDetails()
        contract.m_summary.m_symbol = "A1"
        contract.m_summary.m_secType = "B2"
        contract.m_cusip = "C3"
        contract.m_coupon = 1.5
        contract.m_maturity = "D4"
        contract.m_issueDate = "E5"
        contract.m_ratings = "F6"
        contract.m_bondType = "G7"
        contract.m_couponType = "H8"
        contract.m_convertible = True
        contract.m_callable = True
        contract.m_putable = True
        contract.m_descAppend = "I9"
        contract.m_summary.m_exchange = "J1"
        contract.m_summary.m_currency = "K2"
        contract.m_marketName = "L3"
        contract.m_tradingClass = "M4"
        contract.m_summary.m_conId = 2
        contract.m_minTick = 2.5
        contract.m_orderTypes = "N5"
        contract.m_validExchanges = "O6"
        self.assertEqual(self.wrapper.calldata[0], ("bondContractDetails", (-1, contract), {}))
        contract.m_nextOptionDate = "P7"
        contract.m_nextOptionType = "Q8"
        contract.m_nextOptionPartial = True
        contract.m_notes = "R9"
        self.assertEqual(self.wrapper.calldata[1], ("bondContractDetails", (-1, contract), {}))
        self.assertEqual(self.wrapper.calldata[2], ("bondContractDetails", (4, contract), {}))


    def test_readExecDetails(self):
        self.stream.write("1\x002\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x003\x002.5\x00")
        self.stream.write("2\x002\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x003\x002.5\x004\x00")
        self.stream.write("3\x002\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x003\x002.5\x004\x005\x00")
        self.stream.write("4\x002\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x003\x002.5\x004\x005\x006\x00")
        self.stream.write("5\x002\x007\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x003\x002.5\x004\x005\x006\x00")
        self.stream.write("6\x002\x007\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x003\x002.5\x004\x005\x006\x008\x003.5\x00")
        self.stream.write("7\x009\x002\x007\x00A1\x00B2\x00C3\x001.5\x00D4\x00E5\x00F6\x00G7\x00H8\x00I9\x00J1\x00K2\x00L3\x003\x002.5\x004\x005\x006\x008\x003.5\x00")
        self.stream.seek(0)
        for i in xrange(7): self.reader._readExecDetails()
        self.assertEqual(len(self.wrapper.calldata), 7)
        self.assertEqual(len(self.wrapper.errors), 0)

        contract = Contract()
        execution = Execution()

        contract.m_symbol = "A1"
        contract.m_secType = "B2"
        contract.m_expiry = "C3"
        contract.m_strike = 1.5
        contract.m_right = "D4"
        contract.m_exchange = "E5"
        contract.m_currency = "F6"
        contract.m_localSymbol = "G7"
        execution.m_orderId = 2
        execution.m_execId = "H8"
        execution.m_time = "I9"
        execution.m_acctNumber = "J1"
        execution.m_exchange = "K2"
        execution.m_side = "L3"
        execution.m_shares = 3
        execution.m_price = 2.5
        self.assertEqual(self.wrapper.calldata[0], ("execDetails", (-1, contract, execution), {}))
        execution.m_permId = 4
        self.assertEqual(self.wrapper.calldata[1], ("execDetails", (-1, contract, execution), {}))
        execution.m_clientId = 5
        self.assertEqual(self.wrapper.calldata[2], ("execDetails", (-1, contract, execution), {}))
        execution.m_liquidation = 6
        self.assertEqual(self.wrapper.calldata[3], ("execDetails", (-1, contract, execution), {}))
        contract.m_conId = 7
        self.assertEqual(self.wrapper.calldata[4], ("execDetails", (-1, contract, execution), {}))
        execution.m_cumQty = 8
        execution.m_avgPrice = 3.5
        self.assertEqual(self.wrapper.calldata[5], ("execDetails", (-1, contract, execution), {}))
        self.assertEqual(self.wrapper.calldata[6], ("execDetails", (9, contract, execution), {}))

    def test_readUpdateMktDepth(self):
        self.stream.write("1\x002\x003\x004\x005\x001.5\x006\x00")
        self.stream.seek(0)
        self.reader._readUpdateMktDepth()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("updateMktDepth", (2,3,4,5,1.5,6), {}))

    def test_readUpdateMktDepthL2(self):
        self.stream.write("1\x002\x003\x00A1\x004\x005\x001.5\x006\x00")
        self.stream.seek(0)
        self.reader._readUpdateMktDepthL2()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("updateMktDepthL2", (2,3,"A1",4,5,1.5,6), {}))

    def test_readUpdateNewsBulletin(self):
        self.stream.write("1\x002\x003\x00A1\x00B2\x00")
        self.stream.seek(0)
        self.reader._readUpdateNewsBulletin()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("updateNewsBulletin", (2,3,"A1","B2"), {}))

    def test_readManagedAccounts(self):
        self.stream.write("1\x00A1\x00")
        self.stream.seek(0)
        self.reader._readManagedAccounts()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("managedAccounts", ("A1",), {}))

    def test__readReceiveFA(self):
        self.stream.write("1\x002\x00A1\x00")
        self.stream.seek(0)
        self.reader._readReceiveFA()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("receiveFA", (2, "A1"), {}))

    def test_readHistoricalData(self):
        self.stream.write("1\x003\x002\x00A1\x001.5\x002.5\x003.5\x004.5\x004\x005.5\x00\x00B2\x006.5\x007.5\x008.5\x009.5\x005\x006.5\x00true\x00")
        self.stream.write("2\x003\x00C3\x00D4\x002\x00A1\x001.5\x002.5\x003.5\x004.5\x004\x005.5\x00f\x00B2\x006.5\x007.5\x008.5\x009.5\x005\x006.5\x00true\x00")
        self.stream.write("3\x003\x00C3\x00D4\x002\x00A1\x001.5\x002.5\x003.5\x004.5\x004\x005.5\x00\x006\x00B2\x006.5\x007.5\x008.5\x009.5\x005\x006.5\x00true\x007\x00")
        self.stream.seek(0)
        for i in xrange(3): self.reader._readHistoricalData()

        self.assertEqual(len(self.wrapper.calldata), 9)
        self.assertEqual(len(self.wrapper.errors), 0)

        self.assertEqual(self.wrapper.calldata[0], ("historicalData", (3,"A1",1.5,2.5,3.5,4.5,4,-1,5.5,False), {}))
        self.assertEqual(self.wrapper.calldata[1], ("historicalData", (3,"B2",6.5,7.5,8.5,9.5,5,-1,6.5,True), {}))
        self.assertEqual(self.wrapper.calldata[2], ("historicalData", (3,'finished',-1,-1,-1,-1,-1,-1,-1,False), {}))
        self.assertEqual(self.wrapper.calldata[3], ("historicalData", (3,"A1",1.5,2.5,3.5,4.5,4,-1,5.5,False), {}))
        self.assertEqual(self.wrapper.calldata[4], ("historicalData", (3,"B2",6.5,7.5,8.5,9.5,5,-1,6.5,True), {}))
        self.assertEqual(self.wrapper.calldata[5], ("historicalData", (3,'finished-C3-D4',-1,-1,-1,-1,-1,-1,-1,False), {}))
        self.assertEqual(self.wrapper.calldata[6], ("historicalData", (3,"A1",1.5,2.5,3.5,4.5,4,6,5.5,False), {}))
        self.assertEqual(self.wrapper.calldata[7], ("historicalData", (3,"B2",6.5,7.5,8.5,9.5,5,7,6.5,True), {}))
        self.assertEqual(self.wrapper.calldata[8], ("historicalData", (3,'finished-C3-D4',-1,-1,-1,-1,-1,-1,-1,False), {}))

    def test_readScannerParameters(self):
        self.stream.write("1\x00A1\x00")
        self.stream.seek(0)
        self.reader._readScannerParameters()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("scannerParameters", ("A1",), {}))

    def test_readCurrentTime(self):
        self.stream.write("1\x001234567890\x00")
        self.stream.seek(0)
        self.reader._readCurrentTime()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("currentTime", (1234567890,), {}))

    def test_readRealtimeBar(self):
        self.stream.write("1\x002\x003\x001.5\x002.5\x003.5\x004.5\x005\x006.5\x007\x00")
        self.stream.seek(0)
        self.reader._readRealtimeBar()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("realtimeBar", (2,3,1.5,2.5,3.5,4.5,5,6.5,7), {}))

    def test_readFundamentalData(self):
        self.stream.write("1\x002\x00A1\x00")
        self.stream.seek(0)
        self.reader._readFundamentalData()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("fundamentalData", (2,"A1"), {}))

    def test_readContractDetailsEnd(self):
        self.stream.write("1\x002\x00")
        self.stream.seek(0)
        self.reader._readContractDetailsEnd()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("contractDetailsEnd", (2,), {}))

    def test_readOpenOrderEnd(self):
        self.stream.write("1\x00")
        self.stream.seek(0)
        self.reader._readOpenOrderEnd()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("openOrderEnd", (), {}))

    def test_readAccountDownloadEnd(self):
        self.stream.write("1\x00A1\x00")
        self.stream.seek(0)
        self.reader._readAccountDownloadEnd()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("accountDownloadEnd", ("A1",), {}))

    def test_readExecDetailsEnd(self):
        self.stream.write("1\x002\x00")
        self.stream.seek(0)
        self.reader._readExecDetailsEnd()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)
        self.assertEqual(self.wrapper.calldata[0], ("execDetailsEnd", (2,), {}))

    def test_readDeltaNeutralValidation(self):
        self.stream.write("1\x002\x003\x004.5\x005.5\x00")
        self.stream.seek(0)
        self.reader._readDeltaNeutralValidation()
        self.assertEqual(len(self.wrapper.calldata), 1)
        self.assertEqual(len(self.wrapper.errors), 0)

        undercomp = UnderComp()
        undercomp.m_conId = 3
        undercomp.m_delta = 4.5
        undercomp.m_price = 5.5
        self.assertEqual(self.wrapper.calldata[0], ("deltaNeutralValidation", (2,undercomp), {}))
