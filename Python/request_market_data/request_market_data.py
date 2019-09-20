"""
Copyright (C) 2019 LYNX B.V. All rights reserved.
"""

# Import ibapi deps
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import *
from threading import Thread

from datetime import datetime
from time import sleep

MARKET_ID = 19004

class Wrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        """returns tick-by-tick data for tickType = "MidPoint" """

        print("Midpoint. ReqId:", reqId,
              "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "MidPoint:", midPoint)

class Client(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def get_marketData(self, contract, reqId = MARKET_ID):

        # Here we are requesting tickdata for the EUR.GBP Contract.
        self.reqTickByTickData(reqId, contract, "MidPoint", 0, False)

        MAX_WAITED_SECONDS = 5
        print("Getting tick data from the server... can take %d second to complete" % MAX_WAITED_SECONDS)

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
    
    # Here we call the function that includes the request for market data   
    app.get_marketData(contract)


if __name__ == "__main__":
    main()
