from threading import Thread
from queue import Queue

#####
# Network Modules
from network.multicastClient import MulticastClient
multicastClient = MulticastClient()

#####
# Audio Modules
from audio.audioHandler import AudioHandler
audioHandler = AudioHandler()

#####
# Forward Error Correction Module
from fec import FEC
fec = FEC()


#####

frameQueue = Queue()
frameblock = []





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



