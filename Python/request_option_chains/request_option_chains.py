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

    def requestOptionChains(self, contract):
        print("Requesting..")
        self.reqSecDefOptParams(0, contract.symbol, "", contract.secType, 8314)

class Wrapper(EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str,
        underlyingConId: int, tradingClass: str, multiplier: str,
        expirations: SetOfString, strikes: SetOfFloat):
        """ Returns the option chain for an underlying on an exchange
        specified in reqSecDefOptParams There will be multiple callbacks to
        securityDefinitionOptionParameter if multiple exchanges are specified
        in reqSecDefOptParams

        reqId - ID of the request initiating the callback
        underlyingConId - The conID of the underlying security
        tradingClass -  the option trading class
        multiplier -    the option multiplier
        expirations - a list of the expiries for the options of this underlying
             on this exchange
        strikes - a list of the possible strikes for options of this underlying
             on this exchange """

        super().securityDefinitionOptionParameter(reqId, exchange,
        underlyingConId, tradingClass, multiplier, expirations, strikes)
        print("Exchange:", exchange, "Underlying conId:", underlyingConId, "TradingClass:", tradingClass, "Multiplier:", multiplier,'\n',
        "Expirations:", expirations,'\n', "Strikes:", str(strikes))

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
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                  app.twsConnectionTime()))

    # Define the contract
    contract = Contract()
    contract.symbol = "IBM"
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"

    app.requestOptionChains(contract)

if __name__ == "__main__":
    main()