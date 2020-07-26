#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun May 31 08:03:12 2020
#  Last Modified : <200726.1431>
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

## Power Supply: Mouser #490-PSK-S15C-5
# PCB mount, 28.8mm wide 53.8mm long, 23.5mm high

class PSK_S15C(object):
    _pswidth = 28.8
    _pslength = 53.8
    _psheight = 23.5
    _pspindia = 1.0
    _pspinlength = 6.0
    _pspin1Xoff = ((53.8-45.72)/2.0)+45.72
    _pspin1Yoff = ((28.8-20.32)/2.0)+20.32
    _pspin2Xoff = ((53.8-45.72)/2.0)+45.72
    _pspin2Yoff = (28.8-20.32)/2.0
    _pspin3Xoff = (53.8-45.72)/2.0
    _pspin3Yoff = ((28.8-20.32)/2.0)+10.16
    _pspin4Xoff = (53.8-45.72)/2.0
    _pspin4Yoff = ((28.8-20.32)/2.0)+20.32
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        bodysurf = Part.makePlane(PSK_S15C._pswidth,
                                  PSK_S15C._pslength,
                                  origin)
        self.body = bodysurf.extrude(Base.Vector(0,0,PSK_S15C._psheight))
        self.pin1 = Part.Face(Part.Wire(Part.makeCircle(PSK_S15C._pspindia/2.0,Base.Vector(ox+PSK_S15C._pspin1Yoff,oy+PSK_S15C._pspin1Xoff,oz)))).extrude(Base.Vector(0,0,-PSK_S15C._pspinlength))
        self.pin2 = Part.Face(Part.Wire(Part.makeCircle(PSK_S15C._pspindia/2.0,Base.Vector(ox+PSK_S15C._pspin2Yoff,oy+PSK_S15C._pspin2Xoff,oz)))).extrude(Base.Vector(0,0,-PSK_S15C._pspinlength))
        self.pin3 = Part.Face(Part.Wire(Part.makeCircle(PSK_S15C._pspindia/2.0,Base.Vector(ox+PSK_S15C._pspin3Yoff,oy+PSK_S15C._pspin3Xoff,oz)))).extrude(Base.Vector(0,0,-PSK_S15C._pspinlength))
        self.pin4 = Part.Face(Part.Wire(Part.makeCircle(PSK_S15C._pspindia/2.0,Base.Vector(ox+PSK_S15C._pspin4Yoff,oy+PSK_S15C._pspin4Xoff,oz)))).extrude(Base.Vector(0,0,-PSK_S15C._pspinlength))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_Body')
        obj.Shape = self.body
        obj.Label=self.name+'_Body'
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_Pin1')
        obj.Shape = self.pin1
        obj.Label=self.name+'_Pin1'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_Pin2')
        obj.Shape = self.pin2
        obj.Label=self.name+'_Pin2'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_Pin3')
        obj.Shape = self.pin3
        obj.Label=self.name+'_Pin3'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_Pin4')
        obj.Shape = self.pin4
        obj.Label=self.name+'_Pin4'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])

