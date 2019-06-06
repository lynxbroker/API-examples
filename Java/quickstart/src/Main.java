/**
 * @author LYNX B.V. Amsterdam
 * @version 1.0
 * <p>
 * Copyright (C) 2019 LYNX B.V. All rights reserved.
 * <p>
 * A simple Java implementation for (1) placing an order, (2) requesting contract details, (3) requesting market data or
 * (4) requesting historical data for a product from the TWS (Trader Workstation) or the LYNX Gateway
 */

import com.ib.client.Contract;
import com.ib.client.Order;

import java.util.ArrayList;
import java.util.Scanner;

public class Main {

    private static Contract example_contract;
    private static Order example_order;
    private static TWSConnection twsConnection;


    public static void main(String[] args) {
        // Init twsConnection Object, see TWSConnection.java file
        twsConnection = new TWSConnection();
        twsConnection.makeConnection();

        createSampleContractAndOrder();
        askUserForInput();
    }


    /**
     * Method that initializes a sample contract & order
     */
    private static void createSampleContractAndOrder() {
        // Define Contract details
        example_contract = new Contract();
        example_contract.localSymbol("USD.CAD");
        example_contract.secType("CASH");
        example_contract.currency("CAD");
        example_contract.exchange("IDEALPRO");

        // Define Order details
        example_order = new Order();
        example_order.action("BUY");
        example_order.orderType("MKT");
        example_order.totalQuantity(1);
    }

    /**
     * Asks and listens for user input, therefore firing different actions
     */
    private static void askUserForInput() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("\nPlease choose an action: \n\n(0) Exit\n(1) Place order \n(2) Request contract details\n" +
                "(3) Request market data\n(4) Request historical data\n\nEnter your choice as a number: ");


        int response = checkInput(scanner);

        switch (response) {
            case 0:
                System.out.println("[INFO] Program closed.");
                System.exit(0);
                break;
            case 1:
                System.out.print("\n(1) You chose to place an order.\nDefault contract: USD.CAD/CASH/IDEALPRO & " +
                        "Default order: BUY/MKT/1\n[WARNING] The order type is 'Market Order', therefore it will " +
                        "most likely get filled immediately after placing the order. Do you wish to continue? (y/n)" +
                        "\nResponse (e.g.: y): ");
                if (scanner.nextLine().equals("y")) {
                    twsConnection.client.placeOrder(twsConnection.getNextValidId(), example_contract, example_order);
                } else {
                    System.out.println("\n[INFO] Make another choice.");
                    askUserForInput();
                }
                break;

            case 2:
                System.out.print("\n(2) You chose to request contract details.\nDefault contract: USD.CAD/CASH/IDEALPRO" +
                        "\nDo you wish to continue? (y/n)\nResponse (e.g.: y): ");
                if (scanner.nextLine().equals("y")) {
                    twsConnection.client.reqContractDetails(1, example_contract);
                } else {
                    System.out.println("\n[INFO] Make another choice.");
                    askUserForInput();
                }
                break;

            case 3:
                System.out.print("\n(3) You chose to request market data.\nDefault contract: USD.CAD/CASH/IDEALPRO" +
                        "\nDo you wish to continue? (y/n)\nResponse (e.g.: y): ");
                if (scanner.nextLine().equals("y")) {
                    twsConnection.client.reqMktData(1, example_contract, "", false, false, null);
                } else {
                    System.out.println("\n[INFO] Make another choice.");
                    askUserForInput();
                }
                break;

            case 4:
                System.out.print("\n(4) You chose to request historical data.\nDefault contract: USD.CAD/CASH/IDEALPRO" +
                        "The result will contain midpoint data as 15 mins bars for one day (20190510)." +
                        "\nDo you wish to continue? (y/n)\nResponse (e.g.: y): ");
                if (scanner.nextLine().equals("y")) {
                    twsConnection.client.reqHistoricalData(1, example_contract, "20190510 23:59:59 GMT", "1 D",
                            "15 mins", "MIDPOINT", 1, 1, false, new ArrayList<>());
                } else {
                    System.out.println("\n[INFO] Make another choice.");
                    askUserForInput();
                }
                break;
        }

    }


    /**
     *
     * @param scanner used to get keyboard user input
     * @return response expressed as an integer (1 to 4)
     */
    private static int checkInput(Scanner scanner) {

        String userInput = scanner.nextLine();
        int finalResponse;

        try {
            Integer.parseInt(userInput);
            if (Integer.parseInt(userInput) > 4) {
                System.out.print("Not an available option. Please enter a number (e.g.: 1): ");
                finalResponse = checkInput(scanner);
                return finalResponse;
            }
            return Integer.parseInt(userInput);

        } catch (NumberFormatException e) {
            System.out.print("Wrong input. Please enter a number (e.g.: 1): ");
            finalResponse = checkInput(scanner);
        }

        return finalResponse;
    }
}
