#####
# Network Modules
from network.multicastServer import MulticastServer
'''
Cast multicast traffic from multicast group 
224.1.1.1 on port 5007
'''
multicastServer = MulticastServer('224.1.1.1', 5007)

#####
# Audio Modules
from audio.audioHandler import AudioHandler
audioHandler = AudioHandler()
import wave

#####
# Forward Error Correction Module
from fec.fecHandler import FECHandler
fec = FECHandler()


############
###  Streaming wav File
wf = wave.open('bin/kygo.wav', 'rb')
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
    audioHandler.terminate()
