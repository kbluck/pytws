'''Unit test package for module "tws._TickType".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws.TickType as TickType


class test_TickType(unittest.TestCase):
    '''Test module "tws.TickType"'''

    def test_constants(self):
        # Representative values
        self.assertEqual(TickType.BID_SIZE, 0)
        self.assertEqual(TickType.BID, 1)
        self.assertEqual(TickType.ASK, 2)
        self.assertEqual(TickType.LAST, 4)
        self.assertEqual(TickType.FUNDAMENTAL_RATIOS, 47)

    def test_getField(self):
        # Representative values
        self.assertEqual(TickType.getField(TickType.BID_SIZE), "bidSize")
        self.assertEqual(TickType.getField(TickType.BID), "bidPrice")
        self.assertEqual(TickType.getField(TickType.ASK), "askPrice")
        self.assertEqual(TickType.getField(TickType.LAST), "lastPrice")
        self.assertEqual(TickType.getField(TickType.FUNDAMENTAL_RATIOS), "fundamentals")
        self.assertEqual(TickType.getField(48), "unknown")
