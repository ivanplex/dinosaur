import pyaudio

class AudioHandler():

	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 224

	audio = None
	stream = None

	def __init__(self):

		self.audio = pyaudio.PyAudio()

		self.stream = self.audio.open(format=self.FORMAT, 
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=self.CHUNK)

		print("Format: "+ str(self.FORMAT))
		print("Channel: "+ str(self.CHANNELS))
		print("Frame: "+ str(self.RATE))


	def playAudio(self, frameQueue):
	    """
	    Audio Playing thread
	    
	    Fetch a block of frames from the frameQueue and 
	    combine the entire block of frames into one single
	    bytearray frame. PyAudio then write the block of
	    audio to audio output.
	    """
	    while True:
	        if frameQueue.qsize() > 0:
	            # For debugging frameQueue only
	            print('digested frames. size: '+ str(frameQueue.qsize()))

	            streamData = b''.join(frameQueue.get())
	            for i in range(0, len(streamData), self.CHUNK):
	                # writing to the stream is what *actually* plays the sound.
		            self.stream.write(streamData[i:i+self.CHUNK])

	    return None


	def terminate(self):
		self.stream.stop_stream()
		self.stream.close()
		self.audio.terminate()

	def getStream(self):
		return self.stream

	def getFormat(self):
		return self.FORMAT

	def getChannels(self):
		return self.CHANNELS

	def getRate(self):
		return self.RATE

	def getChunk(self):
		return self.CHUNK
 
