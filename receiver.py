import socket
import struct
import sys

from threading import Thread
from queue import Queue

#####
from audio.audioHandler import AudioHandler
audioHandler = AudioHandler()

#####
from fec import FEC
fec = FEC()


frameQueue = Queue()
frameblock = []
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
    """
    Audio Playing thread
    
    Fetch a block of frames from the frameQueue and 
    combine the entire block of frames into one single
    bytearray frame. PyAudio then write the block of
    audio to audio output.
    """

    stream = audioHandler.getStream()
    CHUNK = audioHandler.getChunk()

    while True:
        if frameQueue.qsize() > 0:
            # For debugging frameQueue only
            print('digested frames. size: '+ str(frameQueue.qsize()))

            streamData = b''.join(frameQueue.get())
            for i in range(0, len(streamData), CHUNK):
                # writing to the stream is what *actually* plays the sound.
                stream.write(streamData[i:i+CHUNK])


audioThread = Thread( target=playAudio, args=("Audio", ) )
audioThread.start()

while True:
    encodedFrame, address = sock.recvfrom(1024)

    # Frames need to be individually decoded
    try:
        frameblock.append(fec.fec_decode(encodedFrame))
    except: 
        print(">>> Broken data, ignoring...")
        pass

    if(len(frameblock)%100) == 0:
        #Put the chunk of packages into a queue
        frameQueue.put(frameblock)
        frameblock = []



