import sys
sys.path.append('../JMSPComm')

from JMSPCommReceiver import JMSPCommReceiver
from JMSPComm_1_0_0 import JMSPCommDataFrameCheckStatus as COM_CHK_ST

import test_helper
import unittest

def onFrameBegin(): print("BEGIN")
def onFrameErr(err): print("ERROR: ", err)
def onBeforeFrameVerifyCRC(): print("Before verify CRC")
def onFrameReceived(): print("Received")

class TestJMSPComm(unittest.TestCase):

	def test_addByte_ok(self):
		data = test_helper.getDataFrame1()
		spcomm = JMSPCommReceiver(maxFrameLen=20)

		spcomm.onFrameBegin = onFrameBegin
		spcomm.onFrameErr = onFrameErr
		spcomm.onBeforeFrameVerifyCRC = onBeforeFrameVerifyCRC
		spcomm.onFrameReceived = onFrameReceived

		for byte in data[test_helper.COL_DATA_FRAME]:
			print(byte)
			spcomm.addByte(byte)
			# self.assertEqual( byte, data[test_helper.COL_DATA_FRAME][i])

	
	def test_addByte_err_header(self):
		data = test_helper.getDataFrame_ERR_Header()
		spcomm = JMSPCommReceiver(maxFrameLen=20)
		spcomm.onFrameBegin = onFrameBegin
		spcomm.onFrameErr = onFrameErr
		spcomm.onBeforeFrameVerifyCRC = onBeforeFrameVerifyCRC
		spcomm.onFrameReceived = onFrameReceived
		for byte in data[test_helper.COL_DATA_FRAME]:
			print(byte)
			spcomm.addByte(byte)

	def test_addByte_err_crc(self):
		data = test_helper.getDataFrame_ERR_CRC()
		spcomm = JMSPCommReceiver(maxFrameLen=20)
		spcomm.onFrameBegin = onFrameBegin
		spcomm.onFrameErr = onFrameErr
		spcomm.onBeforeFrameVerifyCRC = onBeforeFrameVerifyCRC
		spcomm.onFrameReceived = onFrameReceived
		for byte in data[test_helper.COL_DATA_FRAME]:
			print(byte)
			spcomm.addByte(byte)

	def test_addByte_err_len(self):
		data = test_helper.getDataFrame_ERR_LEN()
		spcomm = JMSPCommReceiver(maxFrameLen=20)
		spcomm.onFrameBegin = onFrameBegin
		spcomm.onFrameErr = onFrameErr
		spcomm.onBeforeFrameVerifyCRC = onBeforeFrameVerifyCRC
		spcomm.onFrameReceived = onFrameReceived
		for byte in data[test_helper.COL_DATA_FRAME]:
			print(byte)
			spcomm.addByte(byte)

	def test_addByte_err_len_diff(self):
		data = test_helper.getDataFrame_ERR_LEN_Diff()
		spcomm = JMSPCommReceiver(maxFrameLen=20)
		spcomm.onFrameBegin = onFrameBegin
		spcomm.onFrameErr = onFrameErr
		spcomm.onBeforeFrameVerifyCRC = onBeforeFrameVerifyCRC
		spcomm.onFrameReceived = onFrameReceived
		for byte in data[test_helper.COL_DATA_FRAME]:
			print(byte)
			spcomm.addByte(byte)


if __name__ == '__main__':
	unittest.main()
