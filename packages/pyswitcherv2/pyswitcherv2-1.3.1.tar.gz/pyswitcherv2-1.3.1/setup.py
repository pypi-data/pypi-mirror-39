from setuptools import setup, find_packages

setup(
  name = 'pyswitcherv2',
  packages = ['pyswitcherv2'], 
  version = '1.3.1',
  description = 'Control Switcher V2 water heater via Python',
  author = 'Sagi Lowenhardt',
  author_email = 'sagi@lowenhardt.com',
  url = 'https://github.com/sagilo/pyswitcherv2', 
  download_url = 'https://github.com/sagilo/pyswitcherv2/archive/1.3.1.tar.gz',
  include_package_data = True,
  keywords = ['switcher', 'switcherv2'],
  entry_points = {
      'console_scripts': ['pyswitcherv2=pyswitcherv2.switcher:main'],
  },
  classifiers = [],
)
