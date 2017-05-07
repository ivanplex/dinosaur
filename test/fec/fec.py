"""
Unit test for FEC Module

"""
from fec.fecHandler import FECHandler

test_byte = b'\x10\x01I\x02.\x01A\x02K\x01:\x02]\x01;\x02b\x01G\x02\\\x01^\x02Q\x01y\x02H\x01\x8d\x02K\x01\x91\x02[\x01\x85\x02r\x01k\x02\x88\x01I\x02\x95\x01%\x02\x96\x01\x05\x02\x8f\x01\xe9\x01\x81\x01\xd0\x01m\x01\xba\x01S\x01\xac\x013\x01\xa8\x01\x0c\x01\xac\x01\xdf\x00\xba\x01\xac\x00\xd4\x01u\x00\xf6\x01B\x00\x1e\x02\x18\x00H\x02\xfa\xffo\x02\xf0\xff\x91\x02\xfd\xff\xab\x02\x1c\x00\xbe\x02K\x00\xc8\x02\x84\x00\xc5\x02\xc0\x00\xb2\x02\xfc\x00\x8c\x026\x01O\x02g\x01\x00\x02\x88\x01\xa6\x01\x97\x01L\x01\x92\x01\xfb\x00z\x01\xba\x00V\x01\x90\x000\x01\x7f\x00\r\x01\x83\x00\xf5\x00\x96\x00\xed\x00\xb0\x00\xf5\x00\xce\x00\x0b\x01\xee\x00\'\x01\r\x01C\x01"\x01Y\x01+\x01a\x01)\x01[\x01\x1c\x01I\x01\x03\x010\x01\xe5\x00\x1a\x01\xc4\x00\x12\x01\xa3\x00\x1f\x01\x89\x009\x01{\x00\\\x01y\x00\x85\x01\x85\x00\xad\x01\x9a\x00\xce\x01\xb6\x00\xe8\x01\xd2\x00\xf9\x01\xeb\x00\xfe\x01\xfd\x00\xfc\x01\x01\x01\xf6\x01\xf2\x00\xed\x01\xcb\x00\xde\x01\x8d\x00\xc8\x01?\x00\xaf\x01\xec\xff\x93\x01\xa3\xfft\x01q\xff\\\x01^\xffK\x01n\xff=\x01\x9e\xff0\x01\xe2\xff"\x01)\x00\x10\x01f\x00\xf6\x00\x93\x00\xd2\x00\xa9\x00\xa5\x00\xa6\x00o\x00\x8d\x008\x00c\x00\x04\x001\x00\xda\xff\xff\xff\xc3\xff\xd3\xff\xc2\xff\xb0\xff\xd6\xff\x9c\xff\xfe\xff\x98\xff4\x00\xa4\xffh\x00\xbd\xff\x8c\x00\xe2\xff\x91\x00\r\x00r\x007\x002\x00Z\x00\xd8\xffp\x00s\xff{\x00\x12\xffx\x00\xc5\xfeb\x00\x93\xfe<\x00}\xfe\x0e\x00}\xfe\xdd\xff\x88\xfe\xb3\xff\x98\xfe\x9e\xff\xa3\xfe\xa3\xff\xa3\xfe\xc2\xff\x98\xfe\xf4\xff\x87\xfe-\x00q\xfeb\x00T\xfe\x8d\x007\xfe\xa6\x00\x1c\xfe\xa8\x00\x07\xfe\x99\x00\xfe\xfd\x82\x00\x07\xfek\x00$\xfeY\x00R\xfeJ\x00\x88\xfe;\x00\xb7\xfe1\x00\xd4\xfe)\x00\xd4\xfe \x00\xb5\xfe\x13\x00}\xfe\x07\x007\xfe\xfc\xff\xf1\xfd\xf2\xff\xbb\xfd\xea\xff\xa0\xfd\xe0\xff\x9f\xfd\xd3\xff\xb5\xfd\xc6\xff\xd9\xfd\xba\xff\x01\xfe\xac\xff%\xfe\x9d\xffB\xfe\x90\xffU\xfe\x87\xffc\xfe\x82\xffo\xfe~\xffz\xfe{\xff\x82\xfex\xff\x83\xfev\xff|\xfet\xffp\xfen\xffa\xfeg\xffU\xfe`\xffQ\xfe\\\xff[\xfe^\xffr\xfee\xff\x90\xfev\xff\xa8\xfe\x91\xff\xb7\xfe\xad\xff\xbc\xfe\xc1\xff\xb5\xfe\xc9\xff\xaa\xfe\xc3\xff\xa4\xfe\xad\xff\xa9\xfe\x8e\xff\xbb\xfeo\xff\xd5\xfeW\xff\xf4\xfeH\xff\x13\xffG\xff/\xffM\xffB\xffV\xffK\xff[\xffF\xff\\\xff3\xff\\\xff\x14\xff_\xff\xec\xfea\xff\xc2\xfea\xff\x9d\xfe^\xff\x81\xfeU\xffs\xfeK\xffu\xfeD\xff\x82\xfeC\xff\x94\xfeG\xff\xa1\xfeP\xff\xa3\xfe]\xff\x95\xfek\xffv\xfe{\xffH\xfe\x8c\xff\x13\xfe\x9c\xff\xdf\xfd\xa7\xff\xb8\xfd\xaa\xff\xa0\xfd\xa5\xff\x9a\xfd\x9b\xff\xa3\xfd\x89\xff\xb7\xfdr\xff\xcc\xfdZ\xff\xdb\xfdD\xff\xe1\xfd4\xff\xe5\xfd,\xff\xe6\xfd*\xff\xe7\xfd,\xff\xe8\xfd-\xff\xe9\xfd+\xff\xe7\xfd&\xff\xdf\xfd"\xff\xcf\xfd\x1d\xff\xbb\xfd\x17\xff\xaa\xfd\x0b\xff\x9f\xfd\xf6\xfe\xa0\xfd\xda\xfe\xae\xfd\xbd\xfe\xc5\xfd\xa4\xfe\xde\xfd\x98\xfe\xf3\xfd\x9d\xfe\xfd\xfd\xb3\xfe\xff\xfd\xce\xfe\xff\xfd\xe9\xfe\x05\xfe\xfc\xfe\x15\xfe\x06\xff.\xfe\t\xffM\xfe\x07\xffr\xfe\x02\xff\x99\xfe\xf8\xfe\xbd\xfe\xe5\xfe\xdc\xfe\xc7\xfe\xf1\xfe\x9c\xfe\xf8\xfee\xfe\xf1\xfe&\xfe\xde\xfe\xeb\xfd\xc1\xfe\xbe\xfd\xa1\xfe\xaa\xfd\x86\xfe\xb1\xfdt\xfe\xce\xfdo\xfe\xfb\xfdw\xfe*\xfe'

def test_FEC():
	fec = FECHandler()
	encodedtext = fec.encode(test_byte)
	assert test_byte == fec.decode(encodedtext)