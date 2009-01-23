'''Implements helpful Contract subclasses.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from tws import Contract


class StockContract(Contract):
    '''Description of a stock contract.'''

    def __init__(self, symbol, exchange="SMART", currency="USD", **kwds):
        '''Specialized constructor for stock contracts.

           Params:
             symbol: Always required
             exchange: optional for US stocks, defaults to "Smart"
             currency: optional for US stocks.
             **kwds: Any other keyword args acceptable to tws.Contract
             may be provided as desired.
        '''
        super(StockContract, self).__init__(sec_type="STK",
                                            symbol=symbol,
                                            exchange=exchange,
                                            currency=currency,
                                            **kwds )



class FuturesContract(Contract):
    '''Description of a futures contract.'''

    def __init__(self, exchange, symbol="", expiry="", currency="USD",
                 local_symbol="", **kwds):
        '''Specialized constructor for futures contracts.

           Params:
             exchange: Always required.
             symbol: Required if not specifying local_symbol.
             expiry: Required if not specifying local_symbol.
             currency: optional for US exchanges.
             local_symbol: May be specified instead of symbol and expiry.
             **kwds: Any other keyword args acceptable to tws.Contract
             may be provided as desired.
        '''
        assert (symbol and expiry) or local_symbol

        super(FuturesContract, self).__init__(sec_type="FUT",
                                              exchange=exchange,
                                              symbol=symbol,
                                              expiry=expiry,
                                              currency=currency,
                                              local_symbol=local_symbol,
                                              **kwds )



class OptionContract(Contract):
    '''Description of an option contract.'''

    def __init__(self, symbol="", right="", strike=0.0, expiry="",
                 exchange="SMART", currency="USD",
                 local_symbol="", **kwds):
        '''Specialized constructor for option contracts.

           Params:
             symbol: Required if not specifying local_symbol.
             right:  Required if not specifying local_symbol.
             strike: Required if not specifying local_symbol.
             expiry: Required if not specifying local_symbol.
             exchange: optional for US options, defaults to "Smart"
             currency: optional for US exchanges.
             local_symbol: May be specified instead of symbol, right,
             strike, expiry.
             **kwds: Any other keyword args acceptable to tws.Contract
             may be provided as desired.
        '''
        assert (symbol and right and strike and expiry) or local_symbol

        super(OptionContract, self).__init__(sec_type="OPT",
                                             symbol=symbol,
                                             right=right,
                                             strike=strike,
                                             expiry=expiry,
                                             exchange=exchange,
                                             currency=currency,
                                             local_symbol=local_symbol,
                                              **kwds )


del Contract