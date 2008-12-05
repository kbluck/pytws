'''Execution data structure.'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"


class Execution(object):
    '''Data structure to describe a trade execution.
    '''

    def __init__(self, order_id=0, client_id=0, exec_id='', time='', acct_number='', exchange='', side='',
                       shares=0, price=0.0, perm_id=0, liquidation=0, cum_qty=0, avg_price=0.0):
        self.m_orderId = order_id
        self.m_clientId = client_id
        self.m_execId = exec_id
        self.m_time = time
        self.m_acctNumber = acct_number
        self.m_exchange = exchange
        self.m_side = side
        self.m_shares = shares
        self.m_price = price
        self.m_permId = perm_id
        self.m_liquidation = liquidation
        self.m_cumQty = cum_qty
        self.m_avgPrice = avg_price


    def __eq__(self, other):
        if id(self) == id(other): return True
        if not isinstance(other, self.__class__): return False
        return True if (
            (self.m_execId == other.m_execId)
        ) else False
