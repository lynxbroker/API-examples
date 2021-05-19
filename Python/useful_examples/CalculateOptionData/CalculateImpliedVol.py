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

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run)  # run the socket in a thread
        app_thread.start()

    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        print("TickOptionComputation. TickerId:", reqId, "ImpliedVolatility:", impliedVol,
              "OptionPrice:", optPrice, "UnderlyingPrice:", undPrice)


app = App("localhost", 7496, clientid=0)

time.sleep(1)

contract = Contract()
contract.symbol = "INGA"
contract.secType = "OPT"
contract.exchange = "FTA"
contract.currency = "EUR"
contract.lastTradeDateOrContractMonth = "20210716"
contract.strike = 10
contract.right = "C"
contract.multiplier = "100"

app.calculateImpliedVolatility(5001, contract, 1.2, 11.014, [])
app.calculateOptionPrice(5002, contract, 0.324, 11.014, [])

time.sleep(5)
app.disconnect()
