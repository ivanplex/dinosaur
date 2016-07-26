package TCPComm;

import Discovery.DiscoveryClient;
import Discovery.NoServerFoundException;
import Discovery.ServerIdentification;

import javax.sound.sampled.*;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.util.Iterator;
import java.util.List;

public class StreamClient{

    DiscoveryClient discoveryClient;

    AudioFormat audioFormat = getAudioFormat();
    InputStream inputStream;
    Socket socket;
    String serverAddress;
    int port=3000;
    boolean inVoice = true;

    public StreamClient(){
        try {
            connectServer("PI");
        } catch (NoServerFoundException e) {
            e.printStackTrace();
            System.exit(0);
        }


        new IncomingSoundListener().runListener();
    }

    private void connectServer(String serverName) throws NoServerFoundException {
        discoveryClient = new DiscoveryClient();
        List<ServerIdentification> serversList = discoveryClient.findServers();

        /*
         * Loop through list and find server
         * Connect the first server with matching a machine name
         */
        ServerIdentification id;
        Iterator<ServerIdentification> serverIterator = serversList.iterator();
        while (serverIterator.hasNext()){
            id = serverIterator.next();
            if(id.getServerName().equals(serverName)){
                serverAddress = id.getServerAddress().getHostAddress();
                return;
            }
        }
        throw new NoServerFoundException();
    }

    private AudioFormat getAudioFormat(){
        float sampleRate = 44100.0F;
        int sampleSizeBits = 16;
        int channels = 1;
        boolean signed = true;
        boolean bigEndian = false;

        return new AudioFormat(sampleRate, sampleSizeBits, channels, signed, bigEndian);
    }

    class IncomingSoundListener {
        public void runListener(){
            try{
                System.out.println("Connecting to server:"+serverAddress+" Port:"+port);
                socket = new Socket(serverAddress,port);
                System.out.println("Connected to: "+socket.getRemoteSocketAddress());

                System.out.println("Listening for incoming audio.");
                DataLine.Info speakerInfo = new DataLine.Info(SourceDataLine.class, audioFormat);
                SourceDataLine speaker = (SourceDataLine) AudioSystem.getLine(speakerInfo);
                speaker.open(audioFormat, 256000);
                speaker.start();

                /*
                 *  https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ArrayBlockingQueue.html
                 */
                /*Queue<byte[]> audioPacketQueue = new ArrayBlockingQueue<>(100);
                boolean audioQueueEmptyed = true;

                System.out.println("Loading....");*/
                while(inVoice){
                    inputStream = socket.getInputStream();
                    byte[] data = new byte[4096];
                    //System.out.println(inputStream.available());
                    inputStream.read(data);

                    /*if(audioQueueEmptyed) {
                        try {
                            audioPacketQueue.add(data);
                        } catch (IllegalStateException fullQueueException) {
                            audioQueueEmptyed = false;
                            play(speaker, audioPacketQueue.poll());
                            audioPacketQueue.add(data);
                        }
                    }else{
                        //System.out.println("PLAY");
                        if(audioPacketQueue.peek() != null) {
                            play(speaker, audioPacketQueue.poll());
                        }else{
                            audioQueueEmptyed = true;
                        }
                    }*/
                    play(speaker, data);


                }
                speaker.drain();
                speaker.close();
                System.out.println("Stopped listening to incoming audio.");
            }catch(Exception e){
                e.printStackTrace();
            }
        }

        private void play(SourceDataLine speaker, byte[] data) throws IOException {
            ByteArrayInputStream bais = new ByteArrayInputStream(data);
            AudioInputStream ais = new AudioInputStream(bais, audioFormat, data.length);
            int bytesRead = 0;
            if((bytesRead = ais.read(data)) != -1){
                //System.out.println("Bytes Read:" + bytesRead);  //1024
                //System.out.println("Writing to audio output.");
                speaker.write(data,0,bytesRead);

                //System.out.println(Arrays.toString(data));
                //                 bais.reset();
            }
            ais.close();
            bais.close();
        }
    }

    public static void main(String [] args) throws IOException{
        new StreamClient();
    }
}