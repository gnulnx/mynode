#!/usr/bin/env python

from setuptools import find_packages, setup

VERSION = "0.0.1"

setup(
    name="My Node",
    version=VERSION,
    description="Bitcoin Node Manager",
    author="John Furr",
    author_email="john.furr@gmail.com",
    url="https://github.com/gnulnx/mynode",
    packages=find_packages(),
    entry_points={"console_scripts": ["mynode=scripts.mynode:mynode"]},
    include_package_data=True,
)
