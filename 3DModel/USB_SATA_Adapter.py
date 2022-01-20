#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Wed Jun 3 21:18:32 2020
#  Last Modified : <200606.1915>
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

import sys

class USB_SATA_Adapter_(object):
    _OverallLength     = 62.68
    _Adapter_BoardPoly = [(9.44,15.94,0), (28.15,15.94,0), (28.15,62.85,0), (0,62.85,0), (0,50.21,0), (9.44,28.12,0), (9.44,15.94,0)]
    _RotateOffset      = -(28.15+10)
    _BoardThick        = 1.73
    _USBPlug_XOff      = 14.85
    _USBPlug_YOff      = 0
    _USBPlug_Width     = 12.03
    _USBPlug_Length    = 18.84
    _USBPlug_Height    = 4.57
    @staticmethod
    def _createPolygon(origin,pointTupleList,extrudeVector):
        polypoints = list()
        for tup in pointTupleList:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        return Part.Face(Part.Wire(Part.makePolygon(polypoints))
                        ).extrude(extrudeVector)
    @staticmethod
    def _createPolygonR_90(origin,pointTupleList,extrudeVector):
        polypoints = list()
        for tup in pointTupleList:
            x,y,z = tup
            polypoints.append(Base.Vector(x,y,z))
        polygon = Part.Face(Part.Wire(Part.makePolygon(polypoints)))
        #print >>sys.stderr, "*** USB_SATA_Adapter_._createPolygonR_90(): polygon verts are:"
        #for V in polygon.Vertexes:
        #    print >>sys.stderr, "*** -- ",V.X,V.Y,V.Z
        polygon.translate(Base.Vector(USB_SATA_Adapter_._RotateOffset,0,0))
        #print >>sys.stderr, "*** USB_SATA_Adapter_._createPolygonR_90(): polygon verts (after translate) are:"
        #for V in polygon.Vertexes:
        #    print >>sys.stderr, "*** -- ",V.X,V.Y,V.Z
        polygon.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),-90)
        #print >>sys.stderr, "*** USB_SATA_Adapter_._createPolygonR_90(): polygon verts (after rotate) are:"
        #for V in polygon.Vertexes:
        #    print >>sys.stderr, "*** -- ",V.X,V.Y,V.Z
        polygon.translate(origin)
        #print >>sys.stderr, "*** USB_SATA_Adapter_._createPolygonR_90(): polygon verts (after translate 2) are:"
        #for V in polygon.Vertexes:
        #    print >>sys.stderr, "*** -- ",V.X,V.Y,V.Z
        return polygon.extrude(extrudeVector)    
    def __init__(self):
        raise RuntimeError("No instances allowed for USB_SATA_Adapter_!")
        
class USB_SATA_Adapter(USB_SATA_Adapter_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        bthick = Base.Vector(0,0,USB_SATA_Adapter_._BoardThick)
        self.board = USB_SATA_Adapter_._createPolygon(origin,
                                                      USB_SATA_Adapter_._Adapter_BoardPoly,
                                                      bthick)
        usbplug_orig = origin.add(Base.Vector(USB_SATA_Adapter_._USBPlug_XOff,
                                              USB_SATA_Adapter_._USBPlug_YOff,
                                              0))
        self.usbplug = Part.makePlane(USB_SATA_Adapter_._USBPlug_Width,
                                      USB_SATA_Adapter_._USBPlug_Length,
                                      usbplug_orig
                                     ).extrude(Base.Vector(0,0,USB_SATA_Adapter_._USBPlug_Height))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_board")
        obj.Shape = self.board
        obj.Label=self.name+"_board"
        obj.ViewObject.ShapeColor=tuple([128/255.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_usbplug")
        obj.Shape = self.usbplug
        obj.Label=self.name+"_usbplug"
        obj.ViewObject.ShapeColor=tuple([.95,.95,.95])
        

class USB_SATA_Adapter_Horiz(USB_SATA_Adapter_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        bthick = Base.Vector(0,0,USB_SATA_Adapter_._BoardThick)
        self.board = USB_SATA_Adapter_._createPolygonR_90(origin,
                                                      USB_SATA_Adapter_._Adapter_BoardPoly,
                                                      bthick)
        usbplug_orig = origin.add(Base.Vector(USB_SATA_Adapter_._USBPlug_YOff,
                                              USB_SATA_Adapter_._USBPlug_XOff,
                                              0))
        self.usbplug = Part.makePlane(USB_SATA_Adapter_._USBPlug_Length,
                                      USB_SATA_Adapter_._USBPlug_Width,
                                      usbplug_orig
                                     ).extrude(Base.Vector(0,0,USB_SATA_Adapter_._USBPlug_Height))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_board")
        obj.Shape = self.board
        obj.Label=self.name+"_board"
        obj.ViewObject.ShapeColor=tuple([128/255.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_usbplug")
        obj.Shape = self.usbplug
        obj.Label=self.name+"_usbplug"
        obj.ViewObject.ShapeColor=tuple([.95,.95,.95])
        

class USB_SATA_Adapter_BoardCradleHoriz(object):
    _Upper_Poly = [(0,25.06,2.54), (12.180000,25.06,2.54), 
                   (34.270000,34.5,2.54), (46.91,34.5,2.54), 
                   (46.91,40.85,2.54), (0,40.85,2.54), (0,25.06,2.54)]
    _LowerRect_Width = 6.35
    _Length = 46.91
    _Width = 40.85
    _UnderThick = 2.54
    _CradleThick = 1.7
    _mh1X = 23.455
    _mh1Y = 33
    _mh2X = 11.7275
    _mh2Y = 3.175
    _mh3X = 35.18250
    _mh3Y = 3.175
    _mhdia = 3.5
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        underthick = Base.Vector(0,0,self._UnderThick)
        self.body = Part.makePlane(self._Length,
                                   self._Width,
                                   origin).extrude(underthick)
        polypoints = list()
        for tup in self._Upper_Poly:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        extrudevect = Base.Vector(0,0,self._CradleThick)
        uf = Part.Face(Part.Wire(Part.makePolygon(polypoints))
                        ).extrude(extrudevect)
        self.body = self.body.fuse(uf)
        lf = Part.makePlane(self._Length,
                            self._LowerRect_Width,
                            origin.add(underthick)).extrude(extrudevect)
        self.body = self.body.fuse(lf)
        mrad = self._mhdia / 2.0
        mhHeight = Base.Vector(0,0,self._UnderThick+self._CradleThick)
        self.mh = dict()
        self.mh[1] = origin.add(Base.Vector(self._mh1X,self._mh1Y,0))
        self.mh[2] = origin.add(Base.Vector(self._mh2X,self._mh2Y,0))
        self.mh[3] = origin.add(Base.Vector(self._mh3X,self._mh3Y,0))
        for i in [1,2,3]:
            hole = Part.Face(Part.Wire(Part.makeCircle(mrad,self.mh[i]))
                            ).extrude(mhHeight)
            self.body = self.body.cut(hole)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.body
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        mrad = self._mhdia/2.0
        face = Part.Face(Part.Wire(Part.makeCircle(mrad,mh)))
        return face.extrude(Base.Vector(0,0,panelThick))

if __name__ == '__main__':
    x = USB_SATA_Adapter_BoardCradleHoriz("foocradle",Base.Vector(0,0,0))
    x.show()
