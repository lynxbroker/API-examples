# Copyright (C) 2020 LYNX B.V. All rights reserved.
from ibapi import wrapper
from ibapi.wrapper import EWrapper
from ibapi.client import EClient

# We require common and contract to handle the incoming data
from ibapi.common import *
from ibapi.contract import *

# We require threading to handle the data streams
from threading import Thread

# Client => this is where our requests are made
class Client(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def requestOptionChains(self):
        print("Requesting..")
        self.reqSecDefOptParams(0, "IBM", "", "STK", 8314)

class Wrapper(EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self) 
    def securityDefinitionOptionParameter(self, reqId: int, exchange: str,
        underlyingConId: int, tradingClass: str, multiplier: str,
        expirations: SetOfString, strikes: SetOfFloat):
        super().securityDefinitionOptionParameter(reqId, exchange,
        underlyingConId, tradingClass, multiplier, expirations, strikes)
        print("SecurityDefinitionOptionParameter.",
        "ReqId:", reqId, "Exchange:", exchange, "Underlying conId:", underlyingConId, "TradingClass:", tradingClass, "Multiplier:", multiplier,
        "Expirations:", expirations, "Strikes:", str(strikes))

# App
class App(Wrapper, Client):
    def __init__(self, ipaddress, portid, clientid):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)
        self.connect(ipaddress, portid, clientid)   
        thread = Thread(target = self.run)
        thread.start()
        setattr(self, "_thread", thread)

def main():
    app = App('localhost', 7496, 0)
    app.requestOptionChains()

if __name__ == "__main__":
    main()