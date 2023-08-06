#!/usr/bin/env python3

#!/usr/bin/env python3

"""
Setup script for pyren
"""

from setuptools import setup, find_packages

desc = 'A Python implementation of the Ren data serialization format.'

setup(
	name="pyRen",
	version="0.0.0",
	description=desc,
	long_description=desc,
	url='https://github.com/ocket8888/pyRen',
	author='ocket8888',
	author_email='ocket8888@gmail.com',
	classifiers=[
		'Development Status :: 1 - Planning',
		'Environment :: Web Environment',
		'Intended Audience :: Telecommunications Industry',
		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
		'License :: Public Domain',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: REBOL',
		'Topic :: Communications',
		'Topic :: Software Development :: Libraries',
		'Topic :: Text Processing'
	],
	keywords='Ren data serialization',
	packages=find_packages(exclude=['contrib', 'docs', 'tests']),
	install_requires=['setuptools'],
	python_requires='~=3.6'
)
