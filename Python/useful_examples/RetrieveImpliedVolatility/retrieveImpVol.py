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



app = App("localhost", 7496, clientid = 0)

time.sleep(1)

contract = Contract()
contract.symbol = "INGA"
contract.secType = "STK"
contract.currency = "EUR"
contract.exchange = "AEB"


time.sleep(5)
app.disconnect()