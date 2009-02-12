'''Implements EWrapper hook to handle contractDetails().'''

from __future__ import with_statement

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

import threading as _threading
import tws.EClientErrors as _EClientErrors


class HookContractDetails(object):
    '''Installs hook to handle EWrapper.contractDetails() events.

       To install construct an instance passing the wrapper object to hook.

       After installation, your wrapper object will begin handling the
       EWrapper.contractDetails and EWrapper.contractDetailsEnd() events.
       At any time you may call the method <wrapper>.get_contract_details()
       to obtain the details for a specified contract as reported by the
       TWS application.
    '''

    def __init__(self, wrapper):
        assert isinstance(wrapper, __import__("tws").EWrapper)
        assert hasattr(wrapper,"client")

        self._condition = _threading.Condition()
        self._wrapper = wrapper
        self._details = {}

        wrapper.contractDetails = self.contractDetails
        wrapper.contractDetailsEnd = self.contractDetailsEnd
        wrapper.get_contract_details = self.get_contract_details


    def contractDetails(self, req_id, contract_details):
        '''Handler for EWrapper.contractDetails event.

           Installed using tws.helper.HookContractDetails(wrapper)
        '''
        assert isinstance(req_id, int)
        assert isinstance(contract_details, __import__("tws").ContractDetails)

        with (self._condition):
            try:
                self._details[req_id][0].append(contract_details)
            finally:
                self._condition.notifyAll()


    def contractDetailsEnd(self, req_id):
        '''Handler for EWrapper.contractDetailsEnd event.

           Installed using tws.helper.HookContractDetails(wrapper)
        '''
        assert isinstance(req_id, int)

        with (self._condition):
            try:
                self._details[req_id][1] = True
            finally:
                self._condition.notifyAll()


    def get_contract_details(self, contract):
        '''Details for a particular contract.

           This method returns all details for a particular contract as
           reported by the TWS application. You must provide a filter in
           the form of a tws.Contract object. Details for all contracts
           matching that filter will be obtained by the TWS application.
           Details are returned in the form of a list of tws.ContractDetails
           objects; it is up to you to figure out which contract is which.

           Installed using tws.helper.HookCurrentTime(wrapper)
        '''
        assert isinstance(contract, __import__("tws").Contract)

        with (self._condition):
            # Set up and make request
            req_id = id(contract)
            self._details[req_id] = [[], False]
            self._wrapper.client.reqContractDetails(req_id, contract)

            # Wait for data to return from TWS
            while not self._details[req_id][1]:
                self._condition.wait()

            # Pop collected data and return list of details.
            details = self._details.pop(req_id)
            return details[0]
