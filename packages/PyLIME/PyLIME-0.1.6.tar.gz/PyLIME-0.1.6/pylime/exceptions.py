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

"""Some common error cases in PyLIME."""

class WrongFileFormat(Exception):
    def __init__(self,fn,extra=None):
        self.fn = fn
        self.extra = extra

    def __str__(self):
        men = "the file called '%s' is not a proper LIME file" %(self.fn,)
        men +="\n(or the position is wrong)."
        if self.extra:
            men += " (%s)" %(self.extra)
        return men

