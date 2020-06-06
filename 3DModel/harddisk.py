#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Wed Jun 3 21:48:02 2020
#  Last Modified : <200606.1900>
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

class Disk25_2H(object):
    _Width   = 69.85
    _Length  = 100.29
    _Height  = 9.38
    _MH1X    = 2.8   + (2.7/2.0)
    _MH1Y    = 12.67 + (2.7/2.0)
    _MH2X    = 2.8   + (2.7/2.0)
    _MH2Y    = 89.33 + (2.7/2.0)
    _MH3X    = 64.79 + (2.7/2.0)
    _MH3Y    = 12.67 + (2.7/2.0)
    _MH4X    = 64.79 + (2.7/2.0)
    _MH4Y    = 89.33 + (2.7/2.0)
    _MHDia   = 2.7
    _MHDepth = 4.67
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.body = Part.makePlane(Disk25_2H._Width,
                                   Disk25_2H._Length,
                                   origin).extrude(Base.Vector(0,0,Disk25_2H._Height))
        self.mh = dict()
        self.mh[1] = origin.add(Base.Vector(Disk25_2H._MH1X,
                                            Disk25_2H._MH1Y,
                                            0))
        self.mh[2] = origin.add(Base.Vector(Disk25_2H._MH2X,
                                            Disk25_2H._MH2Y,
                                            0))
        self.mh[3] = origin.add(Base.Vector(Disk25_2H._MH3X,
                                            Disk25_2H._MH3Y,
                                            0))
        self.mh[4] = origin.add(Base.Vector(Disk25_2H._MH4X,
                                            Disk25_2H._MH4Y,
                                            0))
        mrad = Disk25_2H._MHDia/2.0
        mdeep= Base.Vector(0,0,Disk25_2H._MHDepth)
        for i in [1,2,3,4]:
            mhface = Part.Face(Part.Wire(Part.makeCircle(mrad,self.mh[i])))
            self.body = self.body.cut(mhface.extrude(mdeep))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.body
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        mrad = Disk25_2H._MHDia/2.0
        face = Part.Face(Part.Wire(Part.makeCircle(mrad,mh)))
        return face.extrude(Base.Vector(0,0,panelThick))
