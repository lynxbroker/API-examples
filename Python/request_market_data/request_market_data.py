"""
Copyright (C) 2019 LYNX B.V. All rights reserved.
"""

# Import ibapi deps
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper
from ibapi.contract import *
import datetime

class Wrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

class Client(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

class App(Wrapper, Client):
    def __init__(self):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)
        self.started = False

    @iswrapper
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
    
        # we can start now
        self.start()
 
    @iswrapper
    def start(self):
        if self.started:
            return

        self.started = True
        print("Executing requests")

        # Define the contract to request
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "GBP"
        contract.exchange = "IDEALPRO"

        # Here we are requesting tickdata for the EUR.GBP Contract. The contract's specification is defined above
        self.reqTickByTickData(19004, contract, "MidPoint", 0, False)
            
        print("Executing requests ... finished")

    # Here we print the Midpoint, Request ID and Time returned from the request
    @iswrapper
    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        super().tickByTickMidPoint(reqId, time, midPoint)
        print("Midpoint. ReqId:", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "MidPoint:", midPoint)

def main():
    try:
        # Init the App(Wrapper, Client)
        app = App()
        # Connect to TWS via socket port 7496
        app.connect("127.0.0.1", 7496, clientId=0)
        
        print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                      app.twsConnectionTime()))
        # run
        app.run()
        
    except:
        raise
        
if __name__ == "__main__":
    main()
