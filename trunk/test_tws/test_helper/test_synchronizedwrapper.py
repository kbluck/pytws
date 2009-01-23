'''Unit test package for module "tws.helper._synchronizedwrapper".'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import unittest
import tws
import tws.helper
import test_tws


class test_SynchronizedWrapper(unittest.TestCase):

    def setUp(self):
        self.client_wrapper = test_tws.mock_wrapper()
        self.sync_wrapper = tws.helper.SynchronizedWrapper(self.client_wrapper)

    def test_init(self):
        self.assertTrue(isinstance(
            tws.helper.SynchronizedWrapper(tws.EWrapper()), tws.EWrapper))

    def test_put_wrapper_call(self):
        self.assertTrue(self.sync_wrapper._queue.empty())
        self.sync_wrapper._put_wrapper_call("test", 1, 3)
        self.assertFalse(self.sync_wrapper._queue.empty())
        self.assertEqual(self.sync_wrapper._queue.get(), ("test",(1,3)))
        self.assertTrue(self.sync_wrapper._queue.empty())

    def test_dispatch_methods(self):
        self.sync_wrapper.error(tws.EClientErrors.CONNECT_FAIL)
        self.sync_wrapper.connectionClosed()
        self.sync_wrapper.tickPrice(1,2,3.5,4)
        self.sync_wrapper.tickSize(1,2,3)
        self.sync_wrapper.tickOptionComputation(1,2,3.5,4.5,5.5,6.5)
        self.sync_wrapper.tickGeneric(1,2,3.5)
        self.sync_wrapper.tickString(1,2,"A1")
        self.sync_wrapper.tickEFP(1,2,3.5,"A1",4.5,5,"B2",6.5,7.5)
        self.sync_wrapper.orderStatus(1,"A1",2,3,4.5,5,6,7.5,8,"B2")
        self.sync_wrapper.openOrder(1,tws.Contract(),tws.Order(),tws.OrderState())
        self.sync_wrapper.openOrderEnd()
        self.sync_wrapper.updateAccountValue("A1","B2","C3","D4")
        self.sync_wrapper.updatePortfolio(tws.Contract(),2,3.5,4.5,5.5,6.5,7.5,"A1")
        self.sync_wrapper.updateAccountTime("A1")
        self.sync_wrapper.accountDownloadEnd("A1")
        self.sync_wrapper.nextValidId(1)
        self.sync_wrapper.contractDetails(1,tws.ContractDetails())
        self.sync_wrapper.bondContractDetails(1,tws.ContractDetails())
        self.sync_wrapper.contractDetailsEnd(1)
        self.sync_wrapper.execDetails(1,tws.Contract(),tws.Execution())
        self.sync_wrapper.execDetailsEnd(1)
        self.sync_wrapper.updateMktDepth(1,2,3,4,5.5,6)
        self.sync_wrapper.updateMktDepthL2(1,2,"A1",3,4,5.5,6)
        self.sync_wrapper.updateNewsBulletin(1,2,"A1","B2")
        self.sync_wrapper.managedAccounts("A1")
        self.sync_wrapper.receiveFA(1,"A1")
        self.sync_wrapper.historicalData(1,"A1",2.5,3.5,4.5,5.5,6,7,8.5,True)
        self.sync_wrapper.scannerParameters("A1")
        self.sync_wrapper.scannerData(1,2,tws.ContractDetails(),"A1","B2","C3","D4")
        self.sync_wrapper.scannerDataEnd(1)
        self.sync_wrapper.realtimeBar(1,2,3.5,4.5,5.5,6.5,7,8.5,9)
        self.sync_wrapper.currentTime(1)
        self.sync_wrapper.fundamentalData(1,"A1")
        self.sync_wrapper.deltaNeutralValidation(1,tws.UnderComp())

        self.sync_wrapper.dispatch()

        self.assertEqual(len(self.client_wrapper.errors), 1)
        self.assertEqual(self.client_wrapper.errors[0][1], tws.EClientErrors.CONNECT_FAIL.code())

        self.assertEqual(len(self.client_wrapper.calldata), 33)
        self.assertEqual(self.client_wrapper.calldata[0],
            ("connectionClosed",(),{}))
        self.assertEqual(self.client_wrapper.calldata[1],
            ("tickPrice",(1,2,3.5,4),{}))
        self.assertEqual(self.client_wrapper.calldata[2],
            ("tickSize",(1,2,3),{}))
        self.assertEqual(self.client_wrapper.calldata[3],
            ("tickOptionComputation",(1,2,3.5,4.5,5.5,6.5),{}))
        self.assertEqual(self.client_wrapper.calldata[4],
            ("tickGeneric",(1,2,3.5),{}))
        self.assertEqual(self.client_wrapper.calldata[5],
            ("tickString",(1,2,"A1"),{}))
        self.assertEqual(self.client_wrapper.calldata[6],
            ("tickEFP",(1,2,3.5,"A1",4.5,5,"B2",6.5,7.5),{}))
        self.assertEqual(self.client_wrapper.calldata[7],
            ("orderStatus",(1,"A1",2,3,4.5,5,6,7.5,8,"B2"),{}))
        self.assertEqual(self.client_wrapper.calldata[8],
            ("openOrder",(1,tws.Contract(),tws.Order(),tws.OrderState()),{}))
        self.assertEqual(self.client_wrapper.calldata[9],
            ("openOrderEnd",(),{}))
        self.assertEqual(self.client_wrapper.calldata[10],
            ("updateAccountValue",("A1","B2","C3","D4"),{}))
        self.assertEqual(self.client_wrapper.calldata[11],
            ("updatePortfolio",(tws.Contract(),2,3.5,4.5,5.5,6.5,7.5,"A1"),{}))
        self.assertEqual(self.client_wrapper.calldata[12],
            ("updateAccountTime",("A1",),{}))
        self.assertEqual(self.client_wrapper.calldata[13],
            ("accountDownloadEnd",("A1",),{}))
        self.assertEqual(self.client_wrapper.calldata[14],
            ("nextValidId",(1,),{}))
        self.assertEqual(self.client_wrapper.calldata[15],
            ("contractDetails",(1,tws.ContractDetails()),{}))
        self.assertEqual(self.client_wrapper.calldata[16],
            ("bondContractDetails",(1,tws.ContractDetails()),{}))
        self.assertEqual(self.client_wrapper.calldata[17],
            ("contractDetailsEnd",(1,),{}))
        self.assertEqual(self.client_wrapper.calldata[18],
            ("execDetails",(1,tws.Contract(),tws.Execution()),{}))
        self.assertEqual(self.client_wrapper.calldata[19],
            ("execDetailsEnd",(1,),{}))
        self.assertEqual(self.client_wrapper.calldata[20],
            ("updateMktDepth",(1,2,3,4,5.5,6),{}))
        self.assertEqual(self.client_wrapper.calldata[21],
            ("updateMktDepthL2",(1,2,"A1",3,4,5.5,6),{}))
        self.assertEqual(self.client_wrapper.calldata[22],
            ("updateNewsBulletin",(1,2,"A1","B2"),{}))
        self.assertEqual(self.client_wrapper.calldata[23],
            ("managedAccounts",("A1",),{}))
        self.assertEqual(self.client_wrapper.calldata[24],
            ("receiveFA",(1,"A1"),{}))
        self.assertEqual(self.client_wrapper.calldata[25],
            ("historicalData",(1,"A1",2.5,3.5,4.5,5.5,6,7,8.5,True),{}))
        self.assertEqual(self.client_wrapper.calldata[26],
            ("scannerParameters",("A1",),{}))
        self.assertEqual(self.client_wrapper.calldata[27],
            ("scannerData",(1,2,tws.ContractDetails(),"A1","B2","C3","D4"),{}))
        self.assertEqual(self.client_wrapper.calldata[28],
            ("scannerDataEnd",(1,),{}))
        self.assertEqual(self.client_wrapper.calldata[29],
            ("realtimeBar",(1,2,3.5,4.5,5.5,6.5,7,8.5,9),{}))
        self.assertEqual(self.client_wrapper.calldata[30],
            ("currentTime",(1,),{}))
        self.assertEqual(self.client_wrapper.calldata[31],
            ("fundamentalData",(1,"A1"),{}))
        self.assertEqual(self.client_wrapper.calldata[32],
            ("deltaNeutralValidation", (1,tws.UnderComp()),{}))
