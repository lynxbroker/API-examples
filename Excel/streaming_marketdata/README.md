# Receiving Real-Time Quotes in Excel

TWS RTD Server API is a dynamic link library which allows LYNX clients to request real-time market data from TWS via API using Microsoft Excel. The TWS RTD Server API directly connects to TWS via the socket. It allows displaying streaming live (or 15-minute delayed) market data in Excel by entering formulas into an Excel cell following a specific syntax.

> At the current stage, only top-level market data is supported via TWS RTD Server API. No trading capability or other data types are supported. Both Delayed and Real-Time data are supported via TWS RTD Server API. Real-time market data is required for requesting live streaming market data.

Market data can be requested using the following formula:

`=RTD(**ProgID**, **Server**, **String1**, **String2**, ...)`

where

> **ProgID** = "Tws.TwsRtdServerCtrl"
>
> **Server** = "" (empty string)
>
> **String1**, **String2**, ... is a list of strings representing **Ticker**, **Topic**, **Connection Parameters** or other **Complex Syntax** strings.

---

## Quick Start with Excel-RTD

### Requirements:

> - Windows Operating System
> - Microsoft Excel
> - API Software Installed
> - TWS/LYNX Platform Running
> - Socket Connection enabled and configured (in TWS): Configure->API->Settings (Port - 7496 & Enable ActiveX and Socket Clients)



---

### Running Excel-RTD:

Open the Excel-sheet 'TwsRtdServer_SimpleSheet.xls' and go to the Forex Sheet:



![](images/Excel-RTD_3.png)



Now you should see the following sheet, featuring 'Start' and 'End' buttons as well as several Forex pairs:



![](images/Excel-RTD_1.png)



> Using the 'Start' and 'End' buttons allows you to quickly request data for all underlyings in the sheet



After opting to 'Start' quotes should appear within a few seconds in the same fashion as displayed below.



![](images/Excel-RTD_2.png)



These quotes will update in real-time and can be used to make calculations within Excel.

---

### More information:

- [Troubleshooting](https://api.lynx.academy/RTD_Troubleshooting)
- [Simple Syntax](https://api.lynx.academy/RTD_Simple_Syntax)
- [Mixed Syntax](https://api.lynx.academy/RTD_Mixed_Syntax)
- [Complex Syntax](https://api.lynx.academy/RTD_Complex_Syntax)