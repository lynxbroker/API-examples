# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import *
from ibapi.common import BarData

import threading
from datetime import datetime
from datetime import timedelta
from time import sleep
import pandas as pd


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self, self)
        self.data = []  # initialize variable to store data in

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run)  # run the socket in a thread
        app_thread.start()

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

        # append the bardata in the data variable
        self.data.append([bar.date, bar.open, bar.close, bar.high, bar.low])


def main():
    app = App("localhost", 7496, clientid = 0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                  app.twsConnectionTime()))

    # Define the contract
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "GBP"
    contract.exchange = "IDEALPRO"

    # Define the end date of the query. If left empty, the current date/time is taken as the end date.
    queryTime = (datetime.today() - timedelta(days=0)).strftime("%Y%m%d %H:%M:%S")

    # Here we are requesting historical bar data for the the EUR.GBP contract
    reqId = 4001
    app.reqHistoricalData(reqId, contract, queryTime, "1 M", "1 hour", "MIDPOINT", 1, 1, False, [])

    MAX_WAITED_SECONDS = 5
    print("Getting historical data from the server... can take %d second to complete" % MAX_WAITED_SECONDS)

    sleep(MAX_WAITED_SECONDS)

    # Create a CSV file of the historical data
    df = pd.DataFrame(app.data, columns=['DateTime','Open', 'Close', 'High', 'Low'])
    df.to_csv("BarData_{}.csv".format(reqId), index_label='index')
    print("BarData csv file created")

    # The connection can be disconnected after the data has been received
    app.disconnect()


if __name__ == "__main__":
    main()
