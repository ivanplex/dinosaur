from external.reedsolomon.reedsolo import RSCodec

class FECHandler:

	rs = None

	def __init__(self):
		self.rs = RSCodec(10)

	# def fec_encode(self, raw):
	# 	# Encode raw data using FEC

	# 	mutable_bytes = bytearray(raw)
	# 	encoded_bytes = self.rs.encode(mutable_bytes)
	# 	immutable_bytes = bytes(encoded_bytes)

	# 	return immutable_bytes

	# def fec_decode(self, encoded_bytes):
	# 	# Decode FEC encoded data

	# 	mutable_bytes = bytearray(encoded_bytes)
	# 	decoded_bytes = self.rs.decode(mutable_bytes)
	# 	immutable_bytes = bytes(decoded_bytes)

	# 	return immutable_bytes


	#####################################################
	# Performance Testing Only!
	def fec_encode(self, raw):
		return raw

	def fec_decode(self, encoded_bytes):
		return encoded_bytes

