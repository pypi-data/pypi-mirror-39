'''
serialdaq.py

Serial device controller for data acquisition

This module defines classes for controlling Omega DPG-4000 pressure sensors
and the GwInstek LCR-821 meters. This implementation features auto-
connect to the device (by scanning available serial ports) and provides methods
for finite or indefinite data acquisition (and saving to file).

The classes for each are subclasses of a SerialDevice class to allow expansion
for use with other serial devices (simply inherit SerialDevice and define the
get_reading() method, and the baud and data_columns properties).
'''


#-----------------------------------------------------------------------------#
# LIBRARIES
#-----------------------------------------------------------------------------#
import serial               # for serial communication
import time                 # for time delays
import datetime             # for timestamps
import csv                  # for saving each data reading to file
import glob                 # for searching for serial ports
import sys                  # for identifying operating system (to find ports)
import re                   # for regex matching when parsing read data
from pathlib import Path    # for checking if output file exists


#-----------------------------------------------------------------------------#
# CONSTANTS
#-----------------------------------------------------------------------------#
'''Device ID numbers'''
ID_PRESSURE = 'OMEGA,DPG-4000,3515252,4.04'
ID_LCR = 'GwInstek LCR-821 (no ID)'


#-----------------------------------------------------------------------------#
# FUNCTIONS AND CLASSES
#-----------------------------------------------------------------------------#

def  serial_ports():
	''' Lists serial port names

		Args:
			none

		Outputs:
			none

		Raises:
			EnvironmentError : 	On unsupported or unknown platforms

		Returns:
			A list of the serial ports available on the system

		Notes:
			Adapted from https://stackoverflow.com/a/14224477
	'''
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result


def list_devices():
	'''Get list of serial ports and try connecting to each;
	uses the SerialDevice class (which queries device for id upon
	connection).

		Args:
			none

		Outputs:
			Prints results of connection attempt, with device ID if possible

		Raises:
			none

		Returns:
			None
	'''
	print('Looking for ports ...')
	ports = serial_ports() # find serial ports on the system
	print(f'Testing available ports: {ports}\n')
	for port in ports:     # try connecting to each device
		s = SerialDevice(port)
		s.close()
	return


class SerialDevice:
	'''SerialDevice(port=None)

	General serial device class with a null get_reading() method; this method
	must be defined in subclasses to be able to read from devices. The method
	get_id() might also need to be re-difined for initializing device
	communication. Make sure baud is correct. Optionally, define the
	data_columns property to print a header for the	read data.
	'''

    # list of serial commands (add more as necessary for other devices)
	com = {
        'GET_ID'    : '*IDN?',
        'GET_VAL'   : 'VAL?',
		'COMU?'     : 'COMU?',
		'COM_ON'    : 'COMU:ON',
		'COM_OFF'   : 'COMU:OFF',
        'OVER'      : 'COMU:OVER',
        'GET_FREQ'  : 'MAIN:FREQ?',
        'GET_VOLT'  : 'MAIN:VOLT?',
        'SET_MANUAL': 'MAIN:TRIG:MANU',
        'START'     : 'MAIN:STAR',
        }

	baud = 9600
	data_columns = None

	def __init__(self, port=None):
		'''Connects to device and requests device id'''
		self.max_read_len = 9999
		if port is None:
			self.auto_connect()
		else:
			self.port = port
			self.connect() #connects, creates ser and id
		time.sleep(1)

	def open(self):
		'''open serial connection at object's port'''
		try:
			self.ser = serial.Serial(self.port,
									 self.baud,
									 timeout=1,
									 write_timeout=1)
			time.sleep(1)
		except (OSError, serial.SerialException):
			print(f'Could not connect to port {self.port}')
			sys.exit()

	def close(self):
		'''close the serial connection'''
		self.ser.close()

	def connect(self, verbose=True):
		'''open serial connection at object's port and connect to it.
		Fetches device id to check for timeout.
		'''
		self.open()
		try:
			self.id = self.get_id(verbose=False)
			print(f'Connected to {self.id} on port {self.port}'\
			' at baud {self.baud}.')
			return True
		except (OSError, serial.SerialTimeoutException):
			if verbose:
				print(f'{self.port}: Connected but could not query')
			self.close()
			return False

	def auto_connect(self):
		''' Choose a serial port to use.
		Use the first one that can query a device.
		'''
		print('Looking for ports ...')
		ports = serial_ports()
		print(f'Testing available ports: {ports}\n')
		for port in ports:     # try connecting to each device
			self.port = port
			if self.connect(verbose=False):
				return

	@property
	def is_open(self):
		return self.ser.is_open

	def write(self, string):
		encoded = string.encode()        # encode to bytes
		return self.ser.write(encoded)   # write command

	def read(self):
		data = self.ser.read(self.max_read_len)  # read data up to max length
		return data.decode().rstrip()            # decode bytes; remove endline

	def query(self, command):
		'''send serial command and fetch result'''
		full_command = self.com[command] + '\n\r'   # add required line ending
		self.write(full_command)                    # write command
		return self.read()	                        # read result

	def get_id(self, verbose=True):
		data = self.query('GET_ID')
		if data:
			if verbose:
				print(f'Device ID: {data}')
			return data
		if verbose:
			print('NO DEVICE ID FOUND')
		return None

	def get_reading(self):
		'''fetch one reading from device (defined in each device subclass)'''
		pass

	def disconnect(self):
		self.close()

	def start_collection(self, output_filename, dt=10, count=-1, label=None):
		'''collect indefinitely unless a count is given'''
		print(f'Starting collection with {dt}s intervals. '\
		'Press CTRL-C to stop.\n')

		label_list = label if not isinstance(label, str) else [label]

		output_file = Path.cwd()/output_filename
		if output_file.exists():
			print(f'WARNING: Data will be appended to an existing file'\
			' ({output_filename}).\n')

			# mention how the data will be stored/presented
			if self.data_columns:
				print(self.data_columns)

		try:
			while(count):
				record = list(self.get_reading()) # get a reading; save to csv
				if label:
					record = record + label_list
				with open(output_filename, 'a', newline='') as f:
					writer = csv.writer(f)
					writer.writerow(record)
				count -= 1
				time.sleep(dt)
			print('\nData collection ended.\n')
			self.disconnect()
		except KeyboardInterrupt:
			print('\nData collection stopped by user.\n')
			self.disconnect()


