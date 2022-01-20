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
#  Last Modified : <200727.1309>
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

import os
import sys
sys.path.append(os.path.dirname(__file__))

import datetime



from PowerSupply import *
from TerminalBlocks import *
from Capacitors import *
from Diode import *
from FuseHolder import *
from MOV import *
from header import *

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
        while xh <= ox+PCBwithStrips._psPCBwidth:
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
                stripsurf = Part.makePlane(PCBwithStrips._stripWidth,
                                           striplen,stripCP2)
                xh = stripCP2.x + (PCBwithStrips._stripWidth/2.0)
                yh = stripCP2.y + PCBwithStrips._stripOffset
                while yh < stripCP2.y+striplen:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP2.z)
                    yh += PCBwithStrips._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,PCBwithStrips._stripThickness))
                self.strips.append(strip)
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
            sx += PCBwithStrips._stripIncr
    def _drill_leadhole(self,surf,x,y,z):
        return(surf.cut(Part.Face(Part.Wire(Part.makeCircle(PCBwithStrips._leadhole_r,Base.Vector(x,y,z))))))
    def MountingHole(self,i,zBase):
        mhv = self.mhvector[i]
        mhz = Base.Vector(mhv.x,mhv.y,zBase);
        mhcirc = Part.makeCircle(PCBwithStrips._mhdia/2.0,mhz);
        mhwire = Part.Wire(mhcirc)
        return Part.Face(mhwire)
    def Standoff(self,i,zBase,height,diameter):
        stofv = self.mhvector[i]
        stofv = Base.Vector(stofv.x,stofv.y,zBase)
        stofcirc = Part.makeCircle(diameter/2.0,stofv)
        stofwire = Part.Wire(stofcirc)
        stofface = Part.Face(stofwire)
        result = stofface.extrude(Base.Vector(0,0,height))
        return result
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_PSPCB")
        obj.Shape = self.board
        obj.Label=self.name+'_PSPCB'
        obj.ViewObject.ShapeColor=tuple([.8235,.7058,.5490])
        stripno = 1
        for strip in self.strips:
            obj = doc.addObject("Part::Feature",self.name+("_strip%d" % stripno))
            obj.Shape = strip
            obj.Label=self.name+("_strip%d" % stripno)        
            obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
            stripno += 1
                    
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
        PCBwithStrips.__init__(self,name,origin)
        ox = origin.x
        oy = origin.y
        oz = origin.z
        yoff = (PCBwithStrips._psPCBlength - PSK_S15C._pslength)/2.0
        xoff = (PCBwithStrips._psPCBwidth - PSK_S15C._pswidth)/2.0
        psorigin = Base.Vector(ox+xoff,oy+yoff,oz+PCBwithStrips._psPCBThickness)
        self.powersupply = PSK_S15C(name+"_powersupply",psorigin)
        actermorigin = Base.Vector(ox+(PCBwithStrips._psPCBwidth - PCBwithStrips._psactermyoff - TB007_508_03BE.Length()),
                                   oy+(PCBwithStrips._psPCBlength - PCBwithStrips._pstermxoff - TB007_508_xxBE._termwidth),
                                   oz+PCBwithStrips._psPCBThickness)
        self.acterm = TB007_508_03BE(name+"_acterm",actermorigin)
        dctermorigin = Base.Vector(ox+(PCBwithStrips._psPCBwidth - PCBwithStrips._psdctermyoff - TB007_508_02BE.Length()),
                                   oy+(PCBwithStrips._pstermxoff),
                                   oz+PCBwithStrips._psPCBThickness)
        self.dcterm = TB007_508_02BE(name+"_dcterm",dctermorigin)
        self.bypasscap = C333(name+"_bypasscap",Base.Vector(ox+PSOnPCB._bypassY,oy+PSOnPCB._bypassX,oz))
        self.filtercap = AL_CAP_Radial_5mm10x12_5(name+"_filtercap",
                            Base.Vector(ox+PSOnPCB._filterY,
                                        oy+PSOnPCB._filterX,
                                        oz+PCBwithStrips._psPCBThickness))
        self.esd = DO_15_bendedLeads_400_under(name+"_esd",
                            Base.Vector(ox+PSOnPCB._esdY,
                                        oy+PSOnPCB._esdX,
                                        oz))
        self.fuseholder = Littlefuse_FuseHolder_02810007H_02810010H(name+"_fuseholder",
                            Base.Vector(ox+PSOnPCB._fuseholderY,
                                        oy+PSOnPCB._fuseholderX,
                                        oz+PCBwithStrips._psPCBThickness))
        self.mov = B72220S2301K101(name+"_mov",
                            Base.Vector(ox+(PCBwithStrips._psPCBwidth / 2.0),
                                        oy+((PCBwithStrips._psPCBlength - (yoff+PSK_S15C._pspin3Xoff+3) +3.81)),
                                        oz))
        groundj1X = oy+((PCBwithStrips._psPCBlength / 2.0))
        groundj1Y = ox+((PSK_S15C._pspin1Yoff)+yoff)
        groundj1L = 20.32+5.08
        wireradius = PSOnPCB._wiredia / 2.0
        XNorm=Base.Vector(1,0,0)
        YNorm=Base.Vector(0,1,0)
        self.groundwires = list()
        g1=Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(groundj1Y,groundj1X,oz-wireradius),XNorm))
                    ).extrude(Base.Vector(-groundj1L,0,0))
        self.groundwires.append(g1)
        for i in [1,2,3]:
            yy = i*2.54
            xx = (i&1)*2.54
            y1 = groundj1Y + yy
            y2 = groundj1Y-groundj1L-yy
            x  = groundj1X - xx
            gA = Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(y1,x,oz-wireradius),XNorm))
                    ).extrude(Base.Vector(-2.54,0,0))
            gB = Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(y2,x,oz-wireradius),XNorm))
                    ).extrude(Base.Vector(2.54,0,0))
            self.groundwires.append(gA)
            self.groundwires.append(gB)
        self.linewires = list()
        l1Y = ox+PCBwithStrips._psactermyoff + (7*2.54)
        l1X = oy+PCBwithStrips._psPCBlength - (5.08 + 2.54)
        l1L = 5.08
        l1 = Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(l1Y,l1X,oz-wireradius),XNorm))
                      ).extrude(Base.Vector(l1L,0,0))
        self.linewires.append(l1)
        l2Y = l1Y - 5.08 - 5.08
        l2X = oy+PCBwithStrips._psPCBlength-5.08
        l2L = 5.08
        l2 = Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(l2Y,l2X,oz-wireradius),XNorm))
                      ).extrude(Base.Vector(l2L,0,0))
        self.linewires.append(l2)
        self.minuswires = list()
        M1Y = ox+PCBwithStrips._psdctermyoff + (5*2.54)
        M1X = oy+PCBwithStrips._pstermxoff + (TB007_508_xxBE._termwidth/2.0) + 2.54
        M1L = 5.08
        m1 = Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(M1Y,M1X,oz-wireradius),XNorm))
                      ).extrude(Base.Vector(M1L,0,0))
        self.minuswires.append(m1)
        M2Y = M1Y-M1L-2.54
        M2X = M1X+2.54
        M2L = 7.62
        m2 = Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(M2Y,M2X,oz-wireradius),XNorm))
                      ).extrude(Base.Vector(M2L,0,0))
        self.minuswires.append(m2)
        self.pluswires = list()
        P1Y = ox+PCBwithStrips._psdctermyoff + 5.08 + 5.08
        P1X = M2X + 2.54
        P1L = 2.54*5
        p1 = Part.Face(Part.Wire(Part.makeCircle(wireradius,Base.Vector(P1Y,P1X,oz-wireradius),XNorm))
                      ).extrude(Base.Vector(P1L,0,0))
        self.pluswires.append(p1)
    def show(self):
        PCBwithStrips.show(self)
        doc = App.activeDocument()
        self.powersupply.show()
        self.acterm.show()
        self.dcterm.show()
        self.bypasscap.show()
        self.filtercap.show()
        self.esd.show()
        self.fuseholder.show()
        self.mov.show()
        green = tuple([0.0,1.0,0.0])
        gnum = 1
        for gw in self.groundwires:
            obj = doc.addObject("Part::Feature",self.name+('_ground%d' % gnum))
            obj.Shape = gw
            obj.Label=self.name+('_ground%d' % gnum)
            obj.ViewObject.ShapeColor=green
            gnum += 1
        black = tuple([0.0,0.0,0.0])
        lnum = 1
        for lw in self.linewires:
            obj = doc.addObject("Part::Feature",self.name+('_Line%d' % lnum))
            obj.Shape = lw
            obj.Label=self.name+('_Line%d' % lnum)
            obj.ViewObject.ShapeColor=black
            lnum += 1
        mnum = 1
        for mw in self.minuswires:
            obj = doc.addObject("Part::Feature",self.name+('_Minus%d' % lnum))
            obj.Shape = mw
            obj.Label=self.name+('_Minus%d' % mnum)
            obj.ViewObject.ShapeColor=black
            mnum += 1
        red = tuple([1.0,0.0,0.0])
        pnum = 1
        for pl in self.pluswires:
            obj = doc.addObject("Part::Feature",self.name+('_Plus%d' % pnum))
            obj.Shape = pl
            obj.Label=self.name+('_Plus%d' % pnum)
            obj.ViewObject.ShapeColor=red
            pnum += 1

