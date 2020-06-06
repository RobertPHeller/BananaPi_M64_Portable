#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun May 31 20:53:10 2020
#  Last Modified : <200606.1828>
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

# 576-30313150421 3.15A fuse

class Littlefuse_FuseHolder_02810007H_02810010H(object):
    _width =     0.25*25.4
    _length =    0.28*25.4
    _height =    0.26*25.4
    _pinlen =    0.20*25.4
    _pindia =    0.046*25.4
    _pinXspace = 0.1*25.4
    _pinYspace = 0.20*25.4
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        xc = origin.x
        yc = origin.y
        zc = origin.z
        width = Littlefuse_FuseHolder_02810007H_02810010H._width
        w2 = width / 2.0
        length = Littlefuse_FuseHolder_02810007H_02810010H._length
        l2 = length / 2.0
        height = Littlefuse_FuseHolder_02810007H_02810010H._height
        self.body = Part.makePlane(length,width,Base.Vector(xc-l2,yc-w2,zc)
                                  ).extrude(Base.Vector(0,0,height))
        pinrad = Littlefuse_FuseHolder_02810007H_02810010H._pindia/2.0
        pinlen = -Littlefuse_FuseHolder_02810007H_02810010H._pinlen
        pin1x = xc-(Littlefuse_FuseHolder_02810007H_02810010H._pinYspace/2.0)
        pin1y = yc-(Littlefuse_FuseHolder_02810007H_02810010H._pinXspace/2.0)
        self.pin1 = Part.Face(Part.Wire(Part.makeCircle(pinrad,Base.Vector(pin1x,pin1y,zc)))
                             ).extrude(Base.Vector(0,0,pinlen))
        pin2x = xc+(Littlefuse_FuseHolder_02810007H_02810010H._pinYspace/2.0)
        pin2y = yc+(Littlefuse_FuseHolder_02810007H_02810010H._pinXspace/2.0)
        self.pin2 = Part.Face(Part.Wire(Part.makeCircle(pinrad,Base.Vector(pin2x,pin2y,zc)))
                             ).extrude(Base.Vector(0,0,pinlen))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_Body')
        obj.Shape = self.body
        obj.Label=self.name+'_Body'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_Pin1')
        obj.Shape = self.pin1
        obj.Label=self.name+'_Pin1'
        obj.ViewObject.ShapeColor=tuple([.78431,.78431,.78431])
        obj = doc.addObject("Part::Feature",self.name+'_Pin2')
        obj.Shape = self.pin2
        obj.Label=self.name+'_Pin2'
        obj.ViewObject.ShapeColor=tuple([.78431,.78431,.78431])

