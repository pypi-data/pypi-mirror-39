from distutils.core import setup

REQUIRES = [
	'biopython>=1.71',
	'xmltodict',
	'pandas',
]


setup(
	name = 'edgepy',
	version = '0.1.6dev',
	author = 'Alex Summers',
	author_email='asummers.edgepy@gmail.com',
	packages = ['edgepy'],
	url = 'http://pypi.python.org/pypi/edgepy/',
	license = 'LICENSE.txt',
	long_description = open('README.txt').read(),
	#install_requires = REQUIRES,
)

