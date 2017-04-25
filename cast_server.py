import wave
from audio.audioHandler import AudioHandler
from network.multicastServer import MulticastServer
from fec.fecHandler import FECHandler



def cast():
    """
    Begin multicasting wav file
    """

    # Streaming wav File
    wf = wave.open('bin/kygo.wav', 'rb')
    print("recording...")

    try:

        ### Streaming wav
        streamdata = wf.readframes(audioHandler.getChunk())
        
        while len(streamdata) >0:
        
            encoded_bytes = fec.fec_encode(streamdata)
            multicastServer.send(encoded_bytes)

            # FEC Debug
            # print("Raw data: "+ str(len(streamdata)))
            # print("Encoded: "+ str(len(encoded_bytes)))

            streamdata = wf.readframes(audioHandler.getChunk())
           

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

    cast()
