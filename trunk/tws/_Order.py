'''Order data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from tws import _Util


class Order(object):
    '''Data structure with attributes used to describe an order.
    '''

    def __init__(self):
        #main order fields
	self.m_orderId = 0
        self.m_clientId = 0
        self.m_permId = 0
        self.m_action = self.EMPTY_STR
        self.m_totalQuantity = 0
        self.m_orderType = self.EMPTY_STR
        self.m_lmtPrice = 0.0
        self.m_auxPrice = 0.0
        
	#extended order fields
	self.m_tif = self.EMPTY_STR #"Time in Force" - DAY, GTC, etc.
        self.m_ocaGroup = self.EMPTY_STR #once cancels all group names
        self.m_ocaType = 0 #1 = CANCEL_WITH_BLOCK, 2 = REDUCE_WITH_BLOCK, 3 = REDUCE_NON_BLOCK
        self.m_orderRef = self.EMPTY_STR 
        self.m_transmit = True #if false, order will be created but not transmited
        self.m_parentId = 0 #Parent order Id, to associate Auto STP or TRAIL orders with the original order.
        self.m_blockOrder = False
        self.m_sweepToFill = False
        self.m_displaySize = 0
        self.m_triggerMethod = 0 # 0=Default, 1=Double_Bid_Ask, 2=Last, 3=Double_Last, 4=Bid_Ask, 7=Last_or_Bid_Ask, 8=Mid-point
        self.m_outsideRth = False
        self.m_hidden = False
        self.m_goodAfterTime = self.EMPTY_STR #FORMAT: 20060505 08:00:00 {time zone}
        self.m_goodTillDate = self.EMPTY_STR #FORMAT: 20060505 08:00:00 {time zone}
        self.m_overridePercentageConstraints = False
        self.m_rule80A = self.EMPTY_STR #Individual = 'I', Agency = 'A', AgentOtherMember = 'W', IndividualPTIA = 'J', AgencyPTIA = 'U', AgentOtherMemberPTIA = 'M', IndividualPT = 'K', AgencyPT = 'Y', AgentOtherMemberPT = 'N'
        self.m_allOrNone = False
        self.m_minQty = self._INT_MAX_VALUE
        self.m_percentOffset = self._DOUBLE_MAX_VALUE #REL orders only 
        self.m_trailStopPrice = self._DOUBLE_MAX_VALUE #for TRAILLIMIT orders only
        
	#Financial advisors only 
        self.m_faGroup = self.EMPTY_STR
        self.m_faProfile = self.EMPTY_STR
        self.m_faMethod = self.EMPTY_STR
        self.m_faPercentage = self.EMPTY_STR
        
	#Institutional orders only
	self.m_openClose = "O" #O=Open, C=Close
        self.m_origin = self.CUSTOMER #0=Customer, 1=Firm
        self.m_shortSaleSlot = 0 # if you hold the shares, 2 if they will be delivered from elsewhere.  Only for Action="SSHORT
        self.m_designatedLocation = self.EMPTY_STR #set when slot=2 only.
        self.m_exemptCode = -1 

	#SMART routing only
	self.m_discretionaryAmt = 0.0
        self.m_eTradeOnly = False
        self.m_firmQuoteOnly = False
        self.m_nbboPriceCap = self._DOUBLE_MAX_VALUE

	#BOX or VOL ORDERS ONLY	
        self.m_auctionStrategy = 0 #1=AUCTION_MATCH, 2=AUCTION_IMPROVEMENT, 3=AUCTION_TRANSPARENT
        
	#BOX ORDERS ONLY
	self.m_startingPrice = self._DOUBLE_MAX_VALUE
        self.m_stockRefPrice = self._DOUBLE_MAX_VALUE
        self.m_delta = self._DOUBLE_MAX_VALUE

	#pegged to stock or VOL orders
        self.m_stockRangeLower = self._DOUBLE_MAX_VALUE
        self.m_stockRangeUpper = self._DOUBLE_MAX_VALUE
        
	#VOLATILITY ORDERS ONLY
	self.m_volatility = self._DOUBLE_MAX_VALUE
        self.m_volatilityType = self._INT_MAX_VALUE # 1=daily, 2=annual
        self.m_continuousUpdate = 0
        self.m_referencePriceType = self._INT_MAX_VALUE #1=Average, 2 = BidOrAsk
        self.m_deltaNeutralOrderType = self.EMPTY_STR
        self.m_deltaNeutralAuxPrice = self._DOUBLE_MAX_VALUE
        
	#COMBO ORDERS ONLY
	self.m_basisPoints = self._DOUBLE_MAX_VALUE #EFP orders only
        self.m_basisPointsType = self._INT_MAX_VALUE #EFP orders only
        
	#SCALE ORDERS ONLY
	self.m_scaleInitLevelSize = self._INT_MAX_VALUE
        self.m_scaleSubsLevelSize = self._INT_MAX_VALUE
        self.m_scalePriceIncrement = self._DOUBLE_MAX_VALUE
        
	# Clearing info
	self.m_account = self.EMPTY_STR #IB account
        self.m_settlingFirm = self.EMPTY_STR
        self.m_clearingAccount = self.EMPTY_STR #True beneficiary of the order
        self.m_clearingIntent = self.EMPTY_STR #"" (Default), "IB", "Away", "PTA" (PostTrade)
        
	#ALGO ORDERS ONLY
	self.m_algoStrategy = self.EMPTY_STR
        self.m_algoParams = []
        
	#What-if
	self.m_whatIf = False

	#Not Held
	self.m_notHeld = False

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
	    (self.m_notHeld == other.m_notHeld) and
	    (self.m_exemptCode == other.m_exemptCode) and
            (self.m_action.lower() == other.m_action.lower()) and
            (self.m_orderType.lower() == other.m_orderType.lower()) and
            (self.m_tif.lower() == other.m_tif.lower()) and
            (self.m_ocaGroup.lower() == other.m_ocaGroup.lower()) and
            (self.m_orderRef.lower() == other.m_orderRef.lower()) and
            (self.m_goodAfterTime.lower() == other.m_goodAfterTime.lower())and
            (self.m_goodTillDate.lower() == other.m_goodTillDate.lower()) and
            (self.m_rule80A.lower() == other.m_rule80A.lower()) and
            (self.m_faGroup.lower() == other.m_faGroup.lower()) and
            (self.m_faProfile.lower() == other.m_faProfile.lower()) and
            (self.m_faMethod.lower() == other.m_faMethod.lower()) and
            (self.m_faPercentage.lower() == other.m_faPercentage.lower()) and
            (self.m_openClose.lower() == other.m_openClose.lower()) and
            (self.m_designatedLocation.lower() == other.m_designatedLocation.lower()) and
            (self.m_deltaNeutralOrderType.lower() == other.m_deltaNeutralOrderType.lower()) and
            (self.m_account.lower() == other.m_account.lower()) and
            (self.m_settlingFirm.lower() == other.m_settlingFirm.lower()) and
            (self.m_clearingAccount.lower() == other.m_clearingAccount.lower())and
            (self.m_clearingIntent.lower() == other.m_clearingIntent.lower()) and
            (self.m_algoStrategy.lower() == other.m_algoStrategy.lower()) and
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
