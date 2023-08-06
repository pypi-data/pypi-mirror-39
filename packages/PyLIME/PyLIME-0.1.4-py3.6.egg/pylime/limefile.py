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

import os
from pylime.limerecord import LimeRecord

class IterLimeFile(object):
    def __init__(self,limef):
        self.it = iter(limef._records)
        
    def next(self):
        return next(self.it)


class LimeFile(object):
    """The 'LimeFile' is a class that can be used to manipulate LIME
    files. See the doc directory of your PyLIME package for details
    about this format.

    Usage:
      fr = LimeFile("name.of.file","r")
      fw = LimeFile("another.name.of.file","w")
      
    Design notes:
    * limereader and limewriter must be removed. 
    * LimeFile must be a metaclass: depending on the input parameter 'mode'
     one should get different functionality:
     'r' mode: __getitem__: returns a record
               scan: ...
               seek: ...

     'w' mode: __getitem__: ?
               add/append (not yet decided): ...
               write: ...
               seek (?):
     """
    def __init__(self,fn,mode):
        self.fn = fn
        self.mode = mode
        self._records = []
        self._messages = []
        allowed = ["fn", "mode", "_records", "position", "__iter__", "rewind"]
        if mode == "r":
            more = ["read", "scan", "__getitem__", "rewind"]
        elif mode == "w":
            more = ["write", "append"]
        for at in more:
            allowed.append(at)
        self.allowed = allowed
        self.rewind()
        if mode == "r":
            self.scan()

    def __getattribute__(self,name):
        allowed = object.__getattribute__(self,'allowed')
        if name in allowed:
            return object.__getattribute__(self,name)

    def __getitem__(self,item):
        return self._records[item]

    def __iter__(self):
        return IterLimeFile(self)

    def __len__(self):
        return len(self._records)
    
    def rewind(self):
        self.position = 0
        
    def scan(self):
        """The 'scan' method looks for all the records inside a LIME file."""
        # for reading: this method must be re-coded
        file_size = os.path.getsize(self.fn)
        with open(self.fn,self.mode) as f:
            pos = 0
            while True:
                rec = LimeRecord("r", fn=self.fn, pos=pos)
                if rec:
                    self._records.append(rec)
                    pos += len(rec)
                    if pos >= file_size:
                        break
                else:
                    break

    # Do we need a read method?
    # def read(self,item=None):
    #     if item:
    #         return self[item]
    #     return self._records

    def write(self,bin_fmt=None):
        # The binary format used is None by default, meaning that
        # the format will be taken from the records (some format
        # must be set in the records).
        ####################################
        #  First open the file and close it, to empty it,
        # because later the mode must be 'a' (want to add several records):
        f = open(self.fn,'w')
        f.close()
        # Now iterate over all the records that make up the LIME file:
        for rec in self:
            rec.link(self.fn, self.position)
            rec.write(bin_fmt)#???
            self.position += len(rec)

    def append(self,rec):
        # this method should call rec.link with the file name and the
        #position of the record in the file.
        rec.link(self.fn,self.position)
        self._records.append(rec)
        self.position += len(rec)


if __name__ == "__main__":
    rL = LimeFile("macuto","r")
    print(type(rL))
    rL.scan()
    rL.read()
    try:
        rL.write()
    except TypeError:
        print("calling the write method on a read-only file fails!")
    wL = LimeFile("macuto","w")
    wL.write()
    try:
        wL.read()
    except TypeError:
        print("calling the read method on a write-only file fails!")

    # Reading interface:
    rL = LimeFile("macuto.lime","r")# << same as before
    for rec in rL:
        if rec.type == "ildg-binary-data":
            gauge_raw = rec(fmt=">c16")
            break
    # (we start counting messages and records by 1)
    # A second idiom to get a message:
    # the following line returns the 3rd record in a LIME file, 
    # (irrespective of the message number)
    gauge_rec = rL[3]
    gauge_raw2 = gauge_rec(fmt=">c16")
    # A third possibility (message,record-in-that-message):
    gauge_rec_bis = rL[(2,2)]
    gauge_raw3 = gauge_rec_bis(fmt=">c16")

    # Writing interface:
    wL = LimeFile("my.lime.file","w")
    # of course, that is incomplete (not ILDG compilant):
    rec_gauge = LimeRecord(type="ildg-binary-data", MBbit=0, MEbit=0)
    rec_gauge.data = some_gauge
    wL.append(rec_gauge)
    rec_checksum = LimeRecord(type="scidac-checksum", MBbit=0, MEbit=1)
    rec_checksum.data = mychecksum
    wL.append(rec_checksum)
    wL.write()
