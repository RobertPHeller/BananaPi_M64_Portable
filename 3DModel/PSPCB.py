#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 30 22:46:38 2020
#  Last Modified : <200531.0940>
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

from PowerSupply import *
#import TerminalBlocks
#import Capacitors
#import Diode
#import FuseHolder
#import MOV

class PCBwithStrips(object):
    _psPCBwidth = 45.72
    _psPCBlength = 76.2
    _psPCBThickness = (1.0/16.0)*25.4
    _pstermxoff =  0.98
    _psactermyoff =  5.08
    _psdctermyoff =  10.16
    _stripWidth = 2.54*.8
    _stripIncr =  2.54
    _stripOffset = 1.27
    _stripThickness = .1
    _stripExtra = 7.62
    _mhdia = 3.5
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        boardsurf = Part.makePlane(PCBwithStrips._psPCBwidth,
                                   PCBwithStrips._psPCBlength,
                                   origin)
        self.mhvector = {
             1 : Base.Vector(ox+PCBwithStrips._stripIncr,
                             oy+(PCBwithStrips._stripIncr+5*2.54),
                             oz),
             2 : Base.Vector(ox+(PCBwithStrips._psPCBwidth-PCBwithStrips._stripIncr),
                             oy+(PCBwithStrips._stripIncr+5*2.54),
                             oz),
             3 : Base.Vector(ox+PCBwithStrips._stripIncr,
                             oy+(PCBwithStrips._psPCBlength - (PCBwithStrips._stripIncr+5*2.54)),
                             oz),
             4 : Base.Vector(ox+(PCBwithStrips._psPCBwidth-PCBwithStrips._stripIncr),
                             oy+(PCBwithStrips._psPCBlength - (PCBwithStrips._stripIncr+5*2.54)),
                             oz)
        }
        mh1circ = Part.makeCircle(PCBwithStrips._mhdia/2.0,self.mhvector[1])
        mh1wire = Part.Wire(mh1circ)
        mh1 = Part.Face(mh1wire)
        boardsurf = boardsurf.cut(mh1)
        mh2circ = Part.makeCircle(PCBwithStrips._mhdia/2.0,self.mhvector[2])
        mh2wire = Part.Wire(mh2circ)
        mh2 = Part.Face(mh2wire)
        boardsurf = boardsurf.cut(mh2)
        mh3circ = Part.makeCircle(PCBwithStrips._mhdia/2.0,self.mhvector[3])
        mh3wire = Part.Wire(mh3circ)
        mh3 = Part.Face(mh3wire)
        boardsurf = boardsurf.cut(mh3)
        mh4circ = Part.makeCircle(PCBwithStrips._mhdia/2.0,self.mhvector[4])
        mh4wire = Part.Wire(mh4circ)
        mh4 = Part.Face(mh4wire)
        boardsurf = boardsurf.cut(mh4)
        self.board = boardsurf.extrude(Base.Vector(0,0,PCBwithStrips._psPCBThickness))
        Part.show(self.board)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':PSPCB'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.8235,.7058,.5490])
        mh = {
            1 : Part.Face(Part.Wire(Part.makeCircle(PCBwithStrips._mhdia/2.0,Base.Vector(self.mhvector[1].x,self.mhvector[1].y,oz-PCBwithStrips._stripThickness)))),
            2 : Part.Face(Part.Wire(Part.makeCircle(PCBwithStrips._mhdia/2.0,Base.Vector(self.mhvector[2].x,self.mhvector[2].y,oz-PCBwithStrips._stripThickness)))), 
            3 : Part.Face(Part.Wire(Part.makeCircle(PCBwithStrips._mhdia/2.0,Base.Vector(self.mhvector[3].x,self.mhvector[3].y,oz-PCBwithStrips._stripThickness)))), 
            4 : Part.Face(Part.Wire(Part.makeCircle(PCBwithStrips._mhdia/2.0,Base.Vector(self.mhvector[4].x,self.mhvector[4].y,oz-PCBwithStrips._stripThickness))))
        }
        yoff = (PCBwithStrips._psPCBlength - PSK_S15C._pslength)/2.0
        xoff = (PCBwithStrips._psPCBwidth - PSK_S15C._pswidth)/2.0
        pin1X = PSK_S15C._pspin1Yoff+xoff
        pin2X = PSK_S15C._pspin2Yoff+xoff
        sx = PCBwithStrips._stripIncr
        self.strips = list()
        stripno = 1
        while (sx + PCBwithStrips._stripIncr) <= PCBwithStrips._psPCBwidth:
            if sx <= pin1X and sx >= pin2X:
                stripCP1 = Base.Vector(ox+(sx - (PCBwithStrips._stripWidth / 2.0)),
                                       oy+PCBwithStrips._stripOffset,
                                       oz-PCBwithStrips._stripThickness)
                stripCP2 = Base.Vector(ox+(sx - (PCBwithStrips._stripWidth / 2.0)),
                                       oy+(PCBwithStrips._stripOffset + xoff + PSK_S15C._pspin1Xoff - PCBwithStrips._stripExtra),
                                       oz-PCBwithStrips._stripThickness)
                striplen = yoff+PSK_S15C._pspin4Xoff+PCBwithStrips._stripExtra
                stripsurf = Part.makePlane(PCBwithStrips._stripWidth,
                                           striplen,stripCP1)
                strip = stripsurf.extrude(Base.Vector(0,0,PCBwithStrips._stripThickness))
                self.strips.append(strip)
                Part.show(strip)
                last = len(doc.Objects)-1
                doc.Objects[last].Label=name+(":strip%d" % stripno)
                stripno += 1
                doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
                stripsurf = Part.makePlane(PCBwithStrips._stripWidth,
                                           striplen,stripCP2)
                strip = stripsurf.extrude(Base.Vector(0,0,PCBwithStrips._stripThickness))
                self.strips.append(strip)
                Part.show(strip)
                last = len(doc.Objects)-1
                doc.Objects[last].Label=name+(":strip%d" % stripno)
                stripno += 1
                doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
            else:
                stripCP = Base.Vector(ox+(sx - (PCBwithStrips._stripWidth / 2.0)),
                                       oy+PCBwithStrips._stripOffset,
                                       oz-PCBwithStrips._stripThickness)
                stripsurf = Part.makePlane(PCBwithStrips._stripWidth,
                                           PCBwithStrips._psPCBlength - (PCBwithStrips._stripOffset*2),stripCP)
                i = 1
                while i <= 4:
                    h = self.mhvector[i]
                    stripsurf = stripsurf.cut(mh[i])
                    i += 1
                strip = stripsurf.extrude(Base.Vector(0,0,PCBwithStrips._stripThickness))
                self.strips.append(strip)
                Part.show(strip)
                last = len(doc.Objects)-1
                doc.Objects[last].Label=name+(":strip%d" % stripno)
                stripno += 1
                doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
            sx += PCBwithStrips._stripIncr
        
    def MountingHole(self,name,i,zBase):
        mhv = self.mhvector[i]
        mhz = Base.Vector(mhv.x,mhv.y,zBase);
        mhcirc = Part.makeCircle(M64Board._m64_mh_dia/2.0,mhv);
        mhwire = Part.Wire(mhcirc)
        return Part.Face(mhwire)
    def Standoff(self,name,i,zBase,height,diameter,color):
        stofv = self.mhvector[i]
        stofv = Base.Vector(stofv.x,stofv.y,zBase)
        stofcirc = Part.makeCircle(diameter/2.0,stofv)
        stofwire = Part.Wire(stofcirc)
        stofface = Part.Face(stofwire)
        result = stofface.extrude(Base.Vector(0,0,height))
        return result
        

                    
