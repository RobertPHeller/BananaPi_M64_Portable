#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon Jun 1 10:34:36 2020
#  Last Modified : <200601.2106>
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

class Inlet(object):
    _flangewidth = 30.7
    _flangeheight = 23.7
    _flangedepth = 3.2
    _bodywidth = 27
    _bodyheight = 20
    _bodydepth = 16
    _lugwidth = 24
    _lugheight = 16
    _lugdepth = 7
    def Flange(self,yBase,yThick):
        flangeyoff = (Inlet._flangewidth - Inlet._bodywidth)/2.0
        flangexoff = (Inlet._flangeheight- Inlet._bodyheight)/2.0
        flangeorig = Base.Vector(self.origin.x-flangexoff,yBase,self.origin.z-flangeyoff)
        return Part.makePlane(Inlet._flangeheight,
                              Inlet._flangewidth,
                              flangeorig,Base.Vector(0,1,0)).extrude(Base.Vector(0,yThick,0))
    def bodyCutout(self,yBase,yThick):
        cutoutorig = Base.Vector(self.origin.x,yBase,self.origin.z)
        return Part.makePlane(Inlet._bodyheight,
                              Inlet._bodywidth,
                              cutoutorig,Base.Vector(0,1,0)
                              ).extrude(Base.Vector(0,yThick,0))
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        flange = self.Flange(oy,Inlet._flangedepth)
        body = Part.makePlane(Inlet._bodyheight,
                              Inlet._bodywidth,
                              origin,Base.Vector(0,1,0)
                              ).extrude(Base.Vector(0,-Inlet._bodydepth,0))
        self.body = body.fuse(flange)
        lugyoff = (Inlet._bodywidth - Inlet._lugwidth) / 2.0
        lugxoff = (Inlet._bodyheight - Inlet._lugheight) / 2.0
        lugorigin = Base.Vector(ox+lugxoff,oy-Inlet._bodydepth,
                                oz+lugyoff)
        self.solderlugs = Part.makePlane(Inlet._lugheight,
                                         Inlet._lugwidth,
                                         lugorigin,
                                         Base.Vector(0,1,0)
                                         ).extrude(Base.Vector(0,-Inlet._lugdepth))
    def show(self):
        doc = App.activeDocument()
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        Part.show(self.solderlugs)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':solderlugs'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.75,.75,.75])
