# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *

import threading
import time


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self, self)
        self.contract_details = {}

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run)  # run the socket in a thread
        app_thread.start()

    def contractDetails(self, reqId, contractDetails):
        self.contract_details[reqId] = contractDetails

    def get_contract_details(self, reqId, contract):
        self.contract_details[reqId] = None
        self.reqContractDetails(reqId, contract)
        time.sleep(5)
        return self.contract_details[reqId].contract


def contract_def(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "AEB"
    contract.currency = "EUR"
    return contract


app = App("localhost", 7496, clientid=0)

time.sleep(1)

INGA = contract_def('INGA')
INGA = app.get_contract_details(101, INGA)

print(INGA)

app.disconnect()