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
#  Created       : Sun Jun 7 15:27:04 2020
#  Last Modified : <200608.1238>
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
  #
  ## First the LCDMounting Brackets
  ## These are 1/2x1/2 by 222mm long Al. angles with holes drilled and a 
  ## notch cut on one side.
  #####
  ## Left
  doc.addObject('Drawing::FeaturePage','LeftLCDMountBracketPage')
  doc.LeftLCDMountBracketPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
  edt = doc.LeftLCDMountBracketPage.EditableTexts
  edt[0] = unicode("Robert Heller")
  edt[1] = unicode("Left LCD Mounting Bracket")
  edt[4] = unicode("Banana Pi M64 Case (Machine Work)")
  edt[9] = unicode("1 / 5")
  edt[10] = unicode(".5")
  edt[13] = unicode("June 7, 2020")
  doc.LeftLCDMountBracketPage.EditableTexts = edt
  leftBracket = doc.M64Case_middle_LCDLeftBracket
  lbBounds = leftBracket.Shape.BoundBox
  doc.addObject('Drawing::FeatureViewPart','LCDLBEndView')
  doc.LCDLBEndView.Source = leftBracket
  doc.LCDLBEndView.X = (-lbBounds.ZMin*.5)+38.1
  doc.LCDLBEndView.Y = (-lbBounds.XMin*.5)+25.4
  doc.LCDLBEndView.Rotation = 0
  doc.LCDLBEndView.Direction = (0.0,1.0,0.0)
  doc.LCDLBEndView.Scale = .5
  doc.LeftLCDMountBracketPage.addObject(doc.LCDLBEndView)
  doc.addObject('Drawing::FeatureViewPart','LCDLBSideView')
  doc.LCDLBSideView.Source = leftBracket
  doc.LCDLBSideView.X = (-lbBounds.ZMin*.5)+38.1
  doc.LCDLBSideView.Y = (lbBounds.YLength*.5)+76.2
  doc.LCDLBSideView.Rotation = 0
  doc.LCDLBSideView.Direction = (1.0,0.0,0.0)
  doc.LCDLBSideView.Scale = .5
  doc.LeftLCDMountBracketPage.addObject(doc.LCDLBSideView)
  doc.addObject('Drawing::FeatureViewPart','LCDLBBottomView')
  doc.LCDLBBottomView.Source = leftBracket
  doc.LCDLBBottomView.X = (-lbBounds.XMin*.5)+76.2
  doc.LCDLBBottomView.Y = (-lbBounds.YMin*.5)+62
  doc.LCDLBBottomView.Rotation = 0
  doc.LCDLBBottomView.Direction = (0.0,0.0,-1.0)
  doc.LCDLBBottomView.Scale = .5
  doc.LeftLCDMountBracketPage.addObject(doc.LCDLBBottomView)
  ####
  ## Right
  doc.addObject('Drawing::FeaturePage','RightLCDMountBracketPage')
  doc.RightLCDMountBracketPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
  edt = doc.RightLCDMountBracketPage.EditableTexts
  edt[0] = unicode("Robert Heller")
  edt[1] = unicode("Right LCD Mounting Bracket")
  edt[4] = unicode("Banana Pi M64 Case (Machine Work)")
  edt[9] = unicode("2 / 5")
  edt[10] = unicode(".5")
  edt[13] = unicode("June 7, 2020")
  doc.RightLCDMountBracketPage.EditableTexts = edt
  rightBracket = doc.M64Case_middle_LCDRightBracket
  rbBounds = rightBracket.Shape.BoundBox
  doc.addObject('Drawing::FeatureViewPart','LCDRBEndView')
  doc.LCDRBEndView.Source = rightBracket
  doc.LCDRBEndView.X = (-rbBounds.ZMin*.5)+38.1
  doc.LCDRBEndView.Y = (-rbBounds.XMin*.5)+25.4 
  doc.LCDRBEndView.Rotation = 0
  doc.LCDRBEndView.Direction = (0.0,1.0,0.0)
  doc.LCDRBEndView.Scale = .5
  doc.RightLCDMountBracketPage.addObject(doc.LCDRBEndView)
  doc.addObject('Drawing::FeatureViewPart','LCDRBSideView')
  doc.LCDRBSideView.Source = rightBracket
  doc.LCDRBSideView.X = (-rbBounds.ZMin*.5)+38.1
  doc.LCDRBSideView.Y = (rbBounds.YLength*.5)+76.2
  doc.LCDRBSideView.Rotation = 0
  doc.LCDRBSideView.Direction = (1.0,0.0,0.0)
  doc.LCDRBSideView.Scale = .5
  doc.RightLCDMountBracketPage.addObject(doc.LCDRBSideView)
  doc.addObject('Drawing::FeatureViewPart','LCDRBBottomView')
  doc.LCDRBBottomView.Source = rightBracket
  doc.LCDRBBottomView.X = (-rbBounds.XMin*.5)+76.2
  doc.LCDRBBottomView.Y = (-rbBounds.YMin*.5)+90.5+(rbBounds.YLength*.5)
  doc.LCDRBBottomView.Rotation = 180
  doc.LCDRBBottomView.Direction = (0.0,0.0,-1.0)
  doc.LCDRBBottomView.Scale = .5
  doc.RightLCDMountBracketPage.addObject(doc.LCDRBBottomView)
  ####
  ## Power Supply Box
  ## This is a Bud CU3002A that needs some additional machining: four holes
  ## in the bottom on the base half, a cutout for a power inlet module, a
  ## hole for a strain relief in the ends of the base. The cover half needs 
  ## mounting and air flow holes for a pair of small fans.
  ##
  ####
  ## First the base
  doc.addObject('Drawing::FeaturePage','PowerSupplyBoxBasePage')
  doc.PowerSupplyBoxBasePage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
  edt = doc.PowerSupplyBoxBasePage.EditableTexts 
  edt[0] = unicode("Robert Heller")
  edt[1] = unicode("Power Supply Box Base")
  edt[4] = unicode("Banana Pi M64 Case (Machine Work)")
  edt[9] = unicode("3 / 5")
  edt[10] = unicode("1")
  edt[13] = unicode("June 7, 2020")
  doc.PowerSupplyBoxBasePage.EditableTexts = edt
  psboxBase = doc.M64Case_bottom_psbox_CU3002ABase
  psbbBounds = psboxBase.Shape.BoundBox
  print psbbBounds
  doc.addObject('Drawing::FeatureViewPart','psboxBaseTopView')
  doc.psboxBaseTopView.Source = psboxBase
  doc.psboxBaseTopView.X = (-psbbBounds.XMin)+38.1
  doc.psboxBaseTopView.Y = (-psbbBounds.YMin)+25.4
  doc.psboxBaseTopView.Rotation = 0
  doc.psboxBaseTopView.Direction = (0.0,0.0,1.0)
  doc.psboxBaseTopView.Scale = 1
  doc.PowerSupplyBoxBasePage.addObject(doc.psboxBaseTopView)
  doc.addObject('Drawing::FeatureViewPart','psboxBaseFrontView')
  doc.psboxBaseFrontView.Source = psboxBase
  doc.psboxBaseFrontView.X = (-psbbBounds.ZMin*2) + 25.4 + 9.68*psbbBounds.ZLength
  doc.psboxBaseFrontView.Y = psbbBounds.YLength + psbbBounds.ZLength
  doc.psboxBaseFrontView.Rotation = 90
  doc.psboxBaseFrontView.Direction = (0.0,1.0,0.0)
  doc.psboxBaseFrontView.Scale = 1
  doc.PowerSupplyBoxBasePage.addObject(doc.psboxBaseFrontView)
  doc.addObject('Drawing::FeatureViewPart','psboxBaseBackView')
  doc.psboxBaseBackView.Source = psboxBase
  doc.psboxBaseBackView.X = 508
  doc.psboxBaseBackView.Y = 190.525
  doc.psboxBaseBackView.Rotation = 90
  doc.psboxBaseBackView.Direction = (0.0,-1.0,0.0)
  doc.psboxBaseBackView.Scale = 1
  doc.PowerSupplyBoxBasePage.addObject(doc.psboxBaseBackView)
  doc.addObject('Drawing::FeatureViewPart','psboxBaseISOView')
  doc.psboxBaseISOView.Source = psboxBase
  doc.psboxBaseISOView.X = 50
  doc.psboxBaseISOView.Y = -75
  doc.psboxBaseISOView.Rotation = 45
  doc.psboxBaseISOView.Direction = (1.0,1.0,1.0)
  doc.psboxBaseISOView.Scale = .75
  doc.PowerSupplyBoxBasePage.addObject(doc.psboxBaseISOView)
  ## Then the cover
  doc.addObject('Drawing::FeaturePage','PowerSupplyBoxCoverPage')
  doc.PowerSupplyBoxCoverPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
  edt = doc.PowerSupplyBoxCoverPage.EditableTexts 
  edt[0] = unicode("Robert Heller")
  edt[1] = unicode("Power Supply Box Cover")
  edt[4] = unicode("Banana Pi M64 Case (Machine Work)")
  edt[9] = unicode("4 / 5")
  edt[10] = unicode("1")
  edt[13] = unicode("June 7, 2020")
  doc.PowerSupplyBoxCoverPage.EditableTexts = edt
  psboxCover = doc.M64Case_bottom_psbox_CU3002ACover
  psbcBounds = psboxCover.Shape.BoundBox
  doc.addObject('Drawing::FeatureViewPart','psboxCoverLeftView')
  doc.psboxCoverLeftView.Source = psboxCover    
  doc.psboxCoverLeftView.X = -137.5
  doc.psboxCoverLeftView.Y = 25
  doc.psboxCoverLeftView.Rotation = 90
  doc.psboxCoverLeftView.Direction = (1.0,0.0,0.0)
  doc.psboxCoverLeftView.Scale = 1
  doc.PowerSupplyBoxCoverPage.addObject(doc.psboxCoverLeftView)
  doc.addObject('Drawing::FeatureViewPart','psboxCoverRightView')
  doc.psboxCoverRightView.Source = psboxCover
  doc.psboxCoverRightView.X = -137.5
  doc.psboxCoverRightView.Y = 125.0
  doc.psboxCoverRightView.Rotation = 90
  doc.psboxCoverRightView.Direction = (-1.0,0.0,0.0)
  doc.psboxCoverRightView.Scale = 1
  doc.PowerSupplyBoxCoverPage.addObject(doc.psboxCoverRightView)
  doc.addObject('Drawing::FeatureViewPart','psboxCoverISOView')
  doc.psboxCoverISOView.Source = psboxCover
  doc.psboxCoverISOView.X = 150
  doc.psboxCoverISOView.Y = 237.5
  doc.psboxCoverISOView.Rotation = 45.0
  doc.psboxCoverISOView.Direction = (-1.0,-1.0,-1.0)
  doc.psboxCoverISOView.Scale = .5
  doc.PowerSupplyBoxCoverPage.addObject(doc.psboxCoverISOView)
  #### Finally, the main case fan "grill"
  doc.addObject('Drawing::FeaturePage','CaseFanGrillPage')
  doc.CaseFanGrillPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
  edt = doc.CaseFanGrillPage.EditableTexts 
  edt[0] = unicode("Robert Heller")
  edt[1] = unicode("Main Case Fan Frill")
  edt[4] = unicode("Banana Pi M64 Case (Machine Work)")
  edt[9] = unicode("5 / 5")
  edt[10] = unicode("1")
  edt[13] = unicode("June 8, 2020")
  doc.CaseFanGrillPage.EditableTexts = edt    
  fanGrill = doc.M64Case_bottom_psgrill
  fanGrillBounds = fanGrill.Shape.BoundBox 
  print "fanGrillBounds: ",fanGrillBounds
  doc.addObject('Drawing::FeatureViewPart','caseFanGrillView')
  doc.caseFanGrillView.Source = fanGrill
  doc.caseFanGrillView.X = -152.4
  doc.caseFanGrillView.Y = 23.8
  doc.caseFanGrillView.Rotation = 90
  doc.caseFanGrillView.Direction = (1.0,0.0,0.0)
  doc.caseFanGrillView.Scale = 1.0
  doc.CaseFanGrillPage.addObject(doc.caseFanGrillView)
  doc.addObject('Drawing::FeatureViewPart','caseFanGrillISOView')
  doc.caseFanGrillISOView.Source = fanGrill
  doc.caseFanGrillISOView.X = 88.9
  doc.caseFanGrillISOView.Y = -130.2
  doc.caseFanGrillISOView.Rotation = 90
  doc.caseFanGrillISOView.Direction = (1.0,1.0,1.0)
  doc.caseFanGrillISOView.Scale = 1.0
  doc.CaseFanGrillPage.addObject(doc.caseFanGrillISOView)
  #######
  doc.recompute()
  ######
  PageFile = open(App.activeDocument().LeftLCDMountBracketPage.PageResult,'r')
  OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_LeftBracketMount.svg','w')
  OutFile.write(PageFile.read())
  del OutFile,PageFile
  PageFile = open(App.activeDocument().RightLCDMountBracketPage.PageResult,'r')
  OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_RightBracketMount.svg','w')
  OutFile.write(PageFile.read())
  del OutFile,PageFile
  PageFile = open(App.activeDocument().PowerSupplyBoxBasePage.PageResult,'r')
  OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_PSBoxBase.svg','w')
  OutFile.write(PageFile.read())
  del OutFile,PageFile
  PageFile = open(App.activeDocument().PowerSupplyBoxCoverPage.PageResult,'r')
  OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_PSBoxCover.svg','w')
  OutFile.write(PageFile.read())
  del OutFile,PageFile
  PageFile = open(App.activeDocument().CaseFanGrillPage.PageResult,'r')
  OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_CaseFanGrill.svg','w')
  OutFile.write(PageFile.read())
  del OutFile,PageFile
  sys.exit(1)
