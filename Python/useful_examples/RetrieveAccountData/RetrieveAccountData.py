# Copyright (C) 2021 LYNX B.V. All rights reserved.

# Import ibapi deps
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.account_summary_tags import *

import threading
import time
import pandas as pd


class App(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        EClient.__init__(self,self)
        self.account_data = []

        self.connect(ipaddress, portid, clientid)
        app_thread = threading.Thread(target=self.run) #run the socket in a thread
        app_thread.start()

    def accountSummary(self, reqId, account, tag, value, currency):
        self.account_data.append([account, tag, value, currency])


app = App("localhost", 7497, clientid = 0)

time.sleep(1)

app.reqAccountSummary(5001, "All", AccountSummaryTags.AllTags)

time.sleep(5)

df = pd.DataFrame(app.account_data, columns=["Account", "Tag", "Value", "Currency"])

print(df)

app.disconnect()