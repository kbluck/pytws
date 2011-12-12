'''Tick type constants.

   Constants and functions identifying types of tick data.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

# Constants

BID_SIZE = 0
BID = 1
ASK = 2
ASK_SIZE = 3
LAST = 4
LAST_SIZE = 5
HIGH = 6
LOW = 7
VOLUME = 8
CLOSE = 9
BID_OPTION = 10
ASK_OPTION = 11
LAST_OPTION = 12
MODEL_OPTION = 13
OPEN = 14
LOW_13_WEEK = 15
HIGH_13_WEEK = 16
LOW_26_WEEK = 17
HIGH_26_WEEK = 18
LOW_52_WEEK = 19
HIGH_52_WEEK = 20
AVG_VOLUME = 21
OPEN_INTEREST = 22
OPTION_HISTORICAL_VOL = 23
OPTION_IMPLIED_VOL = 24
OPTION_BID_EXCH = 25
OPTION_ASK_EXCH = 26
OPTION_CALL_OPEN_INTEREST = 27
OPTION_PUT_OPEN_INTEREST = 28
OPTION_CALL_VOLUME = 29
OPTION_PUT_VOLUME = 30
INDEX_FUTURE_PREMIUM = 31
BID_EXCH = 32
ASK_EXCH = 33
AUCTION_VOLUME = 34
AUCTION_PRICE = 35
AUCTION_IMBALANCE = 36
MARK_PRICE = 37
BID_EFP_COMPUTATION = 38
ASK_EFP_COMPUTATION = 39
LAST_EFP_COMPUTATION = 40
OPEN_EFP_COMPUTATION = 41
HIGH_EFP_COMPUTATION = 42
LOW_EFP_COMPUTATION = 43
CLOSE_EFP_COMPUTATION = 44
LAST_TIMESTAMP = 45
SHORTABLE = 46
FUNDAMENTAL_RATIOS = 47
RT_VOLUME = 48
HALTED = 49
BID_YIELD = 50
ASK_YIELD = 51
LAST_YIELD = 52    
CUST_OPTION_COMPUTATION = 53  
TRADE_COUNT = 54
TRADE_RATE = 55
VOLUME_RATE = 56
LAST_RTH_TRADE = 57


_field_names = {
    BID_SIZE:                   "bidSize",
    BID:                        "bidPrice",
    ASK:                        "askPrice",
    ASK_SIZE:                   "askSize",
    LAST:                       "lastPrice",
    LAST_SIZE:                  "lastSize",
    HIGH:                       "high",
    LOW:                        "low",
    VOLUME:                     "volume",
    CLOSE:                      "close",
    BID_OPTION:                 "bidOptComp",
    ASK_OPTION:                 "askOptComp",
    LAST_OPTION:                "lastOptComp",
    MODEL_OPTION:               "modelOptComp",
    OPEN:                       "open",
    LOW_13_WEEK:                "13WeekLow",
    HIGH_13_WEEK:               "13WeekHigh",
    LOW_26_WEEK:                "26WeekLow",
    HIGH_26_WEEK:               "26WeekHigh",
    LOW_52_WEEK:                "52WeekLow",
    HIGH_52_WEEK:               "52WeekHigh",
    AVG_VOLUME:                 "AvgVolume",
    OPEN_INTEREST:              "OpenInterest",
    OPTION_HISTORICAL_VOL:      "OptionHistoricalVolatility",
    OPTION_IMPLIED_VOL:         "OptionImpliedVolatility",
    OPTION_BID_EXCH:            "OptionBidExchStr",
    OPTION_ASK_EXCH:            "OptionAskExchStr",
    OPTION_CALL_OPEN_INTEREST:  "OptionCallOpenInterest",
    OPTION_PUT_OPEN_INTEREST:   "OptionPutOpenInterest",
    OPTION_CALL_VOLUME:         "OptionCallVolume",
    OPTION_PUT_VOLUME:          "OptionPutVolume",
    INDEX_FUTURE_PREMIUM:       "IndexFuturePremium",
    BID_EXCH:                   "bidExch",
    ASK_EXCH:                   "askExch",
    AUCTION_VOLUME:             "auctionVolume",
    AUCTION_PRICE:              "auctionPrice",
    AUCTION_IMBALANCE:          "auctionImbalance",
    MARK_PRICE:                 "markPrice",
    BID_EFP_COMPUTATION:        "bidEFP",
    ASK_EFP_COMPUTATION:        "askEFP",
    LAST_EFP_COMPUTATION:       "lastEFP",
    OPEN_EFP_COMPUTATION:       "openEFP",
    HIGH_EFP_COMPUTATION:       "highEFP",
    LOW_EFP_COMPUTATION:        "lowEFP",
    CLOSE_EFP_COMPUTATION:      "closeEFP",
    LAST_TIMESTAMP:             "lastTimestamp",
    SHORTABLE:                  "shortable",
    FUNDAMENTAL_RATIOS:         "fundamentals",
    RT_VOLUME:                  "RTVolume",
    HALTED:                     "halted",
    BID_YIELD:                  "bidYield",
    ASK_YIELD:                  "askYield",
    LAST_YIELD:                 "lastYield",             
    CUST_OPTION_COMPUTATION:    "custOptComp",             
    TRADE_COUNT:                "trades",
    TRADE_RATE:                 "trades/min",
    VOLUME_RATE:                "volume/min",             
    LAST_RTH_TRADE:             "lastRTHTrade"             
}


def getField(tick_type):
    return _field_names.get(tick_type, "unknown")
