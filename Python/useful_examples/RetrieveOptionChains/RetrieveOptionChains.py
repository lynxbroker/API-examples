# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *
import threading
import time


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self,self)
        self.contract_details = {}

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run) # run the socket in a thread
        app_thread.start()

    def contractDetails(self, reqId, contractDetails):
        self.contract_details[reqId] = contractDetails

    def get_contract_details(self, reqId, contract):
        self.contract_details[reqId] = None
        self.reqContractDetails(reqId, contract)
        time.sleep(5)
        return self.contract_details[reqId].contract

    def securityDefinitionOptionParameter(self, reqId, exchange,underlyingConId, tradingClass, multiplier, expirations, strikes):
        print("Exchange:", exchange, "Underlying conId:", underlyingConId, "TradingClass:", tradingClass, "Multiplier:", multiplier,'\n',
        "Expirations:", expirations,'\n', "Strikes:", str(strikes))

    def requestOptionChains(self, contract, conId):
        self.reqSecDefOptParams(1001, contract.symbol, "", contract.secType, conId)


app = App("localhost", 7496, clientid = 0)

time.sleep(1)

contract = Contract()
contract.symbol = "INGA"
contract.secType = "STK"
contract.currency = "EUR"
contract.exchange = "AEB"

INGA = app.get_contract_details(101, contract) # need the conId to request Option Chains

app.requestOptionChains(contract, INGA.conId)

print("Give it some time to start loading data...")
time.sleep(5)

app.disconnect()


