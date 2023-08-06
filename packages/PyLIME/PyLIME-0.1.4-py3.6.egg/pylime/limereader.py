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

"""The LimeReader class can iterate over a collection of Lime files. The
reading is done in a separated thread and we can read in advance some files
such that they are ready to be used when required."""

from pylime.limefile import LimeFile

class LimeReader(LimeFile):
    """A class to read LIME files."""
    def __init__(self,fn):
        LimeFile.__init__(self,fn,'r')
        self.analyze()

    def analyze(self):
        """'LimeReader.analyze' determines the structure of the input
        file as LIME file. In the process, it is checked the compliance
        of the file with the LIME standard.
        The following steps are performed:
        1) Minimum length of the file: a LIME file must be, at least, 144
        bytes long.
        2) read 1 header
        """
        
