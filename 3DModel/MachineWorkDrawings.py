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
#  Last Modified : <200607.1800>
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
    #
    # First the LCDMounting Brackets
    #
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
    
    doc.recompute()

    #PageFile = open(App.activeDocument().LeftLCDMountBracketPage.PageResult,'r')
    #OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_LeftBracketMount.svg','w')
    #OutFile.write(PageFile.read())
    #del OutFile,PageFile
    #PageFile = open(App.activeDocument().RightLCDMountBracketPage.PageResult,'r')
    #OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_RightBracketMount.svg','w')
    #OutFile.write(PageFile.read())
    #del OutFile,PageFile
    #sys.exit(1)