def closeto(a,b,fuzz=.01):
    return (abs(a-b)<fuzz)


class PCB2withStrips(object):
    _psPCBwidth = 63.5
    _psPCBMhOff = 8*2.54
    _psPCBpsw   = 14*2.54
    _psPCBlength = 76.2
    _psPCBThickness = (1.0/16.0)*25.4
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
        boardsurf = Part.makePlane(self._psPCBwidth,
                                   self._psPCBlength,
                                   origin)
        xh = (ox+self._stripIncr)
        while xh <= ox+self._psPCBwidth:
            yh = oy+self._stripIncr
            while yh <= oy+self._psPCBlength:
                boardsurf = self._drill_leadhole(boardsurf,xh,yh,oz)
                yh += self._stripIncr
            xh += self._stripIncr
        self.mhvector = {
             1 : Base.Vector(ox+self._psPCBMhOff+self._stripIncr,
                             oy+(self._stripIncr+5*2.54),
                             oz),
             2 : Base.Vector(ox+self._psPCBMhOff+self._psPCBpsw+self._stripIncr,
                             oy+(self._stripIncr+5*2.54),
                             oz),
             3 : Base.Vector(ox+self._psPCBMhOff+self._stripIncr,
                             oy+(self._psPCBlength - (self._stripIncr+5*2.54)),
                             oz),
             4 : Base.Vector(ox+(self._psPCBMhOff+self._psPCBpsw+self._stripIncr),
                             oy+(self._psPCBlength - (self._stripIncr+5*2.54)),
                             oz)
        }
        mh1circ = Part.makeCircle(self._mhdia/2.0,self.mhvector[1])
        mh1wire = Part.Wire(mh1circ)
        mh1 = Part.Face(mh1wire)
        boardsurf = boardsurf.cut(mh1)
        mh2circ = Part.makeCircle(self._mhdia/2.0,self.mhvector[2])
        mh2wire = Part.Wire(mh2circ)
        mh2 = Part.Face(mh2wire)
        boardsurf = boardsurf.cut(mh2)
        mh3circ = Part.makeCircle(self._mhdia/2.0,self.mhvector[3])
        mh3wire = Part.Wire(mh3circ)
        mh3 = Part.Face(mh3wire)
        boardsurf = boardsurf.cut(mh3)
        mh4circ = Part.makeCircle(self._mhdia/2.0,self.mhvector[4])
        mh4wire = Part.Wire(mh4circ)
        mh4 = Part.Face(mh4wire)
        boardsurf = boardsurf.cut(mh4)
        self.board = boardsurf.extrude(Base.Vector(0,0,self._psPCBThickness))
        mh = {
            1 : Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,Base.Vector(self.mhvector[1].x,self.mhvector[1].y,oz-self._stripThickness)))),
            2 : Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,Base.Vector(self.mhvector[2].x,self.mhvector[2].y,oz-self._stripThickness)))), 
            3 : Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,Base.Vector(self.mhvector[3].x,self.mhvector[3].y,oz-self._stripThickness)))), 
            4 : Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,Base.Vector(self.mhvector[4].x,self.mhvector[4].y,oz-self._stripThickness))))
        }
        yoff = (self._psPCBlength - PSK_S15C._pslength)/2.0
        xoff = self._psPCBMhOff+((self._psPCBpsw - PSK_S15C._pswidth)/2.0)+self._stripIncr
        pin1X = (PSK_S15C._pspin1Yoff+xoff)
        pin2X = (PSK_S15C._pspin2Yoff+xoff)
        sx = self._stripIncr
        vinX = sx+self._stripIncr
        gndX1 = vinX + self._stripIncr
        gndX2 = gndX1 + (3*self._stripIncr)
        voutX = gndX2 + self._stripIncr 
        self.strips = list()
        while (sx + self._stripIncr) <= self._psPCBwidth:
            #sys.__stderr__.write("*** sx = %f, pin1X is %f, pin2X is %f\n"%(sx,pin1X,pin2X))
            #sys.__stderr__.write("*** sx = %f, vinX is %f, voutX is %f\n"%(sx,vinX,voutX))
            if closeto(sx,vinX) or closeto(sx,voutX):
                #sys.__stderr__.write("*** sx hit\n")
                stripCP1 = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+self._stripOffset,
                                       oz-self._stripThickness)
                striplen1 = 6*self._stripIncr
                stripsurf = Part.makePlane(self._stripWidth,striplen1,stripCP1)
                xh = stripCP1.x + (self._stripWidth/2.0)
                yh = stripCP1.y + self._stripOffset
                while yh < stripCP1.y+striplen1:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP1.z)
                    yh += self._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
                stripCP2 = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+(11.5*self._stripIncr),
                                       oz-self._stripThickness)
                striplen2 = self._psPCBlength - (12*self._stripIncr)
                stripsurf = Part.makePlane(self._stripWidth,striplen2,stripCP2)
                xh = stripCP2.x + (self._stripWidth/2.0)
                yh = stripCP2.y + self._stripOffset
                while yh < stripCP2.y+striplen2:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP2.z)
                    yh += self._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
            elif closeto(sx,gndX1) or closeto(sx,gndX2):
                #sys.__stderr__.write("*** sx hit\n")
                stripCP1 = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+self._stripOffset,
                                       oz-self._stripThickness)
                striplen1 = 6*self._stripIncr
                stripsurf = Part.makePlane(self._stripWidth,striplen1,stripCP1)
                xh = stripCP1.x + (self._stripWidth/2.0)
                yh = stripCP1.y + self._stripOffset
                while yh < stripCP1.y+striplen1:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP1.z)
                    yh += self._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
                stripCP2 = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+(11.5*self._stripIncr),
                                       oz-self._stripThickness)
                striplen2 = 5*self._stripIncr
                stripsurf = Part.makePlane(self._stripWidth,striplen2,stripCP2)
                xh = stripCP2.x + (self._stripWidth/2.0)
                yh = stripCP2.y + self._stripOffset
                while yh < stripCP2.y+striplen2:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP2.z)
                    yh += self._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
                stripCP3 = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+(25.5*self._stripIncr),
                                       oz-self._stripThickness)
                striplen3 = 4*self._stripIncr
                stripsurf = Part.makePlane(self._stripWidth,striplen3,stripCP3)
                xh = stripCP3.x + (self._stripWidth/2.0)
                yh = stripCP3.y + self._stripOffset
                while yh < stripCP3.y+striplen3:
                   stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP3.z)
                   yh += self._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
            elif (sx < pin1X or closeto(sx,pin1X)) and \
                 (sx > pin2X or closeto(sx,pin2X)):
                #sys.__stderr__.write("*** sx hit\n")
                stripCP1 = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+self._stripOffset,
                                       oz-self._stripThickness)
                stripCP2 = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+(self._stripOffset + yoff + PSK_S15C._pspin1Xoff - self._stripExtra-2.54),
                                       oz-self._stripThickness)
                striplen = yoff+PSK_S15C._pspin4Xoff+self._stripExtra
                stripsurf = Part.makePlane(self._stripWidth,
                                           striplen,stripCP1)
                xh = stripCP1.x + (self._stripWidth/2.0)
                yh = stripCP1.y + self._stripOffset
                while yh < stripCP1.y+striplen:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP1.z)
                    yh += self._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
                stripsurf = Part.makePlane(self._stripWidth,
                                           striplen,stripCP2)
                xh = stripCP2.x + (self._stripWidth/2.0)
                yh = stripCP2.y + self._stripOffset
                while yh < stripCP2.y+striplen:
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP2.z)
                    yh += self._stripIncr
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
            else:
                stripCP = Base.Vector(ox+(sx - (self._stripWidth / 2.0)),
                                       oy+self._stripOffset,
                                       oz-self._stripThickness)
                stripsurf = Part.makePlane(self._stripWidth,
                                           self._psPCBlength - (self._stripOffset*2),stripCP)
                xh = stripCP.x + (self._stripWidth/2.0)
                yh = stripCP.y + self._stripOffset
                while yh < stripCP.y+self._psPCBlength - (self._stripOffset*2):
                    stripsurf = self._drill_leadhole(stripsurf,xh,yh,stripCP.z)
                    yh += self._stripIncr
                i = 1
                while i <= 4:
                    h = self.mhvector[i]
                    stripsurf = stripsurf.cut(mh[i])
                    i += 1
                strip = stripsurf.extrude(Base.Vector(0,0,self._stripThickness))
                self.strips.append(strip)
            sx += self._stripIncr
    def _drill_leadhole(self,surf,x,y,z):
        return(surf.cut(Part.Face(Part.Wire(Part.makeCircle(self._leadhole_r,Base.Vector(x,y,z))))))
    def MountingHole(self,i,zBase):
        mhv = self.mhvector[i]
        mhz = Base.Vector(mhv.x,mhv.y,zBase);
        mhcirc = Part.makeCircle(self._mhdia/2.0,mhz);
        mhwire = Part.Wire(mhcirc)
        return Part.Face(mhwire)
    def Standoff(self,i,zBase,height,diameter):
        stofv = self.mhvector[i]
        stofv = Base.Vector(stofv.x,stofv.y,zBase)
        stofcirc = Part.makeCircle(diameter/2.0,stofv)
        stofwire = Part.Wire(stofcirc)
        stofface = Part.Face(stofwire)
        result = stofface.extrude(Base.Vector(0,0,height))
        return result
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_PSPCB")
        obj.Shape = self.board
        obj.Label=self.name+'_PSPCB'
        obj.ViewObject.ShapeColor=tuple([.8235,.7058,.5490])
        stripno = 1
        for strip in self.strips:
            obj = doc.addObject("Part::Feature",self.name+("_strip%d" % stripno))
            obj.Shape = strip
            obj.Label=self.name+("_strip%d" % stripno)        
            obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
            stripno += 1
            
