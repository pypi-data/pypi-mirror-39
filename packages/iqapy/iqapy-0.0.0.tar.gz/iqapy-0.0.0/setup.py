#!/usr/bin/env python

"""
A setuptools setup module for iqapy.
"""

# =============================================================================
# Imports
# =============================================================================

from setuptools import setup, find_packages # Always prefer setuptools over distutils
from os import path
from io import open

# =============================================================================
# Setup
# =============================================================================

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
long_description = ''
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

# Get the long description from the README file
version = '0.0.0'
with open(path.join(here, 'VERSION.md'), encoding='utf-8') as f:
	version = f.read()

# Setup
setup(
	# Basic information
	name='iqapy',
	version=version,
	license='GPLv3',

	description='A library for image quality assessment experiments.',
	long_description=long_description,
	long_description_content_type='text/markdown',

	url='https://github.com/jtmalarecki/iqapy',
	author='JT Malarecki',
	author_email='jt.malarecki@gmail.com',

	# Classification
	classifiers=[  # Optional
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 3 - Alpha',

		# Indicate who your project is intended for
		'Intended Audience :: Science/Research',
		'Topic :: Multimedia :: Graphics',
		'Topic :: Scientific/Engineering :: Visualization',

		# Pick your license as you wish
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
	keywords='image quality assessment',

	# Setup
	package_dir = {'': 'src'},
	packages=find_packages('src', exclude=['contrib', 'docs', 'tests']),

	# Miscellaneous
	project_urls={  # Optional
		'Bug Reports': 'https://github.com/jtmalarecki/iqapy/issues',
		# 'Say Thanks!': 'http://saythanks.io/to/example',
		'Source': 'https://github.com/jtmalarecki/iqapy',
	},
)