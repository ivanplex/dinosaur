from threading import Thread
from timesync import timeBroadcaster
from client import syncTestClient

serverThread = Thread( target=timeBroadcaster, args=[] )
serverThread.start()

def createClient():
	syncTestClient()

spawnThread1 = Thread( target=createClient, args=[] )
spawnThread2 = Thread( target=createClient, args=[] )

spawnThread1.start()
spawnThread2.start()