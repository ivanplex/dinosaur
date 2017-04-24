import socket

class MulticastServer:

	MCAST_GRP = None
	MCAST_PORT = None

	sock = None

	def __init__(self, MCAST_GRP_IP, MCAST_PORT):

		self.MCAST_GRP = MCAST_GRP_IP
		self.MCAST_PORT = MCAST_PORT

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

	def send(self, data):
		try:
			self.sock.sendto(data, (self.MCAST_GRP, self.MCAST_PORT))
		except ValueError: #Possible data corruption
			print("> Err [Network]: Incorrect format. Corrupted?")
			pass

	def terminate(self):
		self.sock.close()

	def getMulticastGroup(self):
		return self.MCAST_GRP

	def getMulticastPort(self):
		return self.MCAST_PORT