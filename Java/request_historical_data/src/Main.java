import com.ib.client.Contract;
import com.ib.client.Order;
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
        
        TWSConnection.INSTANCE.client.reqHistoricalData(1, example_contract, "20190510 23:59:59 GMT", "1 D", "15 mins", "MIDPOINT", 1,1, false, new ArrayList<>());
    }
}
