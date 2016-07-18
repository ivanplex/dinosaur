import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.TargetDataLine;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

//import org.apache.commons.io.output.ByteArrayOutputStream;


public class StreamServer {
    //private OutgoingSoudnListener osl = new OutgoingSoudnListener();
    boolean outVoice = true;
    AudioFormat format = getAudioFormat();
    private ServerSocket serverSocket;


    private AudioFormat getAudioFormat() {
        float sampleRate = 16000.0F;
        int sampleSizeBits = 16;
        int channels = 1;
        boolean signed = true;
        boolean bigEndian = false;

        return new AudioFormat(sampleRate, sampleSizeBits, channels, signed, bigEndian);
    }
    public StreamServer() throws IOException{

        Socket socket = null;

        try{
            System.out.println("Creating Socket...");
            serverSocket = new ServerSocket(3000);
            System.out.println("Socket Created.");

            while (true) {
                try {
                    socket = serverSocket.accept();
                } catch (IOException e) {
                    System.out.println("I/O error: " + e);
                }
                // new thread for a client
                new OutgoingSoudnListener(socket).start();
            }
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public class OutgoingSoudnListener extends Thread {

        protected Socket socket;

        public OutgoingSoudnListener(Socket clientSocket) {
            this.socket = clientSocket;
        }

        public void run(){
            try{
                long threadId = Thread.currentThread().getId();
                System.out.println("Listening from mic.");
                DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                DataLine.Info micInfo = new DataLine.Info(TargetDataLine.class,format);
                TargetDataLine mic = (TargetDataLine) AudioSystem.getLine(micInfo);
                mic.open(format);
                System.out.println("Mic open.");
                byte tmpBuff[] = new byte[mic.getBufferSize()/5];
                mic.start();
                while(outVoice) {
                    System.out.println("Reading from mic.");
                    int count = mic.read(tmpBuff,0,tmpBuff.length);
                    if (count > 0){
                        System.out.println(threadId+": Writing buffer to server.");
                        out.write(tmpBuff, 0, count);
                        //System.out.println(Arrays.toString(tmpBuff));
                    }
                }



                mic.drain();
                mic.close();
                System.out.println("Stopped listening from mic.");

                //System.out.println(threadId+" running.");
            }catch(Exception e){
                e.printStackTrace();
            }

        }

    }
    public static void main (String args[]) throws IOException{
        new StreamServer();

    }


}