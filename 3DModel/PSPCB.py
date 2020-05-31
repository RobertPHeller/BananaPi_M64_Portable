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
#  Last Modified : <200531.1833>
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
from TerminalBlocks import *
from Capacitors import *
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
    _leadhole_r = (0.037/2.0)*25.4
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
        xh = (ox+PCBwithStrips._stripIncr)
        while xh < ox+PCBwithStrips._psPCBwidth-PCBwithStrips._stripIncr:
            yh = oy+PCBwithStrips._stripIncr
            while yh <= oy+PCBwithStrips._psPCBlength:
                boardsurf = self._drill_leadhole(boardsurf,xh,yh,oz)
                yh += PCBwithStrips._stripIncr
            xh += PCBwithStrips._stripIncr
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
                                       oy+(PCBwithStrips._stripOffset + yoff + PSK_S15C._pspin1Xoff - PCBwithStrips._stripExtra-2.54),
                                       oz-PCBwithStrips._stripThickness)
                striplen = yoff+PSK_S15C._pspin4Xoff+PCBwithStrips._stripExtra
                stripsurf = Part.makePlane(PCBwithStrips._stripWidth,
                                           striplen,stripCP1)
                xh = stripCP1.x + (PCBwithStrips._stripWidth/2.0)
                yh = stripCP1.y + PCBwithStrips._stripOffset
                while yh < stripCP1.y+striplen:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP1.z)
                    yh += PCBwithStrips._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,PCBwithStrips._stripThickness))
                self.strips.append(strip)
                Part.show(strip)
                last = len(doc.Objects)-1
                doc.Objects[last].Label=name+(":strip%d" % stripno)
                stripno += 1
                doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
                stripsurf = Part.makePlane(PCBwithStrips._stripWidth,
                                           striplen,stripCP2)
                xh = stripCP2.x + (PCBwithStrips._stripWidth/2.0)
                yh = stripCP2.y + PCBwithStrips._stripOffset
                while yh < stripCP2.y+striplen:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP2.z)
                    yh += PCBwithStrips._stripIncr
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
                xh = stripCP.x + (PCBwithStrips._stripWidth/2.0)
                yh = stripCP.y + PCBwithStrips._stripOffset
                while yh < stripCP.y+PCBwithStrips._psPCBlength - (PCBwithStrips._stripOffset*2):
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP.z)
                    yh += PCBwithStrips._stripIncr
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
    def _drill_leadhole(self,surf,x,y,z):
        return(surf.cut(Part.Face(Part.Wire(Part.makeCircle(PCBwithStrips._leadhole_r,Base.Vector(x,y,z))))))
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
        

                    
class PSOnPCB(PCBwithStrips):
    _fuseholderX = 76.2-6.35
    _fuseholderY = 45.72-25.40
    _bypassX = 25.40
    _bypassY = 45.72-15.24
    _filterX = 5.08 #76.2-5.08
    _filterY = 45.72-27.94
    _esdX = 17.78 #76.2-17.78
    _esdY = 45.72-17.78
    _wiredia = 1.5
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        PCBwithStrips.__init__(self,name+":pcb",origin)
        yoff = (PCBwithStrips._psPCBlength - PSK_S15C._pslength)/2.0
        xoff = (PCBwithStrips._psPCBwidth - PSK_S15C._pswidth)/2.0
        psorigin = Base.Vector(ox+xoff,oy+yoff,oz+PCBwithStrips._psPCBThickness)
        self.powersupply = PSK_S15C(name+":powersupply",psorigin)
        actermorigin = Base.Vector(ox+(PCBwithStrips._psPCBwidth - PCBwithStrips._psactermyoff - TB007_508_03BE.Length()),
                                   oy+(PCBwithStrips._psPCBlength - PCBwithStrips._pstermxoff - TB007_508_xxBE._termwidth),
                                   oz+PCBwithStrips._psPCBThickness)
        self.acterm = TB007_508_03BE(name+":acterm",actermorigin)
        dctermorigin = Base.Vector(ox+(PCBwithStrips._psPCBwidth - PCBwithStrips._psdctermyoff - TB007_508_02BE.Length()),
                                   oy+(PCBwithStrips._pstermxoff),
                                   oz+PCBwithStrips._psPCBThickness)
        self.dcterm = TB007_508_02BE(name+":dcterm",dctermorigin)
        self.bypasscap = C333(name+":bypasscap",Base.Vector(ox+PSOnPCB._bypassY,PSOnPCB._bypassX,0))
        self.filtercap = AL_CAP_Radial_5mm10x12_5(name+":filtercap",
                            Base.Vector(ox+PSOnPCB._filterY,
                                        oy+PSOnPCB._filterX,
                                        oz+PCBwithStrips._psPCBThickness))
