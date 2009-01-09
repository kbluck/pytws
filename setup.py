#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''PyTWS - Interactive Brokers Python API

   PyTWS is a Python port of the API used for controlling the Interactive
   Brokers LLC Trader Workstation software.  PyTWS implements similar
   interface and functionality as the proprietary Java API distributed by
   Interactive Brokers.

   PyTWS is not reviewed, supported or endorsed by Interactive Brokers LLC.
'''

__copyright__ = "Copyright (c) 2009 Kevin J Bluck"
__version__   = "$Id$"

from distutils.core import setup


classifiers = '''
    Development Status :: 3 - Alpha
    Intended Audience :: Developers
    OSI Approved :: BSD License (revised)
    Natural Language :: English
    Operating System :: OS Independent
    Programming Language :: Python
    Topic :: Office/Business :: Financial :: Investment
    Topic :: Software Development :: Libraries :: Python Modules
'''


setup(
    name = "PyTWS",
    version = "9.60b-a1",
    description = __doc__.split("\n")[0],
    author = "Kevin Bluck",
    author_email = "kevin.bluck@gmail.com",
    url = "",
    license = "BSD License (revised)",
    packages = ["tws"],
    classifiers = filter(None, classifiers.split("\n")),
    long_description = "\n".join(__doc__.split("\n")[2:]),
    platforms = ["any"],
    download_url = "",
)
