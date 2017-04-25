"""
Ivan Chan (ivan@ivanplex.com)
https://github.com/ivanplex

A python implementation of "A Stream-based Time Synchronization Technique
For Networked Computer Games" by Zachary Booth Simpson 
(http://www.mine-control.com/zack/timesync/timesync.html)

"""

import socket
import time
from threading import Thread
from datetime import datetime
from datetime import timedelta

from network.multicastServer import MulticastServer
from network.multicastClient import MulticastClient


def timeBroadcaster(MCAST_GRP, MCAST_PORT, interval):
	"""
	Broadcast server time using multicast

	:MCAST_GRP: IP address of the multicast group
	:MCAST_PORT: Port number
	:interval: Number of second between each server time broadcast
	:return: return nothing
	"""

	multicastServer = MulticastServer(MCAST_GRP, MCAST_PORT)

	while True:

		#Retrieve client datetime
		dt = str(datetime.now())
		encodedDT = dt.encode('utf-8') #Convert datetime to byte (length 26)
		
		multicastServer.send(encodedDT)
		time.sleep(interval)


def timeConsumer(MCAST_GRP, MCAST_PORT,cb):
	"""
	Time Consumer calculate the time difference between the server and 
	the client (this machine). This estimate the time taken for a UDP
	package to transmit from server to client.

	:MCAST_GRP: IP address of the multicast group
	:MCAST_PORT: Port number
	:cb: Call-back returns the time delta
	:return: return nothing
	"""


	multicastClient = MulticastClient(MCAST_GRP, MCAST_PORT)

	while True:

		data, addr = multicastClient.receive(26)

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
