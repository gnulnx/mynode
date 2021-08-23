#!/usr/bin/env python

from distutils.core import setup

VERSION = "0.0.1"

setup(
    name='My Node',
    version=VERSION,
    description='Bitcoin Node Manager',
    author='John Furr',
    author_email='john.furr@gmail.com',
    url='https://github.com/gnulnx/mynode',
    scripts=["scripts/mynode"]
)