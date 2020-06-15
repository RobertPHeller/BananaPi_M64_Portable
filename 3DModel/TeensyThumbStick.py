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
#  Created       : Thu Jun 4 19:26:24 2020
#  Last Modified : <200614.2319>
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


import Part, TechDraw, Spreadsheet, TechDrawGui
import FreeCADGui
from FreeCAD import Console
from FreeCAD import Base
import FreeCAD as App

import os
import sys
sys.path.append(os.path.dirname(__file__))

import datetime



class TeensyThumbStick_(object):
    _Width = 68.62
    _Height = 65.35
    _BoardThick = 1.6
    _ThumbHeight = 18.45-1.6
    _ThumbX = 55.28
    _ThumbY = 45.48
    _ThumbDia = 14.22
    _TeensyHeight = 17-1.6
    _TeensyLength = 35.57
    _TeensyWidth = 17.77
    _TeensyX = 0
    _TeensyY = 65.35-(8.63+17.77)
    _MHWidth = 61.49
    _MHHeight = 60.86
    _MHDia = .125*25.4
    _CutoutX = 0
    _CutoutY = 6.35
    _CutoutH = 65.35 - (6.35*2)
    _CoverThick = .0625*25.4
    _CoverCutoutX = 0
    _CoverCutoutY = 30.5
    _CoverCutoutWidth = 68.62
    _CoverCutoutHeight = 34.39-6.35
    _CoverButtonHoleY = 19.62
    _CoverButtonHole1X = 48.59
    _CoverButtonHole2X = 56.28
    _CoverButtonHole3X = 63.94
    _CoverButtonHoleDia = 5.08
    def __init__(self):
        raise RuntimeError("No Instances allowed for TeensyThumbStick_!")
    
