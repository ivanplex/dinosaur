'''
import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
        print >>sys.stderr, '\nwaiting to receive message'
        data, address = sock.recvfrom(1024)
                
        print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
        print >>sys.stderr, data

        print >>sys.stderr, 'sending acknowledgement to', address
        sock.sendto('ack', address)
'''


import socket
import struct
import sys
import pyaudio

from threading import Thread
from queue import Queue

### Temp Modules
import time


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

#while True:
#	data, address = sock.recvfrom(1024)
                
#	print('received %s bytes from %s' % (len(data), address))
#	print(data.decode())

	#NAK
	#print >>sys.stderr, 'sending negative acknowledgement to', address
	#sock.sendto('ack', address)

#data, address = sock.recvfrom(4096)
#print(len(data))


def playAudio(self):
    while True:
        if frameQueue.qsize() > 0:
            print('digested frames. size: '+ str(frameQueue.qsize()))

            streamData = b''.join(frameQueue.get())
            for i in range(0, len(streamData), CHUNK):
                # writing to the stream is what *actually* plays the sound.
                stream.write(streamData[i:i+CHUNK])


audioThread = Thread( target=playAudio, args=("Audio", ) )
audioThread.start()

while True:
#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data, address = sock.recvfrom(4096)
    frames.append(data)

    if(len(frames)%100) == 0:
        #Put the chunk of packages into a queue
        frameQueue.put(frames)
        frames = []

    ## Introduce deley to miss out packages
    # Test only
    time.sleep(0.05) 


