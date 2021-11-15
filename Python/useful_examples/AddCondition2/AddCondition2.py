# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *
from ibapi.order import *
import threading
import time
import pandas as pd


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self, self)
        self.bardata = {}

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run)  # run the socket in a thread
        app_thread.start()

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def getTickData(self, reqId, contract):
        self.bardata[reqId] = pd.DataFrame(columns=['Time', 'Last Price'])
        self.bardata[reqId].set_index('Time', inplace = True)
        self.reqTickByTickData(reqId, contract, "Last", 0, True)
        return self.bardata[reqId]

    def tickByTickAllLast(self, reqId, tickType, time, price, size, tickAtrribLast, exchange, specialConditions):
        if tickType == 1:
            self.bardata[reqId].loc[pd.to_datetime(time, unit='s')] = price

def contract_def(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "AEB"
    contract.currency = "EUR"
    return contract

def submit_order(contract, action):
    order = Order()
    order.action = action
    order.totalQuantity = 100
    order.orderType = 'LMT'
    order.lmtPrice = 9
    order.transmit = True

    app.placeOrder(app.nextorderId, contract, order)
    app.nextorderId += 1

def trade_condition(df, contract):
    start_time = df.index[-1] - pd.Timedelta(minutes=10)  # subtract 10 minutes from the last data point
    min_value = df[start_time:].price.min()
    max_value = df[start_time:].price.max()

    if df.price.iloc[-1] < max_value * 0.95:
        submit_order(contract, 'BUY')
        return True

    elif df.price.iloc[-1] > min_value * 1.05:
        submit_order(contract, 'BUY')
        return True


app = App("localhost", 7496, clientid=0)

time.sleep(1)

INGA = contract_def('INGA')
ASML = contract_def('ASML')

df = app.getTickData(101, ASML)

# Verify data stream
time.sleep(10)
for i in range(100):
    if len(df) > 0:
        print("Succesfull")
        break
    time.sleep(0.3)

if i == 99:
    app.disconnect()
    raise Exception('Error with Tick data stream')

# Check data
data_length = df.index[-1] - df.index[0]
if data_length.seconds < 600:
    time.sleep(600 - data_length.seconds)

# Main loop
while True:
    if trade_condition(df, INGA): break
    time.sleep(0.1)

