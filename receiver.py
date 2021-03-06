from threading import Thread
from queue import Queue

from network.multicastClient import MulticastClient
from audio.audioHandler import AudioHandler
from fec.fecHandler import FECHandler



def listen():
    frameQueue = Queue()
    frameblock = []
    frameblockStartTime = None

    # Start processing frames when they come available
    audioThread = Thread( target=audioHandler.playAudio, args=[frameQueue] )
    audioThread.start()

    try:
        while True:
            encodedFrame, address = multicastClient.receive(1024)

            # Frames need to be individually decoded
            try:
                # First 26 byte is server timestamp
                if(frameblockStartTime == None):
                    serverTimeStamp = encodedFrame[0:26] 
                    frameblockStartTime = serverTimeStamp
                    # print(serverTimeStamp.decode('utf-8'))


                decodedPacket = fec.fec_decode(encodedFrame[26:])

                frameblock.append(decodedPacket)

            except: 
                print(">>> Broken data, ignoring...")
                pass

            if(len(frameblock)%100) == 0:
                #Put the chunk of packages into a queue
                frameQueue.put([frameblockStartTime,frameblock])
                frameblock = []
                frameblockStartTime = None


    finally:
        print('closing socket')
        multicastClient.terminate()
        audioHandler.terminate()


if __name__ == "__main__":
    '''
    Accept multicast traffic from multicast group 
    224.1.1.1 on port 5007
    '''
    multicastClient = MulticastClient('224.1.1.1', 5007)
    audioHandler = AudioHandler()
    fec = FECHandler()

    listen()
