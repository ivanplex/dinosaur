from reedsolo.reedsolo import RSCodec

def fec_encode(raw):

	rs = RSCodec()


	mutable_bytes = bytearray(raw)

	#encoded_bytes = rs.encode(mutable_bytes)
	#decoded_bytes = rs.decode(encoded_bytes)


	immutable_bytes = bytes(mutable_bytes)

	return immutable_bytes

def fec_decode(raw):
	return None
