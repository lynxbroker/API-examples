// Copyright (C) 2019 LYNX B.V. All rights reserved.
import com.ib.client.Contract;

public class Main {

    public static void main(String[] args){
        // Init twsConnection Object, see TWSConnection.java file
        TWSConnection twsConnection = new TWSConnection();
        twsConnection.makeConnection();

        // Define Contract details
        Contract example_contract = new Contract();
        example_contract.localSymbol("USD.CAD");
        example_contract.secType("CASH");
        example_contract.currency("CAD");
        example_contract.exchange("IDEALPRO");

        // Define Order details
        Order example_order = new Order();
        example_order.action("BUY");
        example_order.orderType("LMT");
        example_order.totalQuantity(10);
        example_order.lmtPrice(1.34);

        // Send the order request to the API
        TWSConnection.INSTANCE.client.placeOrder(1, example_contract, example_order);
    }
}
