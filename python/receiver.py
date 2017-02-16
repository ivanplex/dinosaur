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

#####
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, 
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

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

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data, address = sock.recvfrom(4096)
    #stream.write(data)
    frames.append(data)
    print(len(frames))
print("finished recording")

streamData = b''.join(frames)
for i in range(0, len(streamData), CHUNK):
    # writing to the stream is what *actually* plays the sound.
    stream.write(streamData[i:i+CHUNK])

#waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#waveFile.setnchannels(CHANNELS)
#waveFile.setsampwidth(audio.get_sample_size(FORMAT))
#waveFile.setframerate(RATE)
#waveFile.writeframes(b''.join(frames))
#waveFile.close()