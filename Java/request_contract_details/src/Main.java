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
