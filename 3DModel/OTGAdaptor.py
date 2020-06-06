#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Wed Jun 3 20:43:35 2020
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

class OTGAdaptor(object):
    _ADepth        = 9.28
    _ZDisp         = -2.91
    _XOffA         = -2.94
    _GrossWidth    = 17.58
    _GrossThick    = 9.82
    _BodyLength    = 32.74
    _BodyPoly      = [(0,32.74,0), (17.58,32.74,0), (17.58,15.12,0), (12.36,0,0), (3.48,0,0), (0,15.12,0), (0,32.74,0)]
    _MicroB_Length = 5.92
    _MicroB_Width  = 6.85
    _MicroB_Thick  = 1.8
    _MicroB_XOff   = 4.35
    _MicroB_ZOff   = 3.49
    @staticmethod
    def _createPolygon(origin,pointTupleList,extrudeVector):
        polypoints = list()
        for tup in pointTupleList:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        return Part.Face(Part.Wire(Part.makePolygon(polypoints))
                        ).extrude(extrudeVector)
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        thick = Base.Vector(0,0,OTGAdaptor._GrossThick)
        self.body = OTGAdaptor._createPolygon(origin,
                                              OTGAdaptor._BodyPoly,
                                              thick)
        microborig = origin.add(Base.Vector(OTGAdaptor._MicroB_XOff,
                                            -OTGAdaptor._MicroB_Length,
                                            OTGAdaptor._MicroB_ZOff))
        microbthick = Base.Vector(0,0,OTGAdaptor._MicroB_Thick)
        self.microb = Part.makePlane(OTGAdaptor._MicroB_Width,
                                     OTGAdaptor._MicroB_Length,
                                     microborig).extrude(microbthick)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.body
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_microb")
        obj.Shape = self.microb
        obj.Label=self.name+"_microb"
        obj.ViewObject.ShapeColor=tuple([0.95,0.95,0.95])
                