class TeensyThumbStick(TeensyThumbStick_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        bthick = Base.Vector(0,0,self._BoardThick)
        self.board = Part.makePlane(self._Width,
                                    self._Height,
                                    origin).extrude(bthick)
        self.mh = dict()
        mh1X = (self._Width - self._MHWidth)/2.0
        mh1Y = (self._Height - self._MHHeight) / 2.0
        self.mh[1] = origin.add(Base.Vector(mh1X,mh1Y,0))
        mh2X = mh1X + self._MHWidth
        mh2Y = mh1Y
        self.mh[2] = origin.add(Base.Vector(mh2X,mh2Y,0))
        mh3X = mh2X
        mh3Y = mh2Y + self._MHHeight
        self.mh[3] = origin.add(Base.Vector(mh3X,mh3Y,0))
        mh4X = mh1X
        mh4Y = mh3Y
        self.mh[4] = origin.add(Base.Vector(mh4X,mh4Y,0))
        mhrad = self._MHDia / 2.0
        for i in [1,2,3,4]:
            mhole = Part.Face(Part.Wire(Part.makeCircle(mhrad,self.mh[i]))).extrude(bthick)
            self.board = self.board.cut(mhole)
        thumbstickorig = origin.add(Base.Vector(self._ThumbX,
                                                self._ThumbY,
                                                self._BoardThick))
        thumbstickrad = self._ThumbDia / 2.0
        self.thumbstick = Part.Face(Part.Wire(Part.makeCircle(thumbstickrad,
                                                              thumbstickorig))
                                   ).extrude(Base.Vector(0,0,self._ThumbHeight))
        teensyorig = origin.add(Base.Vector(self._TeensyX,
                                            self._TeensyY,
                                            self._BoardThick))
        self.teensy = Part.makePlane(self._TeensyLength,
                                     self._TeensyWidth,
                                     teensyorig).extrude(Base.Vector(0,0,self._TeensyHeight))
        self.cutoutorigin = origin.add(Base.Vector(self._CutoutX,self._CutoutY,0))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_board")
        obj.Shape = self.board
        obj.Label=self.name+"_board"
        obj.ViewObject.ShapeColor=tuple([210/255.0,180/255.0,140/255.0])
        obj = doc.addObject("Part::Feature",self.name+"_thumbstick")
        obj.Shape = self.thumbstick
        obj.Label=self.name+"_thumbstick"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_teensy")
        obj.Shape = self.teensy
        obj.Label=self.name+"_teensy"
        obj.ViewObject.ShapeColor=tuple([0.0,192/255.0,0.0])
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        thick = Base.Vector(0,0,panelThick)
        mrad = self._MHDia/2.0
        return Part.Face(Part.Wire(Part.makeCircle(mrad,mh))).extrude(thick)
    def Standoff(self,i,zBase,height,diameter):
        soff = self.mh[i] 
        soff = Base.Vector(soff.x,soff.y,zBase)
        stall = Base.Vector(0,0,height)
        srad = diameter/2.0
        return Part.Face(Part.Wire(Part.makeCircle(srad,soff))).extrude(stall)
    def Cutout(self,zBase,panelThick):
        cutouto = self.cutoutorigin
        cutouto = Base.Vector(cutouto.x,cutouto.y,zBase)
        thick = Base.Vector(0,0,panelThick)
        return Part.makePlane(self._Width,
                              self._CutoutH,
                              cutouto).extrude(thick)
            

class TeensyThumbStickCover(TeensyThumbStick_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.corner = origin.add(Base.Vector(-6.35,0,0))
        coverthick = Base.Vector(0,0,self._CoverThick)
        self.coverpanel = Part.makePlane(self._Width + 12.7,
                                         self._Height,
                                         self.corner).extrude(coverthick)
        self.mh = dict()
        mh1X = (self._Width - self._MHWidth)/2.0
        mh1Y = (self._Height - self._MHHeight) / 2.0
        self.mh[1] = origin.add(Base.Vector(mh1X,mh1Y,0))
        mh2X = mh1X + self._MHWidth
        mh2Y = mh1Y
        self.mh[2] = origin.add(Base.Vector(mh2X,mh2Y,0))
        mh3X = mh2X
        mh3Y = mh2Y + self._MHHeight
        self.mh[3] = origin.add(Base.Vector(mh3X,mh3Y,0))
        mh4X = mh1X
        mh4Y = mh3Y
        self.mh[4] = origin.add(Base.Vector(mh4X,mh4Y,0))
        mhrad = self._MHDia / 2.0
        for i in [1,2,3,4]:
            mhole = Part.Face(Part.Wire(Part.makeCircle(mhrad,self.mh[i]))).extrude(coverthick)
            self.coverpanel = self.coverpanel.cut(mhole)
        self.cutoutorigin = origin.add(Base.Vector(self._CoverCutoutX,
                                                   self._CoverCutoutY,
                                                   0))
        cutout = Part.makePlane(self._CoverCutoutWidth,
                                self._CoverCutoutHeight,
                                self.cutoutorigin).extrude(coverthick)
        self.coverpanel = self.coverpanel.cut(cutout)
        bholerad = self._CoverButtonHoleDia / 2.0
        bholeorig = origin.add(Base.Vector(self._CoverButtonHole1X,
                                           self._CoverButtonHoleY,0))
        bhole = Part.Face(Part.Wire(Part.makeCircle(bholerad,
                                                    bholeorig))
                         ).extrude(coverthick)
        self.coverpanel = self.coverpanel.cut(bhole)
        bholeorig = origin.add(Base.Vector(self._CoverButtonHole2X,
                                           self._CoverButtonHoleY,0))
        bhole = Part.Face(Part.Wire(Part.makeCircle(bholerad,
                                                    bholeorig))
                         ).extrude(coverthick)
        self.coverpanel = self.coverpanel.cut(bhole)
        bholeorig = origin.add(Base.Vector(self._CoverButtonHole3X,
                                           self._CoverButtonHoleY,0))
        bhole = Part.Face(Part.Wire(Part.makeCircle(bholerad,
                                                    bholeorig))
                         ).extrude(coverthick)
        self.coverpanel = self.coverpanel.cut(bhole)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.coverpanel
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj.ViewObject.Transparency=20
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        thick = Base.Vector(0,0,panelThick)
        mrad = self._MHDia/2.0
        return Part.Face(Part.Wire(Part.makeCircle(mrad,mh))).extrude(thick)
    def Cutout(self,zBase,panelThick):
        cutouto = self.cutoutorigin
        cutouto = Base.Vector(cutouto.x,cutouto.y,zBase)
        thick = Base.Vector(0,0,panelThick)
        return Part.makePlane(self._CoverCutoutWidth,
                              self._CoverCutoutHeight,
                              cutouto).extrude(thick)

if __name__ == '__main__':
    if "TeensyThumbStickCoverTechDrawing" in App.listDocuments().keys():
        App.closeDocument("TeensyThumbStickCoverTechDrawing")
    App.ActiveDocument=App.newDocument("TeensyThumbStickCoverTechDrawing")
    doc = App.activeDocument()
    orig = Base.Vector(0,0,0)
    thick = .125*25.4
    thickness = Base.Vector(0,0,thick)
    teensyThumbStickDrop = .25*25.4
    panel = Part.makePlane(150,150,orig).extrude(thickness)
    teensythumborig = orig.add(Base.Vector(25,
                                    25,
                                    -(teensyThumbStickDrop+TeensyThumbStick_._BoardThick)))
    teensythumbstick = TeensyThumbStick("teensythumbstick",teensythumborig)
    panel = panel.cut(teensythumbstick.MountingHole(1,0,thick))
    panel = panel.cut(teensythumbstick.MountingHole(2,0,thick))
    panel = panel.cut(teensythumbstick.MountingHole(3,0,thick))
    panel = panel.cut(teensythumbstick.MountingHole(4,0,thick))
    standoff1 = teensythumbstick.Standoff(1,0,-teensyThumbStickDrop,.25*25.4)
    standoff2 = teensythumbstick.Standoff(2,0,-teensyThumbStickDrop,.25*25.4)
    standoff3 = teensythumbstick.Standoff(3,0,-teensyThumbStickDrop,.25*25.4)
    standoff4 = teensythumbstick.Standoff(4,0,-teensyThumbStickDrop,.25*25.4)
    teensythumbstickcoverorig = orig.add(Base.Vector(25,25,thick))
    teensythumbstickcover = TeensyThumbStickCover("teensythumbstickcover",teensythumbstickcoverorig)
    panel = panel.cut(teensythumbstick.Cutout(0,thick))
    doc = App.activeDocument()
    obj = doc.addObject("Part::Feature","panel")
    obj.Shape = panel
    obj.Label="panel"
    obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
    obj = doc.addObject("Part::Feature","standoff1")
    obj.Shape = standoff1
    obj.Label="standoff1"
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
    obj = doc.addObject("Part::Feature","standoff2")
    obj.Shape = standoff2
    obj.Label="standoff2"
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
    obj = doc.addObject("Part::Feature","standoff3")
    obj.Shape = standoff3
    obj.Label="standoff3"
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
    obj = doc.addObject("Part::Feature","standoff4")
    obj.Shape = standoff4
    obj.Label="standoff4"
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
    teensythumbstick.show()
    teensythumbstickcover.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewIsometric()
    coverbounds = teensythumbstickcover.coverpanel.BoundBox
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = doc.USLetterTemplate.EditableTexts
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    doc.addObject('TechDraw::DrawPage','TeensyThumbStickCoverPage')
    doc.TeensyThumbStickCoverPage.Template = doc.USLetterTemplate
    edt = doc.TeensyThumbStickCoverPage.Template.EditableTexts
    edt['CompanyName'] = "Deepwoods Software"
    edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA'    
    edt['DrawingTitle1']= 'Teensy Cover Panel'
    edt['DrawingTitle3']= ""
    edt['DrawnBy'] = "Robert Heller"
    edt['CheckedBy'] = ""
    edt['Approved1'] = ""
    edt['Approved2'] = ""
    edt['Code'] = ""
    edt['Weight'] = ''
    edt['DrawingNumber'] = datetime.datetime.now().ctime()
    edt['Revision'] = "A"
    edt['DrawingTitle2']= ""
    edt['Scale'] = '1:1'
    edt['Sheet'] = "Sheet 1 of 1"
    doc.TeensyThumbStickCoverPage.Template.EditableTexts = edt
    doc.TeensyThumbStickCoverPage.ViewObject.show()
    sheet = doc.addObject('Spreadsheet::Sheet','DimensionTable')
    sheet.set("A1",'%-11.11s'%"Dim")
    sheet.set("B1",'%10.10s'%"inch")
    sheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','TopView')
    doc.TeensyThumbStickCoverPage.addView(doc.TopView)
    doc.TopView.Source = doc.teensythumbstickcover
    doc.TopView.X = 75
    doc.TopView.Y = 155
    doc.TopView.Direction=(0.0,0.0,1.0)
    
    doc.addObject('TechDraw::DrawViewDimension','Height')
    doc.Height.Type = 'DistanceY'
    doc.Height.References2D=[(doc.TopView,'Vertex0'),\
                             (doc.TopView,'Vertex3')]
    doc.Height.FormatSpec='h'
    doc.Height.Arbitrary = True
    doc.Height.X = -50
    doc.Height.Y = 0
    doc.TeensyThumbStickCoverPage.addView(doc.Height)
    sheet.set("A%d"%ir,'%-11.11s'%"h")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._Height/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._Height)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Width')
    doc.Width.Type = 'DistanceX'
    doc.Width.References2D=[(doc.TopView,'Vertex0'),\
                            (doc.TopView,'Vertex3')]
    doc.Width.FormatSpec='w'
    doc.Width.Arbitrary = True
    doc.Width.X = 0
    doc.Width.Y = -50
    doc.TeensyThumbStickCoverPage.addView(doc.Width)
    sheet.set("A%d"%ir,'%-11.11s'%"w")
    sheet.set("B%d"%ir,'%10.6f'%((TeensyThumbStickCover._Width+12.7)/25.4))
    sheet.set("C%d"%ir,'%10.6f'%(TeensyThumbStickCover._Width+12.7))
    ir += 1

    doc.addObject('TechDraw::DrawViewDimension','CutoutHeight')
    doc.CutoutHeight.Type = 'DistanceY'
    doc.CutoutHeight.References2D=[(doc.TopView,'Vertex19'),\
                             (doc.TopView,'Vertex22')]
    doc.CutoutHeight.FormatSpec='H'
    doc.CutoutHeight.Arbitrary = True
    doc.CutoutHeight.X = 17
    doc.CutoutHeight.Y = 11
    doc.TeensyThumbStickCoverPage.addView(doc.CutoutHeight)
    sheet.set("A%d"%ir,'%-11.11s'%"H")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._CoverCutoutHeight/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._CoverCutoutHeight)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CutoutWidth')
    doc.CutoutWidth.Type = 'DistanceX'
    doc.CutoutWidth.References2D=[(doc.TopView,'Vertex19'),\
                            (doc.TopView,'Vertex22')]
    doc.CutoutWidth.FormatSpec='W'
    doc.CutoutWidth.Arbitrary = True
    doc.CutoutWidth.X = 0
    doc.CutoutWidth.Y = 8
    doc.TeensyThumbStickCoverPage.addView(doc.CutoutWidth)
    sheet.set("A%d"%ir,'%-11.11s'%"W")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._CoverCutoutWidth/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._CoverCutoutWidth)
    ir += 1


    doc.addObject('TechDraw::DrawViewDimension','CutoutY')
    doc.CutoutY.Type = 'DistanceY'
    doc.CutoutY.References2D=[(doc.TopView,'Vertex19'),\
                             (doc.TopView,'Vertex0')]
    doc.CutoutY.FormatSpec='Y'
    doc.CutoutY.Arbitrary = True
    doc.CutoutY.X = -18
    doc.CutoutY.Y = -20
    doc.TeensyThumbStickCoverPage.addView(doc.CutoutY)
    sheet.set("A%d"%ir,'%-11.11s'%"Y")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._CoverCutoutY/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._CoverCutoutY)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CutoutX')
    doc.CutoutX.Type = 'DistanceX'
    doc.CutoutX.References2D=[(doc.TopView,'Vertex19'),\
                            (doc.TopView,'Vertex0')]
    doc.CutoutX.FormatSpec='X'
    doc.CutoutX.Arbitrary = True
    doc.CutoutX.X = -32
    doc.CutoutX.Y = -9
    doc.TeensyThumbStickCoverPage.addView(doc.CutoutX)
    sheet.set("A%d"%ir,'%-11.11s'%"X")
    sheet.set("B%d"%ir,'%10.6f'%((TeensyThumbStickCover._CoverCutoutX+6.35)/25.4))
    sheet.set("C%d"%ir,'%10.6f'%(TeensyThumbStickCover._CoverCutoutX+6.35))
    ir += 1

    doc.addObject('TechDraw::DrawViewDimension','MHole')
    doc.MHole.Type = 'Diameter'
    doc.MHole.References2D=[(doc.TopView,'Edge13')]
    doc.MHole.FormatSpec='MDia (4x)'
    doc.MHole.Arbitrary = True
    doc.MHole.X = 55
    doc.MHole.Y = 20
    doc.TeensyThumbStickCoverPage.addView(doc.MHole)
    sheet.set("A%d"%ir,'%-11.11s'%"MDia")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._MHDia/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._MHDia)
    ir += 1
    
    cwidth = TeensyThumbStickCover._Width+12.7
    mhxoff = (cwidth-TeensyThumbStickCover._MHWidth)/2
    mhyoff = (TeensyThumbStickCover._Height-TeensyThumbStickCover._MHHeight)/2.0
    
    doc.addObject('TechDraw::DrawViewDimension','MHYOff')
    doc.MHYOff.Type = 'DistanceY'
    doc.MHYOff.References2D=[(doc.TopView,'Vertex18'),\
                             (doc.TopView,'Vertex0')]
    doc.MHYOff.FormatSpec='y'
    doc.MHYOff.Arbitrary = True
    doc.MHYOff.X = -22.5
    doc.MHYOff.Y = -38
    doc.TeensyThumbStickCoverPage.addView(doc.MHYOff)
    sheet.set("A%d"%ir,'%-11.11s'%"y")
    sheet.set("B%d"%ir,'%10.6f'%(mhyoff/25.4))
    sheet.set("C%d"%ir,'%10.6f'%mhyoff)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MHXOff')
    doc.MHXOff.Type = 'DistanceX'
    doc.MHXOff.References2D=[(doc.TopView,'Vertex18'),\
                            (doc.TopView,'Vertex0')]
    doc.MHXOff.FormatSpec='x'
    doc.MHXOff.Arbitrary = True
    doc.MHXOff.X = -36
    doc.MHXOff.Y = -37
    doc.TeensyThumbStickCoverPage.addView(doc.MHXOff)
    sheet.set("A%d"%ir,'%-11.11s'%"x")
    sheet.set("B%d"%ir,'%10.6f'%(mhxoff/25.4))
    sheet.set("C%d"%ir,'%10.6f'%mhxoff)
    ir += 1

    doc.addObject('TechDraw::DrawViewDimension','MHHeight')
    doc.MHHeight.Type = 'DistanceY'
    doc.MHHeight.References2D=[(doc.TopView,'Vertex18'),\
                             (doc.TopView,'Vertex25')]
    doc.MHHeight.FormatSpec='mh'
    doc.MHHeight.Arbitrary = True
    doc.MHHeight.X = -10
    doc.MHHeight.Y =  14.5
    doc.TeensyThumbStickCoverPage.addView(doc.MHHeight)
    sheet.set("A%d"%ir,'%-11.11s'%"mh")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._MHHeight/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._MHHeight)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MHWidth')
    doc.MHWidth.Type = 'DistanceX'
    doc.MHWidth.References2D=[(doc.TopView,'Vertex18'),\
                            (doc.TopView,'Vertex25')]
    doc.MHWidth.FormatSpec='mw'
    doc.MHWidth.Arbitrary = True
    doc.MHWidth.X = -24
    doc.MHWidth.Y = -19
    doc.TeensyThumbStickCoverPage.addView(doc.MHWidth)
    sheet.set("A%d"%ir,'%-11.11s'%"mw")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._MHWidth/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._MHWidth)
    ir += 1

    # Edge6    (right [dia])
    doc.addObject('TechDraw::DrawViewDimension','ButtonHoleDia')
    doc.ButtonHoleDia.Type = 'Diameter'
    doc.ButtonHoleDia.References2D=[(doc.TopView,'Edge6')]
    doc.ButtonHoleDia.FormatSpec='BDia (3x)'
    doc.ButtonHoleDia.Arbitrary = True
    doc.ButtonHoleDia.X = 55
    doc.ButtonHoleDia.Y =  0
    doc.TeensyThumbStickCoverPage.addView(doc.ButtonHoleDia)
    sheet.set("A%d"%ir,'%-11.11s'%"BDia")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStickCover._CoverButtonHoleDia/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStickCover._CoverButtonHoleDia)
    ir += 1
    
    # Vertex9  (left)
    doc.addObject('TechDraw::DrawViewDimension','BHYOff')
    doc.BHYOff.Type = 'DistanceY'
    doc.BHYOff.References2D=[(doc.TopView,'Vertex9'),\
                             (doc.TopView,'Vertex0')]
    doc.BHYOff.FormatSpec='bhy'
    doc.BHYOff.Arbitrary = True
    doc.BHYOff.X =   6
    doc.BHYOff.Y = -24
    doc.TeensyThumbStickCoverPage.addView(doc.BHYOff)
    sheet.set("A%d"%ir,'%-11.11s'%"bhy")
    sheet.set("B%d"%ir,'%10.6f'%(TeensyThumbStick_._CoverButtonHoleY/25.4))
    sheet.set("C%d"%ir,'%10.6f'%TeensyThumbStick_._CoverButtonHoleY)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BH1XOff')
    doc.BH1XOff.Type = 'DistanceX'
    doc.BH1XOff.References2D=[(doc.TopView,'Vertex9'),\
                            (doc.TopView,'Vertex0')]
    doc.BH1XOff.FormatSpec='bhx'
    doc.BH1XOff.Arbitrary = True
    doc.BH1XOff.X = -23
    doc.BH1XOff.Y = -12
    doc.TeensyThumbStickCoverPage.addView(doc.BH1XOff)
    sheet.set("A%d"%ir,'%-11.11s'%"bhx")
    sheet.set("B%d"%ir,'%10.6f'%((TeensyThumbStick_._CoverButtonHole1X+6.35)/25.4))
    sheet.set("C%d"%ir,'%10.6f'%(TeensyThumbStick_._CoverButtonHole1X+6.35))
    ir += 1

    # Vertex15 (middle)
    bhdx = TeensyThumbStick_._CoverButtonHole2X - \
           TeensyThumbStick_._CoverButtonHole1X
    doc.addObject('TechDraw::DrawViewDimension','BH12DX')
    doc.BH12DX.Type = 'DistanceX'
    doc.BH12DX.References2D=[(doc.TopView,'Vertex9'),\
                            (doc.TopView,'Vertex15')]
    doc.BH12DX.FormatSpec='bhdx1'
    doc.BH12DX.Arbitrary = True
    doc.BH12DX.X =  19
    doc.BH12DX.Y =  -5
    doc.TeensyThumbStickCoverPage.addView(doc.BH12DX)
    sheet.set("A%d"%ir,'%-11.11s'%"bhdx1")
    sheet.set("B%d"%ir,'%10.6f'%(bhdx/25.4))
    sheet.set("C%d"%ir,'%10.6f'%bhdx)
    ir += 1

    # Vertex12 (right)
    bhdx = TeensyThumbStick_._CoverButtonHole3X - \
           TeensyThumbStick_._CoverButtonHole2X
    doc.addObject('TechDraw::DrawViewDimension','BH23DX')
    doc.BH23DX.Type = 'DistanceX'
    doc.BH23DX.References2D=[(doc.TopView,'Vertex15'),\
                            (doc.TopView,'Vertex12')]
    doc.BH23DX.FormatSpec='bhdx2'
    doc.BH23DX.Arbitrary = True
    doc.BH23DX.X =  48.5
    doc.BH23DX.Y = -15.4
    doc.TeensyThumbStickCoverPage.addView(doc.BH23DX)
    sheet.set("A%d"%ir,'%-11.11s'%"bhdx2")
    sheet.set("B%d"%ir,'%10.6f'%(bhdx/25.4))
    sheet.set("C%d"%ir,'%10.6f'%bhdx)
    ir += 1


    doc.addObject('TechDraw::DrawViewPart','ISOView')
    doc.TeensyThumbStickCoverPage.addView(doc.ISOView)
    doc.ISOView.Source = doc.teensythumbstickcover
    doc.ISOView.X = 60
    doc.ISOView.Y = 73
    doc.ISOView.Scale = .5
    doc.ISOView.Direction=(1.0,-1.0,1.0)
    

    sheet.recompute()
    doc.addObject('TechDraw::DrawViewSpreadsheet','DimBlock')
    doc.DimBlock.Source = sheet
    doc.DimBlock.TextSize = 8
    doc.DimBlock.CellEnd = "C%d"%(ir-1)
    doc.TeensyThumbStickCoverPage.addView(doc.DimBlock)
    doc.DimBlock.recompute()
    doc.DimBlock.X = 200
    doc.DimBlock.Y = 150
    
    doc.TeensyThumbStickCoverPage.recompute()
    doc.recompute()
    
    
    TechDrawGui.exportPageAsPdf(doc.TeensyThumbStickCoverPage,"BananaPiM64Model_TeensyThumbStickCover.pdf")
    sys.exit(1)
