import socket
import time
import sys

#####
import pyaudio
import wave

#####
from fec import fec_encode

FORMAT = pyaudio.paInt16
#FORMAT = 8
CHANNELS = 2
RATE = 44100
CHUNK = 1024
 
audio = pyaudio.PyAudio()

############
###  Streaming wav File
wf = wave.open('kygo.wav', 'rb')
print("Format: "+ str(audio.get_format_from_width(wf.getsampwidth())))
print("Channel: "+ str(wf.getnchannels()))
print("Frame: "+ str(wf.getframerate()))

stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
               channels=wf.getnchannels(),
               rate=wf.getframerate(),
               output=True)
############

# Streaming Audio Input
# stream = audio.open(format=FORMAT, channels=CHANNELS,
#                 rate=RATE, input=True,
#                 frames_per_buffer=CHUNK)

print("recording...")
#####

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

try:
    ### Streaming wav
    streamdata = wf.readframes(CHUNK)

    ######
    # PLAY ZONE
    
    
    while len(streamdata) >0:

        encoded_bytes = fec_encode(streamdata)
        sock.sendto(encoded_bytes, (MCAST_GRP, MCAST_PORT))
        streamdata = wf.readframes(CHUNK)
        #time.sleep(0.01)
       



    #####

    # while len(streamdata) >0:
    #    sock.sendto(streamdata, (MCAST_GRP, MCAST_PORT))
    #    streamdata = wf.readframes(CHUNK)
       #time.sleep(0.01)
    #    print("Sent packet "+str(count))
    #    count = count+1


    ### Streaming Audio Input
    # while True:       
    #     sock.sendto(stream.read(CHUNK), (MCAST_GRP, MCAST_PORT))
finally:
    print('closing socket')
    sock.close()

    ###
    stream.stop_stream()
    stream.close()
    audio.terminate()
    ###
