#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun May 31 20:52:40 2020
#  Last Modified : <200606.1835>
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

class DO_15_bendedLeads_400_under(object):
    _bodydia = 3.6
    _bodylen = 7.6
    _leadspacing = .400*25.4
    _leaddia = 0.9
    _totalleadLength = 25.4
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        xc = origin.x
        yc = origin.y
        zc = origin.z
        l2 = DO_15_bendedLeads_400_under._bodylen / 2.0
        brad = DO_15_bendedLeads_400_under._bodydia / 2.0
        leadhlen = (DO_15_bendedLeads_400_under._leadspacing-DO_15_bendedLeads_400_under._bodylen)/2.0
        availleadvlen = DO_15_bendedLeads_400_under._totalleadLength - leadhlen
        leadvlen = brad+((1.0/16.0)*25.4)
        if leadvlen > availleadvlen:
            leadvlen = availleadvlen
        self.body = Part.Face(Part.Wire(Part.makeCircle(brad,Base.Vector(xc-l2,yc,zc-brad),Base.Vector(1.0,0,0)))
                             ).extrude(Base.Vector(DO_15_bendedLeads_400_under._bodylen,0,0))
        leadrad = DO_15_bendedLeads_400_under._leaddia/2.0
        lead1 = Part.Face(Part.Wire(Part.makeCircle(leadrad,Base.Vector(xc-l2,yc,zc - brad),Base.Vector(1.0,0,0)))
                         ).extrude(Base.Vector(-(leadhlen+leadrad),0,0))
        lead2 = Part.Face(Part.Wire(Part.makeCircle(leadrad,Base.Vector(xc+l2,yc,zc-brad),Base.Vector(1.0,0,0)))
                         ).extrude(Base.Vector(leadhlen+leadrad,0,0))
        halfleadspacing = DO_15_bendedLeads_400_under._leadspacing/2.0
        self.lead1 = lead1.fuse(Part.Face(Part.Wire(Part.makeCircle(leadrad,Base.Vector(xc - halfleadspacing,yc,zc-brad)))
                                    ).extrude(Base.Vector(0,0,leadvlen)))
        self.lead2 = lead2.fuse(Part.Face(Part.Wire(Part.makeCircle(leadrad,Base.Vector(xc + halfleadspacing,yc,zc-brad)))
                                    ).extrude(Base.Vector(0,0,leadvlen)))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_Body')
        obj.Shape = self.body
        obj.Label=self.name+'_Body'
        obj.ViewObject.ShapeColor=tuple([.19607,.19607,.19607])
        obj = doc.addObject("Part::Feature",self.name+'_lead1')
        obj.Shape = self.lead1
        obj.Label=self.name+'_lead1'
        obj.ViewObject.ShapeColor=tuple([.98039,.98039,.98039])
        obj = doc.addObject("Part::Feature",self.name+'_lead2')
        obj.Shape = self.lead2
        obj.Label=self.name+'_lead2'
        obj.ViewObject.ShapeColor=tuple([.98039,.98039,.98039])
