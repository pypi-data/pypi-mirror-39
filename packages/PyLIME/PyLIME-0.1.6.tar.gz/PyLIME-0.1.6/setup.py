#!/bin/env python

########################################################################
# Copyright (C) 2013, 2018 David Palao
#
# This file is part of PyLIME.

#  PyLIME is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyLIME is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyLIME. If not, see <http://www.gnu.org/licenses/>.
########################################################################

from setuptools import setup, find_packages

import sys
import os

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme, 'r').read()# + '\n\n'

setup(
    name='PyLIME',
    use_scm_version={"write_to": os.path.join("pylime", "version.py")},
    setup_requires=["setuptools_scm"],
    description='Python LIME file format library',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license='GNU General Public License (GPLv3)',
    author='David Palao',
    author_email='david.palao@gmail.com',
    url='http://th.physik.uni-frankfurt.de/~palao/software/PyLIME',
    platforms=['GNU/Linux'],
    packages=['pylime'],
    provides=['pylime'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"
    ],
    keywords='LIME LQCD Lattice QCD',
)

