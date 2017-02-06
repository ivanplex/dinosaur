package Discovery;

import java.io.Serializable;
import java.net.InetAddress;

/**
 * Created by ivan on 22/07/2016.
 */
public class ServerIdentification implements Serializable {

    private String serverName;
    private String description;
    private InetAddress serverAddress;
    private int port;

    public ServerIdentification(String serverName, String description, InetAddress serverAddress, int port) {
        this.serverName = serverName;
        this.description = description;
        this.serverAddress = serverAddress;
        this.port = port;
    }

    /**
     * Server's Machine Name
     * @return  String  Server name
     */
    public String getServerName() {
        return serverName;
    }

    /**
     * Description of the server.
     * @return  String  description
     */
    public String getDescription() {
        return description;
    }

    /**
     * Get server's local IP address
     * @return
     */
    public InetAddress getServerAddress() {
        return serverAddress;
    }

    /**
     * Get the port number of the service which it is running.
     * @return  int  port number
     */
    public int getPort() {
        return port;
    }
}
