#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyTWS - Interactive Brokers Python API

PyTWS is a Python port of the API used for accessing the Interactive Brokers
Trader Workstation software.  PyTWS implements the same functionality as the
proprietary Java API distributed by Interactive Brokers.
'''

__copyright__ = "Copyright (c) 2008 Kevin J Bluck"
__version__   = "$Id$"

from distutils.core import setup


classifiers = '''
    Development Status :: 2 - Pre-Alpha
    Intended Audience :: Developers
    License :: OSI Approved :: MIT/X Consortium License
    Natural Language :: English
    Operating System :: OS Independent
    Programming Language :: Python
    Topic :: Office/Business :: Financial
    Topic :: Office/Business :: Financial :: Investment
    Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
    Topic :: Software Development :: Libraries
    Topic :: Software Development :: Libraries :: Python Modules
'''


setup(
    name = 'PyTWS',
    version = "0.0.1-9.61b",
    description = __doc__.split('\n')[0],
    author = 'Kevin Bluck',
    author_email = 'kevin.bluck@gmail.com',
    url = '',
    license = 'MIT License',
    packages = ['pytws'],
    classifiers = filter(None, classifiers.split('\n')),
    long_description = '\n'.join(__doc__.split('\n')[2:]),
    platforms = ['any'],
    download_url = '',
)
