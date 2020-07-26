#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat Jul 25 16:31:39 2020
#  Last Modified : <200725.2027>
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

from abc import ABCMeta, abstractmethod, abstractproperty

class Pin(object):
    __metaclass__ = ABCMeta
    _totalPinLength  = 11.7
    _tailbelow       = 3.43
    _bodyheight      = 2.60
    _pinsquare       = 0.69
    _bodysquare      = 2.54
    

class Pin_AboveUp(Pin):
    def addPin(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        pinoffset = Base.Vector(-self._pinsquare/2.0,-self._pinsquare/2.0,-self._tailbelow)
        self.pins.append(Part.makePlane(self._pinsquare,self._pinsquare,origin.add(pinoffset)).extrude(Base.Vector(0,0,self._totalPinLength)))
        bodyoffset = Base.Vector(-self._bodysquare/2.0,-self._bodysquare/2.0,0)
        if self.body == None:
            self.body = Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight))
        else:
            self.body = self.body.fuse(Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight)))
        

class Pin_AboveDown(Pin):
    def addPin(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        pinoffset = Base.Vector(-self._pinsquare/2.0,-self._pinsquare/2.0,\
                -(self._totalPinLength-self._bodyheight-self._tailbelow))
        self.pins.append(Part.makePlane(self._pinsquare,self._pinsquare,origin.add(pinoffset)).extrude(Base.Vector(0,0,self._totalPinLength)))
        bodyoffset = Base.Vector(-self._bodysquare/2.0,-self._bodysquare/2.0,0)
        if self.body == None:
            self.body = Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight))
        else:
            self.body = self.body.fuse(Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight)))

class Pin_BelowUp(Pin):
    def addPin(self,origin):
        if not isinstance(origin,Base.Vector,boardthickness=1.6):
            raise RuntimeError("origin is not a Vector")
        origin = origin
        pinoffset = Base.Vector(-self._pinsquare/2.0,-self._pinsquare/2.0,\
                    -(self._tailbelow+self._bodyheight+boardthickness))
        self.pins.append(Part.makePlane(self._pinsquare,self._pinsquare,origin.add(pinoffset)).extrude(Base.Vector(0,0,self._totalPinLength)))
        bodyoffset = Base.Vector(-self._bodysquare/2.0,-self._bodysquare/2.0,-boardthickness)
        if self.body == None:
            self.body = Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight))
        else:
            self.body = self.body.fuse(Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight)))
        
class Pin_BelowDown(Pin):    
    def addPin(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        origin = origin
        pinoffset = Base.Vector(-self._pinsquare/2.0,-self._pinsquare/2.0,\
                    -(self._totalPinLength-self._tailbelow+boardthickness))
        self.pins.append(Part.makePlane(self._pinsquare,self._pinsquare,origin.add(pinoffset)).extrude(Base.Vector(0,0,self._totalPinLength)))
        bodyoffset = Base.Vector(-self._bodysquare/2.0,-self._bodysquare/2.0,-boardthickness)
        if self.body == None:
            self.body = Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight))
        else:
            self.body = self.body.fuse(Part.makePlane(self._bodysquare,self._bodysquare,origin.add(bodyoffset)).extrude(Base.Vector(0,0,self._bodyheight)))

class HeaderMixin(object):
    __metaclass__ = ABCMeta
    _rows  = 1
    _positions = 40
    _orientation = 'Horizontal'
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.pins = list()
        self.body = None
        if self._orientation == 'Horizontal':
            for ir in range(self._rows):
                roworigin = self.origin.add(Base.Vector(0,self._bodysquare*ir,0))
                for ip in range(self._positions):
                    pinorigin = roworigin.add(Base.Vector(self._bodysquare*ip,0,0))
                    self.addPin(pinorigin)
        elif self._orientation == 'Vertical':
            for ir in range(self._rows):
                roworigin = self.origin.add(Base.Vector(self._bodysquare*ir,0,0))
                for ip in range(self._positions):
                    pinorigin = roworigin.add(Base.Vector(0,self._bodysquare*ip,0))
                    self.addPin(pinorigin)
    def show(self):
        i = 1
        for pin in self.pins:
            pinname = self.name+('_pin%d'%i)
            doc = App.activeDocument()
            obj = doc.addObject("Part::Feature",pinname)
            obj.Shape = pin
            obj.Label=pinname
            obj.ViewObject.ShapeColor=tuple([.85,.85,.85])
            i += 1
        bodyname = self.name+'_body'
        obj = doc.addObject("Part::Feature",bodyname)
        obj.Shape = self.body
        obj.Label=bodyname
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])

class Header6_AboveDown(HeaderMixin,Pin_AboveDown):
    _positions = 6
    def __init__(self,name,origin):
        HeaderMixin.__init__(self,name,origin)

class Header1_AboveDown(HeaderMixin,Pin_AboveDown):
    _positions = 1
    def __init__(self,name,origin):
        HeaderMixin.__init__(self,name,origin)

if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("test")
    doc = App.activeDocument()
    o = Base.Vector(0,0,0)
    header = Header1_AboveDown("header",o)
    header.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewIsometric()