class MHCD42(object):
    _width = 16
    _length = 25
    _boardthickness = 1.6
    _height = 4.5
    _headerY = 2.0
    _headerX = 1.65
    _headerHoleDia = .95
    _headholePadTypes = ['R','O','O','R','O','R']
    _headholePadNames = ['Vin','Gnd','Gnd','Bat','Gnd','Vout']
    _padsizeX = 1.5748
    _padsizeY = 2.286
    _padThick = .1
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        boardthick = Base.Vector(0,0,self._boardthickness)
        padthick   = Base.Vector(0,0,self._padThick)
        self.board = Part.makePlane(self._width,self._length,self.origin).extrude(boardthick)
        headholeX = self._headerX+ox
        headholeY = self._headerY+oy
        headholeRadius = self._headerHoleDia/2.0
        self.pads = list()
        for holePadType in self._headholePadTypes:
            holeorig = Base.Vector(headholeX,headholeY,oz)
            self.board = \
               self.board.cut(Part.Face(Part.Wire(Part.makeCircle(\
                            headholeRadius,holeorig))).extrude(boardthick))
            if holePadType == 'R':
                padOrigin = holeorig.add(Base.Vector(-self._padsizeX/2,\
                                                     -self._padsizeY/2,\
                                                     self._boardthickness))
                padsurf = Part.makePlane(self._padsizeX,self._padsizeY,padOrigin)
            elif holePadType == 'O':
                padOrigin = holeorig.add(Base.Vector(0,0,self._boardthickness))
                S1 = padOrigin.add(Base.Vector(0,self._padsizeY/2,0))
                S2 = padOrigin.add(Base.Vector(self._padsizeX/2,0,0))
                padsurf = Part.Face(Part.Wire(Part.Edge(Part.Ellipse(S1,S2,padOrigin))))
            h = Part.Face(Part.Wire(Part.makeCircle(headholeRadius,holeorig.add(Base.Vector(0,0,self._boardthickness))))).extrude(padthick)
            self.pads.append(padsurf.extrude(padthick).cut(h))
            headholeX += 2.54
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_Board')
        obj.Shape = self.board
        obj.Label=self.name+'_Board'
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        for p,n in zip(self.pads,self._headholePadNames):
            padname = self.name+'_pad_'+n
            obj = doc.addObject("Part::Feature",padname)
            obj.Shape = p
            obj.Label=padname
            obj.ViewObject.ShapeColor=tuple([.9,.9,.5])
        
class MT3608(object):
    _width = 17.34
    _length = 37.34
    _boardthickness = 1.2
    _height = 6.42
    _minusXoff = 5.18
    _plusXoff  = 12
    _inYoff    = 3.05
    _outYOff   = 33.35
    _padHoleDia = 1.95
    _padsizeX  = 3.36
    _padsizeY  = 5.08
    _padThick  = .1
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        boardthick = Base.Vector(0,0,self._boardthickness)
        self.board = Part.makePlane(self._width,self._length,self.origin).extrude(boardthick)
        self.vinM = self._padHole(self._minusXoff,self._inYoff)
        self.vinP = self._padHole(self._plusXoff,self._inYoff)
        self.voutM = self._padHole(self._minusXoff,self._outYOff)
        self.voutP = self._padHole(self._plusXoff,self._outYOff)
    def _padHole(self,x,y):
        holeorig = self.origin.add(Base.Vector(x,y,0))
        holethick = Base.Vector(0,0,self._boardthickness+self._padThick)
        hole = Part.Face(Part.Wire(Part.makeCircle(self._padHoleDia/2,holeorig))).extrude(holethick)
        self.board = self.board.cut(hole)
        padorig = holeorig.add(Base.Vector(-self._padsizeX/2,-self._padsizeY/2,self._boardthickness))
        pad = Part.makePlane(self._padsizeX,self._padsizeY,padorig).extrude(Base.Vector(0,0,self._padThick))
        return (pad.cut(hole))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_Board')
        obj.Shape = self.board
        obj.Label=self.name+'_Board'
        obj.ViewObject.ShapeColor=tuple([0.0,0.5,.75])
        obj = doc.addObject("Part::Feature",self.name+'_vinM')
        obj.Shape = self.vinM
        obj.Label=self.name+'_vinM'
        obj.ViewObject.ShapeColor=tuple([.9,.9,.9])
        obj = doc.addObject("Part::Feature",self.name+'_vinP')
        obj.Shape = self.vinP
        obj.Label=self.name+'_vinP'
        obj.ViewObject.ShapeColor=tuple([.9,.9,.9])
        obj = doc.addObject("Part::Feature",self.name+'_voutM')
        obj.Shape = self.voutM
        obj.Label=self.name+'_voutM'
        obj.ViewObject.ShapeColor=tuple([.9,.9,.9])
        obj = doc.addObject("Part::Feature",self.name+'_voutP')
        obj.Shape = self.voutP
        obj.Label=self.name+'_voutP'
        obj.ViewObject.ShapeColor=tuple([.9,.9,.9])

if __name__ == '__main__':
     App.ActiveDocument=App.newDocument("test")
     doc = App.activeDocument()
     o = Base.Vector(0,0,0)
     ps = MT3608("MT3608",o)
     ps.show()
     Gui.SendMsgToActiveView("ViewFit")
