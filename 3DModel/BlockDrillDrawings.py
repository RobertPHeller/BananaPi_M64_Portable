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
#  Created       : Mon Jun 8 14:19:16 2020
#  Last Modified : <200608.1626>
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
    #############
    ##
    ## Top Block: hinge
    ##
    doc.addObject('Drawing::FeaturePage','TopBackBlockDrillSheetPage')
    doc.TopBackBlockDrillSheetPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
    edt = doc.TopBackBlockDrillSheetPage.EditableTexts
    edt[0] = unicode("Robert Heller")
    edt[1] = unicode("Top Block Drill Sheet (back block hinge holes)")
    edt[4] = unicode("Banana Pi M64 Case (Drill Sheets)")
    edt[9] = unicode("1 / 5")
    edt[10] = unicode(".375")
    edt[13] = unicode("June 8, 2020")
    doc.TopBackBlockDrillSheetPage.EditableTexts = edt
    topBackBlock = doc.M64Case_top_backblock
    topBBBounds = topBackBlock.Shape.BoundBox
    doc.addObject('Drawing::FeatureViewPart','TopBlockView')
    doc.TopBlockView.Source = topBackBlock
    doc.TopBlockView.X = 12.7
    doc.TopBlockView.Y = 50.8
    doc.TopBlockView.Rotation = 0
    doc.TopBlockView.Direction = (0.0,1.0,0.0)
    doc.TopBlockView.Scale=.375
    doc.TopBackBlockDrillSheetPage.addObject(doc.TopBlockView)
    #############
    ##
    ## MiddleBlocks: Speakers, HDMI aux boards
    ##
    doc.addObject('Drawing::FeaturePage','MiddleBackBlockDrillSheetPage')
    doc.MiddleBackBlockDrillSheetPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
    edt = doc.MiddleBackBlockDrillSheetPage.EditableTexts
    edt[0] = unicode("Robert Heller")
    edt[1] = unicode("Middle Back Block Drill Sheet (HDMI Aux Boards holes)")
    edt[4] = unicode("Banana Pi M64 Case (Drill Sheets)")
    edt[9] = unicode("2 / 5")
    edt[10] = unicode(".375")
    edt[13] = unicode("June 8, 2020")
    doc.MiddleBackBlockDrillSheetPage.EditableTexts = edt
    middleBackBlock = doc.M64Case_middle_backblock
    middleBBBounds = middleBackBlock.Shape.BoundBox
    doc.addObject('Drawing::FeatureViewPart','MiddleBackBlockView')
    doc.MiddleBackBlockView.Source = middleBackBlock
    doc.MiddleBackBlockView.X = 150
    doc.MiddleBackBlockView.Y = 25
    doc.MiddleBackBlockView.Rotation = 90
    doc.MiddleBackBlockView.Direction = (0.0,0.0,1.0)
    doc.MiddleBackBlockView.Scale = .375
    doc.MiddleBackBlockDrillSheetPage.addObject(doc.MiddleBackBlockView)
    #
    doc.addObject('Drawing::FeaturePage','MiddleLeftBlockDrillSheetPage')
    doc.MiddleLeftBlockDrillSheetPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
    edt = doc.MiddleLeftBlockDrillSheetPage.EditableTexts
    edt[0] = unicode("Robert Heller")
    edt[1] = unicode("Middle Left Block Drill Sheet (Speaker Mounting holes)")
    edt[4] = unicode("Banana Pi M64 Case (Drill Sheets)")
    edt[9] = unicode("3 / 5")
    edt[10] = unicode(".5")
    edt[13] = unicode("June 8, 2020")
    doc.MiddleLeftBlockDrillSheetPage.EditableTexts = edt
    middleLeftBlock = doc.M64Case_middle_leftblock
    middleLBBounds = middleLeftBlock.Shape.BoundBox
    doc.addObject('Drawing::FeatureViewPart','MiddleLeftBlockView')
    doc.MiddleLeftBlockView.Source = middleLeftBlock
    doc.MiddleLeftBlockView.X = 50.8
    doc.MiddleLeftBlockView.Y = 25.4
    doc.MiddleLeftBlockView.Rotation = 0
    doc.MiddleLeftBlockView.Direction = (0.0,0.0,1.0)
    doc.MiddleLeftBlockView.Scale = .5
    doc.MiddleLeftBlockDrillSheetPage.addObject(doc.MiddleLeftBlockView)
    #
    doc.addObject('Drawing::FeaturePage','MiddleRightBlockDrillSheetPage')
    doc.MiddleRightBlockDrillSheetPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
    edt = doc.MiddleRightBlockDrillSheetPage.EditableTexts
    edt[0] = unicode("Robert Heller")
    edt[1] = unicode("Middle Right Block Drill Sheet (Speaker Mounting holes)")
    edt[4] = unicode("Banana Pi M64 Case (Drill Sheets)")
    edt[9] = unicode("4 / 5")
    edt[10] = unicode(".5")
    edt[13] = unicode("June 8, 2020")
    doc.MiddleRightBlockDrillSheetPage.EditableTexts = edt
    middleRightBlock = doc.M64Case_middle_rightblock
    middleRBBounds = middleRightBlock.Shape.BoundBox
    doc.addObject('Drawing::FeatureViewPart','MiddleRightBlockView')
    doc.MiddleRightBlockView.Source = middleRightBlock
    doc.MiddleRightBlockView.X = -125 
    doc.MiddleRightBlockView.Y = 50.8
    doc.MiddleRightBlockView.Rotation = 0
    doc.MiddleRightBlockView.Direction = (0.0,0.0,1.0)
    doc.MiddleRightBlockView.Scale = .5
    doc.MiddleRightBlockDrillSheetPage.addObject(doc.MiddleRightBlockView)
    #############
    ##
    ## Keyboard HingeBlock
    ##
    doc.addObject('Drawing::FeaturePage','KeyboardHingeBlockBlockDrillSheetPage')
    doc.KeyboardHingeBlockBlockDrillSheetPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/Letter_Portrait_ISO7200.svg"
    edt = doc.KeyboardHingeBlockBlockDrillSheetPage.EditableTexts
    edt[0] = unicode("Robert Heller")
    edt[1] = unicode("Keyboard Hinge Block Drill Sheet (hinge holes)")
    edt[4] = unicode("Banana Pi M64 Case (Drill Sheets)")
    edt[9] = unicode("5 / 5")
    edt[10] = unicode(".375")
    edt[13] = unicode("June 8, 2020")
    doc.KeyboardHingeBlockBlockDrillSheetPage.EditableTexts = edt
    keyboardshelfHingeblock = doc.M64Case_keyboardshelf_hingeblock
    keyboardshelfHBounds = keyboardshelfHingeblock.Shape.BoundBox
    doc.addObject('Drawing::FeatureViewPart','KeyboardShelfHingeBlockView')
    doc.KeyboardShelfHingeBlockView.Source = keyboardshelfHingeblock
    doc.KeyboardShelfHingeBlockView.X = 25.4
    doc.KeyboardShelfHingeBlockView.Y = 50.8
    doc.KeyboardShelfHingeBlockView.Rotation = 0
    doc.KeyboardShelfHingeBlockView.Direction = (0.0,1.0,0.0)
    doc.KeyboardShelfHingeBlockView.Scale = .375
    doc.KeyboardHingeBlockBlockDrillSheetPage.addObject(doc.KeyboardShelfHingeBlockView)
    ####
    doc.recompute()
    PageFile = open(App.activeDocument().TopBackBlockDrillSheetPage.PageResult,'r')
    OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_topBackBlockDrillSheet.svg','w')
    OutFile.write(PageFile.read())
    del OutFile,PageFile
    PageFile = open(App.activeDocument().MiddleBackBlockDrillSheetPage.PageResult,'r')
    OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_middleBackBlockDrillSheet.svg','w')
    OutFile.write(PageFile.read())
    del OutFile,PageFile
    PageFile = open(App.activeDocument().MiddleLeftBlockDrillSheetPage.PageResult,'r')
    OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_middleLeftBlockDrillSheet.svg','w')
    OutFile.write(PageFile.read())
    del OutFile,PageFile
    PageFile = open(App.activeDocument().MiddleRightBlockDrillSheetPage.PageResult,'r')
    OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_middleRightBlockDrillSheet.svg','w')
    OutFile.write(PageFile.read())
    del OutFile,PageFile
    PageFile = open(App.activeDocument().KeyboardHingeBlockBlockDrillSheetPage.PageResult,'r')
    OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_keyboardHingeBlockBlockDrillSheetPage.svg','w')
    OutFile.write(PageFile.read())
    del OutFile,PageFile
    sys.exit(1)
    
