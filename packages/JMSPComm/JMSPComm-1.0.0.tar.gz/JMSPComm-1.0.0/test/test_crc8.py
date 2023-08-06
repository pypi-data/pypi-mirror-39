import sys
sys.path.append('../JMSPComm')

import test_helper
import JMSPCRC8
import unittest

class TestCRC8(unittest.TestCase):

	def test_crc8_byte(self):
		oldCRC = 0x00
		self.assertEqual( JMSPCRC8.crc8FromByte(0x11, oldCRC), 0xC3)
		self.assertEqual( JMSPCRC8.crc8FromByte(0x10, oldCRC), 0x9D)
		self.assertEqual( JMSPCRC8.crc8FromByte(0xAA, oldCRC), 0xD1)

	def test_crc8_bytes(self):
		dataFrame = test_helper.getDataFrame1()
		crc = JMSPCRC8.crc8FromBytes(dataFrame[test_helper.COL_DATA_FRAME], 2, dataFrame[test_helper.COL_DATA_FRAME_LEN]);
		self.assertEqual( crc, dataFrame[test_helper.COL_DATA_FRAME_CRC])

if __name__ == '__main__':
    unittest.main()