# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *
from ibapi.order import *
from ibapi.order_condition import *
import threading
import time


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self, self)
        self.contract_details = {} #initialize a dictionairy to store the contract details

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
ASML = contract_def('ASML')

# Get contract details
ASML = app.get_contract_details(1001, ASML)

# Price condition
priceCondition = Create(OrderCondition.Price)
priceCondition.conId = ASML.conId
priceCondition.exchange = ASML.exchange

priceCondition.isMore = True
priceCondition.triggerMethod = priceCondition.TriggerMethodEnum.Last
priceCondition.price = 550.00

order = Order()
order.action = 'BUY'
order.totalQuantity = 100
order.orderType = 'LMT'
order.lmtPrice = 9
order.conditions.append(priceCondition)
order.transmit = True

app.placeOrder(app.nextorderId, INGA, order)
# app.nextorderId += 1

time.sleep(10)

print('Cancelling order')
app.cancelOrder(app.nextorderId)

app.disconnect()
