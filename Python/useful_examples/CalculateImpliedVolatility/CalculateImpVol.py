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

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run) #run the socket in a thread
        app_thread.start()

    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):

        if reqId == 1:
            print("The implied volatility for the hypothetical information is: %s" % impliedVol)
        else:
            print("The option price for the hypothetical information is: %s" % optPrice)


app = App("localhost", 7496, clientid = 0)

time.sleep(1)

contract = Contract()
contract.symbol = "INGA"
contract.secType = "OPT"
contract.exchange = "FTA"
contract.currency = "EUR"
contract.lastTradeDateOrContractMonth = "20211217"
contract.strike = 13
contract.right = "C"
contract.multiplier = "100"

hypothetical_option_price = 1.4
hypothetical_stock_price = 13.5
hypothetical_volatility = 0.3

# Calculate either the implied volatility or the option price
app.calculateImpliedVolatility(1, contract, hypothetical_option_price, hypothetical_stock_price, [])
time.sleep(5)
app.calculateOptionPrice(2, contract, hypothetical_volatility, hypothetical_stock_price, [])

time.sleep(5)
app.disconnect()