from threading import Thread
from datetime import datetime
from datetime import timedelta
import time
from timesync import timeConsumer

import pyaudio  
import wave  

# deltaTime = datetime.now()

# def updateDeltaTime(delta):
# 	deltaTime = delta
	
# syncThread = Thread( target=timeConsumer, args=[updateDeltaTime] )
# syncThread.start()

# time.sleep(5)
# dt = datetime.now() + deltaTime
# starttime = dt + timedelta(seconds=3)

class syncTestClient:

	serverClientDelta = None
	starttime = None

	def __init__(self):

		syncThread = Thread( target=timeConsumer, args=[self.updateDeltaTime] )
		actionThread = Thread( target=self.timedAction, args=[] )

		syncThread.start()
		time.sleep(5)
		self.starttime = datetime.now() + self.serverClientDelta + timedelta(seconds=3)
		actionThread.start()

	def updateDeltaTime(self, delta):
		print("Delta Updated! >" + str(delta))
		self.serverClientDelta = delta

	def timedAction(self):
		while True:
			if self.starttime == datetime.now():

				#define stream chunk   
				chunk = 1024  

				#open a wav format music  
				f = wave.open("kygo.wav","rb")  
				#instantiate PyAudio  
				p = pyaudio.PyAudio()  
				#open stream  
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
				                channels = f.getnchannels(),  
				                rate = f.getframerate(),  
				                output = True)  

				#read data  
				data = f.readframes(chunk)  

				#play stream  
				while data:  
				    stream.write(data)  
				    data = f.readframes(chunk)  

				#stop stream  s
				stream.stop_stream()  
				stream.close()  

				#close PyAudio  
				p.terminate()  


				break
