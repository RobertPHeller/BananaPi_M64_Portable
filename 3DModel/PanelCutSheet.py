#!/usr/local/bin/FreeCAD018
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
#  Last Modified : <200619.1912>
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
from Battery import *
if __name__ == '__main__':
    doc = None
    for docname in App.listDocuments():
        lddoc = App.getDocument(docname)
        if lddoc.Label == 'BananaPiM64Model':
            doc = lddoc
            break
    if doc == None:
        App.open("/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model.fcstd")
        doc = App.getDocument('BananaPiM64Model')
    App.ActiveDocument=doc
    doc = App.activeDocument()
    # Clean out old garbage, if any
    for g in doc.findObjects('TechDraw::DrawSVGTemplate'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('TechDraw::DrawPage'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('TechDraw::DrawViewPart'):
        doc.removeObject(g.Name)
    # insert a Page object and assign a template
    doc.addObject('TechDraw::DrawSVGTemplate','LargeCutPanelTemplate')
    doc.LargeCutPanelTemplate.Template = "largecutpanel.svg"
    doc.addObject('TechDraw::DrawPage','LargeCutPanelPage')
    doc.LargeCutPanelPage.Template = doc.LargeCutPanelTemplate
    doc.LargeCutPanelPage.ViewObject.show()
    panelWidth = PortableM64CaseCommon._Width - \
                (PortableM64CaseCommon._WallThickness*2)
    panelHeight = PortableM64CaseCommon._Height - \
                (PortableM64CaseCommon._WallThickness*2)
    panel_centerX = panelHeight/2.0
    panel_centerY = panelWidth/2.0
    # Bottom section
    bottomPanel = doc.M64Case_bottom_panel
    doc.addObject('TechDraw::DrawViewPart','Bottom_Panel')
    doc.LargeCutPanelPage.addView(doc.Bottom_Panel)
    doc.Bottom_Panel.Source = bottomPanel
    doc.Bottom_Panel.X = 6.35+panel_centerX
    doc.Bottom_Panel.Y = 6.35+panel_centerY
    doc.Bottom_Panel.Rotation = 90.0
    doc.Bottom_Panel.Direction = (0.0,0.0,1.0)
    bottomLeft = doc.M64Case_bottom_left
    doc.addObject('TechDraw::DrawViewPart','Bottom_Left')
    doc.LargeCutPanelPage.addView(doc.Bottom_Left)
    doc.Bottom_Left.Source = bottomLeft
    
    doc.Bottom_Left.X = 6.35+PortableM64CaseCommon._Height+\
                        (PortableM64CaseCommon._BottomDepth/2.0)+\
                         6.35
    doc.Bottom_Left.Y = 6.35+panel_centerX
    doc.Bottom_Left.Rotation = 90.0
    doc.Bottom_Left.Direction = (1.0,0.0,0.0)
    bottomRight = doc.M64Case_bottom_right
    doc.addObject('TechDraw::DrawViewPart','Bottom_Right')
    doc.LargeCutPanelPage.addView(doc.Bottom_Right)
    doc.Bottom_Right.Source = bottomRight
    doc.Bottom_Right.X = 6.35+PortableM64CaseCommon._Height+\
                         6.35+PortableM64CaseCommon._BottomDepth+\
                         (PortableM64CaseCommon._BottomDepth/2.0)+\
                         6.35
    doc.Bottom_Right.Y = 6.35+panel_centerX
    doc.Bottom_Right.Rotation = 270.0
    doc.Bottom_Right.Direction = (-1.0,0.0,0.0)
    bottomFront = doc.M64Case_bottom_front
    doc.addObject('TechDraw::DrawViewPart','Bottom_Front')
    doc.LargeCutPanelPage.addView(doc.Bottom_Front)
    doc.Bottom_Front.Source = bottomFront
    doc.Bottom_Front.X = 6.35+PortableM64CaseCommon._Height+\
                         (2*(6.35+PortableM64CaseCommon._BottomDepth))+\
                         (PortableM64CaseCommon._BottomDepth/2.0)+\
                         6.35
    doc.Bottom_Front.Y = 6.35+panel_centerY+\
                         PortableM64CaseCommon._WallThickness
    doc.Bottom_Front.Rotation = 90.0
    doc.Bottom_Front.Direction = (0.0,1.0,0.0)
    bottomBack = doc.M64Case_bottom_back
    doc.addObject('TechDraw::DrawViewPart','Bottom_Back')
    doc.LargeCutPanelPage.addView(doc.Bottom_Back)
    doc.Bottom_Back.Source = bottomBack
    doc.Bottom_Back.X = 6.35+PortableM64CaseCommon._Height+\
                         (3*(6.35+PortableM64CaseCommon._BottomDepth))+\
                         (PortableM64CaseCommon._BottomDepth/2.0)+\
                         6.35+\
                         PortableM64CaseCommon._WallThickness
    doc.Bottom_Back.Y = 6.35+panel_centerY
    doc.Bottom_Back.Rotation = 90.0
    doc.Bottom_Back.Direction = (0.0,1.0,0.0)
    # MiddleSection
    middlePanel = doc.M64Case_middle_panel
    doc.addObject('TechDraw::DrawViewPart','Middle_Panel')
    doc.LargeCutPanelPage.addView(doc.Middle_Panel)
    doc.Middle_Panel.Source = middlePanel
    doc.Middle_Panel.X = 6.35+panel_centerX
    doc.Middle_Panel.Y = 6.35+panelWidth+\
                         6.35+panel_centerY+\
                         (2*PortableM64CaseCommon._WallThickness)
    doc.Middle_Panel.Rotation = 90.0
    doc.Middle_Panel.Direction = (0.0,0.0,1.0)
    middleLeft = doc.M64Case_middle_left
    doc.addObject('TechDraw::DrawViewPart','Middle_Left')
    doc.LargeCutPanelPage.addView(doc.Middle_Left)
    doc.Middle_Left.Source = middleLeft
    doc.Middle_Left.X = 6.35+PortableM64CaseCommon._Height+\
                         (PortableM64CaseCommon._MiddleTotalDepth/2.0)+\
                         6.35
    doc.Middle_Left.Y = 6.35+panelWidth+\
                        6.35+panel_centerX+\
                         (2*PortableM64CaseCommon._WallThickness)
    doc.Middle_Left.Rotation = 90.0
    doc.Middle_Left.Direction = (1.0,0.0,0.0)
    middleRight = doc.M64Case_middle_right
    doc.addObject('TechDraw::DrawViewPart','Middle_Right')
    doc.LargeCutPanelPage.addView(doc.Middle_Right)
    doc.Middle_Right.Source = middleRight
    doc.Middle_Right.X = 6.35+PortableM64CaseCommon._Height+\
                         (PortableM64CaseCommon._MiddleTotalDepth/2.0)+\
                         6.35+\
                         PortableM64CaseCommon._MiddleTotalDepth+6.35
    doc.Middle_Right.Y = 6.35+panelWidth+\
                         6.35+panel_centerX+\
                         (2*PortableM64CaseCommon._WallThickness)
    doc.Middle_Right.Rotation = 90.0
    doc.Middle_Right.Direction = (1.0,0.0,0.0)
    middleFront = doc.M64Case_middle_front
    doc.addObject('TechDraw::DrawViewPart','Middle_Front')
    doc.LargeCutPanelPage.addView(doc.Middle_Front)
    doc.Middle_Front.Source = middleFront
    doc.Middle_Front.X = 6.35+PortableM64CaseCommon._Height+\
                         (PortableM64CaseCommon._MiddleTotalDepth/2.0)+\
                         6.35+\
                         ((PortableM64CaseCommon._MiddleTotalDepth+6.35)*2)
    doc.Middle_Front.Y = 6.35+panelWidth+\
                         6.35+panel_centerY+\
                         (3*PortableM64CaseCommon._WallThickness)
    doc.Middle_Front.Rotation = 90.0
    doc.Middle_Front.Direction = (0.0,1.0,0.0)
    middleBack = doc.M64Case_middle_back
    doc.addObject('TechDraw::DrawViewPart','Middle_Back')
    doc.LargeCutPanelPage.addView(doc.Middle_Back)
    doc.Middle_Back.Source = middleBack
    doc.Middle_Back.X = 6.35+PortableM64CaseCommon._Height+\
                         (PortableM64CaseCommon._MiddleTotalDepth/2.0)+\
                         6.35+\
                         ((PortableM64CaseCommon._MiddleTotalDepth+6.35)*3)
    doc.Middle_Back.Y = 6.35+panelWidth+\
                         6.35+panel_centerY+\
                         (3*PortableM64CaseCommon._WallThickness)
    doc.Middle_Back.Rotation = 90.0
    doc.Middle_Back.Direction = (0.0,1.0,0.0)
    # TopSection
    topPanel = doc.M64Case_top_panel
    doc.addObject('TechDraw::DrawViewPart','Top_Panel')
    doc.LargeCutPanelPage.addView(doc.Top_Panel)
    doc.Top_Panel.Source = topPanel
    doc.Top_Panel.X = 6.35+panel_centerX
    doc.Top_Panel.Y = ((6.35+panelWidth)*2)+\
                         6.35+panel_centerY+\
                         (4*PortableM64CaseCommon._WallThickness)
    doc.Top_Panel.Rotation = 90.0
    doc.Top_Panel.Direction = (0.0,0.0,1.0)
    topLeft = doc.M64Case_top_left
    doc.addObject('TechDraw::DrawViewPart','Top_Left')
    doc.LargeCutPanelPage.addView(doc.Top_Left)
    doc.Top_Left.Source = topLeft
    doc.Top_Left.X = 6.35+PortableM64CaseCommon._Height+\
                     (PortableM64CaseCommon._TopDepth/2.0)+\
                     6.35
    doc.Top_Left.Y = ((6.35+panelWidth)*2)+\
                         6.35+panel_centerX+\
                         (4*PortableM64CaseCommon._WallThickness)
    doc.Top_Left.Rotation = 90.0
    doc.Top_Left.Direction = (1.0,0.0,0.0)
    topRight = doc.M64Case_top_right
    doc.addObject('TechDraw::DrawViewPart','Top_Right')
    doc.LargeCutPanelPage.addView(doc.Top_Right)
    doc.Top_Right.Source = topRight
    doc.Top_Right.X = 6.35+PortableM64CaseCommon._Height+\
                     (PortableM64CaseCommon._TopDepth/2.0)+\
                     (PortableM64CaseCommon._TopDepth+6.35)+\
                     6.35
    doc.Top_Right.Y = ((6.35+panelWidth)*2)+\
                         6.35+panel_centerX+\
                         (4*PortableM64CaseCommon._WallThickness)
    doc.Top_Right.Rotation = 90.0
    doc.Top_Right.Direction = (1.0,0.0,0.0)
    topFront = doc.M64Case_top_front
    doc.addObject('TechDraw::DrawViewPart','Top_Front')
    doc.LargeCutPanelPage.addView(doc.Top_Front)
    doc.Top_Front.Source = topFront
    doc.Top_Front.X = 6.35+PortableM64CaseCommon._Height+\
                     (PortableM64CaseCommon._TopDepth/2.0)+\
                     (2*(PortableM64CaseCommon._TopDepth+6.35))+\
                     6.35
    doc.Top_Front.Y = ((6.35+panelWidth)*2)+\
                         6.35+panel_centerY+\
                         (5*PortableM64CaseCommon._WallThickness)
    doc.Top_Front.Rotation = 90.0
    doc.Top_Front.Direction = (0.0,1.0,0.0)
    topBack = doc.M64Case_top_back
    doc.addObject('TechDraw::DrawViewPart','Top_Back')
    doc.LargeCutPanelPage.addView(doc.Top_Back)
    doc.Top_Back.Source = topBack
    doc.Top_Back.X = 6.35+PortableM64CaseCommon._Height+\
                     (PortableM64CaseCommon._TopDepth/2.0)+\
                     (3*(PortableM64CaseCommon._TopDepth+6.35))+\
                     6.35
    doc.Top_Back.Y = ((6.35+panelWidth)*2)+\
                         6.35+panel_centerY+\
                         (5*PortableM64CaseCommon._WallThickness)
    doc.Top_Back.Rotation = 90.0
    doc.Top_Back.Direction = (0.0,1.0,0.0)
    # Keyboard Shelf
    keyboardShelf = doc.M64Case_keyboardshelf_shelf
    doc.addObject('TechDraw::DrawViewPart','Keyboard_Shelf')
    doc.LargeCutPanelPage.addView(doc.Keyboard_Shelf)
    doc.Keyboard_Shelf.Source = keyboardShelf
    doc.Keyboard_Shelf.X = 6.35+PortableM64CaseCommon._Height+\
                     (PortableM64CaseCommon._ShelfLength/2.0)+\
                     (4*(PortableM64CaseCommon._TopDepth+6.35))+\
                     6.35
    doc.Keyboard_Shelf.Y = ((6.35+panelWidth)*2)+\
                         6.35+panel_centerY+\
                         (4*PortableM64CaseCommon._WallThickness)
    doc.Keyboard_Shelf.Rotation = 90.0
    doc.Keyboard_Shelf.Direction = (0.0,0.0,1.0)
    # Battery cover panel
    BatteryPanel = doc.M64Case_bottom_batterypanel
    doc.addObject('TechDraw::DrawViewPart','Battery_Panel')
    doc.LargeCutPanelPage.addView(doc.Battery_Panel)
    doc.Battery_Panel.Source = BatteryPanel
    doc.Battery_Panel.X = 6.35+PortableM64CaseCommon._Height+\
                         ((Battery._Width+(BlockX._BlockWidth*2))/2.0)+\
                         6.35+\
                         ((PortableM64CaseCommon._MiddleTotalDepth+6.35)*4)
    doc.Battery_Panel.Y = 6.35+panelWidth+\
                         6.35+panel_centerY+\
                         (2*PortableM64CaseCommon._WallThickness)
    doc.Battery_Panel.Rotation = 90.0
    doc.Battery_Panel.Direction = (0.0,0.0,1.0)
    #
    doc.recompute()
    TechDrawGui.exportPageAsSvg(doc.LargeCutPanelPage,"BananaPiM64Model_New.svg")
    sys.exit(1)
