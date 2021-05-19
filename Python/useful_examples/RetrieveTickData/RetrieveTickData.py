# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *
import threading
import pandas as pd
import time


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self,self)
        self.bardata = {}

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run) #run the socket in a thread
        app_thread.start()

    def getTickData(self, reqId, contract):
        self.bardata[reqId] = pd.DataFrame(columns=['Time', 'Last Price'])
        self.bardata[reqId].set_index('Time', inplace = True)
        self.reqTickByTickData(reqId, contract, "Last", 0, True)
        return self.bardata[reqId]

    def tickByTickAllLast(self, reqId, tickType, time, price, size, tickAtrribLast, exchange, specialConditions):
        if tickType == 1:
            self.bardata[reqId].loc[pd.to_datetime(time, unit='s')] = price


app = App("localhost", 7496, clientid = 0)

time.sleep(1)

contract = Contract()
contract.symbol = "INGA"
contract.secType = "STK"
contract.currency = "EUR"
contract.exchange = "AEB"

df = app.getTickData(101, contract)

print("Give it some time to start loading data...")
time.sleep(30)
print(df)

app.disconnect()