from threading import Thread
from queue import Queue

#####
# Network Modules
from network.multicastClient import MulticastClient

'''
Accept multicast traffic from multicast group 
224.1.1.1 on port 5007
'''
multicastClient = MulticastClient('224.1.1.1', 5007)

#####
# Audio Modules
from audio.audioHandler import AudioHandler
audioHandler = AudioHandler()

#####
# Forward Error Correction Module
from fec.fecHandler import FECHandler
fec = FECHandler()



frameQueue = Queue()
frameblock = []

# Start processing frames when they come available
audioThread = Thread( target=audioHandler.playAudio, args=[frameQueue] )
audioThread.start()

try:
    while True:
        encodedFrame, address = multicastClient.receive(1024)

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

finally:
    print('closing socket')
    multicastClient.terminate()
    audioHandler.terminate()
