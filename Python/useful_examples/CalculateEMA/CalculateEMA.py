# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *
import threading
import time
import pandas
import indicators


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self, self)
        self.data = [] #initialize variable

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run)  # run the socket in a thread
        app_thread.start()

    def historicalData(self, reqId, bar):
        self.data.append([bar.date, bar.close])


app = App("localhost", 7496, clientid=0)

time.sleep(1)

contract = Contract()
contract.symbol = "INGA"
contract.secType = "STK"
contract.currency = "EUR"
contract.exchange = "AEB"

app.reqHistoricalData(1, contract, '', '5 D', '1 hour', 'TRADES', 0, 2, False, [])

time.sleep(5)

df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
df = indicators.exponential_moving_average(df, 20)
df.to_csv('INGA_Hourly_EMA.csv')

print(df.tail(20))

app.disconnect()