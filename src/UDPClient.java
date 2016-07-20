import javax.sound.sampled.*;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;

/**
 * Created by ivan on 20/07/2016.
 */
public class UDPClient {

    AudioFormat format;
    private DatagramSocket socket;
    private DatagramPacket packet = null;

    public UDPClient() throws SocketException {
        socket = new DatagramSocket();

        AudioSetting audioSetting = new AudioSetting();
        format = audioSetting.getAudioFormat();
    }

    private void listen(){

        try {
            DataLine.Info speakerInfo = new DataLine.Info(SourceDataLine.class,format);
            SourceDataLine speaker = (SourceDataLine) AudioSystem.getLine(speakerInfo);
            speaker.open(format);
            speaker.start();

            while (true) {
                byte[] data = new byte[1024];
                packet = new DatagramPacket(data, data.length);
                socket.receive(packet);

                ByteArrayInputStream bais = new ByteArrayInputStream(data);
                AudioInputStream ais = new AudioInputStream(bais,format,data.length);
                int bytesRead = 0;
                if((bytesRead = ais.read(data)) != -1){
                    System.out.println("Writing to audio output.");
                    speaker.write(data,0,bytesRead);

                    //System.out.println(Arrays.toString(data));
                    //                 bais.reset();
                }
                ais.close();
                bais.close();
            }


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws IOException {

        UDPClient client = new UDPClient();
        client.listen();
    }
}
