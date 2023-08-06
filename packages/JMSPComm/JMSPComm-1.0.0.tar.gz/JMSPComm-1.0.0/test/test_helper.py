
COL_DATA_FRAME = 0
COL_DATA_FRAME_LEN = 1
COL_DATA_FRAME_CRC = 2

def getDataFrame1():
	fLen = 0x05
	dCRC = 0xAB

	data = bytearray()
	data.append(0x02)
	data.append(0x3C)
	data.append(fLen)
	data.append(0x10)
	data.append(0x10)
	data.append(0x03)
	data.append(0x01)
	data.append(dCRC)

	return (data, fLen, dCRC)


def getDataFrame_ERR_Header():
	fLen = 0x05
	dCRC = 0xAB

	data = bytearray()
	data.append(0x02)
	data.append(0x32)
	data.append(fLen)
	data.append(0x10)
	data.append(0x10)
	data.append(0x03)
	data.append(0x01)
	data.append(dCRC)

	return (data, fLen, dCRC)


def getDataFrame_ERR_CRC():
	fLen = 0x05
	dCRC = 0x03

	data = bytearray()
	data.append(0x02)
	data.append(0x3C)
	data.append(fLen)
	data.append(0x10)
	data.append(0x10)
	data.append(0x03)
	data.append(0x01)
	data.append(dCRC)

	return (data, fLen, dCRC)


def getDataFrame_ERR_LEN():
	fLen = 0x09
	dCRC = 0xAB

	data = bytearray()
	data.append(0x02)
	data.append(0x3C)
	data.append(fLen)
	data.append(0x10)
	data.append(0x10)
	data.append(0x03)
	data.append(0x01)
	data.append(dCRC)

	return (data, fLen, dCRC)


def getDataFrame_ERR_LEN_Diff():
	fLen = 0x05
	dCRC = 0xAB

	data = bytearray()
	data.append(0x02)
	data.append(0x3C)
	data.append(fLen)
	data.append(0x10)
	data.append(0x10)
	data.append(0x03)
	data.append(0x01)
	data.append(0x20)
	data.append(0x55)
	data.append(0x9C)
	data.append(dCRC)

	return (data, fLen, dCRC)