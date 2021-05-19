# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *
from ibapi.order import *
import threading
import time


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self,self)

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run) #run the socket in a thread
        app_thread.start()

    def nextValidId(self, orderId:int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId , status, filled,remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


app = App("localhost", 7496, clientid = 0)

time.sleep(1)

contract = Contract()
contract.symbol = "INGA"
contract.secType = "STK"
contract.currency = "EUR"
contract.exchange = "AEB"

order = Order()
order.action = 'BUY'
order.totalQuantity = 100
order.orderType = 'LMT'
order.lmtPrice = '9'
order.orderId = app.nextorderId
app.nextorderId += 1
order.transmit = False

#Stop loss order
stop_order = Order()
stop_order.action = 'SELL'
stop_order.totalQuantity = 100
stop_order.orderType = 'STP'
stop_order.auxPrice = '7'
stop_order.orderId = app.nextorderId
app.nextorderId += 1
stop_order.parentId = order.orderId
order.transmit = True

app.placeOrder(order.orderId, contract, order)
app.placeOrder(stop_order.orderId, contract, stop_order)

time.sleep(10)

print('Cancelling orders')
app.cancelOrder(order.orderId)

app.disconnect()