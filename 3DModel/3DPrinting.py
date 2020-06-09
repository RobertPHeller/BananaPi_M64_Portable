#!/usr/bin/FreeCAD
#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Jun 9 07:52:03 2020
#  Last Modified : <200609.0756>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
#    Copyright (C) 2020  Robert Heller D/B/A Deepwoods Software
#			51 Locke Hill Road
#			Wendell, MA 01379-9728
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# 
#
#*****************************************************************************


import FreeCAD as App
import Part
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))

from SectionList import *
from Case import *

if __name__ == '__main__':
  if not App.listDocuments().has_key("BananaPiM64Model"):
     App.open("/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model.fcstd")
  App.setActiveDocument("BananaPiM64Model")
  App.ActiveDocument=App.getDocument("BananaPiM64Model")
  doc = App.activeDocument()
  usbsataboardcradle = doc.M64Case_bottom_cradle
  usbsataboardcradle.Shape.exportStl("/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_usbsataboardcradle.stl")
  sys.exit(1)
