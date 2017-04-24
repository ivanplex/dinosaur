"""
Ivan Chan (ivan@ivanplex.com)

A python implementation of "A Stream-based Time Synchronization Technique
For Networked Computer Games" by Zachary Booth Simpson 
(http://www.mine-control.com/zack/timesync/timesync.html)

"""

import socket
import time
from threading import Thread
from datetime import datetime
from datetime import timedelta

def timeBroadcaster():
	
	#Network setup
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5005

	try:
		while True:

			#Retrieve client datetime
			dt = str(datetime.now())
			encodedDT = dt.encode('utf-8') #Convert datetime to byte (length 26)

			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			sock.sendto(encodedDT, (UDP_IP, UDP_PORT))

			time.sleep(2)

	finally:
		sock.close()
	
	#send
	return True


def timeConsumer(cb):
	"""
	Time Consumer calculate the time difference between the server and 
	the client (this machine). This estimate the time taken for a UDP
	package to transmit from server to client.

	:cb: Call-back returns the time delta
	:return: return nothing
	"""
	#Network setup
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5005
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))

	try:
		while True:
			#Listen for client's time
			data, addr = sock.recvfrom(26) # buffer size is 26 bytes

			#Convert into datetime
			try:
				decodedData = data.decode('utf-8')
				clientTime = datetime.strptime(decodedData, '%Y-%m-%d %H:%M:%S.%f')

				#Calculate time difference
				serverTime = datetime.now()
				delta = serverTime - clientTime
				cb(delta)
				#print(str(delta))

			except ValueError: #Possible data corruption
				print("> Err [Time Sync]: Incorrect format. Corrupted?")
				pass
			except Exception as e: #Log and ignore other exception
				print("> Err [Time Sync]: "+str(e))
				pass


	finally:
		sock.close()


# def updateTimeDelta(delta):
# 	print(str(delta))


# serverThread = Thread( target=timeBroadcaster, args=[] )
# serverThread.start()


# clientThread1 = Thread( target=timeConsumer, args=[updateTimeDelta] )
# clientThread1.start()