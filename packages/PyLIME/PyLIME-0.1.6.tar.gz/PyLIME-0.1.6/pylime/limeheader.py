#!/bin/env python

########################################################################
# Copyright (C) 2013 David Palao
#
# This file is part of PyLIME.
#
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

"""Stuff to manipulate LIME headers. To see details about this format, 
go to the PyLIME/doc directory."""

import os
import struct
from pylime.exceptions import WrongFileFormat
from pylime.globals import lime_header_size, lime_magic_number
from pylime.globals import lime_file_version_number, lime_type_length

# Note: this class requires a revision to make its design clean.

class LimeHeader(object):
    """The 'LimeHeader' class...
    For the parts of the header I'd like to use properties."""
    def __init__(self, fn=None, pos=None, LIME_type=None,
                 MBbit=None, MEbit=None):
        """Description of parameters:
        *) 'fn' is the file name of an alleged LIME file.
        *) 'pos' is the position, in bytes, where the header is
          supposed to start within the given file.
        """
        # No call to link, I want to initialize:
        self.fn = fn
        self.pos = pos
        self.LIME_type = LIME_type
        self.MBbit = MBbit
        self.MEbit = MEbit

    LIME_type_doc = """The LIME type is defined by an ASCII string of,
    at most, 'lime_type_length' characters (usually %d). When setting this 
    parameter ('LIME_type'), if the value given is bigger that 128 in
    length, it will be cut and a warning will appear.""" % (lime_type_length,)

    def _get_LIME_type(self):
        return self._LIME_type

    def _set_LIME_type(self,val):
        newval = "%s" % (val,)
        if len(newval) > lime_type_length:
            men = "Trying to set 'LIME_type' to something longer than "
            men += "{0} chars. Cutting it to {0}.".format(lime_type_length)
            raise UserWarning(men)
        self._LIME_type = newval[:lime_type_length]

    LIME_type = property(_get_LIME_type, _set_LIME_type, None, LIME_type_doc)
    
    def check_read(self):
        fsize = os.path.getsize(self.fn)
        if fsize-self.pos < lime_header_size:
            men = "remaining unread data < %d bytes" %(lime_header_size,)
            raise WrongFileFormat(self.fn,men)
        
    def link(self, fn=None, pos=None):
        if not fn is None:
            self.fn = fn
        if not pos is None:
            self.pos = pos

    def validate_bits(self, *protobits):
        bits = []
        for protobit in protobits:
            if protobit == 1 or protobit is True:
                bits.append(1)
            elif protobit == 0 or protobit is False:
                bits.append(0)
            else:
                men = "Not sure about what bit to assign to '%s'" % (protobit,)
                raise TypeError(men)
        return tuple(bits)

    def write(self, data_length, MBbit=None, MEbit=None, lime_type=None,
              mode='ab', fn=None):
        if fn is None:
            fn = self.fn
        self.link(fn,None)
        if not "b" in mode:
            mode += "b"
        if MBbit is None:
            MBbit = self.MBbit
        if MEbit is None:
            MEbit = self.MEbit
        bits = self.validate_bits(MBbit,MEbit)
        b0 = bits[0] << 15
        b1 = bits[1] << 14
        bits = b0 | b1
        if lime_type:
            self.LIME_type = lime_type
        fmt = ">lhHq%ds" % (lime_type_length,)
        predata = (lime_magic_number,lime_file_version_number,bits)
        predata += (data_length, self.LIME_type)
        data = struct.pack(fmt,*predata)
        with open(self.fn,mode) as f:
            f.write(data)
            
    def read(self,fn=None,pos=None):
        """Reads the header and assigns some data members."""
        self.link(fn,pos)
        self.check_read()
        with open(self.fn,'r') as f:
            f.seek(self.pos)
            self.f = f
            self.read_magic_number()
            self.read_file_version_number()
            self.read_msg_bits()
            self.read_data_length()
            self.read_LIME_type()
            self.f = None

    def read_data(self,t,pos=None):
        """The 'read_data' method is the generic method for reading 
        one block of data."""
        if pos:
            self.f.seek(pos)
        data=self.f.read(struct.calcsize(t))
        return struct.unpack_from(t,data)[0]
        
    def read_magic_number(self):
        self.magic_number = self.read_data('>l')
        if self.magic_number != lime_magic_number:
            raise WrongFileFormat(self.fn,"wrong magic number")
        
    def read_file_version_number(self):
        self.file_version_number = self.read_data('>h')
        
    def read_msg_bits(self):
        bitsNrest = self.read_data('>h')
        bits = bitsNrest
        mask_MBb = 1 << 15
        self.MBbit = (bits & mask_MBb) >> 15
        mask_MEb = 1 << 14
        self.MEbit = (bits & mask_MEb) >> 14

    def read_data_length(self):
        self.data_length = self.read_data('>q')
        
    def read_LIME_type(self):
        self.LIME_type = self.read_data('%ds'%(lime_type_length,))

    def __str__(self):
        s =  "-----------\n"
        s += "LIME Header\n"
        s += "-----------\n"
        s += "MBbit:\t\t%s\n" % (self.MBbit,)
        s += "MEbit:\t\t%s\n" % (self.MEbit,)
        s += "record type:\t'%s'\n" % (self.LIME_type,)
        s += "data length:\t%d\n" % (self.data_length,)
        return s
    
if __name__ == "__main__":
    import sys
    try:
        pos = int(sys.argv[2])
    except IndexError:
        pos = 0
    header = LimeHeader(sys.argv[1],pos)
    header.read()
    print("."*30)
    print("magic number:",header.magic_number)
    print("file version number:",header.file_version_number)
    print("msg begin bit:",header.MBbit)
    print("msg end bit:",header.MEbit)
    print("data length:",header.data_length)
    print("LIME type:",header.LIME_type)
    print("."*30)
