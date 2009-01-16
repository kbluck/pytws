'''Implements helpful Contract subclasses.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from tws import Contract


class StockContract(Contract):
    '''Description of a stock contract.

       Specialized constructor to make it easier to create contract
       objects referring to a stock instrument.
       
       Params:
         symbol: Always required
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



class FuturesContract(Contract):
    '''Description of a futures contract.

       Specialized constructor to make it easier to create contract
       objects referring to a futures instrument.
       
       Params:
         exchange: Always required.
         symbol: Required if not specifying local_symbol.
         expiry: Required if not specifying local_symbol.
         currency: optional for US exchanges.
         local_symbol: May be specified instead of symbol and expiry.
         **kwds: Any other keyword args acceptable to tws.Contract
         may be provided as desired.
    '''

    def __init__(self, exchange, symbol="", expiry="", currency="USD", 
                 local_symbol="", **kwds):
        assert (symbol and expiry) or local_symbol

        super(FuturesContract, self).__init__(sec_type="FUT",
                                              exchange=exchange,
                                              symbol=symbol,
                                              expiry=expiry,
                                              currency=currency,
                                              local_symbol=local_symbol,
                                              **kwds )


del Contract