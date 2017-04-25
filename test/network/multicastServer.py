from network.multicastServer import MulticastServer

def test_Object_Creation():
	obj = MulticastServer('127.0.0.1',5000)
	assert obj != None