class PS2OnPCB(PCB2withStrips):
    _bypassX = 25.40
    _bypassY = 48.26
    _filterX = 5.08
    _filterY = 45.72+2.54
    _esdX = 17.78
    _esdY = 45.72
    _wiredia = 1.5
    def __init__(self,name,origin):
        PCB2withStrips.__init__(self,name,origin)
        ox = origin.x
        oy = origin.y
        oz = origin.z
        vinX = self._stripIncr*2
        gndX1 = vinX + self._stripIncr
        gndX2 = gndX1 + (3*self._stripIncr)
        mhcd42HeaderOrig = Base.Vector(ox+vinX,
                                       oy+(5*self._stripIncr),
                                       oz+self._psPCBThickness)
        self.mhcd42Header = Header6_AboveDown(name+'_mhcd42Header',mhcd42HeaderOrig)
        yin = 15*self._stripIncr
        self.mt3608vinM = Header1_AboveDown(name+'_mt3608vinM',Base.Vector(ox+gndX1,
                                                                    oy+yin,
                                                                    oz+self._psPCBThickness))
        self.mt3608vinP = Header1_AboveDown(name+'_mt3608vinP',Base.Vector(ox+gndX2,
                                                                    oy+yin,
                                                                    oz+self._psPCBThickness))
        yout = 27*self._stripIncr
        self.mt3608voutM = Header1_AboveDown(name+'_mt3608voutM',Base.Vector(ox+gndX1,
                                                                     oy+yout,
                                                                     oz+self._psPCBThickness))

        self.mt3608voutP = Header1_AboveDown(name+'_mt3608voutP',Base.Vector(ox+gndX2,
                                                                    oy+yout,
                                                                    oz+self._psPCBThickness))
        yoff = (self._psPCBlength - PSK_S15C._pslength)/2.0
        xoff = self._psPCBMhOff+((self._psPCBpsw - PSK_S15C._pswidth)/2.0)+self._stripIncr
        psorigin = Base.Vector(ox+xoff,oy+yoff,oz+PCBwithStrips._psPCBThickness)
        self.powersupply = PSK_S15C(name+"_powersupply",psorigin)
        mhcd42orig = mhcd42HeaderOrig.add(Base.Vector(-MHCD42._headerX,-MHCD42._headerY,Pin._bodyheight))
        self.mhcd42 = MHCD42(name+"_mhcd42",mhcd42orig)
        mt3608CenterHX = (gndX1+gndX2)/2.0
        mt3608CenterHY = (yin+yout)/2.0
        mt3608CenterOrig = Base.Vector(ox+mt3608CenterHX,oy+mt3608CenterHY,oz+self._psPCBThickness+Pin._bodyheight)
        mt3608orig = mt3608CenterOrig.add(Base.Vector(-MT3608._width/2.0,
                                                      -MT3608._length/2.0,
                                                      0))
        self.mt3608 = MT3608(name+"_mt3608",mt3608orig)
        self.bypasscap = C333(name+"_bypasscap",Base.Vector(ox+self._bypassY,oy+self._bypassX,oz))
        self.filtercap = AL_CAP_Radial_5mm10x12_5(name+"_filtercap",
                            Base.Vector(ox+self._filterY,
                                        oy+self._filterX,
                                        oz+self._psPCBThickness))
        self.esd = DO_15_bendedLeads_400_under(name+"_esd",
                            Base.Vector(ox+self._esdY,
                                        oy+self._esdX,
                                        oz))
    def VAdjustY(self):
        return self.mt3608.origin.y+MT3608._vadjustYOff
    def VAdjustZ(self):
        return self.mt3608.origin.z+MT3608._vadjustZOff
    def KeyButtonY(self):
        return self.mhcd42.origin.y+MHCD42._keybuttonYOff
    def KeyButtonZ(self):
        return self.mhcd42.origin.z+MHCD42._keybuttonZOff
    def show(self):
        PCB2withStrips.show(self)
        self.mhcd42Header.show()
        self.mt3608vinM.show()
        self.mt3608vinP.show()
        self.mt3608voutM.show()
        self.mt3608voutP.show()
        self.powersupply.show()
        self.mhcd42.show()
        self.mt3608.show()
        self.bypasscap.show()
        self.filtercap.show()
        self.esd.show()

if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("test")
    doc = App.activeDocument()
    o = Base.Vector(0,0,0)
    pcb = PS2OnPCB("pcb2",o)
    pcb.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewIsometric()
