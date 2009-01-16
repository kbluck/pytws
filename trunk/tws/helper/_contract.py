'''Implements helpful Contract subclasses.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from tws import Contract


class StockContract(Contract):
    '''Description of a stock contract.

       Specialized constructor to make it easier to create contract
       objects referring to a stock instrument.
       
       Params:
         symbol: Required
         exchange: optional for US stocks, defaults to "Smart"
         currency: optional for US stocks.
         **kwds: Any other keyword args acceptable to tws.Contract
         may be provided as desired.
    '''

    def __init__(self, symbol, exchange="SMART", currency="USD", **kwds):
        super(StockContract, self).__init__(sec_type="STK",
                                            symbol=symbol,
                                            exchange=exchange,
                                            currency=currency,
                                            **kwds )


del Contract