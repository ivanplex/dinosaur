import socket
import struct

class MulticastClient:

	MCAST_GRP = None
	MCAST_PORT = None

	sock = None

	def __init__(self, MCAST_GRP_IP, MCAST_PORT):

		self.MCAST_GRP = MCAST_GRP_IP
		self.MCAST_PORT = MCAST_PORT

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', self.MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
		                             # to MCAST_GRP, not all groups on MCAST_PORT
		mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)

		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	def receive(self, size):
		""" Receive data from socket

		size: number of byte to receive
		"""
		return self.sock.recvfrom(size)

	def terminate(self):
		self.sock.close()

	def getMulticastGroup(self):
		return self.MCAST_GRP

	def getMulticastPort(self):
		return self.MCAST_PORT