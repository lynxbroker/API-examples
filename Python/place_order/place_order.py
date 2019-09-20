
# Copyright (C) 2019 LYNX B.V. All rights reserved.


# Import ibapi deps
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import *
from ibapi.order import *
from threading import Thread

from time import sleep

nextValidOrderId = 0

class Wrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

    def nextValidId(self, orderId: int):
        """ Receives next valid order id."""

        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

        global nextValidOrderId

        nextValidOrderId = orderId

class Client(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def place_order(self, contract, order):
        MAX_WAITED_SECONDS = 5

        global nextValidOrderId

        print("Getting the next valid orderid from the server...")
        sleep(MAX_WAITED_SECONDS)

        # Here we are plcaing the request for the order
        self.placeOrder(nextValidOrderId, contract, order)

        print("Placing order... can take %d second to complete" % MAX_WAITED_SECONDS)
        sleep(MAX_WAITED_SECONDS)


class TestApp(Wrapper, Client):
    def __init__(self, ipaddress, portid, clientid):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)

        thread = Thread(target=self.run)
        thread.start()

        setattr(self, "_thread", thread)


def main():
    # Init the TestApp(Wrapper, Client)
    app = TestApp("localhost", 7496, clientid = 0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                  app.twsConnectionTime()))

    # Define the contract
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"

    # Define the order to place
    order = Order()
    order.action = "BUY"
    order.orderType = "LMT"
    order.totalQuantity = 1000
    order.lmtPrice = 1.12

    app.place_order(contract, order)

if __name__ == "__main__":
    main()
