from setuptools import setup, find_packages


REQUIRES = [
	'biopython>=1.71',
	'xmltodict',
	'pandas',
	'bcbio-gff',
]


setup(
	name = 'edgepy',
	version = '0.1.16dev',
	author = 'Alex Summers',
	author_email='asummers.edgepy@gmail.com',
	packages = find_packages(),
	url = 'http://pypi.python.org/pypi/edgepy/',
	license = 'LICENSE.txt',
	long_description = open('README.txt').read(),
	install_requires = REQUIRES,
	include_package_data = True,
	package_data={'edgepy': ['docs/*']},
)

