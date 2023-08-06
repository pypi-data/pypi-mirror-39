#
# JMSPComm Small Pack Comm
# Author: Kunpeng Zhang
#
# 2018.10.25
#

from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 4 - Beta',
	'Operating System :: POSIX :: Linux',
	'License :: OSI Approved :: MIT License',
	'Intended Audience :: Developers',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Topic :: Communications'
]

keywords = (
	"communication protocol"
	"wireless comm"
	"arduino"
	"433MHz 315MHz"
)

desc = "Implement a simple serial communication protocol. Use binary mode with frame CRC check. Each data length is no more than 256 bytes (including frame header)."

pagekages = find_packages()

setup (
	name				= 'JMSPComm',
	version				= '1.0.0',
	author				= 'Kunpeng Zhang',
	author_email		= 'zkppro@gmail.com',
	description			= desc,
	long_description	= desc,
	platforms			= ['Linux'],
	license				= 'MIT',
	classifiers			= classifiers,
	keywords			= keywords,
	url					= 'https://github.com/mobinrg/JMSPComm_python',
	dependency_links	= [],
	install_requires	= [],
	packages			= pagekages,
	scripts				= [],
)
