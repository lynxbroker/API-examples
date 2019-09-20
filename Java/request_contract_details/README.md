## Java and the <span style="color:green">LYNX API</span>

*A simple Java implementation for requesting streaming market data or placing an order for a product from the TWS (Trader Workstation) or the LYNX Gateway.*

### Requirements:

- Java TWS API library (included in the repository or [check available versions](https://api.lynx.academy/API_versions))
- TWS running
- Socket Connection enabled and configured: *Configure->API->Settings* *(Port 7496 & Enable ActiveX and Socket Clients)*
- [Java JDK 8+](https://www.oracle.com/technetwork/java/javase/downloads/index.html)



### Library location

> If you want to manually add the java LYNX API library, the location can be found at ".../TWS_installation_folder/source/JavaClient":

<p align="center">
  <img src="images/jar_location.png">
</p>


### The [TWSConnection.java](https://github.com/lynxbroker/API-examples/blob/master/Java/request_contract_details/src/TWSConnection.java) class:

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





### The [Main.java](https://github.com/lynxbroker/API-examples/blob/master/Java/request_contract_details/src/Main.java) class:

> The place where the API calls are made from & the connection to the API is established. Once the connection to the API is created through the TWSConnection class object, different types of requests can be made. Below, some examples are provided.



#### Requesting contract details:

> In order to request information in regard to a product such as: conid, minimum tick, trading hours, multiplier etc., the following API call has to be made:



```java
// Copyright (C) 2019 LYNX B.V. All rights reserved.
import com.ib.client.Contract;

public class Main {

    public static void main(String[] args){
        // Init twsConnection Object, see TWSConnection.java file
        TWSConnection twsConnection = new TWSConnection();
        twsConnection.makeConnection();

        // Define the Contract
        Contract example_contract = new Contract();
        example_contract.localSymbol("USD.CAD");
        example_contract.secType("CASH");
        example_contract.currency("CAD");
        example_contract.exchange("IDEALPRO");

        // Request the Contract details
        TWSConnection.INSTANCE.client.reqContractDetails(1, example_contract);
    }
}
```



> After invoking the [reqContractDetails](https://api.lynx.academy/EClient?id=reqcontractdetails) method, the result will be sent to the [contractDetails](https://api.lynx.academy/EWrapper?id=contractdetails) function (in TWSConnection.java class). Finally, the output looks like this:




![](images/request_contract_details.png)
