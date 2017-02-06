package Discovery;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

/**
 * Created by ivan on 21/07/2016.
 */
public class DiscoveryBroadcastThread extends Thread {

    ServerIdentification serverIdentification;
    ByteArrayOutputStream arrayOutputStream;
    ObjectOutputStream os;
    DatagramSocket socket;

    @Override
    public void run() {

        try {
            /*
             * Setup local identification
             */
            serverIdentification = new ServerIdentification("PI",
                    "TV speaker in the living room",
                    InetAddress.getLocalHost(),
                    3000);
            //Setup streams to send ID object over network
            arrayOutputStream = new ByteArrayOutputStream();
            os = new ObjectOutputStream(arrayOutputStream);
            os.writeObject(serverIdentification);

            //Keep a socket open to listen to all the UDP trafic that is destined for this port
            socket = new DatagramSocket(8888, InetAddress.getByName("0.0.0.0"));
            socket.setBroadcast(true);



            while (true) {
                System.out.println(getClass().getName() + ">>>Ready to receive broadcast packets!");

                //Receive a packet
                byte[] recvBuf = new byte[15000];
                DatagramPacket packet = new DatagramPacket(recvBuf, recvBuf.length);
                socket.receive(packet);

                //Packet received
                System.out.println(getClass().getName() + ">>>Discovery packet received from: " + packet.getAddress().getHostAddress());
                System.out.println(getClass().getName() + ">>>Packet received; data: " + new String(packet.getData()));

                //See if the packet holds the right command (message)
                String message = new String(packet.getData()).trim();
                if (message.equals("DISCOVER_FUIFSERVER_REQUEST")) {
                    byte[] sendData = arrayOutputStream.toByteArray();

                    //Send a response
                    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, packet.getAddress(), packet.getPort());
                    socket.send(sendPacket);

                    System.out.println(getClass().getName() + ">>>Sent packet to: " + sendPacket.getAddress().getHostAddress());
                }
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
