#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Thu Jun 4 19:26:46 2020
#  Last Modified : <200615.1749>
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

class PianoHinge_(object):
    _Length = 12*25.4
    _Thick  = 1.00
    _FoldHeight = 15.93
    _FlangeWidth = 10.54
    _PinDia = 4.4
    _PinOff = 16-4.4-10.54
    _PinFlangeL = 12.7
    _HoleDia = 4.75
    _1stHoleOff = 25.4
    _Holespace  = 50.8
    _HoleCount = 6
    _HoleSideOff = 10.54/2.0
    def __init__(self):
        raise RuntimeError("No Instances allowed for PianoHinge_!")
    @staticmethod
    def _flange(origin,startConn=True,connectAbove=True):
        YNorm = Base.Vector(0,1,0)
        Thick = Base.Vector(0,PianoHinge_._Thick,0)
        base = Part.makePlane(PianoHinge_._FlangeWidth,PianoHinge_._Length,
                              origin,YNorm).extrude(Thick)
        if connectAbove:
            zoff = PianoHinge_._FlangeWidth
        else:
            zoff = -(PianoHinge_._PinOff+(PianoHinge_._PinDia/2.0))
        if startConn:
            xoff = 0
        else:
            xoff = PianoHinge_._PinFlangeL
        while xoff < PianoHinge_._Length:
            o = origin.add(Base.Vector(xoff,0,zoff))
            conn = Part.makePlane(PianoHinge_._PinOff+(PianoHinge_._PinDia/2.0),
                                  PianoHinge_._PinFlangeL,
                                  o,YNorm).extrude(Thick)
            base = base.fuse(conn)
            xoff += PianoHinge_._PinFlangeL*2
        holex = PianoHinge_._1stHoleOff
        holeRad = PianoHinge_._HoleDia/2.0
        holes = list()
        while holex < PianoHinge_._Length:
            ho = origin.add(Base.Vector(holex,0,PianoHinge_._HoleSideOff))
            holes.append(ho)
            hole = Part.Face(Part.Wire(Part.makeCircle(holeRad,ho,YNorm))
                            ).extrude(Thick)
            base = base.cut(hole)
            holex += PianoHinge_._Holespace
        return (base,holes)
            
class PianoHingeFlatOutsideBack(PianoHinge_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        flange1,holes1 = PianoHinge_._flange(origin,startConn=False,connectAbove=True)
        pinorig = origin.add(Base.Vector(0,
                                         PianoHinge_._PinDia/2.0,
                                 PianoHinge_._FlangeWidth+PianoHinge_._PinOff+PianoHinge_._PinDia/2.0))
        XNorm = Base.Vector(1,0,0)
        pinL  = Base.Vector(PianoHinge_._Length,0,0)
        pin = Part.Face(Part.Wire(Part.makeCircle(PianoHinge_._PinDia/2.0,
                                                 pinorig,
                                                 XNorm))).extrude(pinL)
        flange2o = origin.add(Base.Vector(0,0,
                        PianoHinge_._FlangeWidth+(PianoHinge_._PinOff*2.0)+PianoHinge_._PinDia))
        flange2,holes2 = PianoHinge_._flange(flange2o,
                                      startConn=True,connectAbove=False)
        self.hinge = flange1.fuse(pin.fuse(flange2))
        self.holes = dict()
        hi = 1
        for h in holes1:
            self.holes[1,hi] = h
            hi += 1
        hi = 1
        for h in holes2:
            self.holes[2,hi] = h
            hi += 1
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.hinge
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([190/255.0,190/255.0,190/255.0])
    def MountingHole(self,f,h,baseY,height):
        mh = self.holes[f,h]
        mh = Base.Vector(mh.x,baseY,mh.z)
        return Part.Face(Part.Wire(Part.makeCircle(PianoHinge_._HoleDia/2.0,
                                   mh,Base.Vector(0,1,0)))
                        ).extrude(Base.Vector(0,height,0))


class PianoHingeFlatInsideClosedFront(PianoHinge_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        flange1,holes1 = PianoHinge_._flange(origin,startConn=False,connectAbove=True)
        pinorig = origin.add(Base.Vector(0,
                                         PianoHinge_._PinDia/2.0,
                                 PianoHinge_._FlangeWidth+PianoHinge_._PinOff+PianoHinge_._PinDia/2.0))
        XNorm = Base.Vector(1,0,0)
        pinL  = Base.Vector(PianoHinge_._Length,0,0)
        pin = Part.Face(Part.Wire(Part.makeCircle(PianoHinge_._PinDia/2.0,
                                                 pinorig,
                                                 XNorm))).extrude(pinL)
        flange2o = origin.add(Base.Vector(0,PianoHinge_._PinDia-PianoHinge_._Thick,0))
        flange2,holes2 = PianoHinge_._flange(flange2o,
                                      startConn=True,connectAbove=True)
        self.hinge = flange1.fuse(pin.fuse(flange2))
        self.holes = dict()
        hi = 1
        for h in holes1:
            self.holes[1,hi] = h
            hi += 1
        hi = 1
        for h in holes2:
            self.holes[2,hi] = h
            hi += 1
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.hinge
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([190/255.0,190/255.0,190/255.0])
    def MountingHole(self,f,h,baseY,height):
        mh = self.holes[f,h]
        mh = Base.Vector(mh.x,baseY,mh.z)
        return Part.Face(Part.Wire(Part.makeCircle(PianoHinge_._HoleDia/2.0,
                                   mh,Base.Vector(0,1,0)))
                        ).extrude(Base.Vector(0,height,0))




if __name__ == '__main__':
    hinge = PianoHingeFlatInsideClosedFront("testhinge",Base.Vector(0,0,0))
    hinge.show()
