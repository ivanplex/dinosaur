"""
Ivan Chan (ivan@ivanplex.com)
https://github.com/ivanplex

Test time synchonazation between server and client

syncTest define a time 

"""
import time
from threading import Thread
from datetime import datetime
from datetime import timedelta
from sync.timesync import timeBroadcaster
from test.syncTestClient import syncTestClient


'''
:triggerTime: 
The time when server want the client to start playing music

We allow 3 seconds for the clients to sync up!
'''

triggerTime = datetime.now() + timedelta(seconds=7)

serverThread = Thread( target=timeBroadcaster, args=['224.1.1.1', 5005, 1] )
serverThread.start()

def createClient():
	syncTestClient(triggerTime)

spawnThread1 = Thread( target=createClient, args=[] )
spawnThread2 = Thread( target=createClient, args=[] )
spawnThread3 = Thread( target=createClient, args=[] )

spawnThread1.start()
time.sleep(2) # Simulate slightly different start time
spawnThread2.start()
time.sleep(1) # Simate slightly different start time
spawnThread3.start()