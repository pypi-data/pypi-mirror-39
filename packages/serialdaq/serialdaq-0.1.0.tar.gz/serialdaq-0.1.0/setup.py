# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['serialdaq']

package_data = \
{'': ['*']}

install_requires = \
['datetime>=4.3,<5.0', 'pathlib>=1.0,<2.0', 'pyserial>=3.4,<4.0']

setup_kwargs = {
    'name': 'serialdaq',
    'version': '0.1.0',
    'description': 'Serial device controller for data acquisition. Currently supports Omega DPG-4000 pressure sensor and GwInstek LCR-821 meter.',
    'long_description': "# serialdaq\nThis module defines classes for controlling Omega DPG-4000 pressure sensors\nand the GwInstek LCR-821 meters. This implementation features auto-connect to the device (by scanning available serial ports) and provides methods for finite- or indefinite-time data acquisition (and saving to file).\n\nThe classes for each device are subclasses of a SerialDevice class to allow expansion for use with other serial devices (simply inherit SerialDevice and define the get_reading() method, and the baud and data_columns properties).\n\n# Installation\nTo install serialdaq, use pip (or similar):\n```{.sourceCode .bash}\npip install serialdaq\n```\n\n# Documentation\n\nThis package detects the device automatically if only one is connected;\nif not, specify port. Collects every 10s forever unless count is given.\nData is saved to specified file (filename required).\n\n## LCR meter example\n```python\nlcr = serialdaq.LCRMeter()\nlcr.start_collection('output_filename.csv')\n```\n\n## Omega pressure sensor example\n```python\nomega = serialdaq.PressureSensor()\nomega.start_collection('output_filename.csv')\n```\n\n## Other ways of using this module\n```python\nserialdaq.serial_ports()                 # list all available serial ports\nserialdaq.list_devices()                 # list all devices\n\nomega = serialdaq.PressureSensor('COM5') # connect to a specific port\nomega.get_reading()                      # get a single reading\n\nomega.start_collection('output_filename.csv',    # output filename (required)\n\t\t\t\t\t\t dt=5,                   # sample interval (seconds)\n\t\t\t\t\t\t count=20,               # number of readings to get\n\t\t\t\t\t\t label='50um')           # single label for data\n\nomega.start_collection('output_filename.csv',     # output filename (required)\n\t\t\t\t\t\tdt=10,                    # sample interval (seconds)\n\t\t\t\t\t\tcount=10,                 # number of readings to get\n\t\t\t\t\t\tlabel=['50um', 'trial1']) # multiple labels for data\n```\n",
    'author': 'Manny Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
