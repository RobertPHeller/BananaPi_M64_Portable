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
#  Created       : Sun Jun 7 10:11:02 2020
#  Last Modified : <200607.1528>
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
    # insert a Page object and assign a template
    doc.addObject('Drawing::FeaturePage','PanelCutPage')
    doc.PanelCutPage.Template = "/home/heller/BananaPi_M64_Portable/3DModel/largecutpanel.svg"
    # Bottom section
    bottomPanel = doc.M64Case_bottom_panel
    doc.addObject('Drawing::FeatureViewPart','Bottom_Panel')
    doc.Bottom_Panel.Source = bottomPanel
    doc.Bottom_Panel.X = 6.35+PortableM64CaseCommon._Height
    doc.Bottom_Panel.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*2)
    doc.Bottom_Panel.Rotation = 90.0
    doc.Bottom_Panel.Direction = (0.0,0.0,1.0)
    doc.PanelCutPage.addObject(doc.Bottom_Panel)
    bottomLeft = doc.M64Case_bottom_left
    doc.addObject('Drawing::FeatureViewPart','Bottom_Left')
    doc.Bottom_Left.Source = bottomLeft
    doc.Bottom_Left.X = 6.35+PortableM64CaseCommon._Height+\
                         6.35#+PortableM64CaseCommon._BottomDepth
    doc.Bottom_Left.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*2)+\
                        PortableM64CaseCommon._Height
    doc.Bottom_Left.Rotation = 0.0
    doc.Bottom_Left.Direction = (1.0,0.0,0.0)
    doc.PanelCutPage.addObject(doc.Bottom_Left)
    bottomRight = doc.M64Case_bottom_right
    doc.addObject('Drawing::FeatureViewPart','Bottom_Right')
    doc.Bottom_Right.Source = bottomRight
    doc.Bottom_Right.X = 6.35+PortableM64CaseCommon._Height+\
                         6.35+PortableM64CaseCommon._BottomDepth
    doc.Bottom_Right.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*2)
    doc.Bottom_Right.Rotation = 180.0
    doc.Bottom_Right.Direction = (-1.0,0.0,0.0)
    doc.PanelCutPage.addObject(doc.Bottom_Right)
    bottomFront = doc.M64Case_bottom_front
    doc.addObject('Drawing::FeatureViewPart','Bottom_Front')
    doc.Bottom_Front.Source = bottomFront
    doc.Bottom_Front.X = 6.35+PortableM64CaseCommon._Height+\
                         (2*(6.35+PortableM64CaseCommon._BottomDepth))
    doc.Bottom_Front.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*2)
    doc.Bottom_Front.Rotation = 0.0
    doc.Bottom_Front.Direction = (0.0,1.0,0.0)
    doc.PanelCutPage.addObject(doc.Bottom_Front)
    bottomBack = doc.M64Case_bottom_back
    doc.addObject('Drawing::FeatureViewPart','Bottom_Back')
    doc.Bottom_Back.Source = bottomBack
    doc.Bottom_Back.X = 6.35+PortableM64CaseCommon._Height+\
                         (3*(6.35+PortableM64CaseCommon._BottomDepth))
    doc.Bottom_Back.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*2)
    doc.Bottom_Back.Rotation = 0.0
    doc.Bottom_Back.Direction = (0.0,1.0,0.0)
    doc.PanelCutPage.addObject(doc.Bottom_Back)
    # MiddleSection
    middlePanel = doc.M64Case_middle_panel
    doc.addObject('Drawing::FeatureViewPart','Middle_Panel')
    doc.Middle_Panel.Source = middlePanel
    doc.Middle_Panel.X = 6.35+PortableM64CaseCommon._Height
    doc.Middle_Panel.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*1)
    doc.Middle_Panel.Rotation = 90.0
    doc.Middle_Panel.Direction = (0.0,0.0,1.0)
    doc.PanelCutPage.addObject(doc.Middle_Panel)
    middleLeft = doc.M64Case_middle_left
    doc.addObject('Drawing::FeatureViewPart','Middle_Left')
    doc.Middle_Left.Source = middleLeft
    doc.Middle_Left.X = 6.35+PortableM64CaseCommon._Height+\
                         6.35-PortableM64CaseCommon._BottomDepth
    doc.Middle_Left.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*1)+\
                        PortableM64CaseCommon._Height
    doc.Middle_Left.Rotation = 0.0
    doc.Middle_Left.Direction = (1.0,0.0,0.0)
    doc.PanelCutPage.addObject(doc.Middle_Left)
    middleRight = doc.M64Case_middle_right
    doc.addObject('Drawing::FeatureViewPart','Middle_Right')
    doc.Middle_Right.Source = middleRight
    doc.Middle_Right.X = 6.35+PortableM64CaseCommon._Height+\
                         6.35+PortableM64CaseCommon._MiddleTotalDepth\
                         -PortableM64CaseCommon._BottomDepth
    doc.Middle_Right.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*1)+\
                        PortableM64CaseCommon._Height
    doc.Middle_Right.Rotation = 0.0
    doc.Middle_Right.Direction = (1.0,0.0,0.0)
    doc.PanelCutPage.addObject(doc.Middle_Right)

    middleFront = doc.M64Case_middle_front
    doc.addObject('Drawing::FeatureViewPart','Middle_Front')
    doc.Middle_Front.Source = middleFront
    doc.Middle_Front.X = 6.35+PortableM64CaseCommon._Height+\
                         (2*(6.35+PortableM64CaseCommon._MiddleTotalDepth))\
                         -PortableM64CaseCommon._BottomDepth
    doc.Middle_Front.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*1)
    doc.Middle_Front.Rotation = 0.0
    doc.Middle_Front.Direction = (0.0,1.0,0.0)
    doc.PanelCutPage.addObject(doc.Middle_Front)
    middleBack = doc.M64Case_middle_back
    doc.addObject('Drawing::FeatureViewPart','Middle_Back')
    doc.Middle_Back.Source = middleBack
    doc.Middle_Back.X = 6.35+PortableM64CaseCommon._Height+\
                         (3*(6.35+PortableM64CaseCommon._MiddleTotalDepth))\
                         -PortableM64CaseCommon._BottomDepth
    doc.Middle_Back.Y = 6.35+((PortableM64CaseCommon._Width+6.35)*1)
    doc.Middle_Back.Rotation = 0.0
    doc.Middle_Back.Direction = (0.0,1.0,0.0)
    doc.PanelCutPage.addObject(doc.Middle_Back)
    # TopSection
    topPanel = doc.M64Case_top_panel
    doc.addObject('Drawing::FeatureViewPart','Top_Panel')
    doc.Top_Panel.Source = topPanel
    doc.Top_Panel.X = 6.35+PortableM64CaseCommon._Height
    doc.Top_Panel.Y = 6.35
    doc.Top_Panel.Rotation = 90.0
    doc.Top_Panel.Direction = (0.0,0.0,1.0)
    doc.PanelCutPage.addObject(doc.Top_Panel)
    topLeft = doc.M64Case_top_left
    doc.addObject('Drawing::FeatureViewPart','Top_Left')
    doc.Top_Left.Source = topLeft
    doc.Top_Left.X = 6.35+PortableM64CaseCommon._Height+\
                         6.35-PortableM64CaseCommon._BottomDepth\
                         -PortableM64CaseCommon._MiddleTotalDepth
    doc.Top_Left.Y = 6.35+PortableM64CaseCommon._Height
    doc.Top_Left.Rotation = 0.0
    doc.Top_Left.Direction = (1.0,0.0,0.0)
    doc.PanelCutPage.addObject(doc.Top_Left)
    topRight = doc.M64Case_top_right
    doc.addObject('Drawing::FeatureViewPart','Top_Right')
    doc.Top_Right.Source = topRight
    doc.Top_Right.X = 6.35+PortableM64CaseCommon._Height+\
                         6.35+PortableM64CaseCommon._TopDepth\
                         -PortableM64CaseCommon._BottomDepth\
                         -PortableM64CaseCommon._MiddleTotalDepth
    doc.Top_Right.Y = 6.35+PortableM64CaseCommon._Height
    doc.Top_Right.Rotation = 0.0
    doc.Top_Right.Direction = (1.0,0.0,0.0)
    doc.PanelCutPage.addObject(doc.Top_Right)

    topFront = doc.M64Case_top_front
    doc.addObject('Drawing::FeatureViewPart','Top_Front')
    doc.Top_Front.Source = topFront
    doc.Top_Front.X = 6.35+PortableM64CaseCommon._Height+\
                         (2*(6.35+PortableM64CaseCommon._TopDepth))\
                         -PortableM64CaseCommon._BottomDepth\
                         -PortableM64CaseCommon._MiddleTotalDepth
    doc.Top_Front.Y = 6.35
    doc.Top_Front.Rotation = 0.0
    doc.Top_Front.Direction = (0.0,1.0,0.0)
    doc.PanelCutPage.addObject(doc.Top_Front)
    topBack = doc.M64Case_top_back
    doc.addObject('Drawing::FeatureViewPart','Top_Back')
    doc.Top_Back.Source = topBack
    doc.Top_Back.X = 6.35+PortableM64CaseCommon._Height+\
                         (3*(6.35+PortableM64CaseCommon._TopDepth))\
                         -PortableM64CaseCommon._BottomDepth\
                         -PortableM64CaseCommon._MiddleTotalDepth
    doc.Top_Back.Y = 6.35
    doc.Top_Back.Rotation = 0.0
    doc.Top_Back.Direction = (0.0,1.0,0.0)
    doc.PanelCutPage.addObject(doc.Top_Back)
    # Keyboard Shelf
    keyboardShelf = doc.M64Case_keyboardshelf_shelf
    doc.addObject('Drawing::FeatureViewPart','Keyboard_Shelf')
    doc.Keyboard_Shelf.Source = keyboardShelf
    doc.Keyboard_Shelf.X = 6.35+PortableM64CaseCommon._Height+\
                        (4*(6.35+PortableM64CaseCommon._TopDepth))+\
                        PortableM64CaseCommon._ShelfHeight+\
                        (6*(6.35+PortableM64CaseCommon._TopDepth))
    doc.Keyboard_Shelf.Y = 6.35
    doc.Keyboard_Shelf.Rotation = 90.0
    doc.Keyboard_Shelf.Direction = (0.0,0.0,1.0)
    doc.PanelCutPage.addObject(doc.Keyboard_Shelf)
    #
    doc.recompute()    
    PageFile = open(App.activeDocument().PanelCutPage.PageResult,'r')
    OutFile = open('/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model_New.svg','w')
    OutFile.write(PageFile.read())
    del OutFile,PageFile
    sys.exit(1)
