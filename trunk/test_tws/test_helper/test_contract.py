'''Unit test package for module "tws.helper._contract".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws.helper import StockContract, FuturesContract
from tws import UnderComp


class test_helper_StockContract(unittest.TestCase):
    '''Test type "tws.helper.StockContract"'''

    def test_init(self):
        self.assertRaises(TypeError, StockContract)
        
        test1 = StockContract("IBM")
        test2 = StockContract("SGE", "LSE", "GBP", con_id=1)

        self.assertEqual(test1.m_conId, 0)
        self.assertEqual(test1.m_symbol, "IBM")
        self.assertEqual(test1.m_secType, "STK")
        self.assertEqual(test1.m_expiry, "")
        self.assertEqual(test1.m_strike, 0.0)
        self.assertEqual(test1.m_right, "")
        self.assertEqual(test1.m_multiplier, "")
        self.assertEqual(test1.m_exchange, "SMART")
        self.assertEqual(test1.m_currency, "USD")
        self.assertEqual(test1.m_localSymbol, "")
        self.assertEqual(test1.m_comboLegs, [])
        self.assertEqual(test1.m_primaryExch, "")
        self.assertEqual(test1.m_includeExpired, False)
        self.assertEqual(test1.m_comboLegsDescrip, "")
        self.assertEqual(test1.m_underComp, UnderComp())

        self.assertEqual(test2.m_conId, 1)
        self.assertEqual(test2.m_symbol, "SGE")
        self.assertEqual(test2.m_secType, "STK")
        self.assertEqual(test2.m_expiry, "")
        self.assertEqual(test2.m_strike, 0.0)
        self.assertEqual(test2.m_right, "")
        self.assertEqual(test2.m_multiplier, "")
        self.assertEqual(test2.m_exchange, "LSE")
        self.assertEqual(test2.m_currency, "GBP")
        self.assertEqual(test2.m_localSymbol, "")
        self.assertEqual(test2.m_comboLegs, [])
        self.assertEqual(test2.m_primaryExch, "")
        self.assertEqual(test2.m_includeExpired, False)
        self.assertEqual(test2.m_comboLegsDescrip, "")
        self.assertEqual(test2.m_underComp, UnderComp())


class test_helper_FuturesContract(unittest.TestCase):
    '''Test type "tws.helper.FuturesContract"'''

    def test_init(self):
        self.assertRaises(TypeError, FuturesContract)
        
        test1 = FuturesContract("GLOBEX", local_symbol="NQH9")
        test2 = FuturesContract("ECBOT", "YM", "200903", con_id=2)

        self.assertEqual(test1.m_conId, 0)
        self.assertEqual(test1.m_symbol, "")
        self.assertEqual(test1.m_secType, "FUT")
        self.assertEqual(test1.m_expiry, "")
        self.assertEqual(test1.m_strike, 0.0)
        self.assertEqual(test1.m_right, "")
        self.assertEqual(test1.m_multiplier, "")
        self.assertEqual(test1.m_exchange, "GLOBEX")
        self.assertEqual(test1.m_currency, "USD")
        self.assertEqual(test1.m_localSymbol, "NQH9")
        self.assertEqual(test1.m_comboLegs, [])
        self.assertEqual(test1.m_primaryExch, "")
        self.assertEqual(test1.m_includeExpired, False)
        self.assertEqual(test1.m_comboLegsDescrip, "")
        self.assertEqual(test1.m_underComp, UnderComp())

        self.assertEqual(test2.m_conId, 2)
        self.assertEqual(test2.m_symbol, "YM")
        self.assertEqual(test2.m_secType, "FUT")
        self.assertEqual(test2.m_expiry, "200903")
        self.assertEqual(test2.m_strike, 0.0)
        self.assertEqual(test2.m_right, "")
        self.assertEqual(test2.m_multiplier, "")
        self.assertEqual(test2.m_exchange, "ECBOT")
        self.assertEqual(test2.m_currency, "USD")
        self.assertEqual(test2.m_localSymbol, "")
        self.assertEqual(test2.m_comboLegs, [])
        self.assertEqual(test2.m_primaryExch, "")
        self.assertEqual(test2.m_includeExpired, False)
        self.assertEqual(test2.m_comboLegsDescrip, "")
        self.assertEqual(test2.m_underComp, UnderComp())

        if __debug__:
            self.assertRaises(AssertionError, FuturesContract,"X",symbol="X")
            self.assertRaises(AssertionError, FuturesContract,"X",expiry="X")
            