class PressureSensor(SerialDevice):
	''' Subclass of SerialDevice for controlling the Omega pressure sensor.

		Example:
			>>> omega = pressureSerial()
			>>> omega.start_collection()
	'''

	baud = 3600
	data_columns = 'timestamp, value, unit'

	def get_reading(self):
		'''get one reading from omega pressure sensor'''
		data = self.query('GET_VAL')
		timestamp = datetime.datetime.now()
		if data:
			val, unit = data.split(',')
		else:
			val = 'NaN'
			unit = 'NaN'
		print (timestamp, val, unit)
		return timestamp, val, unit


class LCRMeter(SerialDevice):
	''' Subclass of SerialDevice for controlling the GwInstek LCR-821.

		Example:
			>>> lcr = pressureSerial()
			>>> lcr.start_collection()
	'''

	baud = 38400
	data_columns = 'timestamp  freq  volt  primary  secondary  units'

	def get_id(self, verbose=True):
		'''Special case since LCR meter does not respond to *IDN?'''
		data = self.query('COMU?')
		if data == 'COMU:ON..':
			# self.query('SET_MANUAL')
			self.query('OVER')
			if verbose:
				print(f'Found LCR meter in manual mode')
			return ID_LCR
		if verbose:
			print('NO DEVICE ID FOUND')
		return None

	def get_reading(self):
		'''get one reading from lcr meter'''
		freq = self.query('GET_FREQ').split()[1]
		volt = self.query('GET_VOLT').split()[1]
		timestamp = datetime.datetime.now()
		data = self.query('START')
		if data:
			data = re.findall(r'\d+.\d+|[A-z]+', data)
			primary=data[2]
			secondary=data[5]
			units = data[-1]
		else:
			primary = 'NaN'
			secondary = 'NaN'
			units = 'NaN'
		print(timestamp, freq, volt, primary, secondary, units)
		return timestamp, freq, volt, primary, secondary, units


#-----------------------------------------------------------------------------#
# SCRIPT (update this part as needed for controlling the device)
#-----------------------------------------------------------------------------#

'''LCR meter example (uncomment the lines below)
	It should detect device automatically if only one is connected;
	if not, specify port. Collects every 10s forever unless count is given.
	Saves data to specified file (filename required).
'''
# lcr = LCRMeter()
# lcr.start_collection('output_filename.csv')


'''Omega pressure sensor example (uncomment the lines below)'''
# omega = PressureSensor()
# omega.start_collection('output_filename.csv')


'''Other ways of using this module (uncomment the lines below)'''
# serial_ports()                 # list all available serial ports
# list_devices()                 # list all devices

# omega = PressureSensor('COM5') # connect to a specific port
# omega.get_reading()            # get a single reading

# omega.start_collection('output_filename.csv',    # output filename (required)
						 # dt=5,                   # sample interval (seconds)
						 # count=20,               # number of readings to get
						 # label='50um')           # single label for data

# omega.start_collection('output_filename.csv',     # output filename (required)
						# dt=10,                    # sample interval (seconds)
						# count=10,                 # number of readings to get
						# label=['50um', 'trial1']) # multiple labels for data
