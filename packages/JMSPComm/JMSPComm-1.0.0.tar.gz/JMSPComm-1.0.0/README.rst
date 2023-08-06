JMASPComm Small Pack Communication Protocol

v1.0 for iOS ( 2014.02 )

JungleMetal Software. support@junglemetal.com

2018.10.25	Kunpeng Zhang <zkppro@gmail.com> modified for python

Implement a simple serial communication. Use binary mode with frame CRC check. Each data length is no more than 256 bytes (including frame header).

	+----------------------------------+
	| Frame header: 0x023C 2 bytes
	+----------------------------------+
	| Frame Length: 0xXX 1 byte
	+----------------------------------+
	| Communication version: 0x10 1 byte
	+----------------------------------+
	| Data version: 0x10 1 byte
	+----------------------------------+
	| Data area
	| ......
	| ......
	+----------------------------------+
	| CRC: 0xXX 1 byte. 
	| included: frame long + communication version + data version + data area
	+----------------------------------+

### Class Descriptions:

* JMSPComm 
	communication base class Implement data buffer operations, communication protocol information attributes, basic protocol interpretation, and verification functions.

* JMSPCommReceiver
	communication protocol receiving class Implement the receive of communication data

* JMSPCommSender 
	communication protocol sending class Implement protocol packaging


### Other classes

* JMACRC8
	CRC check calculation function, byte flip function


### Other platform
* Arduino
	https://github.com/mobinrg/JMASPComm

----------------------------------------------

JMASPComm 简单小包通讯协议

v1.0 for iOS ( 2014.02 )

JungleMetal Software. support@junglemetal.com

2018.10.25	Kunpeng Zhang <zkppro@gmail.com> modified for python

实现一个简单的串行通讯协议。使用二进制方式，带数据帧 CRC 校验。 每个数据帧长度不超过 256 字节（包含帧头）。

	+----------------------------------+
	| 帧头: 0x023C  2字节
	+----------------------------------+
	| 帧长: 0xXX	1字节
	+----------------------------------+
	| 通讯版本: 0x10 1字节 
	+----------------------------------+
	| 数据版本: 0x10 1字节
	+----------------------------------+
	| 数据区
	| ......
	| ......
	+----------------------------------+
	| CRC: 0xXX 1字节。
	| 计算内容：帧长+通讯版本+数据版本+数据区
	+----------------------------------+

### 类说明：

* JMSPComm 通讯基类 实现数据缓存操作，通讯协议信息属性，协议基本解读，校验功能。

* JMSPCommReceiver 通讯协议接收类 实现通讯数据的接收

* JMSPCommSender 通讯协议发送类 实现数据协议打包工作


### 其他辅助类

* JMSPCRC8
	CRC 校验计算函数, 字节翻转函数

### 其他平台
* Arduino
	https://github.com/mobinrg/JMASPComm
