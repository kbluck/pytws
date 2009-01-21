'''Order data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from tws import _Util


class Order(object):
    '''Data structure with attributes used to describe an order.
    '''

    def __init__(self):
        self.m_orderId = 0
        self.m_clientId = 0
        self.m_permId = 0
        self.m_action = self.EMPTY_STR
        self.m_totalQuantity = 0
        self.m_orderType = self.EMPTY_STR
        self.m_lmtPrice = 0.0
        self.m_auxPrice = 0.0
        self.m_tif = self.EMPTY_STR
        self.m_ocaGroup = self.EMPTY_STR
        self.m_ocaType = 0
        self.m_orderRef = self.EMPTY_STR
        self.m_transmit = True
        self.m_parentId = 0
        self.m_blockOrder = False
        self.m_sweepToFill = False
        self.m_displaySize = 0
        self.m_triggerMethod = 0
        self.m_outsideRth = False
        self.m_hidden = False
        self.m_goodAfterTime = self.EMPTY_STR
        self.m_goodTillDate = self.EMPTY_STR
        self.m_overridePercentageConstraints = False
        self.m_rule80A = self.EMPTY_STR
        self.m_allOrNone = False
        self.m_minQty = self._INT_MAX_VALUE
        self.m_percentOffset = self._DOUBLE_MAX_VALUE
        self.m_trailStopPrice = self._DOUBLE_MAX_VALUE
        self.m_faGroup = self.EMPTY_STR
        self.m_faProfile = self.EMPTY_STR
        self.m_faMethod = self.EMPTY_STR
        self.m_faPercentage = self.EMPTY_STR
        self.m_openClose = "O"
        self.m_origin = self.CUSTOMER
        self.m_shortSaleSlot = 0
        self.m_designatedLocation = self.EMPTY_STR
        self.m_discretionaryAmt = 0.0
        self.m_eTradeOnly = False
        self.m_firmQuoteOnly = False
        self.m_nbboPriceCap = self._DOUBLE_MAX_VALUE
        self.m_auctionStrategy = 0
        self.m_startingPrice = self._DOUBLE_MAX_VALUE
        self.m_stockRefPrice = self._DOUBLE_MAX_VALUE
        self.m_delta = self._DOUBLE_MAX_VALUE
        self.m_stockRangeLower = self._DOUBLE_MAX_VALUE
        self.m_stockRangeUpper = self._DOUBLE_MAX_VALUE
        self.m_volatility = self._DOUBLE_MAX_VALUE
        self.m_volatilityType = self._INT_MAX_VALUE
        self.m_continuousUpdate = 0
        self.m_referencePriceType = self._INT_MAX_VALUE
        self.m_deltaNeutralOrderType = self.EMPTY_STR
        self.m_deltaNeutralAuxPrice = self._DOUBLE_MAX_VALUE
        self.m_basisPoints = self._DOUBLE_MAX_VALUE
        self.m_basisPointsType = self._INT_MAX_VALUE
        self.m_scaleInitLevelSize = self._INT_MAX_VALUE
        self.m_scaleSubsLevelSize = self._INT_MAX_VALUE
        self.m_scalePriceIncrement = self._DOUBLE_MAX_VALUE
        self.m_account = self.EMPTY_STR
        self.m_settlingFirm = self.EMPTY_STR
        self.m_clearingAccount = self.EMPTY_STR
        self.m_clearingIntent = self.EMPTY_STR
        self.m_algoStrategy = self.EMPTY_STR
        self.m_algoParams = []
        self.m_whatIf = False


    def __eq__(self, other):
        if not isinstance(other, self.__class__): return False
        if (self.m_permId == other.m_permId): return True
        return True if (
            (self.m_orderId == other.m_orderId) and
            (self.m_clientId == other.m_clientId) and
            (self.m_totalQuantity == other.m_totalQuantity) and
            (self.m_lmtPrice == other.m_lmtPrice) and
            (self.m_auxPrice == other.m_auxPrice) and
            (self.m_ocaType == other.m_ocaType) and
            (self.m_transmit == other.m_transmit) and
            (self.m_parentId == other.m_parentId) and
            (self.m_blockOrder == other.m_blockOrder) and
            (self.m_sweepToFill == other.m_sweepToFill) and
            (self.m_displaySize == other.m_displaySize) and
            (self.m_triggerMethod == other.m_triggerMethod) and
            (self.m_outsideRth == other.m_outsideRth) and
            (self.m_hidden == other.m_hidden) and
            (self.m_overridePercentageConstraints == other.m_overridePercentageConstraints) and
            (self.m_allOrNone == other.m_allOrNone) and
            (self.m_minQty == other.m_minQty) and
            (self.m_percentOffset == other.m_percentOffset) and
            (self.m_trailStopPrice == other.m_trailStopPrice) and
            (self.m_origin == other.m_origin) and
            (self.m_shortSaleSlot == other.m_shortSaleSlot) and
            (self.m_discretionaryAmt == other.m_discretionaryAmt) and
            (self.m_eTradeOnly == other.m_eTradeOnly) and
            (self.m_firmQuoteOnly == other.m_firmQuoteOnly) and
            (self.m_nbboPriceCap == other.m_nbboPriceCap) and
            (self.m_auctionStrategy == other.m_auctionStrategy) and
            (self.m_startingPrice == other.m_startingPrice) and
            (self.m_stockRefPrice == other.m_stockRefPrice) and
            (self.m_delta == other.m_delta) and
            (self.m_stockRangeLower == other.m_stockRangeLower) and
            (self.m_stockRangeUpper == other.m_stockRangeUpper) and
            (self.m_volatility == other.m_volatility) and
            (self.m_volatilityType == other.m_volatilityType) and
            (self.m_continuousUpdate == other.m_continuousUpdate) and
            (self.m_referencePriceType == other.m_referencePriceType) and
            (self.m_deltaNeutralAuxPrice == other.m_deltaNeutralAuxPrice) and
            (self.m_basisPoints == other.m_basisPoints) and
            (self.m_basisPointsType == other.m_basisPointsType) and
            (self.m_scaleInitLevelSize == other.m_scaleInitLevelSize) and
            (self.m_scaleSubsLevelSize == other.m_scaleSubsLevelSize) and
            (self.m_scalePriceIncrement == other.m_scalePriceIncrement) and
            (self.m_whatIf == other.m_whatIf) and
            (self.m_action == other.m_action) and
            (self.m_orderType == other.m_orderType) and
            (self.m_tif == other.m_tif) and
            (self.m_ocaGroup == other.m_ocaGroup) and
            (self.m_orderRef == other.m_orderRef) and
            (self.m_goodAfterTime == other.m_goodAfterTime)and
            (self.m_goodTillDate == other.m_goodTillDate) and
            (self.m_rule80A == other.m_rule80A) and
            (self.m_faGroup == other.m_faGroup) and
            (self.m_faProfile == other.m_faProfile) and
            (self.m_faMethod == other.m_faMethod) and
            (self.m_faPercentage == other.m_faPercentage) and
            (self.m_openClose == other.m_openClose) and
            (self.m_designatedLocation == other.m_designatedLocation) and
            (self.m_deltaNeutralOrderType == other.m_deltaNeutralOrderType) and
            (self.m_account == other.m_account) and
            (self.m_settlingFirm == other.m_settlingFirm) and
            (self.m_clearingAccount == other.m_clearingAccount)and
            (self.m_clearingIntent == other.m_clearingIntent) and
            (self.m_algoStrategy == other.m_algoStrategy) and
             _Util.VectorEqualsUnordered(self.m_algoParams, other.m_algoParams)
        ) else False


    # Class constants
    CUSTOMER = 0
    FIRM = 1
    OPT_UNKNOWN = '?'
    OPT_BROKER_DEALER = 'b'
    OPT_CUSTOMER = 'c'
    OPT_FIRM = 'f'
    OPT_ISEMM = 'm'
    OPT_FARMM = 'n'
    OPT_SPECIALIST = 'y'
    AUCTION_MATCH = 1
    AUCTION_IMPROVEMENT = 2
    AUCTION_TRANSPARENT = 3
    EMPTY_STR = ""

    from tws._Util import _INT_MAX_VALUE
    from tws._Util import _DOUBLE_MAX_VALUE
