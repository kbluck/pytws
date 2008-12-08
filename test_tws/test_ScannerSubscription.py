'''Unit test package for module "tws._ScannerSubscription".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import ScannerSubscription


class test_ScannerSubscription(unittest.TestCase):
    '''Test type "tws.ScannerSubscription"'''

    def test_init(self):
        test1 = ScannerSubscription()

        self.assertEqual(test1.numberOfRows(), ScannerSubscription.NO_ROW_NUMBER_SPECIFIED)
        self.assertEqual(test1.instrument(), "")
        self.assertEqual(test1.locationCode(), "")
        self.assertEqual(test1.scanCode(), "")
        self.assertEqual(test1.abovePrice(), ScannerSubscription._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.belowPrice(), ScannerSubscription._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.aboveVolume(), ScannerSubscription._INT_MAX_VALUE)
        self.assertEqual(test1.averageOptionVolumeAbove(), ScannerSubscription._INT_MAX_VALUE)
        self.assertEqual(test1.marketCapAbove(), ScannerSubscription._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.marketCapBelow(), ScannerSubscription._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.moodyRatingAbove(), "")
        self.assertEqual(test1.moodyRatingBelow(), "")
        self.assertEqual(test1.spRatingAbove(), "")
        self.assertEqual(test1.spRatingBelow(), "")
        self.assertEqual(test1.maturityDateAbove(), "")
        self.assertEqual(test1.maturityDateBelow(), "")
        self.assertEqual(test1.couponRateAbove(), ScannerSubscription._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.couponRateBelow(), ScannerSubscription._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.excludeConvertible(), "")
        self.assertEqual(test1.scannerSettingPairs(), "")
        self.assertEqual(test1.stockTypeFilter(), "")

    def test_fields(self):
        test = ScannerSubscription()

        test.numberOfRows(1)
        test.instrument("ab")
        test.locationCode("cd")
        test.scanCode("ef")
        test.abovePrice(2.5)
        test.belowPrice(3.5)
        test.aboveVolume(4)
        test.averageOptionVolumeAbove(5)
        test.marketCapAbove(6.5)
        test.marketCapBelow(7.5)
        test.moodyRatingAbove("gh")
        test.moodyRatingBelow("ij")
        test.spRatingAbove("kl")
        test.spRatingBelow("mn")
        test.maturityDateAbove("op")
        test.maturityDateBelow("qr")
        test.couponRateAbove(8.5)
        test.couponRateBelow(9.5)
        test.excludeConvertible("st")
        test.scannerSettingPairs("uv")
        test.stockTypeFilter("wx")

        self.assertEqual(test.numberOfRows(), 1)
        self.assertEqual(test.instrument(), "ab")
        self.assertEqual(test.locationCode(), "cd")
        self.assertEqual(test.scanCode(), "ef")
        self.assertEqual(test.abovePrice(), 2.5)
        self.assertEqual(test.belowPrice(), 3.5)
        self.assertEqual(test.aboveVolume(), 4)
        self.assertEqual(test.averageOptionVolumeAbove(), 5)
        self.assertEqual(test.marketCapAbove(), 6.5)
        self.assertEqual(test.marketCapBelow(), 7.5)
        self.assertEqual(test.moodyRatingAbove(), "gh")
        self.assertEqual(test.moodyRatingBelow(), "ij")
        self.assertEqual(test.spRatingAbove(), "kl")
        self.assertEqual(test.spRatingBelow(), "mn")
        self.assertEqual(test.maturityDateAbove(), "op")
        self.assertEqual(test.maturityDateBelow(), "qr")
        self.assertEqual(test.couponRateAbove(), 8.5)
        self.assertEqual(test.couponRateBelow(), 9.5)
        self.assertEqual(test.excludeConvertible(), "st")
        self.assertEqual(test.scannerSettingPairs(), "uv")
        self.assertEqual(test.stockTypeFilter(), "wx")
