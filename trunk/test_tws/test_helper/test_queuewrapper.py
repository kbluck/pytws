'''Unit test package for module "tws.helper._queuewrapper".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import Queue
import tws
from tws.helper import QueueWrapper


class test_QueueWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = QueueWrapper()

    def test_init(self):
        self.assertTrue(isinstance(QueueWrapper(), tws.EWrapper))
        self.assertTrue(isinstance(QueueWrapper(), Queue.Queue))
        self.assertTrue(QueueWrapper().empty())
        self.assertFalse(QueueWrapper().full())
        self.assertEqual(QueueWrapper().qsize(), 0)
        self.assertRaises(Queue.Empty, QueueWrapper().get_nowait)

    def test_put(self):
        self.assertTrue(self.wrapper.empty())
        self.wrapper.put(item=("test1",{"A1":1,"B2":3}))
        self.assertFalse(self.wrapper.empty())
        self.assertEqual(self.wrapper.get(), ("test1",{"A1":1,"B2":3}))

        self.assertTrue(self.wrapper.empty())
        self.wrapper.put_nowait(item=("test2",{"C3":2,"D4":4}))
        self.assertFalse(self.wrapper.empty())
        self.assertEqual(self.wrapper.get(), ("test2",{"C3":2,"D4":4}))

    def test_put_wrapper_call(self):
        self.assertTrue(self.wrapper.empty())
        self.wrapper._put_wrapper_call("test", A1=1, B2=3)
        self.assertFalse(self.wrapper.empty())
        self.assertEqual(self.wrapper.get(), ("test",{"A1":1,"B2":3}))
        self.assertTrue(self.wrapper.empty())

    def test_wrapper_methods(self):
        self.assertTrue(self.wrapper.empty())

        self.wrapper.error(tws.EClientErrors.CONNECT_FAIL)
        self.assertEqual(self.wrapper.get(), ("error",
            {"e":tws.EClientErrors.CONNECT_FAIL}))

        self.wrapper.connectionClosed()
        self.assertEqual(self.wrapper.get(), ("connectionClosed",
            {}))

        self.wrapper.tickPrice(1,2,3.5,4)
        self.assertEqual(self.wrapper.get(), ("tickPrice",
            {"tickerId":1,"field":2,"price":3.5,"canAutoExecute":4}))

        self.wrapper.tickSize(1,2,3)
        self.assertEqual(self.wrapper.get(), ("tickSize",
            {"tickerId":1,"field":2,"size":3}))

        self.wrapper.tickOptionComputation(1,2,3.5,4.5,5.5,6.5)
        self.assertEqual(self.wrapper.get(), ("tickOptionComputation",
            {"tickerId":1,"field":2,"impliedVol":3.5,"delta":4.5,
             "modelPrice":5.5,"pvDividend":6.5}))

        self.wrapper.tickGeneric(1,2,3.5)
        self.assertEqual(self.wrapper.get(), ("tickGeneric",
            {"tickerId":1,"tickType":2,"value":3.5}))

        self.wrapper.tickString(1,2,"A1")
        self.assertEqual(self.wrapper.get(), ("tickString",
            {"tickerId":1,"tickType":2,"value":"A1"}))

        self.wrapper.tickEFP(1,2,3.5,"A1",4.5,5,"B2",6.5,7.5)
        self.assertEqual(self.wrapper.get(), ("tickEFP",
            {"tickerId":1,"tickType":2,"basisPoints":3.5,
             "formattedBasisPoints":"A1","impliedFuture":4.5,
             "holdDays":5,"futureExpiry":"B2","dividendImpact":6.5,
             "dividendsToExpiry":7.5}))

        self.wrapper.orderStatus(1,"A1",2,3,4.5,5,6,7.5,8,"B2")
        self.assertEqual(self.wrapper.get(), ("orderStatus",
            {"orderId":1,"status":"A1","filled":2,"remaining":3,
             "avgFillPrice":4.5,"permId":5,"parentId":6,"lastFillPrice":7.5,
             "clientId":8,"whyHeld":"B2"}))

        self.wrapper.openOrder(1,tws.Contract(),tws.Order(),tws.OrderState())
        self.assertEqual(self.wrapper.get(), ("openOrder",
            {"orderId":1,"contract":tws.Contract(),"order":tws.Order(),
             "orderState":tws.OrderState()}))

        self.wrapper.openOrderEnd()
        self.assertEqual(self.wrapper.get(), ("openOrderEnd",
            {}))

        self.wrapper.updateAccountValue("A1","B2","C3","D4")
        self.assertEqual(self.wrapper.get(), ("updateAccountValue",
            {"key":"A1","value":"B2","currency":"C3","accountName":"D4"}))

        self.wrapper.updatePortfolio(tws.Contract(),2,3.5,4.5,5.5,6.5,7.5,"A1")
        self.assertEqual(self.wrapper.get(), ("updatePortfolio",
            {"contract":tws.Contract(),"position":2,"marketPrice":3.5,
             "marketValue":4.5,"averageCost":5.5,"unrealizedPNL":6.5,
             "realizedPNL":7.5,"accountName":"A1"}))

        self.wrapper.updateAccountTime("A1")
        self.assertEqual(self.wrapper.get(), ("updateAccountTime",
            {"timeStamp":"A1"}))

        self.wrapper.accountDownloadEnd("A1")
        self.assertEqual(self.wrapper.get(), ("accountDownloadEnd",
            {"accountName":"A1"}))

        self.wrapper.nextValidId(1)
        self.assertEqual(self.wrapper.get(), ("nextValidId",
            {"orderId":1}))

        self.wrapper.contractDetails(1,tws.ContractDetails())
        self.assertEqual(self.wrapper.get(), ("contractDetails",
            {"reqId":1,"contractDetails":tws.ContractDetails()}))

        self.wrapper.bondContractDetails(1,tws.ContractDetails())
        self.assertEqual(self.wrapper.get(), ("bondContractDetails",
            {"reqId":1,"contractDetails":tws.ContractDetails()}))

        self.wrapper.contractDetailsEnd(1)
        self.assertEqual(self.wrapper.get(), ("contractDetailsEnd",
            {"reqId":1}))

        self.wrapper.execDetails(1,tws.Contract(),tws.Execution())
        self.assertEqual(self.wrapper.get(), ("execDetails",
            {"reqId":1,"contract":tws.Contract(),
             "execution":tws.Execution()}))

        self.wrapper.execDetailsEnd(1)
        self.assertEqual(self.wrapper.get(), ("execDetailsEnd",
            {"reqId":1}))

        self.wrapper.updateMktDepth(1,2,3,4,5.5,6)
        self.assertEqual(self.wrapper.get(), ("updateMktDepth",
            {"tickerId":1,"position":2,"operation":3,"side":4,
             "price":5.5,"size":6}))

        self.wrapper.updateMktDepthL2(1,2,"A1",3,4,5.5,6)
        self.assertEqual(self.wrapper.get(), ("updateMktDepthL2",
            {"tickerId":1,"position":2,"marketMaker":"A1","operation":3,
             "side":4,"price":5.5,"size":6}))

        self.wrapper.updateNewsBulletin(1,2,"A1","B2")
        self.assertEqual(self.wrapper.get(), ("updateNewsBulletin",
            {"msgId":1,"msgType":2,"message":"A1","origExchange":"B2"}))

        self.wrapper.managedAccounts("A1")
        self.assertEqual(self.wrapper.get(), ("managedAccounts",
            {"accountsList":"A1"}))

        self.wrapper.receiveFA(1,"A1")
        self.assertEqual(self.wrapper.get(), ("receiveFA",
            {"faDataType":1,"xml":"A1"}))

        self.wrapper.historicalData(1,"A1",2.5,3.5,4.5,5.5,6,7,8.5,True)
        self.assertEqual(self.wrapper.get(), ("historicalData",
            {"reqId":1,"date":"A1","open":2.5,"high":3.5,"low":4.5,
             "close":5.5,"volume":6,"count":7,"wap":8.5,"hasGaps":True}))

        self.wrapper.scannerParameters("A1")
        self.assertEqual(self.wrapper.get(), ("scannerParameters",
            {"xml":"A1"}))

        self.wrapper.scannerData(1,2,tws.ContractDetails(),"A1","B2",
                                 "C3","D4")
        self.assertEqual(self.wrapper.get(), ("scannerData",
            {"reqId":1,"rank":2,"contractDetails":tws.ContractDetails(),
             "distance":"A1","benchmark":"B2","projection":"C3",
             "legsStr":"D4"}))

        self.wrapper.scannerDataEnd(1)
        self.assertEqual(self.wrapper.get(), ("scannerDataEnd",
            {"reqId":1}))

        self.wrapper.realtimeBar(1,2,3.5,4.5,5.5,6.5,7,8.5,9)
        self.assertEqual(self.wrapper.get(), ("realtimeBar",
            {"reqId":1,"time":2,"open":3.5,"high":4.5,"low":5.5,"close":6.5,
             "volume":7,"wap":8.5,"count":9}))

        self.wrapper.currentTime(1)
        self.assertEqual(self.wrapper.get(), ("currentTime",
            {"time":1}))

        self.wrapper.fundamentalData(1,"A1")
        self.assertEqual(self.wrapper.get(), ("fundamentalData",
            {"reqId":1,"data":"A1"}))

        self.wrapper.deltaNeutralValidation(1,tws.UnderComp())
        self.assertEqual(self.wrapper.get(), ("deltaNeutralValidation",
            {"reqId":1,"underComp":tws.UnderComp()}))
