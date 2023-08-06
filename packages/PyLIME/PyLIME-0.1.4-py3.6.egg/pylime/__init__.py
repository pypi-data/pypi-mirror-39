#!/bin/env python

########################################################################
# Copyright (C) 2012 David Palao
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
#  along with PyLIME.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

"""The pylime module provides to users with three main objects:
* 'LimeFile': it is the simplest object in the PyLIME package, it
             provides access for reading or writing to a LIME file.
* 'LimeReader': 'buffered' reading of LIME files. 
* 'LimeWriter': 'buffered' writing of LIME files.
  
 The LimeReader/Writer objects are intended to be used when 
several LIME files must be processed sequentially, ie for computing 
something on a set of LIME files with the same structure.
"""

from pylime.limefile import LimeFile
from pylime.limerecord import LimeRecord

#from pylime.limereader import LimeReader
#from pylime.limewriter import LimeWriter

if __name__ == "__main__":
    import sys
    f = LimeFile(sys.argv[1],'r')
    # I just want to make a guideline for the interface here:
    # An iterator for LimeFile returns records:
    for record in f:
        print(record.header)
        if record.data_type == "binary":
            a = record(">f4") # numpy array of big endian 32-bit floats
    for irecord in range(f.nrecords):
        if record.data_type == "binary":
            # it returns a numpy array of little endian 128-bit complexes:
            a = f[irecord]("<c16")
    for msg,rec in f.items:
        if record.data_type == "binary":
            # it returns a numpy array of little endian 64-bit ints:
            a = f[(msg,rec)](">i8")
