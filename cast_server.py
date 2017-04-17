#####
# Network Modules
from network.multicastServer import MulticastServer
multicastServer = MulticastServer()

#####
# Audio Modules
from audio.audioHandler import AudioHandler
audioHandler = AudioHandler()
import wave

#####
# Forward Error Correction Module
from fec import FEC
fec = FEC()


############
###  Streaming wav File
wf = wave.open('kygo.wav', 'rb')

print("recording...")
#####



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

    ###
    audioHandler.terminate()
    ###
