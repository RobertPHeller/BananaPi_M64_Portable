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
#  Created       : Mon Jun 8 22:28:15 2020
#  Last Modified : <200608.2250>
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
import Part, Drawing
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
  garbage = doc.findObjects('Drawing::FeatureViewPart')
  for g in garbage:
     doc.removeObject(g.Name)
  garbage = doc.findObjects('Drawing::FeaturePage')
  for g in garbage:
     doc.removeObject(g.Name)
  doc.addObject('Drawing::FeaturePage','TeensyThumbStickCoverPlatePage')
  doc.TeensyThumbStickCoverPlatePage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
  edt = doc.TeensyThumbStickCoverPlatePage.EditableTexts
  edt[0] = unicode("Robert Heller")
  edt[1] = unicode("Teensy ThumbStick Cover Plate")
  edt[4] = unicode("Banana Pi M64 Case (Plastic Machine Work)")
  edt[9] = unicode("1 / 1")
  edt[10] = unicode("1")
  edt[13] = unicode("June 9, 2020")
  doc.TeensyThumbStickCoverPlatePage.EditableTexts = edt
  teensyCover = doc.M64Case_keyboardshelf_teensythumbstickcover
  tcBounds = teensyCover.Shape.BoundBox
  doc.addObject('Drawing::FeatureViewPart','TeensyThumbStickCoverPlateView')
  doc.TeensyThumbStickCoverPlateView.Source = teensyCover
  doc.TeensyThumbStickCoverPlateView.X = -250
  doc.TeensyThumbStickCoverPlateView.Y = 0
  doc.TeensyThumbStickCoverPlateView.Rotation = 0
  doc.TeensyThumbStickCoverPlateView.Direction = (0.0,0.0,1.0)
  doc.TeensyThumbStickCoverPlateView.Scale = 1
  doc.TeensyThumbStickCoverPlatePage.addObject(doc.TeensyThumbStickCoverPlateView)
  #########
  doc.recompute()
  #########
  PageFile = open(App.activeDocument().TeensyThumbStickCoverPlatePage.PageResult,'r')
  OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_TeensyThumbStickCoverPlate.svg','w')
  OutFile.write(PageFile.read())
  del OutFile,PageFile
  sys.exit(1)
  
