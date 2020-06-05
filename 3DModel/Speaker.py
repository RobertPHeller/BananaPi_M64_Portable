#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Thu Jun 4 19:26:36 2020
#  Last Modified : <200604.2016>
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

class Speaker_(object):
    _Width = 18.86
    _Length = 93.71
    _Thickness = 7.14
    _MHoleDia = 2.5
    _LTopHoleX = 6.43 + (2.5/2.0)
    _RTopHoleX = 10.29 + (2.5/2.0)
    _TopHoleY = 84.5 + (2.5/2.0)
    _LBottomHoleX = 8.2 + (2.5/2.0)
    _RBottomHoleX = 8.41 + (2.5/2.0)
    _BottomHoleY = 4.66 + (2.5/2.0)
    _StandoffRecessDia = 6.16
    _StandoffRecessDepth = 3.15
    def __init__(self):
        raise RuntimeError("No instances of Speaker_ allowed!")
        

class SpeakerLeft_UpsideDown(Speaker_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        totalthick = Base.Vector(0,0,-self._Thickness)
        self.body = Part.makePlane(self._Width,
                                   self._Length,
                                   origin).extrude(totalthick)
        mhTopX = self._LTopHoleX
        mhTopY = self._Length - self._TopHoleY
        self.mh = dict()
        self.mh["top"] = origin.add(Base.Vector(mhTopX,mhTopY,0))
        mhBottomX = self._LBottomHoleX
        mhBottomY = self._Length - self._BottomHoleY
        self.mh["bottom"] = origin.add(Base.Vector(mhBottomX,mhBottomY,0))
        mhrad = self._MHoleDia/2.0
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(mhrad,
                                                                      self.mh["top"]))
                                           ).extrude(totalthick))
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(mhrad,
                                                                      self.mh["bottom"]))
                                           ).extrude(totalthick))
        recessbottom = (origin.z - self._Thickness)+self._StandoffRecessDepth
        recessdepth = Base.Vector(0,0,-self._StandoffRecessDepth)
        recessrad = self._StandoffRecessDia/2.0
        toprecess = Base.Vector(self.mh["top"].x,self.mh["top"].y,recessbottom)
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(recessrad,toprecess))
                                           ).extrude(recessdepth))
        bottomrecess = Base.Vector(self.mh["bottom"].x,self.mh["bottom"].y,recessbottom)
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(recessrad,bottomrecess))
                                           ).extrude(recessdepth))
    def show(self):
        doc = App.activeDocument()
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        mrad = self._MHoleDia/2.0
        face = Part.Face(Part.Wire(Part.makeCircle(mrad,mh)))
        return face.extrude(Base.Vector(0,0,panelThick))
    def Standoff(self,i,zBase,height,diameter):
        soff = self.mh[i] 
        soff = Base.Vector(soff.x,soff.y,zBase)
        stall = Base.Vector(0,0,height)
        srad = diameter/2.0
        return Part.Face(Part.Wire(Part.makeCircle(srad,soff))).extrude(stall)

class SpeakerRight_UpsideDown(Speaker_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        totalthick = Base.Vector(0,0,-self._Thickness)
        self.body = Part.makePlane(self._Width,
                                   self._Length,
                                   origin).extrude(totalthick)
        self.mh = dict()
        mhTopX = self._RTopHoleX
        mhTopY = self._Length - self._TopHoleY
        self.mh["top"] = origin.add(Base.Vector(mhTopX,mhTopY,0))
        mhBottomX = self._RBottomHoleX
        mhBottomY = self._Length - self._BottomHoleY
        self.mh["bottom"] = origin.add(Base.Vector(mhBottomX,mhBottomY,0))
        mhrad = self._MHoleDia/2.0
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(mhrad,
                                                                      self.mh["top"]))
                                           ).extrude(totalthick))
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(mhrad,
                                                                      self.mh["bottom"]))
                                           ).extrude(totalthick))
        recessbottom = (origin.z - self._Thickness)+self._StandoffRecessDepth
        recessdepth = Base.Vector(0,0,-self._StandoffRecessDepth)
        recessrad = self._StandoffRecessDia/2.0
        toprecess = Base.Vector(self.mh["top"].x,self.mh["top"].y,recessbottom)
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(recessrad,toprecess))
                                           ).extrude(recessdepth))
        bottomrecess = Base.Vector(self.mh["bottom"].x,self.mh["bottom"].y,recessbottom)
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(recessrad,bottomrecess))
                                           ).extrude(recessdepth))
    def show(self):
        doc = App.activeDocument()
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])        
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        mrad = self._MHoleDia/2.0
        face = Part.Face(Part.Wire(Part.makeCircle(mrad,mh)))
        return face.extrude(Base.Vector(0,0,panelThick))
    def Standoff(self,i,zBase,height,diameter):
        soff = self.mh[i] 
        soff = Base.Vector(soff.x,soff.y,zBase)
        stall = Base.Vector(0,0,height)
        srad = diameter/2.0
        return Part.Face(Part.Wire(Part.makeCircle(srad,soff))).extrude(stall)
