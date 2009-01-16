'''Implements EWrapper subclass QueueWrapper.'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from Queue import Queue
from tws import EWrapper


class QueueWrapper(Queue, EWrapper):

    def __init__(self):
        super(QueueWrapper, self).__init__()


    if __debug__: # Assert structure of items put into Queue
        _queue_type = Queue

        def _put(self, item):
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)
            assert isinstance(item[1], dict)

            QueueWrapper._queue_type._put(self, item)


    def _put_wrapper_call(self, method_name, **kwds):
        self.put(item=(method_name, kwds), block=False, timeout=None)


    def error(self, e):
        self._put_wrapper_call("error", e=e)


    def connectionClosed(self):
        self._put_wrapper_call("connectionClosed")


    def tickPrice(self, tickerId, field, price, canAutoExecute):
        self._put_wrapper_call("tickPrice", tickerId=tickerId, field=field,
                               price=price, canAutoExecute=canAutoExecute)


    def tickSize(self, tickerId, field, size):
        self._put_wrapper_call("tickSize", tickerId=tickerId, field=field,
                               size=size)


    def tickOptionComputation(self, tickerId, field, impliedVol,
                              delta, modelPrice, pvDividend):
        self._put_wrapper_call("tickOptionComputation", tickerId=tickerId,
                               field=field, impliedVol=impliedVol,
                               delta=delta, modelPrice=modelPrice,
                               pvDividend=pvDividend)


    def tickGeneric(self, tickerId, tickType, value):
        self._put_wrapper_call("tickGeneric", tickerId=tickerId,
                               tickType=tickType, value=value)


    def tickString(self, tickerId, tickType, value):
        self._put_wrapper_call("tickString", tickerId=tickerId,
                               tickType=tickType, value=value)


    def tickEFP(self, tickerId, tickType, basisPoints, formattedBasisPoints,
                impliedFuture, holdDays, futureExpiry, dividendImpact,
                dividendsToExpiry):
        self._put_wrapper_call("tickEFP", tickerId=tickerId,
                               tickType=tickType, basisPoints=basisPoints,
                               formattedBasisPoints=formattedBasisPoints,
                               impliedFuture=impliedFuture, holdDays=holdDays,
                               futureExpiry=futureExpiry,
                               dividendImpact=dividendImpact,
                               dividendsToExpiry=dividendsToExpiry)


    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice,
                    permId, parentId, lastFillPrice, clientId, whyHeld):
        self._put_wrapper_call("orderStatus", orderId=orderId, status=status,
                               filled=filled, remaining=remaining,
                               avgFillPrice=avgFillPrice, permId=permId,
                               parentId=parentId, lastFillPrice=lastFillPrice,
                               clientId=clientId, whyHeld=whyHeld)


    def openOrder(self, orderId, contract, order, orderState):
        self._put_wrapper_call("openOrder", orderId=orderId,
                               contract=contract, order=order,
                               orderState=orderState)


    def openOrderEnd(self):
        self._put_wrapper_call("openOrderEnd")


    def updateAccountValue(self, key, value, currency, accountName):
        self._put_wrapper_call("updateAccountValue", key=key, value=value,
                               currency=currency, accountName=accountName)


    def updatePortfolio(self, contract, position, marketPrice, marketValue,
                        averageCost, unrealizedPNL, realizedPNL, accountName):
        self._put_wrapper_call("updatePortfolio", contract=contract,
                               position=position, marketPrice=marketPrice,
                               marketValue=marketValue,
                               averageCost=averageCost,
                               unrealizedPNL=unrealizedPNL,
                               realizedPNL=realizedPNL,
                               accountName=accountName)


    def updateAccountTime(self, timeStamp):
        self._put_wrapper_call("updateAccountTime", timeStamp=timeStamp)


    def accountDownloadEnd(self, accountName):
        self._put_wrapper_call("accountDownloadEnd", accountName=accountName)


    def nextValidId(self, orderId):
        self._put_wrapper_call("nextValidId", orderId=orderId)


    def contractDetails(self, reqId, contractDetails):
        self._put_wrapper_call("contractDetails", reqId=reqId,
                               contractDetails=contractDetails)


    def bondContractDetails(self, reqId, contractDetails):
        self._put_wrapper_call("bondContractDetails", reqId=reqId,
                               contractDetails=contractDetails)


    def contractDetailsEnd(self, reqId):
        self._put_wrapper_call("contractDetailsEnd", reqId=reqId)


    def execDetails(self, reqId, contract, execution):
        self._put_wrapper_call("execDetails", reqId=reqId, contract=contract,
                               execution=execution)


    def execDetailsEnd(self, reqId):
        self._put_wrapper_call("execDetailsEnd", reqId=reqId)


    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        self._put_wrapper_call("updateMktDepth", tickerId=tickerId,
                               position=position, operation=operation,
                               side=side, price=price, size=size)


    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, side, price, size):
        self._put_wrapper_call("updateMktDepthL2", tickerId=tickerId,
                               position=position, marketMaker=marketMaker,
                               operation=operation, side=side, price=price,
                               size=size)


    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        self._put_wrapper_call("updateNewsBulletin", msgId=msgId,
                               msgType=msgType, message=message,
                               origExchange=origExchange)


    def managedAccounts(self, accountsList):
        self._put_wrapper_call("managedAccounts", accountsList=accountsList)


    def receiveFA(self, faDataType, xml):
        self._put_wrapper_call("receiveFA", faDataType=faDataType, xml=xml)


    def historicalData(self, reqId, date, open, high, low, close, volume, count, wap, hasGaps):
        self._put_wrapper_call("historicalData", reqId=reqId, date=date,
                               open=open, high=high, low=low, close=close,
                               volume=volume, count=count, wap=wap,
                               hasGaps=hasGaps)


    def scannerParameters(self, xml):
        self._put_wrapper_call("scannerParameters", xml=xml)


    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        self._put_wrapper_call("scannerData", reqId=reqId, rank=rank,
                               contractDetails=contractDetails,
                               distance=distance, benchmark=benchmark,
                               projection=projection, legsStr=legsStr)


    def scannerDataEnd(self, reqId):
        self._put_wrapper_call("scannerDataEnd", reqId=reqId)


    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap, count):
        self._put_wrapper_call("realtimeBar", reqId=reqId, time=time,
                               open=open, high=high, low=low, close=close,
                               volume=volume, wap=wap, count=count)


    def currentTime(self, time):
        self._put_wrapper_call("currentTime", time=time)


    def fundamentalData(self, reqId, data):
        self._put_wrapper_call("fundamentalData", reqId=reqId, data=data)


    def deltaNeutralValidation(self, reqId, underComp):
        self._put_wrapper_call("deltaNeutralValidation", reqId=reqId,
                               underComp=underComp)


del EWrapper
del Queue
