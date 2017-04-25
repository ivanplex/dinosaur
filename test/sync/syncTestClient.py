import time
from threading import Thread
from datetime import datetime
from datetime import timedelta
from sync.timesync import timeConsumer

import pyaudio  
import wave  

class syncTestClient:

	serverClientDelta = None
	adjustedTime = None

	def __init__(self, triggerTime):

		syncThread = Thread( target=timeConsumer, args=['224.1.1.1', 5005, self.updateDeltaTime] )
		actionThread = Thread( target=self.timedAction, args=[] )

		syncThread.start()
		time.sleep(4) #Time to get SYNC!!!
		self.adjustedTime = triggerTime - self.serverClientDelta
		actionThread.start()

	def updateDeltaTime(self, delta):
		print("Delta Updated! >" + str(delta))
		self.serverClientDelta = delta

	def timedAction(self):
		#print(self.adjustedTime)
		while True:
			'''
			'''
			if (self.adjustedTime < datetime.now()) and (self.adjustedTime + timedelta(microseconds=500)) < datetime.now():
			# now = datetime.now()
			# if self.adjustedTime < now:
			# 	print(now - self.adjustedTime)

				print("PLAY!")
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
