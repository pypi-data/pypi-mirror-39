import sys
sys.path.append('../JMSPComm')

from JMSPCommSender import JMSPCommSender

import test_helper
import unittest

class TestJMSPCommSender(unittest.TestCase):

	def test_JMSPCommSender(self):
		spcomm = JMSPCommSender()
		spcomm.comMainVer = 0x10
		spcomm.comDataVer = 0x10
		spcomm.initFrame()

		spcomm.addBuffer(0x03)
		spcomm.addBuffer(0x01)

		spcomm.buildCommPack()

		data = test_helper.getDataFrame1()

		print(data)
		print(spcomm.dataFrame, len(spcomm.dataFrame), spcomm.dataCRC)
		i = 0
		for byte in spcomm.dataFrame:
			print(byte, data[test_helper.COL_DATA_FRAME][i])
			self.assertEqual( byte, data[test_helper.COL_DATA_FRAME][i])
			i += 1

		self.assertEqual( spcomm.comMainVer, 0x10)
		self.assertEqual( spcomm.comDataVer, 0x10)
		self.assertEqual( spcomm.dataCRC, data[test_helper.COL_DATA_FRAME_CRC])


if __name__ == '__main__':
	unittest.main()