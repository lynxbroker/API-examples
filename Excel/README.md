### [What You Will Need](https://lynxbroker.github.io/#/RTD_Server_for_Excel?id=what-you-will-need)

#### Windows Operating System

Since the TWS RTD Server API technology directly refers to the C# API client source functions, it is supported on [Windows Environment](https://lynxbroker.github.io/#/SystemRequirements) only.

#### API version 9.73.03+

You need to download [API](https://lynxbroker.github.io/#/API_versions) Windows version 9.73.03 or higher and install on your computer. Once you have installed the API, you can verify the API Version by checking *C:\TWS API\API_VersionNum.txt* by default.

#### TWS (or LYNX Gateway) Build 963+

By default, market data requests sent via TWS RTD Server will automatically request for all possible [Generic Tick Types](https://lynxbroker.github.io/#/RTD_Simple_Syntax?id=generic-tick-types). There are several generic tick types being requested that are only supported in TWS 963 or higher. Sending any RTD market data request with default generic tick list to an old build of TWS will trigger a "TwsRtdServer error" indicating incorrect generic tick list is sent. Make sure a [TWS builds 963+](https://www.lynx.nl/service/handelsplatform/installeren/) is downloaded from LYNX website and kept running at the background for TWS RTD Server API to function properly.

#### Enable Socket Client in TWS (or IB Gateway)

Since the TWS RTD Server API directly refers to the C# API source, RTD market data requests will be sent via the socket layer. Please make sure to [Enable ActiveX and Socket Client](https://lynxbroker.github.io/#/initial_setup?id=enable-api-connections-) settings in your TWS.

Please also be mindful of the socket port that you configure in your TWS API settings. The default socket port TWS will listen on is **7496** for a live session, and **7497** for a paper session. It is further discussed in section [Connection Parameters](https://lynxbroker.github.io/#/RTD_Simple_Syntax?id=rtd_simple_syntax_conn) that TWS RTD Server connects to port **7496** by default, and you are able to customize the port number to connect by specifying pre-defined [Connection Parameters](https://lynxbroker.github.io/#/RTD_Simple_Syntax?id=rtd_simple_syntax_conn) or using string "port=". You can use any valid port for connection as you wish, and you just need to make sure that the port you are trying to connect to via the API is the same port your TWS is listening on.

#### Microsoft Excel

After installing the API, the pre-compiled RTD library file (located at *C:\TWS API\source\csharpclient\TwsRtdServer\bin\Release\TwsRtdServer.dll* by default) registered on your computer will be in 32-bit by default for API versions from 973.03 to 973.06. If you are using 64-bit Microsoft Excel, you would need to re-compile RTD server dll file into 64-bit and register the library by re-building the RTD source solution using Visual Studio. Please refer to the [TWS Excel APIs, featuring the RealTimeData Server](https://attendee.gotowebinar.com/register/7412660386944689921) recorded webinar for more information. Beginning in API v973.07* it is expected that the API installer for RTD Server will be compatible with both 32 bit and 64 bit Excel (* expected version number).