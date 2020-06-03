#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Jun 2 18:44:55 2020
#  Last Modified : <200602.2003>
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

class DCDC_5_12_(object):
    _width = 31.75
    def Width(self):
        return DCDC_5_12_._width
    _height = 45.720
    def Height(self):
        return DCDC_5_12_._height
    _holeEdgeOffset = 3.81
    def HoleEdgeOffset(self):
        return DCDC_5_12_._holeEdgeOffset
    _holeHSpacing = 29.21
    def HoleHSpacing(self):
        return DCDC_5_12_._holeHSpacing
    _holeWSpacing = 24.13
    def HoleWSpacing(self):
        return DCDC_5_12_._holeWSpacing
    _holeDia = 2.7
    def HoleDia(self):
        return DCDC_5_12_._holeDia
    _boardthickness = 1.6
    def Boardthickness(self):
        return DCDC_5_12_._boardthickness
    def __init__(self):
        raise RuntimeError("No Instances allowed for DCDC_5_12_!")

class DCDC_5_12_Vert12Down(DCDC_5_12_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        bthick = Base.Vector(0,0,self.Boardthickness())
        self.board = Part.makePlane(self.Width(),self.Height(),origin
                                   ).extrude(bthick)
        self.mh = dict()
        mh1x = origin.x + self.HoleEdgeOffset()
        mh1y = origin.y + self.HoleEdgeOffset()
        self.mh[1] = Base.Vector(mh1x,mh1y,origin.z)
        mh2x = mh1x + self.HoleWSpacing()
        mh2y = mh1y
        self.mh[2] = Base.Vector(mh2x,mh2y,origin.z)
        mh3x = mh2x
        mh3y = mh2y + self.HoleHSpacing()
        self.mh[3] = Base.Vector(mh3x,mh3y,origin.z)
        mh4x = mh1x
        mh4y = mh3y
        self.mh[4] = Base.Vector(mh4x,mh4y,origin.z)
        mhrad = self.HoleDia()/2.0
        for i in [1,2,3,4]:
            mho = self.mh[i]
            mhf = Part.Face(Part.Wire(Part.makeCircle(mhrad,mho)))
            self.board = self.board.cut(mhf.extrude(bthick))
    def MountingHole(self,i,zBase,panelThick):
        mho = self.mh[i]
        mho = Base.Vector(mho.x,mho.y,zBase)
        mhrad = self.HoleDia()/2.0
        pthick = Base.Vector(0,0,panelThick)
        return  Part.Face(Part.Wire(Part.makeCircle(mhrad,mho))).extrude(pthick)
    def Standoff(self,i,zBase,height,diameter):
        mho = self.mh[i]
        mho = Base.Vector(mho.x,mho.y,zBase)
        srad = diameter/2.0
        hvect = Base.Vector(0,0,height)
        return  Part.Face(Part.Wire(Part.makeCircle(srad,mho))).extrude(hvect)
    def show(self):
        Part.show(self.board)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([210/255.0,180/255.0,140/255.0])        

class DCDC_5_12_Horiz12Right(DCDC_5_12_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        bthick = Base.Vector(0,0,self.Boardthickness())
        self.board = Part.makePlane(self.Height(),self.Width(),origin
                                   ).extrude(bthick)
        self.mh = dict()
        mh1x = origin.x + (self.Height()-self.HoleEdgeOffset())
        mh1y = origin.y + self.HoleEdgeOffset()
        self.mh[1] = Base.Vector(mh1x,mh1y,origin.z)
        mh2x = mh1x - self.HoleHSpacing()
        mh2y = mh1y
        self.mh[2] = Base.Vector(mh2x,mh2y,origin.z)
        mh3x = mh2x
        mh3y = mh2y + self.HoleWSpacing()
        self.mh[3] = Base.Vector(mh3x,mh3y,origin.z)
        mh4x = mh1x
        mh4y = mh3y
        self.mh[4] = Base.Vector(mh4x,mh4y,origin.z)
        mhrad = self.HoleDia()/2.0
        for i in [1,2,3,4]:
            mho = self.mh[i]
            mhf = Part.Face(Part.Wire(Part.makeCircle(mhrad,mho)))
            self.board = self.board.cut(mhf.extrude(bthick))
    def MountingHole(self,i,zBase,panelThick):
        mho = self.mh[i]
        mho = Base.Vector(mho.x,mho.y,zBase)
        mhrad = self.HoleDia()/2.0
        pthick = Base.Vector(0,0,panelThick)
        return  Part.Face(Part.Wire(Part.makeCircle(mhrad,mho))).extrude(pthick)
    def Standoff(self,i,zBase,diameter,height):
        mho = self.mh[i]
        mho = Base.Vector(mho.x,mho.y,zBase)
        srad = diameter/2.0
        hvect = Base.Vector(0,0,height)
        return  Part.Face(Part.Wire(Part.makeCircle(srad,mho))).extrude(hvect)
    def show(self):
        Part.show(self.board)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([210/255.0,180/255.0,140/255.0])        

