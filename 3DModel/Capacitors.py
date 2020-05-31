#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun May 31 16:36:29 2020
#  Last Modified : <200531.1924>
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

class C333(object):
    _C333_L = 7.11
    _C333_H = 10.16
    _C333_T = 4.07
    _C333_LeadSpacing = 5.08
    _C333_LeadDia = 0.51
    _C333_LL = 7.00
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        w2 = C333._C333_L/2.0
        self.body = Part.makePlane(C333._C333_L,C333._C333_H,
                                   Base.Vector(ox-w2,oy,oz)
                                   ).extrude(Base.Vector(0,0,-C333._C333_T))
        Part.show(self.body)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        ls2 = C333._C333_LeadSpacing / 2.0
        t2  = C333._C333_T / 2.0
        bend = 2.54
        afterbend = C333._C333_LL-bend
        self.lead1 = Part.Face(Part.Wire(Part.makeCircle(C333._C333_LeadDia/2.0,
                                                         Base.Vector(ox-ls2,oy,oz-t2),
                                                         Base.Vector(0,1,0)))
                              ).extrude(Base.Vector(0,-(bend+C333._C333_LeadDia/2.0),0))
        self.lead1 = self.lead1.fuse(Part.Face(Part.Wire(Part.makeCircle(C333._C333_LeadDia/2.0,
                                                         Base.Vector(ox-ls2,
                                                                     oy-bend,
                                                                     oz-t2)))
                                               ).extrude(Base.Vector(0,
                                                                     0,
                                                                     afterbend)))
        Part.show(self.lead1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Lead1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.75,.75,.75])
        self.lead2 = Part.Face(Part.Wire(Part.makeCircle(C333._C333_LeadDia/2.0,
                                                         Base.Vector(ox+ls2,oy,oz-t2),
                                                         Base.Vector(0,1,0)))
                              ).extrude(Base.Vector(0,-(bend+C333._C333_LeadDia/2.0)))
        self.lead2 = self.lead2.fuse(Part.Face(Part.Wire(Part.makeCircle(C333._C333_LeadDia/2.0,
                                                            Base.Vector(ox+ls2,
                                                            oy-bend,oz-t2)))).extrude(Base.Vector(0,0,afterbend)))
        Part.show(self.lead2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Lead2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.75,.75,.75])
        
                                   
class AL_CAP_Radial_5mm10x12_5(object):
    _diameter = 10
    _length =  12.5
    _leaddia = .6
    _leadspacing = 5
    _leadlength = (1.75/16.0)*25.4
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        xc = origin.x
        yc = origin.y
        zc = origin.z
        bodyradius = AL_CAP_Radial_5mm10x12_5._diameter/2.0
        self.body = Part.Face(Part.Wire(Part.makeCircle(bodyradius,origin))
                             ).extrude(Base.Vector(0,0,AL_CAP_Radial_5mm10x12_5._length))
        Part.show(self.body)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.94117,.94117,.94117])
        leadradius = AL_CAP_Radial_5mm10x12_5._leaddia/2.0
        leadoff = (AL_CAP_Radial_5mm10x12_5._leadspacing/2.0)
        lead1circ = Part.makeCircle(leadradius,Base.Vector(xc-leadoff,yc,zc))
        lead1face = Part.Face(Part.Wire(lead1circ))
        self.lead1 = lead1face.extrude(Base.Vector(0,0,-AL_CAP_Radial_5mm10x12_5._leadlength))
        Part.show(self.lead1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':lead1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.75,.75,.75])
        lead2circ = Part.makeCircle(leadradius,Base.Vector(xc+leadoff,yc,zc))
        lead2face = Part.Face(Part.Wire(lead2circ))
        self.lead2 = lead2face.extrude(Base.Vector(0,0,-AL_CAP_Radial_5mm10x12_5._leadlength))
        Part.show(self.lead2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':lead2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.75,.75,.75])

