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
CHUNK = 224
 
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, 
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

encodedFrameQueue = Queue()
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
        if encodedFrameQueue.qsize() > 0:
            print('digested frames. size: '+ str(encodedFrameQueue.qsize()))

            # # Frames need to be individually decoded
            # encodedFrames = encodedFrameQueue.get()
            # decodedFrames = []
            # while len(encodedFrames) >0:
            #     decodedFrames.append(fec.fec_decode(encodedFrames.pop()))

            streamData = b''.join(encodedFrameQueue.get())

            try:
                for i in range(0, len(streamData), CHUNK):
                    # writing to the stream is what *actually* plays the sound.
                    stream.write(streamData[i:i+CHUNK])
            except: 
                print(">>> Broken data, ignoring...")
                pass

            streamData = b''.join(encodedFrameQueue.get())
            for i in range(0, len(streamData), CHUNK):
                # writing to the stream is what *actually* plays the sound.
                stream.write(streamData[i:i+CHUNK])


audioThread = Thread( target=playAudio, args=("Audio", ) )
audioThread.start()

while True:
    data, address = sock.recvfrom(1024)

    # Frames need to be individually decoded
    frames.append(fec.fec_decode(data))

    if(len(frames)%100) == 0:
        #Put the chunk of packages into a queue
        encodedFrameQueue.put(frames)
        frames = []



