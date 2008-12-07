'''OrderState data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class OrderState(object):
    '''Data structure containing attributes to describe the status of an
       order.
    '''

    def __init__(self, status="", init_margin="", maint_margin="", equity_with_loan="", commission=0.0,
                       min_commission=0.0, max_commission=0.0, commission_currency="", warning_text=""):
        self.m_status = status                 # Missing from Java source; IB Bug?
        self.m_initMargin = init_margin
        self.m_maintMargin = maint_margin
        self.m_equityWithLoan = equity_with_loan
        self.m_commission = commission
        self.m_minCommission = min_commission
        self.m_maxCommission = max_commission
        self.m_commissionCurrency = commission_currency
        self.m_warningText = warning_text


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        return True if (
            (self.m_status == other.m_status) and 
            (self.m_initMargin == other.m_initMargin) and 
            (self.m_maintMargin == other.m_maintMargin) and 
            (self.m_equityWithLoan == other.m_equityWithLoan) and 
            (self.m_commission == other.m_commission) and 
            (self.m_minCommission == other.m_minCommission) and 
            (self.m_maxCommission == other.m_maxCommission) and 
            (self.m_commissionCurrency == other.m_commissionCurrency) and 
            (self.m_warningText == other.m_warningText) 
        ) else False
