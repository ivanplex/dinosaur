package UDPComm;

import TCPComm.AudioSetting;

import javax.sound.sampled.*;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

/**
 * Created by ivan on 20/07/2016.
 */
public class UDPServerThread extends Thread{

    AudioFormat format;
    protected DatagramSocket socket = null;
    long threadId;

    DatagramPacket packet = null;

    public UDPServerThread() throws SocketException {
        socket = new DatagramSocket(3000);
        threadId = Thread.currentThread().getId();

        AudioSetting audioSetting = new AudioSetting();
        format = audioSetting.getAudioFormat();
    }

    public void run(){

        try {
            DataLine.Info micInfo = new DataLine.Info(TargetDataLine.class,format);
            TargetDataLine mic = (TargetDataLine) AudioSystem.getLine(micInfo);
            mic.open(format);
            System.out.println("On Air");
            byte tmpBuff[] = new byte[mic.getBufferSize()/5];
            mic.start();

            while(true) {
                System.out.println("Reading from mic.");
                int count = mic.read(tmpBuff,0,tmpBuff.length);
                if (count > 0){
                    System.out.println(threadId+": Writing buffer to server.");
                    InetAddress addr = InetAddress.getByName("localhost");
                    packet = new DatagramPacket(tmpBuff, 0, tmpBuff.length, addr, 3000);
                    socket.send(packet);
                    //System.out.println(Arrays.toString(tmpBuff));
                }
            }
        } catch (LineUnavailableException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}

