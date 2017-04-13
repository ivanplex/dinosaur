import socket
import struct
import sys
import pyaudio

from threading import Thread
from queue import Queue

### Temp Modules
import time

#####
from fec import FEC

fec = FEC()


FORMAT = pyaudio.paInt16
#FORMAT = 8
CHANNELS = 2
RATE = 44100
CHUNK = 1024
 
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, 
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

frameQueue = Queue()
frames = []
#####

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def playAudio(self):
    while True:
        if frameQueue.qsize() > 0:
            print('digested frames. size: '+ str(frameQueue.qsize()))

            streamData = b''.join(frameQueue.get())
            print(len(streamData))
            audio_data = fec.fec_decode(streamData)
            for i in range(0, len(audio_data), CHUNK):
                # writing to the stream is what *actually* plays the sound.
                stream.write(audio_data[i:i+CHUNK])


audioThread = Thread( target=playAudio, args=("Audio", ) )
audioThread.start()

while True:
    data, address = sock.recvfrom(4096)
    frames.append(data)

    if(len(frames)%100) == 0:
        #Put the chunk of packages into a queue
        frameQueue.put(frames)
        frames = []



