package Discovery;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.*;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;

/**
 * Created by ivan on 21/07/2016.
 */
public class DiscoveryClient {

    List<ServerIdentification> listOfServers;
    DatagramSocket c;

    /**
     * Find all service related servers under unknown network settings.
     * Design to be run at startup, once.
     * @return List  service servers' ID
     */
    public List<ServerIdentification> findServers(){

        listOfServers = new ArrayList<ServerIdentification>();


        // Find the server using UDP broadcast
        try {
            //Open a random port to send the package
            c = new DatagramSocket();
            c.setBroadcast(true);

            byte[] sendData = "DISCOVER_FUIFSERVER_REQUEST".getBytes();

            //Try the 255.255.255.255 first
            try {
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, InetAddress.getByName("255.255.255.255"), 8888);
                c.send(sendPacket);
                System.out.println("Network Discovery>>> Request packet sent to: 255.255.255.255 (DEFAULT)");
            } catch (Exception e) {
            }

            // Broadcast the message over all the network interfaces
            Enumeration interfaces = NetworkInterface.getNetworkInterfaces();
            while (interfaces.hasMoreElements()) {
                NetworkInterface networkInterface = (NetworkInterface) interfaces.nextElement();

                if (networkInterface.isLoopback() || !networkInterface.isUp()) {
                    continue; // Don't want to broadcast to the loopback interface
                }

                for (InterfaceAddress interfaceAddress : networkInterface.getInterfaceAddresses()) {
                    InetAddress broadcast = interfaceAddress.getBroadcast();
                    if (broadcast == null) {
                        continue;
                    }

                    // Send the broadcast package!
                    try {
                        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, broadcast, 8888);
                        c.send(sendPacket);
                    } catch (Exception e) {
                    }

                    System.out.println("Network Discovery>>> Request packet sent to: " + broadcast.getHostAddress() + "; Interface: " + networkInterface.getDisplayName());
                }
            }

            System.out.println("Network Discovery>>> Done looping over all network interfaces. Now waiting for a reply!");

            //Wait for a response
            byte[] recvBuf = new byte[15000];
            DatagramPacket receivePacket = new DatagramPacket(recvBuf, recvBuf.length);
            c.receive(receivePacket);

            //We have a response
            System.out.println("Network Discovery>>> Broadcast response from server: " + receivePacket.getAddress().getHostAddress());

            byte[] receivedData = receivePacket.getData();
            ByteArrayInputStream in = new ByteArrayInputStream(receivedData);
            ObjectInputStream is = new ObjectInputStream(in);
            try {
                Object receivedObject = is.readObject();
                if(receivedObject instanceof ServerIdentification){
                    System.out.println("Network Discovery>>>Server Name: "+((ServerIdentification) receivedObject).getServerName());
                    System.out.println("Network Discovery>>>Server Description: "+((ServerIdentification) receivedObject).getDescription());
                    System.out.println("Network Discovery>>>Server IP: "+((ServerIdentification) receivedObject).getServerAddress());
                    System.out.println("Network Discovery>>>Server Port: "+((ServerIdentification) receivedObject).getPort());

                    listOfServers.add((ServerIdentification) receivedObject);
                }
            } catch (ClassNotFoundException e) {
                //Ignore non-class and unrelated objects
            }

            //Check if the message is correct
            /*String message = new String(receivePacket.getData()).trim();
            if (message.equals("DISCOVER_FUIFSERVER_RESPONSE")) {
                //DO SOMETHING WITH THE SERVER'S IP (for example, store it in your controller)
                //Controller_Base.setServerIp(receivePacket.getAddress());

                return receivePacket.getAddress();
            }*/

            //Close the port!
            c.close();
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        return listOfServers;
    }
}
