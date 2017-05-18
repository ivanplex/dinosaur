import wave
from threading import Thread
from datetime import datetime
from audio.audioHandler import AudioHandler
from network.multicastServer import MulticastServer
from fec.fecHandler import FECHandler
import sync.timesync



def cast():
    """
    Begin multicasting wav file
    """

    # Streaming wav File
    wf = wave.open('bin/kygo22050.wav', 'rb')
    print("recording...")

    try:

        ### Streaming wav
        audioData = wf.readframes(audioHandler.getChunk())


        
        while len(audioData) >0:
        
            encoded_bytes = fec.fec_encode(audioData)

            serverTimeStamp = str(datetime.now()).encode('utf-8') #Convert datetime to byte (length 26)
            packetToSend = serverTimeStamp + encoded_bytes

            multicastServer.send(packetToSend)

            # FEC Debug
            # print("Raw data: "+ str(len(audioData)))
            # print("Encoded: "+ str(len(encoded_bytes)))

            audioData = wf.readframes(audioHandler.getChunk())
            #print(audioData)
            #print(len(packetToSend))
           

    finally:
        print('closing socket')
        multicastServer.terminate()
        audioHandler.terminate()


if __name__ == "__main__":

    '''
    Cast multicast traffic from multicast group 
    224.1.1.1 on port 5007
    '''
    multicastServer = MulticastServer('224.1.1.1', 5007)
    audioHandler = AudioHandler()
    fec = FECHandler()

    # Synchonization time cast
    timeBroadcastThread = Thread( target=sync.timesync.timeBroadcaster, args=['224.1.1.1', 5005, 1] )
    timeBroadcastThread.start()

    cast()
