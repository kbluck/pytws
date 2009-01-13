'''Implements EWrapper subclass SynchronizedWrapper.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import Queue
from tws import EWrapper


class SynchronizedWrapper(EWrapper):
    '''Synchronizes wrapper events into another thread.

       Since the client socket is read in a worker thread, calls to
       EWrapper will be made in the context of that thread, potentially
       leading to synchronization errors. Constructing an instance of this
       class with a chained EWrapper instance ensures that the chained
       EWrapper's event method calls will be synchronized into a desired
       client thread, usually the main thread.

       The client thread must periodically invoke the dispatch() method to
       cause waiting events to be invoked upon the chained EWrapper. The
       exact means of starting dispatch will depend on the nature of the
       application; command lines will do things differently than GUIs, and
       any given GUI framework will have its own method. Timers, idle event
       handlers, or simple polling loops are all possible means of making
       dispatch happen at frequent intervals. It is important to understand
       that nothing will happen until dispatch() is called, so it should be
       called as frequently as necessary to avoid undesirable latency.
    '''

    _queue_factory = Queue.Queue
    _queue_empty = Queue.Empty

    def __init__(self, wrapper):
        assert(isinstance(wrapper, __import__("tws").EWrapper))

        super(SynchronizedWrapper, self).__init__()

        self._queue = self._queue_factory()
        self._chained_wrapper = wrapper


    def _put_wrapper_call(self, method_name, *args):
        self._queue.put(item=(method_name, args), block=False)


    def dispatch(self):
        '''Invokes waiting wrapper calls.

           Wrapper calls are collected asynchronously from the socket reader
           thread while the main thread executes. Periodically, this method
           must be invoked to dispatch those waiting calls into the chained
           EWrapper object. All waiting calls will be dispatched one after
           another until the waiting queue is empty or an exception occurs.
        '''
        try:
            # Keep trying to suck in waiting items and invoke the matching
            # named methods on the chained wrapper object.
            while True:
                item = self._queue.get(block=False)
                getattr(self._chained_wrapper, item[0])(*item[1])

        # Once waiting queue is empty, just return.                 
        except self._queue_empty:
            return


    def error(self, e):
        self._put_wrapper_call("error", e)


    def connectionClosed(self):
        self._put_wrapper_call("connectionClosed")


    def tickPrice(self, tickerId, field, price, canAutoExecute):
        self._put_wrapper_call("tickPrice", tickerId, field, price,
                               canAutoExecute)


    def tickSize(self, tickerId, field, size):
        self._put_wrapper_call("tickSize", tickerId, field, size)


    def tickOptionComputation(self, tickerId, field, impliedVol,
                              delta, modelPrice, pvDividend):
        self._put_wrapper_call("tickOptionComputation", tickerId, field,
                               impliedVol, delta, modelPrice, pvDividend)


    def tickGeneric(self, tickerId, tickType, value):
        self._put_wrapper_call("tickGeneric", tickerId, tickType, value)


    def tickString(self, tickerId, tickType, value):
        self._put_wrapper_call("tickString", tickerId, tickType, value)


    def tickEFP(self, tickerId, tickType, basisPoints, formattedBasisPoints,
                impliedFuture, holdDays, futureExpiry, dividendImpact,
                dividendsToExpiry):
        self._put_wrapper_call("tickEFP", tickerId, tickType, basisPoints,
                               formattedBasisPoints, impliedFuture,
                               holdDays, futureExpiry, dividendImpact,
                               dividendsToExpiry)


    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice,
                    permId, parentId, lastFillPrice, clientId, whyHeld):
        self._put_wrapper_call("orderStatus", orderId, status, filled,
                               remaining, avgFillPrice, permId, parentId,
                               lastFillPrice, clientId, whyHeld)


    def openOrder(self, orderId, contract, order, orderState):
        self._put_wrapper_call("openOrder", orderId, contract, order,
                               orderState)


    def openOrderEnd(self):
        self._put_wrapper_call("openOrderEnd")


    def updateAccountValue(self, key, value, currency, accountName):
        self._put_wrapper_call("updateAccountValue", key, value, currency,
                               accountName)


    def updatePortfolio(self, contract, position, marketPrice, marketValue,
                        averageCost, unrealizedPNL, realizedPNL, accountName):
        self._put_wrapper_call("updatePortfolio", contract, position,
                               marketPrice, marketValue, averageCost,
                               unrealizedPNL, realizedPNL, accountName)


    def updateAccountTime(self, timeStamp):
        self._put_wrapper_call("updateAccountTime", timeStamp)


    def accountDownloadEnd(self, accountName):
        self._put_wrapper_call("accountDownloadEnd", accountName)


    def nextValidId(self, orderId):
        self._put_wrapper_call("nextValidId", orderId)


    def contractDetails(self, reqId, contractDetails):
        self._put_wrapper_call("contractDetails", reqId, contractDetails)


    def bondContractDetails(self, reqId, contractDetails):
        self._put_wrapper_call("bondContractDetails", reqId, contractDetails)


    def contractDetailsEnd(self, reqId):
        self._put_wrapper_call("contractDetailsEnd", reqId)


    def execDetails(self, reqId, contract, execution):
        self._put_wrapper_call("execDetails", reqId, contract, execution)


    def execDetailsEnd(self, reqId):
        self._put_wrapper_call("execDetailsEnd", reqId)


    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        self._put_wrapper_call("updateMktDepth", tickerId, position,
                               operation, side, price, size)


    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, 
                               side, price, size):
        self._put_wrapper_call("updateMktDepthL2", tickerId, position,
                               marketMaker, operation, side, price, size)


    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        self._put_wrapper_call("updateNewsBulletin", msgId, msgType, message,
                               origExchange)


    def managedAccounts(self, accountsList):
        self._put_wrapper_call("managedAccounts", accountsList)


    def receiveFA(self, faDataType, xml):
        self._put_wrapper_call("receiveFA", faDataType, xml)


    def historicalData(self, reqId, date, open, high, low, close, volume,
                             count, wap, hasGaps):
        self._put_wrapper_call("historicalData", reqId, date, open, high, 
                               low, close, volume, count, wap, hasGaps)


    def scannerParameters(self, xml):
        self._put_wrapper_call("scannerParameters", xml)


    def scannerData(self, reqId, rank, contractDetails, distance, benchmark,
                          projection, legsStr):
        self._put_wrapper_call("scannerData", reqId, rank, contractDetails,
                               distance, benchmark, projection, legsStr)


    def scannerDataEnd(self, reqId):
        self._put_wrapper_call("scannerDataEnd", reqId)


    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap,
                          count):
        self._put_wrapper_call("realtimeBar", reqId, time, open, high, low,
                               close, volume, wap, count)


    def currentTime(self, time):
        self._put_wrapper_call("currentTime", time)


    def fundamentalData(self, reqId, data):
        self._put_wrapper_call("fundamentalData", reqId, data)


    def deltaNeutralValidation(self, reqId, underComp):
        self._put_wrapper_call("deltaNeutralValidation", reqId, underComp)


del EWrapper
del Queue
