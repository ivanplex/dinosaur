import javax.sound.sampled.*;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

public class StreamClient{

    private static String serverIP;

    public StreamClient(String serverIP) throws IOException{
        this.serverIP = serverIP;
        isl.runListener();
    }

    private IncomingSoundListener isl = new IncomingSoundListener();
    AudioFormat format = getAudioFormat();
    InputStream is;
    Socket client;
    String serverName = serverIP.toString();
    int port=3000;
    boolean inVoice = true;


    private AudioFormat getAudioFormat(){
        float sampleRate = 16000.0F;
        int sampleSizeBits = 16;
        int channels = 1;
        boolean signed = true;
        boolean bigEndian = false;

        return new AudioFormat(sampleRate, sampleSizeBits, channels, signed, bigEndian);
    }
    class IncomingSoundListener {
        public void runListener(){
            try{
                System.out.println("Connecting to server:"+serverName+" Port:"+port);
                client = new Socket(serverName,port);
                System.out.println("Connected to: "+client.getRemoteSocketAddress());
                System.out.println("Listening for incoming audio.");
                DataLine.Info speakerInfo = new DataLine.Info(SourceDataLine.class,format);
                SourceDataLine speaker = (SourceDataLine) AudioSystem.getLine(speakerInfo);
                speaker.open(format);
                speaker.start();
                while(inVoice){
                    is = client.getInputStream();
                    byte[] data = new byte[1024];
                    is.read(data);

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
                speaker.drain();
                speaker.close();
                System.out.println("Stopped listening to incoming audio.");
            }catch(Exception e){
                e.printStackTrace();
            }
        }
    }
    public static void main(String [] args) throws IOException{
        new StreamClient(args[0]);
    }
}