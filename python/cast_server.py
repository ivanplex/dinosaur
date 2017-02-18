'''
import socket
import struct
import sys

message = 'very important data'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:

    # Send data to the multicast group
    print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, multicast_group)

	# Look for responses from all recipients
    while True:
        print >>sys.stderr, 'waiting to receive'
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
        	print >>sys.stderr, 'timed out, no more responses'
        	break
        else:
            print >>sys.stderr, 'received "%s" from %s' % (data, server)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
'''

import socket
import time
import sys

#####
import pyaudio
import wave

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
    while len(streamdata) >0:
       sock.sendto(streamdata, (MCAST_GRP, MCAST_PORT))
       streamdata = wf.readframes(CHUNK)
       time.sleep(0.02)


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
