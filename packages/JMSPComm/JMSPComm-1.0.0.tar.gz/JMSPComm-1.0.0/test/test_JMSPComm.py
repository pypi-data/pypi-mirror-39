import sys
sys.path.append('../JMSPComm')

from JMSPComm import JMSPComm
from JMSPComm_1_0_0 import JMSPCommDataFrameCheckStatus as COM_CHK_ST

import test_helper
import unittest

class TestJMSPComm(unittest.TestCase):

	def test_addBuffer(self):
		data = test_helper.getDataFrame1()

		spcomm = JMSPComm()
		spcomm.addBuffer(data[test_helper.COL_DATA_FRAME])

		i = 0
		for byte in spcomm.dataFrame:
			print(byte, data[test_helper.COL_DATA_FRAME][i])
			self.assertEqual( byte, data[test_helper.COL_DATA_FRAME][i])
			i += 1

	def test_checkPack_OK(self):
		data = test_helper.getDataFrame1()

		spcomm = JMSPComm()
		spcomm.addBuffer(data[test_helper.COL_DATA_FRAME])

		isOK = spcomm.checkDataFrames()
		self.assertEqual( isOK, COM_CHK_ST.DF_CHECK_OK)
		self.assertEqual( spcomm.comMainVer, 0x10)
		self.assertEqual( spcomm.comDataVer, 0x10)


	def test_checkPack_err_header(self):
		data = test_helper.getDataFrame_ERR_Header()

		spcomm = JMSPComm()
		spcomm.addBuffer(data[test_helper.COL_DATA_FRAME])

		isOK = spcomm.checkDataFrames()
		self.assertEqual( isOK, COM_CHK_ST.DF_CHECK_ERROR_FRAME_HEADER)


	def test_checkPack_err_crc(self):
		data = test_helper.getDataFrame_ERR_CRC()

		spcomm = JMSPComm()
		spcomm.addBuffer(data[test_helper.COL_DATA_FRAME])

		isOK = spcomm.checkDataFrames()
		self.assertEqual( isOK, COM_CHK_ST.DF_CHECK_ERROR_CRC)


	def test_checkPack_err_len(self):
		data = test_helper.getDataFrame_ERR_LEN()

		spcomm = JMSPComm()
		spcomm.addBuffer(data[test_helper.COL_DATA_FRAME])

		isOK = spcomm.checkDataFrames()
		self.assertEqual( isOK, COM_CHK_ST.DF_CHECK_ERROR_DATA_LENGTH)


	def test_checkPack_err_len_diff(self):
		data = test_helper.getDataFrame_ERR_LEN_Diff()

		spcomm = JMSPComm()
		spcomm.addBuffer(data[test_helper.COL_DATA_FRAME])

		isOK = spcomm.checkDataFrames()
		self.assertEqual( isOK, COM_CHK_ST.DF_CHECK_ERROR_DATA_LENGTH)


if __name__ == '__main__':
	unittest.main()
