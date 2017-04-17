import socket

class MulticastServer():

	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007

	sock = None

	def __init__(self):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

	def send(self, data):
		self.sock.sendto(data, (self.MCAST_GRP, self.MCAST_PORT))

	def terminate(self):
		self.sock.close()

	def getMulticastGroup(self):
		return self.MCAST_GRP

	def getMulticastPort(self):
		return self.MCAST_PORT