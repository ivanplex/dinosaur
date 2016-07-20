import java.io.IOException;

/**
 * Created by ivan on 20/07/2016.
 */
public class UDPServer{

    public static void main(String[]args)throws IOException {
        new UDPServerThread().start();
    }
}
