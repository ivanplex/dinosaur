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
 