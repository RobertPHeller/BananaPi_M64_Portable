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
#  Last Modified : <200606.1914>
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


import Part
from FreeCAD import Base
import FreeCAD as App

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
    
