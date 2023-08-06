# serialdaq
This module defines classes for controlling Omega DPG-4000 pressure sensors
and the GwInstek LCR-821 meters. This implementation features auto-connect to the device (by scanning available serial ports) and provides methods for finite- or indefinite-time data acquisition (and saving to file).

The classes for each device are subclasses of a SerialDevice class to allow expansion for use with other serial devices (simply inherit SerialDevice and define the get_reading() method, and the baud and data_columns properties).

# Installation
To install serialdaq, use pip (or similar):
```{.sourceCode .bash}
pip install serialdaq
```

# Documentation

This package detects the device automatically if only one is connected;
if not, specify port. Collects every 10s forever unless count is given.
Data is saved to specified file (filename required).

## LCR meter example
```python
lcr = serialdaq.LCRMeter()
lcr.start_collection('output_filename.csv')
```

## Omega pressure sensor example
```python
omega = serialdaq.PressureSensor()
omega.start_collection('output_filename.csv')
```

## Other ways of using this module
```python
serialdaq.serial_ports()                 # list all available serial ports
serialdaq.list_devices()                 # list all devices

omega = serialdaq.PressureSensor('COM5') # connect to a specific port
omega.get_reading()                      # get a single reading

omega.start_collection('output_filename.csv',    # output filename (required)
						 dt=5,                   # sample interval (seconds)
						 count=20,               # number of readings to get
						 label='50um')           # single label for data

omega.start_collection('output_filename.csv',     # output filename (required)
						dt=10,                    # sample interval (seconds)
						count=10,                 # number of readings to get
						label=['50um', 'trial1']) # multiple labels for data
```
