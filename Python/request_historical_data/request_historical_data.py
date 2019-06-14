"""
Copyright (C) 2019 LYNX B.V. All rights reserved.
"""

# Import ibapi deps
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.common import *
from ibapi.contract import *
from threading import Thread

from datetime import datetime
from datetime import timedelta
from time import sleep

import pandas as pd

# Create a global DataFrame to insert the data in
historical_data = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low'])

HISTORIC_ID = 5001

class Wrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

    def historicalData(self, reqId: int, bar: BarData):
        """ returns the requested historical data bars

        reqId - the request's identifier
        date  - the bar's date and time (either as a yyyymmss hh:mm:ssformatted
             string or as system time according to the request)
        open  - the bar's open point
        high  - the bar's high point
        low   - the bar's low point
        close - the bar's closing point
        volume - the bar's traded volume if available
        count - the number of trades during the bar's timespan (only available
            for TRADES).
        WAP -   the bar's Weighted Average Price
        hasGaps  -indicates if the data has gaps or not. """

        global historical_data

        historical_data = historical_data.append({'Date': str(bar.date), 'Open': float(bar.open), 'Close': float(bar.close), \
                        'High': float(bar.high), 'Low': float(bar.low)}, ignore_index=True)


    def historicalDataEnd(self, reqId:int, start:str, end:str):
        """ Marks the ending of the historical bars reception. """

        print("Finished downloading historical data")


class Client(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def get_historicalData(self, contract, duration = "1 M", barSize = "1 hour", reqId = HISTORIC_ID):

        queryTime = (datetime.today() - timedelta(days=0)).strftime("%Y%m%d %H:%M:%S")  # Define the end date of the query

        # Here we are requesting historical bar data for the the contract
        self.reqHistoricalData(reqId, contract, queryTime,
                               duration, barSize, "MIDPOINT", 1, 1, False, [])

        MAX_WAITED_SECONDS = 5
        print("Getting historical data from the server... can take %d second to complete" % MAX_WAITED_SECONDS)

        sleep(MAX_WAITED_SECONDS)

        global historical_data

        return historical_data


class TestApp(Wrapper, Client):
    def __init__(self, ipaddress, portid, clientid):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)

        thread = Thread(target = self.run)
        thread.start()

        setattr(self, "_thread", thread)


def main():
    app = TestApp("localhost", 7496, clientid = 0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                  app.twsConnectionTime()))

    # Define the contract
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"

    historical_data = app.get_historicalData(contract)

    historical_data.to_csv("BarData_{}.csv".format(HISTORIC_ID), index_label='index')
    print("BarData csv file created")

    app.disconnect()
    print("We have disconnected from the server")


if __name__ == "__main__":
    main()
