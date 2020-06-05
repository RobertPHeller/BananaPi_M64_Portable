#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Wed Jun 3 19:32:20 2020
#  Last Modified : <200603.2025>
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

class USBHub_(object):
    _Length     = 104.66
    _Height     = 36
    _Width      = 22.24
    _EndPoly    = [(0,0,0),(0,22.24,0),(0,22.24,27.55),(0,15.38,36),(0,0,36),(0,0,0)]
    _EndPoly90  = [(0,0,0),(0,0,27.55),(15.38,0,36),(22.24,0,36),(22.24,0,0),(0,0,0)]
    _EndPoly270 = [(0,0,0),(0,0,36),(15.38,0,36),(22.24,0,27.55),(22.24,0,0),(0,0,0)]
    @staticmethod
    def _createPolygon(origin,pointTupleList,extrudeVector):
        polypoints = list()
        for tup in pointTupleList:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        return Part.Face(Part.Wire(Part.makePolygon(polypoints))
                        ).extrude(extrudeVector)
    def __init__(self):
        raise RuntimeError("No instances allowed for USBHub_!")
        
class USBHub(USBHub_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.body = USBHub_._createPolygon(origin,USBHub_._EndPoly,
                                           Base.Vector(USBHub_._Length,0,0))
    def show(self):
        Part.show(self.body)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
                                                    
class USBHub90(USBHub_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.body = USBHub_._createPolygon(origin,USBHub_._EndPoly90,
                                           Base.Vector(0,USBHub_._Length,0))
    def show(self):
        Part.show(self.body)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
                                                    
class USBHub270(USBHub_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.body = USBHub_._createPolygon(origin,USBHub_._EndPoly270,
                                           Base.Vector(0,USBHub_._Length,0))
    def show(self):
        Part.show(self.body)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
                                                    
