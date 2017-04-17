import socket
import time
import sys

#####
from audio.audioHandler import AudioHandler
audioHandler = AudioHandler()
import wave

#####
from fec import FEC
fec = FEC()


############
###  Streaming wav File
wf = wave.open('kygo.wav', 'rb')

print("recording...")
#####

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

try:
    ### Streaming wav
    streamdata = wf.readframes(audioHandler.getChunk())
    
    while len(streamdata) >0:
    
        encoded_bytes = fec.fec_encode(streamdata)
        sock.sendto(encoded_bytes, (MCAST_GRP, MCAST_PORT))

        # FEC Debug
        # print("Raw data: "+ str(len(streamdata)))
        # print("Encoded: "+ str(len(encoded_bytes)))

        streamdata = wf.readframes(audioHandler.getChunk())
        #time.sleep(0.01)
       

finally:
    print('closing socket')
    sock.close()

    ###
    audioHandler.terminate()
    ###
