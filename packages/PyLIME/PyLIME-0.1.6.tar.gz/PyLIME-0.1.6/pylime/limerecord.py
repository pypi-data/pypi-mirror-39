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

"""The 'pylime.limerecord' is a module to manipulate 
LIME records (see the doc directory for a description of a LIME 
record).
"""

import os
import struct
from pylime.globals import lime_header_size
from pylime.limeheader import LimeHeader

class IterRecordRead(object):
    """An iterable that returns the data in a record in pieces."""
    def __init__(self, wrapped, fmt, bytes_per_item, nitems):
        self.idx = 0
        self.nitems = nitems
        self.bytes = bytes_per_item
        self.f = open(wrapped.file_name, "rb")
        self.DataStruct = struct.Struct(fmt)
        self.f.seek(wrapped.actual_position)
        self.wrapped = wrapped
        
    def __iter__(self):
        return self

    def next(self):
        if self.idx >= self.nitems:
            self.wrapped.actual_position = self.wrapped.record_position
            self.f.close()
            raise StopIteration
        else:
            data = self.f.read(self.bytes)
            item = self.DataStruct.unpack(data)
            self.wrapped.actual_position += self.bytes
            self.idx += 1
            return item


class LimeRecord(object):
    """The 'LimeRecord' class is useful to manipulate records in LIME
    files (recall that a LIME file is just a set of LIME records one after
    the other).
    A LimeRecord instance can be 'read' oriented or 'write' oriented (during
    its live, one record can be used for both reading and writing).
    Some examples:
    - using a record for writing:
    > wrec = LimeRecord("w", record_type='ildg-binary-data', MBbit=1, MEbit=1)
    > wrec.data = some_data
    > wrec.write(data_fmt='>d', fn='conf.1000', pos=some_position_in_file)
    - using a record for reading:
    > rrec = LimeRecord("r", fn='conf.1000', pos=some_position_in_file)
    > rrec.read(data_fmt='>d')
    > my_data = some_func(rrec.data)
    """

    def __init__(self, mode, data_fmt=None, fn=None, pos=None, **kwargs):
        """The 'mode' determines the initialization of the record:
        'r' initializes it as a read LimeRecord;
        'w' initializes the record to be used for writing.
        However, this does not restrict the possibilities of a LimeRecord:
        it does not matter what initalization was used the LimeRecord should
        be able to both read and write.
        The two initializations (modes) are provided to ease the usage
        of the records under normal circumstances."""
        self.file_name = fn
        self.record_position = pos
        self.actual_position = pos
        self.header = LimeHeader(self.file_name,self.record_position)
        self._data = None
        self._length = None
        self._lendata = None
        self.padding_length = 0
        self.mode = mode
        self.data_fmt = data_fmt
        # self._status is True when the record is complete:
        self._status = False
        if mode == "r":
            self.prep_for_reading(self.file_name,self.record_position)
        elif mode == "w":
            self.prep_for_writing(**kwargs)

    def prep_for_writing(self, record_type=None, MBbit=None, MEbit=None):
        """The creation of a record for writing is managed by this method."""
        self.record_type = record_type
        self.MBbit = MBbit
        self.MEbit = MEbit

    def prep_for_reading(self, fn, pos):
        """This is a method used when creating a record to read from."""
        self.link(fn,pos)
        self.check_readability()
        
    def check_readability(self):
        self.read_header()
        self.check_size()
        self._status = True

    def check_size(self):
        ini = self.record_position
        full_size = os.path.getsize(self.file_name)
        rec_length = self.__len__()
        if full_size-ini < rec_length:
            men = "record length (%d) is bigger than " % (rec_length,)
            men += "readable data from pos=%d: " %(ini,)
            men += "from that position there are %d bytes" %(full_size-ini,)
            raise WrongFileFormat(self.file_name, men)

    def read_header(self, fn=None, pos=None):
        if fn is None:
            fn = self.file_name
        if pos is None:
            pos = self.record_position
        header = self.header
        header.read(fn,pos)
        self._set_len(header.data_length)
        self.actual_position = self.record_position + lime_header_size
        
    data_doc = """The data attirbute of the record refers only to the contents
    of the record without metadata. If 'rec' is an instance of LimeRecord,
    'a=rec.data' returns the data part of a LIME record, as a binary string.
    'rec.data = xxx', of course sets the data in the record.
    """

    def _set_data(self,data):
        prelen = self.__len__()
        self._data = data
        self._set_len()

    def _get_data(self):
        return self._data

    def _del_data(self):
        self._set_data(None)

    data = property(_get_data, _set_data, _del_data, data_doc)
    
    def __len__(self):
        """The lenght (in bytes) of the full record, including
        header and padding."""
        if not self._length:
            try:
                reclen = self.header.data_length
            except AttributeError:
                reclen = None
            self._set_len(reclen)
        return self._length
        
    def _set_len(self,length_data=None):
        if length_data:
            lendata = length_data
        else:
            if self._data:
                itemsize = struct.calcsize(self.data_fmt)
                lendata = len(self._data)*itemsize
            else:
                lendata = 0
        rem = lendata % 8
        self._lendata = lendata
        self.header.data_length = self._lendata
        self.padding_length = (8-rem)%8
        self._length = lime_header_size+lendata+self.padding_length
        
    record_type_doc = """The LIME record type."""

    def _get_type(self):
        return self.header.LIME_type
        # if not self._record_type:
        #     self._set_type(None)
        # return self._record_type

    def _set_type(self,val):
        self.header.LIME_type = val
        # # Of course the meaning of "getting the type"
        # # depends on whether we are reading or writing.
        # if val is None:
        #     if self.header:
        #         self._record_type = self.header.LIME_type
        #         return
        # self._record_type = val

    record_type = property(_get_type, _set_type, None, record_type_doc)
                
    MBbit_doc = """The 'message begin' bit. The value is '1' when the
    record starts a message. The flag value is '0' otherwise."""

    def _get_MBbit(self):
        return self.header.MBbit

    def _set_MBbit(self,val):
        self.header.MBbit = val

    MBbit = property(_get_MBbit, _set_MBbit, None, MBbit_doc)
                
    MEbit_doc = """The 'message end' bit. The value is '1' when the
    record ends a message. The flag value is '0' otherwise."""

    def _get_MEbit(self):
        return self.header.MEbit

    def _set_MEbit(self,val):
        self.header.MEbit = val

    MEbit = property(_get_MEbit, _set_MEbit, None, MEbit_doc)
                
    def link(self, fn=None, pos=None):
        """It just links a record to a file."""
        if not fn is None:
            self.file_name = fn
            self.header.link(fn=self.file_name)
        if not pos is None:
            self.record_position = pos
            self.header.link(pos=self.record_position)

    def __nonzero__(self):
        return self._status

    def read_items(self, data_fmt=None, fn=None, pos=None):
        return self.read(data_fmt=data_fmt, fn=fn, pos=pos, iter=True)
        
    def read(self, data_fmt=None, fn=None, pos=None, iter=False):
        """The 'read' method reads the full record from the linked file."""
        self.read_header(fn, pos)
        # self.record_type = header.LIME_type
        self.link(fn,pos)
        if data_fmt:
            item_fmt = data_fmt
            self.data_fmt = data_fmt
        else:
            item_fmt = self.data_fmt
        if item_fmt[0] in ("@","=",">","<","!"):
            order = item_fmt[0]
            proto_fmt = item_fmt[1:]
        else:
            order = ""
            proto_fmt = item_fmt
        bytes_per_item = struct.calcsize(item_fmt)
        items_data = self._lendata/bytes_per_item
        if self._lendata%bytes_per_item != 0:
            men = "The data length (%d) is not a multiple of " %(self._lendata,)
            men += "the format type (%s) size (%d)." % (item_fmt,bytes_per_item)
            raise ValueError(men)
        if iter:
            return IterRecordRead(self, item_fmt, bytes_per_item, items_data)
        else:
            fmt = "%s%d%s" % (order, items_data, proto_fmt)
            DataStruct = struct.Struct(fmt)
            with open(self.file_name,'rb') as f:
                f.seek(self.actual_position)
                data = f.read(self._lendata)
                self.data = DataStruct.unpack(data)
            self.actual_position = self.record_position
    
    def write(self, data_fmt=None, fn=None, mode="ab"):
        """The 'write' method writes in the linked file a record described by
        the LimeRecord instance the method applies to."""
        self.link(fn,None)
        self.actual_position = os.path.getsize(self.file_name)
        if data_fmt:
            item_fmt = data_fmt
            self.data_fmt = data_fmt
        else:
            item_fmt = self.data_fmt
        if item_fmt[0] in ("@","=",">","<","!"):
            order = item_fmt[0]
        else:
            order = ""
        bytes_per_item = struct.calcsize(item_fmt)
        items_data = self._lendata/bytes_per_item
        if self._lendata%bytes_per_item != 0:
            men = "The data length (%d) is not a multiple of " %(self._lendata,)
            men += "the format type (%s) size (%d)." % (item_fmt,bytes_per_item)
            raise ValueError(men)
        padding_fmt = "%s%dB" % (order,self.padding_length)
        padding = tuple([0 for i in range(self.padding_length)])
        DataStruct = struct.Struct(item_fmt)
        self.header.write(self._lendata, mode=mode)
        with open(self.file_name,mode) as f:
            # This part is probably a performance bottleneck:
            for it in self.data:
                data = DataStruct.pack(it)
                f.write(data)
            data_pad = struct.pack(padding_fmt, *padding)
            f.write(data_pad)
        self.actual_position += self._lendata
            

