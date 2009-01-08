'''Unit test package for module "tws._Order".'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

import unittest
from tws import Order


class test_Order(unittest.TestCase):
    '''Test type "tws.Order"'''

    def test_init(self):
        test1 = Order()

        self.assertEqual(test1.m_orderId, 0)
        self.assertEqual(test1.m_clientId, 0)
        self.assertEqual(test1.m_permId, 0)
        self.assertEqual(test1.m_action, Order.EMPTY_STR)
        self.assertEqual(test1.m_totalQuantity, 0)
        self.assertEqual(test1.m_orderType, Order.EMPTY_STR)
        self.assertEqual(test1.m_lmtPrice, 0.0)
        self.assertEqual(test1.m_auxPrice, 0.0)
        self.assertEqual(test1.m_tif, Order.EMPTY_STR)
        self.assertEqual(test1.m_ocaGroup, Order.EMPTY_STR)
        self.assertEqual(test1.m_ocaType, 0)
        self.assertEqual(test1.m_orderRef, Order.EMPTY_STR)
        self.assertEqual(test1.m_transmit, True)
        self.assertEqual(test1.m_parentId, 0)
        self.assertEqual(test1.m_blockOrder, False)
        self.assertEqual(test1.m_sweepToFill, False)
        self.assertEqual(test1.m_displaySize, 0)
        self.assertEqual(test1.m_triggerMethod, 0)
        self.assertEqual(test1.m_outsideRth, False)
        self.assertEqual(test1.m_hidden, False)
        self.assertEqual(test1.m_goodAfterTime, Order.EMPTY_STR)
        self.assertEqual(test1.m_goodTillDate, Order.EMPTY_STR)
        self.assertEqual(test1.m_overridePercentageConstraints, False)
        self.assertEqual(test1.m_rule80A, Order.EMPTY_STR)
        self.assertEqual(test1.m_allOrNone, False)
        self.assertEqual(test1.m_minQty, Order._INT_MAX_VALUE)
        self.assertEqual(test1.m_percentOffset, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_trailStopPrice, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_faGroup, Order.EMPTY_STR)
        self.assertEqual(test1.m_faProfile, Order.EMPTY_STR)
        self.assertEqual(test1.m_faMethod, Order.EMPTY_STR)
        self.assertEqual(test1.m_faPercentage, Order.EMPTY_STR)
        self.assertEqual(test1.m_openClose, "O")
        self.assertEqual(test1.m_origin, Order.CUSTOMER)
        self.assertEqual(test1.m_shortSaleSlot, 0)
        self.assertEqual(test1.m_designatedLocation, Order.EMPTY_STR)
        self.assertEqual(test1.m_discretionaryAmt, 0.0)
        self.assertEqual(test1.m_eTradeOnly, False)
        self.assertEqual(test1.m_firmQuoteOnly, False)
        self.assertEqual(test1.m_nbboPriceCap, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_auctionStrategy, 0)
        self.assertEqual(test1.m_startingPrice, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_stockRefPrice, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_delta, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_stockRangeLower, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_stockRangeUpper, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_volatility, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_volatilityType, Order._INT_MAX_VALUE)
        self.assertEqual(test1.m_continuousUpdate, 0)
        self.assertEqual(test1.m_referencePriceType, Order._INT_MAX_VALUE)
        self.assertEqual(test1.m_deltaNeutralOrderType, Order.EMPTY_STR)
        self.assertEqual(test1.m_deltaNeutralAuxPrice, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_basisPoints, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_basisPointsType, Order._INT_MAX_VALUE)
        self.assertEqual(test1.m_scaleInitLevelSize, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_scaleSubsLevelSize, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_scalePriceIncrement, Order._DOUBLE_MAX_VALUE)
        self.assertEqual(test1.m_account, Order.EMPTY_STR)
        self.assertEqual(test1.m_settlingFirm, Order.EMPTY_STR)
        self.assertEqual(test1.m_clearingAccount, Order.EMPTY_STR)
        self.assertEqual(test1.m_clearingIntent, Order.EMPTY_STR)
        self.assertEqual(test1.m_algoStrategy, Order.EMPTY_STR)
        self.assertEqual(test1.m_algoParams, [])
        self.assertEqual(test1.m_whatIf, False)

    def test_fields(self):
        test = Order()

        test.m_orderId = 1
        test.m_clientId = 2
        test.m_permId = 3
        test.m_action = 'a1'
        test.m_totalQuantity = 4
        test.m_orderType = 'b2'
        test.m_lmtPrice = 1.5
        test.m_auxPrice = 2.5
        test.m_tif = 'c3'
        test.m_ocaGroup = 'd4'
        test.m_ocaType = 5
        test.m_orderRef = 'e5'
        test.m_transmit = False
        test.m_parentId = 6
        test.m_blockOrder = True
        test.m_sweepToFill = True
        test.m_displaySize = 7
        test.m_triggerMethod = 8
        test.m_outsideRth = True
        test.m_hidden = True
        test.m_goodAfterTime = 'f7'
        test.m_goodTillDate = 'g8'
        test.m_overridePercentageConstraints = True
        test.m_rule80A = 'h9'
        test.m_allOrNone = True
        test.m_minQty = 9
        test.m_percentOffset = 3.5
        test.m_trailStopPrice = 4.5
        test.m_faGroup = 'i1'
        test.m_faProfile = 'j2'
        test.m_faMethod = 'k3'
        test.m_faPercentage = 'l4'
        test.m_openClose = "1"
        test.m_origin = Order.FIRM
        test.m_shortSaleSlot = 10
        test.m_designatedLocation = 'm5'
        test.m_discretionaryAmt = 5.5
        test.m_eTradeOnly = True
        test.m_firmQuoteOnly = True
        test.m_nbboPriceCap = 6.5
        test.m_auctionStrategy = 11
        test.m_startingPrice = 7.5
        test.m_stockRefPrice = 8.5
        test.m_delta = 9.5
        test.m_stockRangeLower = 10.5
        test.m_stockRangeUpper = 11.5
        test.m_volatility = 12.5
        test.m_volatilityType = 12
        test.m_continuousUpdate = 13
        test.m_referencePriceType = 14
        test.m_deltaNeutralOrderType = 'n6'
        test.m_deltaNeutralAuxPrice = 13.5
        test.m_basisPoints = 14.5
        test.m_basisPointsType = 15
        test.m_scaleInitLevelSize = 15.5
        test.m_scaleSubsLevelSize = 16.5
        test.m_scalePriceIncrement = 17.5
        test.m_account = 'o7'
        test.m_settlingFirm = 'p8'
        test.m_clearingAccount = 'q9'
        test.m_clearingIntent = 'r1'
        test.m_algoStrategy = 's2'
        test.m_algoParams = ['t3','u4']
        test.m_whatIf = True

        self.assertEqual(test.m_orderId, 1)
        self.assertEqual(test.m_clientId, 2)
        self.assertEqual(test.m_permId, 3)
        self.assertEqual(test.m_action, 'a1')
        self.assertEqual(test.m_totalQuantity, 4)
        self.assertEqual(test.m_orderType, 'b2')
        self.assertEqual(test.m_lmtPrice, 1.5)
        self.assertEqual(test.m_auxPrice, 2.5)
        self.assertEqual(test.m_tif, 'c3')
        self.assertEqual(test.m_ocaGroup, 'd4')
        self.assertEqual(test.m_ocaType, 5)
        self.assertEqual(test.m_orderRef, 'e5')
        self.assertEqual(test.m_transmit, False)
        self.assertEqual(test.m_parentId, 6)
        self.assertEqual(test.m_blockOrder, True)
        self.assertEqual(test.m_sweepToFill, True)
        self.assertEqual(test.m_displaySize, 7)
        self.assertEqual(test.m_triggerMethod, 8)
        self.assertEqual(test.m_outsideRth, True)
        self.assertEqual(test.m_hidden, True)
        self.assertEqual(test.m_goodAfterTime, 'f7')
        self.assertEqual(test.m_goodTillDate, 'g8')
        self.assertEqual(test.m_overridePercentageConstraints, True)
        self.assertEqual(test.m_rule80A, 'h9')
        self.assertEqual(test.m_allOrNone, True)
        self.assertEqual(test.m_minQty, 9)
        self.assertEqual(test.m_percentOffset, 3.5)
        self.assertEqual(test.m_trailStopPrice, 4.5)
        self.assertEqual(test.m_faGroup, 'i1')
        self.assertEqual(test.m_faProfile, 'j2')
        self.assertEqual(test.m_faMethod, 'k3')
        self.assertEqual(test.m_faPercentage, 'l4')
        self.assertEqual(test.m_openClose, "1")
        self.assertEqual(test.m_origin, Order.FIRM)
        self.assertEqual(test.m_shortSaleSlot, 10)
        self.assertEqual(test.m_designatedLocation, 'm5')
        self.assertEqual(test.m_discretionaryAmt, 5.5)
        self.assertEqual(test.m_eTradeOnly, True)
        self.assertEqual(test.m_firmQuoteOnly, True)
        self.assertEqual(test.m_nbboPriceCap, 6.5)
        self.assertEqual(test.m_auctionStrategy, 11)
        self.assertEqual(test.m_startingPrice, 7.5)
        self.assertEqual(test.m_stockRefPrice, 8.5)
        self.assertEqual(test.m_delta, 9.5)
        self.assertEqual(test.m_stockRangeLower, 10.5)
        self.assertEqual(test.m_stockRangeUpper, 11.5)
        self.assertEqual(test.m_volatility, 12.5)
        self.assertEqual(test.m_volatilityType, 12)
        self.assertEqual(test.m_continuousUpdate, 13)
        self.assertEqual(test.m_referencePriceType, 14)
        self.assertEqual(test.m_deltaNeutralOrderType, 'n6')
        self.assertEqual(test.m_deltaNeutralAuxPrice, 13.5)
        self.assertEqual(test.m_basisPoints, 14.5)
        self.assertEqual(test.m_basisPointsType, 15)
        self.assertEqual(test.m_scaleInitLevelSize, 15.5)
        self.assertEqual(test.m_scaleSubsLevelSize, 16.5)
        self.assertEqual(test.m_scalePriceIncrement, 17.5)
        self.assertEqual(test.m_account, 'o7')
        self.assertEqual(test.m_settlingFirm, 'p8')
        self.assertEqual(test.m_clearingAccount, 'q9')
        self.assertEqual(test.m_clearingIntent, 'r1')
        self.assertEqual(test.m_algoStrategy, 's2')
        self.assertEqual(test.m_algoParams, ['t3','u4'])
        self.assertEqual(test.m_whatIf, True)

    def test_equals(self):
        test1 = Order()
        test2 = Order()
        test3 = Order()
        test4 = Order()

        test3.m_permId = 3

        test4.m_orderId = 1
        test4.m_clientId = 2
        test4.m_permId = 3
        test4.m_action = 'a1'
        test4.m_totalQuantity = 4
        test4.m_orderType = 'b2'
        test4.m_lmtPrice = 1.5
        test4.m_auxPrice = 2.5
        test4.m_tif = 'c3'
        test4.m_ocaGroup = 'd4'
        test4.m_ocaType = 5
        test4.m_orderRef = 'e5'
        test4.m_transmit = False
        test4.m_parentId = 6
        test4.m_blockOrder = True
        test4.m_sweepToFill = True
        test4.m_displaySize = 7
        test4.m_triggerMethod = 8
        test4.m_outsideRth = True
        test4.m_hidden = True
        test4.m_goodAfterTime = 'f7'
        test4.m_goodTillDate = 'g8'
        test4.m_overridePercentageConstraints = True
        test4.m_rule80A = 'h9'
        test4.m_allOrNone = True
        test4.m_minQty = 9
        test4.m_percentOffset = 3.5
        test4.m_trailStopPrice = 4.5
        test4.m_faGroup = 'i1'
        test4.m_faProfile = 'j2'
        test4.m_faMethod = 'k3'
        test4.m_faPercentage = 'l4'
        test4.m_openClose = "1"
        test4.m_origin = Order.FIRM
        test4.m_shortSaleSlot = 10
        test4.m_designatedLocation = 'm5'
        test4.m_discretionaryAmt = 5.5
        test4.m_eTradeOnly = True
        test4.m_firmQuoteOnly = True
        test4.m_nbboPriceCap = 6.5
        test4.m_auctionStrategy = 11
        test4.m_startingPrice = 7.5
        test4.m_stockRefPrice = 8.5
        test4.m_delta = 9.5
        test4.m_stockRangeLower = 10.5
        test4.m_stockRangeUpper = 11.5
        test4.m_volatility = 12.5
        test4.m_volatilityType = 12
        test4.m_continuousUpdate = 13
        test4.m_referencePriceType = 14
        test4.m_deltaNeutralOrderType = 'n6'
        test4.m_deltaNeutralAuxPrice = 13.5
        test4.m_basisPoints = 14.5
        test4.m_basisPointsType = 15
        test4.m_scaleInitLevelSize = 15.5
        test4.m_scaleSubsLevelSize = 16.5
        test4.m_scalePriceIncrement = 17.5
        test4.m_account = 'o7'
        test4.m_settlingFirm = 'p8'
        test4.m_clearingAccount = 'q9'
        test4.m_clearingIntent = 'r1'
        test4.m_algoStrategy = 's2'
        test4.m_algoParams = ['t3','u4']
        test4.m_whatIf = True

        self.assertEqual(test1, test1)
        self.assertEqual(test1, test2)
        self.assertNotEqual(test1, None)
        self.assertNotEqual(test1, "")
        self.assertEqual(test3, test3)
        self.assertEqual(test3, test4)
        self.assertEqual(test1, test3)    # Strange but true. IB bug?
        self.assertNotEqual(test1, test4)
