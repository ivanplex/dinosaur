"""
Ivan Chan (ivan@ivanplex.com)
https://github.com/ivanplex

Test time synchonazation between server and client

syncTest define a time 

"""
from threading import Thread
from timesync import timeBroadcaster
from syncTestClient import syncTestClient
from datetime import datetime
from datetime import timedelta
import time

'''
:triggerTime: 
The time when server want the client to start playing music

We allow 3 seconds for the clients to sync up!
'''
triggerTime = datetime.now() + timedelta(seconds=5)

serverThread = Thread( target=timeBroadcaster, args=['224.1.1.1', 5005, 2] )
serverThread.start()

def createClient():
	syncTestClient(triggerTime)

spawnThread1 = Thread( target=createClient, args=[] )
spawnThread2 = Thread( target=createClient, args=[] )
spawnThread3 = Thread( target=createClient, args=[] )

spawnThread1.start()
time.sleep(0.02) # Simulate slightly different start time
spawnThread2.start()
time.sleep(0.02) # Simulate slightly different start time
spawnThread3.start()