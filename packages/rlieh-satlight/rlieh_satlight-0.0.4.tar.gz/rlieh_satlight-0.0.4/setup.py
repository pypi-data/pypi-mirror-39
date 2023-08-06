# @Author: Olivier Watté <user>
# @Date:   2018-04-22T10:15:39-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2018-12-18T14:52:30-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions



#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Rlieh-pwm provides an interface to manage light phases using .ini file to
# build remote call to a RLIEH satellite web API

# Copyright (C) 2018 Olivier Watté
#
# This file is part of Rlieh-satlight.
#
# Rlieh-satlight is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rlieh-satlight is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rlieh-pwm.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

import rlieh_satlight

setup(
    name='rlieh_satlight',
    version=rlieh_satlight.__version__,
    packages=find_packages(),
    author="Olivier Watté - RLIEH project by Biolo.tech",
    author_email="owatte@biolo.tech",
    description="This module provides an interface to manage light phases using .ini file to perform remote call to a RLIEH satellite",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://github.com/owatte/rlieh-satlight',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    entry_points={
        'console_scripts': ['rlieh-satlight=rlieh_satlight.core:main'],
    },
    install_requires=[
          'argparse',
          'configparser',
          'requests',
      ],
)
