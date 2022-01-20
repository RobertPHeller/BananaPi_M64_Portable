#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun May 31 20:53:19 2020
#  Last Modified : <200606.1830>
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

class B72220S2301K101(object):
    _W = 21.5
    _th = 6.1
    _h = 25.5
    _d = 1.0
    _e = 10
    _a = 2.1
    _l = 25.0
    _seatoffset = 3
    _leadspacing = 8 * 2.54
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        xc = origin.x
        yc = origin.y
        zc = origin.z
        bodyradius = B72220S2301K101._W / 2.0
        self.body = Part.Face(Part.Wire(Part.makeCircle(bodyradius,Base.Vector(xc,yc-bodyradius,zc)))
                             ).extrude(Base.Vector(0,0,-B72220S2301K101._th))
        d = B72220S2301K101._d
        e2 = B72220S2301K101._e/2.0
        yseat = yc+(B72220S2301K101._seatoffset/2.0)
        seatlenVect = Base.Vector(0,B72220S2301K101._seatoffset*(-1.5),0)
        th2 = B72220S2301K101._th/2.0
        a2  = B72220S2301K101._a/2.0
        seat1 = Part.Face(Part.Wire(Part.makeCircle(d,Base.Vector(xc-e2,yseat,zc-th2-a2),Base.Vector(0,1,0)))
                              ).extrude(seatlenVect)
        seat2 = Part.Face(Part.Wire(Part.makeCircle(d,Base.Vector(xc+e2,yseat,zc-th2+a2),Base.Vector(0,1,0)))
                              ).extrude(seatlenVect)
        self.body = self.body.fuse(seat1)
        self.body = self.body.fuse(seat2)
        leadhlen = (B72220S2301K101._leadspacing/2.0)-e2
        leadrad = B72220S2301K101._d/2.0
        XNorm = Base.Vector(1,0,0)
        YNorm = Base.Vector(0,1,0)
        ZNorm = Base.Vector(0,0,1)
        lead1hb = Base.Vector(xc-e2,yseat,zc-th2-a2)
        l1x=lead1hb.x
        l1y=lead1hb.y
        l1z=lead1hb.z
        self.lead1 = Part.Face(Part.Wire(Part.makeCircle(leadrad,lead1hb,XNorm))
                              ).extrude(Base.Vector(-(leadhlen+leadrad),0,0))
        l1vheight = abs(zc-(((1/16.0)*2.54))+l1z)
        l1vx = l1x-leadhlen
        self.lead1 = self.lead1.fuse(Part.Face(Part.Wire(Part.makeCircle(leadrad,Base.Vector(l1vx,l1y,l1z),ZNorm))
                                              ).extrude(Base.Vector(0,0,l1vheight)))
        lead2hb = Base.Vector(xc+e2,yseat,zc-th2+a2)
        l2x=lead2hb.x
        l2y=lead2hb.y
        l2z=lead2hb.z
        self.lead2 = Part.Face(Part.Wire(Part.makeCircle(leadrad,lead2hb,XNorm))
                              ).extrude(Base.Vector((leadhlen+leadrad),0,0))
        l2vheight = abs(zc-(((1/16.0)*2.54)) + l2z)
        l2vx      = l2x + leadhlen
        self.lead2 = self.lead2.fuse(Part.Face(Part.Wire(Part.makeCircle(leadrad,Base.Vector(l2vx,l2y,l2z),ZNorm))
                                              ).extrude(Base.Vector(0,0,l2vheight)))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_Body')
        obj.Shape = self.body
        obj.Label=self.name+'_Body'
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_lead1')
        obj.Shape = self.lead1
        obj.Label=self.name+'_lead1'
        obj.ViewObject.ShapeColor=tuple([0.98,0.98,0.98])
        obj = doc.addObject("Part::Feature",self.name+'_lead2')
        obj.Shape = self.lead2
        obj.Label=self.name+'_lead2'
        obj.ViewObject.ShapeColor=tuple([0.98,0.98,0.98])
