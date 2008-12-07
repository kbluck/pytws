'''ScannerSubscription data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class ScannerSubscription(object):
    '''Data structure containing attributes used to describe the elements
       of a market scan.
       
       Somebody at IB decided to undertake a completely superfluous exercise
       in overloaded "getter/setter" methods for absolutely no useful reason
       that I can see. Grr...
    '''

    def __init__(self):
        self._numberOfRows = self.NO_ROW_NUMBER_SPECIFIED
        self._instrument = ""
        self._locationCode = ""
        self._scanCode = ""
        self._abovePrice = self._DOUBLE_MAX_VALUE
        self._belowPrice = self._DOUBLE_MAX_VALUE
        self._aboveVolume = self._INT_MAX_VALUE
        self._averageOptionVolumeAbove = self._INT_MAX_VALUE
        self._marketCapAbove = self._DOUBLE_MAX_VALUE
        self._marketCapBelow = self._DOUBLE_MAX_VALUE
        self._moodyRatingAbove = ""
        self._moodyRatingBelow = ""
        self._spRatingAbove = ""
        self._spRatingBelow = ""
        self._maturityDateAbove = ""
        self._maturityDateBelow = ""
        self._couponRateAbove = self._DOUBLE_MAX_VALUE
        self._couponRateBelow = self._DOUBLE_MAX_VALUE
        self._excludeConvertible = ""
        self._scannerSettingPairs = ""
        self._stockTypeFilter = ""


    def numberOfRows(self, num=None):
        '''Number of rows of data to return for a query.'''
        if num != None: self._numberOfRows = num
        return self._numberOfRows if num == None else None


    def instrument(self, txt=None):
        '''Instrument type for the scan.'''
        if txt != None: self._instrument = txt
        return self._instrument if txt == None else None


    def locationCode(self, txt=None):
        '''The scan location. Currently the only valid location is US stocks.'''
        if txt != None: self._locationCode = txt
        return self._locationCode if txt == None else None


    def scanCode(self, txt=None):
        '''Can be left blank.'''
        if txt != None: self._scanCode = txt
        return self._scanCode if txt == None else None


    def abovePrice(self, price=None):
        '''Filter out contracts with a price lower than this value. Can be left blank.'''
        if price != None: self._abovePrice = price
        return self._abovePrice if price == None else None


    def belowPrice(self, price=None):
        '''Filter out contracts with a price higher than this value. Can be left blank.'''
        if price != None: self._belowPrice = price
        return self._belowPrice if price == None else None


    def aboveVolume(self, volume=None):
        '''Filter out contracts with a volume lower than this value. Can be left blank.'''
        if volume != None: self._aboveVolume = volume
        return self._aboveVolume if volume == None else None


    def averageOptionVolumeAbove(self, volume=None):
        '''Filter out contracts with an option volume lower than this value. Can be left blank.'''
        if volume != None: self._averageOptionVolumeAbove = volume
        return self._averageOptionVolumeAbove if volume == None else None


    def marketCapAbove(self, cap=None):
        '''Filter out contracts with a market cap below this value. Can be left blank.'''
        if cap != None: self._marketCapAbove = cap
        return self._marketCapAbove if cap == None else None


    def marketCapBelow(self, cap=None):
        '''Filter out contracts with a market cap above this value. Can be left blank.'''
        if cap != None: self._marketCapBelow = cap
        return self._marketCapBelow if cap == None else None


    def moodyRatingAbove(self, r=None):
        '''Filter out contracts with a Moody rating below this value. Can be left blank.'''
        if r != None: self._moodyRatingAbove = r
        return self._moodyRatingAbove if r == None else None


    def moodyRatingBelow(self, r=None):
        '''Filter out contracts with an Moody rating above this value. Can be left blank.'''
        if r != None: self._moodyRatingBelow = r
        return self._moodyRatingBelow if r == None else None


    def spRatingAbove(self, r=None):
        '''Filter out contracts with an S&P rating below this value. Can be left blank.'''
        if r != None: self._spRatingAbove = r
        return self._spRatingAbove if r == None else None


    def spRatingBelow(self, r=None):
        '''Filter out contracts with an S&P rating above this value. Can be left blank.'''
        if r != None: self._spRatingBelow = r
        return self._spRatingBelow if r == None else None


    def maturityDateAbove(self, d=None):
        '''Filter out contracts with a maturity date earlier than this value. Can be left blank.'''
        if d != None: self._maturityDateAbove = d
        return self._maturityDateAbove if d == None else None


    def maturityDateBelow(self, d=None):
        '''Filter out contracts with a maturity date later than this value. Can be left blank.'''
        if d != None: self._maturityDateBelow = d
        return self._maturityDateBelow if d == None else None


    def couponRateAbove(self, r=None):
        '''Filter out contracts with a coupon rate lower than this value. Can be left blank.'''
        if r != None: self._couponRateAbove = r
        return self._couponRateAbove if r == None else None


    def couponRateBelow(self, r=None):
        '''Filter out contracts with a coupon rate higher than this value. Can be left blank.'''
        if r != None: self._couponRateBelow = r
        return self._couponRateBelow if r == None else None


    def excludeConvertible(self, c=None):
        '''Filter out convertible bonds.  Can be left blank.'''
        if c != None: self._excludeConvertible = c
        return self._excludeConvertible if c == None else None


    def scannerSettingPairs(self, val=None):
        '''Specify scanner setting options. Can leave empty.

           For example, a pairing "Annual, true" used on the "top Option
           Implied Vol % Gainers" scan would return annualized volatilities.
        '''
        if val != None: self._scannerSettingPairs = val
        return self._scannerSettingPairs if val == None else None


    def stockTypeFilter(self, val=None):
        '''Include only specified types of stocks.
        
           Valid values are:
           * ALL (excludes nothing)
           * STOCK (excludes ETFs)
           * ETF (includes ETFs)
        '''
        if val != None: self._stockTypeFilter = val
        return self._stockTypeFilter if val == None else None

    # Class constants
    NO_ROW_NUMBER_SPECIFIED = -1

    from tws._Util import _INT_MAX_VALUE
    from tws._Util import _DOUBLE_MAX_VALUE
