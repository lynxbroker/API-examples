
# Copyright (C) 2019 LYNX B.V. All rights reserved.


# Import ibapi deps
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import *
from threading import Thread

from datetime import datetime
from time import sleep

CONTRACT_ID = 4001

class Wrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""

        print("marketName: ", contractDetails.marketName, "\nvalidExchanges: ", contractDetails.validExchanges,\
              "\nlongName: ", contractDetails.longName, "\nminTick: ",contractDetails.minTick)
        #printinstance(contractDetails) using this print statement all of the availabe details will be printed out.


class Client(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def get_contractDetails(self, contract, reqId = CONTRACT_ID):

        # Here we are requesting contract details for the EUR.USD Contract
        self.reqContractDetails(reqId, contract)

        MAX_WAITED_SECONDS = 5
        print("Getting contract details from the server... can take %d second to complete" % MAX_WAITED_SECONDS)

        sleep(MAX_WAITED_SECONDS)

class TestApp(Wrapper, Client):
    def __init__(self, ipaddress, portid, clientid):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)

        thread = Thread(target=self.run)
        thread.start()

        setattr(self, "_thread", thread)

def printinstance(inst:Object):
    attrs = vars(inst)
    print('\n'.join("%s: %s" % item for item in attrs.items()))

def main():
    app = TestApp("localhost", 7496, clientid = 0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                  app.twsConnectionTime()))

    # Define the contract
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"

    app.get_contractDetails(contract)

if __name__ == "__main__":
    main()
