#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun May 31 14:49:02 2020
#  Last Modified : <200601.1459>
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

class TB007_508_xxBE(object):
    _termwidth = 8.2
    _termheight = 10.0
    _termpitch =  5.08
    _3belength = 15.24
    _2belength = 10.16
    _termhyoff = 2.54
    _termhxoff = 4.10
    _termpindia = 1.3
    _termpinlen = 3.8

class TB007_508_03BE(TB007_508_xxBE):
    @staticmethod
    def Length():
        return TB007_508_xxBE._3belength
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        self.body = Part.makePlane(TB007_508_xxBE._3belength,
                                   TB007_508_xxBE._termwidth,
                                   origin).extrude(Base.Vector(0,0,TB007_508_xxBE._termheight))
        self.pin1 = Part.Face(Part.Wire(Part.makeCircle(TB007_508_xxBE._termpindia/2.0,
                                                        Base.Vector(ox+TB007_508_xxBE._termhyoff,
                                                                    oy+TB007_508_xxBE._termhxoff,
                                                                    oz)))).extrude(Base.Vector(0,0,-TB007_508_xxBE._termpinlen))
        self.pin2 = Part.Face(Part.Wire(Part.makeCircle(TB007_508_xxBE._termpindia/2.0,
                                                        Base.Vector(ox+TB007_508_xxBE._termhyoff+TB007_508_xxBE._termpitch,
                                                                    oy+TB007_508_xxBE._termhxoff,
                                                                    oz)))).extrude(Base.Vector(0,0,-TB007_508_xxBE._termpinlen))
        self.pin3 = Part.Face(Part.Wire(Part.makeCircle(TB007_508_xxBE._termpindia/2.0,
                                                        Base.Vector(ox+TB007_508_xxBE._termhyoff+(2*TB007_508_xxBE._termpitch),
                                                                    oy+TB007_508_xxBE._termhxoff,
                                                                    oz)))).extrude(Base.Vector(0,0,-TB007_508_xxBE._termpinlen))
    def show(self):
        doc = App.activeDocument()
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':Body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,1.0])
        Part.show(self.pin1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':Pin1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.pin2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':Pin2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.pin3)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':Pin3'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        
class TB007_508_02BE(TB007_508_xxBE):
    @staticmethod
    def Length():
        return TB007_508_xxBE._2belength
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        self.body = Part.makePlane(TB007_508_xxBE._2belength,
                                   TB007_508_xxBE._termwidth,
                                   origin).extrude(Base.Vector(0,0,TB007_508_xxBE._termheight))
        self.pin1 = Part.Face(Part.Wire(Part.makeCircle(TB007_508_xxBE._termpindia/2.0,
                                                        Base.Vector(ox+TB007_508_xxBE._termhyoff,
                                                                    oy+TB007_508_xxBE._termhxoff,
                                                                    oz)))).extrude(Base.Vector(0,0,-TB007_508_xxBE._termpinlen))
        self.pin2 = Part.Face(Part.Wire(Part.makeCircle(TB007_508_xxBE._termpindia/2.0,
                                                        Base.Vector(ox+TB007_508_xxBE._termhyoff+TB007_508_xxBE._termpitch,
                                                                    oy+TB007_508_xxBE._termhxoff,
                                                                    oz)))).extrude(Base.Vector(0,0,-TB007_508_xxBE._termpinlen))
    def show(self):        
        doc = App.activeDocument()
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':Body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,1.0])
        Part.show(self.pin1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':Pin1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.pin2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':Pin2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
