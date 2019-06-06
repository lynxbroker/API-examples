## Java and the LYNX API

*A simple Java implementation for requesting streaming market data or placing an order for a product from the TWS (Trader Workstation) or the LYNX Gateway.*

### Requirements:

- Java TWS API library (included in the repository or [check available versions](https://lynxbroker.github.io/#/API_versions))
- TWS running
- Socket Connection enabled and configured: *Configure->API->Settings* *(Port 7496 & Enable ActiveX and Socket Clients)*
- [Java JDK 8+](https://www.oracle.com/technetwork/java/javase/downloads/index.html)



### Library location

> If you want to manually add the java LYNX API library, the location can be found at ".../TWS_installation_folder/source/JavaClient":

<p align="center">
  <img src="images/jar_location.png">
</p>


### The [TWSConnection.java](https://github.com/lynxbroker/API-examples/blob/master/Java/request_historical_data/src/TWSConnection.java) class:

> Handles the connection and the incoming messages/requests.
>
> As an example, the following function facilitates the parsing of the price information for the products. The *"field"* parameter gives the type of the value (e.g.: bid, ask, low, high etc.) in relation with the *"tickerId"* (unique for each contract).

```java
...
@Override
public void tickPrice(int tickerId, int field, double price, TickAttrib tickAttrib) {

    //bid
    if (field == 1) {
        System.out.println("Bid price: " + price + " for contract with id " + tickerId);
    }

    //ask
    if (field == 2) {
        System.out.println("Ask price: " + price + " for contract with id " + tickerId);
    }
}
...
```





### The [Main.java](https://github.com/lynxbroker/API-examples/blob/master/Java/request_historical_data/src/Main.java) class:

> The place where the API calls are made from & the connection to the API is established. Once the connection to the API is created through the TWSConnection class object, different types of requests can be made. Below, some examples are provided.



#### Requesting historical data:

> In order to request historical data for a specific contract, the following API call has to be made:



```java
// Copyright (C) 2019 LYNX B.V. All rights reserved.
import com.ib.client.Contract;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args){
        TWSConnection twsConnection = new TWSConnection();
        twsConnection.makeConnection();

        Contract example_contract = new Contract();
        example_contract.localSymbol("USD.CAD");
        example_contract.secType("CASH");
        example_contract.currency("CAD");
        example_contract.exchange("IDEALPRO");
        
        TWSConnection.INSTANCE.client.reqHistoricalData(1, example_contract, "20190510 23:59:59 GMT", "1 D", "15 mins", "MIDPOINT", 1, 1, false, new ArrayList<>());
    }
}
```



> After invoking the [reqHistoricalData](https://lynxbroker.github.io/#/EClient?id=reqhistoricaldata) method, the result containing *midpoint* data as *15 mins bars* for *one day* will be sent to the [historicalData](https://lynxbroker.github.io/#/EWrapper?id=historicaldata) function (in TWSConnection.java class). Finally, the output looks like this:

<p align="center">
  <img src="images/request_historical_data.png">
</p>
