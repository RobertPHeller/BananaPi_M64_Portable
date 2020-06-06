#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Jun 2 22:09:55 2020
#  Last Modified : <200606.1937>
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

class HDMIConverterDims(object):
    _mainboardWidth = 139
    def mainboardWidth(self):
        return HDMIConverterDims._mainboardWidth
    _mainboardHeight = 58
    def mainboardHeight(self):
        return HDMIConverterDims._mainboardHeight
    _mainBoardMHDia = 3.5
    def mainBoardMHDia(self):
        return HDMIConverterDims._mainBoardMHDia
    _mainboardMH1_x = 124.47 + (3.5/2.0)
    def mainboardMH1_x(self):
        return HDMIConverterDims._mainboardMH1_x
    _mainboardMH1_y = 19.24 + (3.5/2.0)
    def mainboardMH1_y(self):
        return HDMIConverterDims._mainboardMH1_y
    _mainboardMH2_x = 123.03 + (3.5/2.0)
    def mainboardMH2_x(self):
        return HDMIConverterDims._mainboardMH2_x
    _mainboardMH2_y = 47.32 + (3.5/2.0)
    def mainboardMH2_y(self):
        return HDMIConverterDims._mainboardMH2_y
    _mainboardMH3_x = 12.36 + (3.5/2.0)
    def mainboardMH3_x(self):
        return HDMIConverterDims._mainboardMH3_x
    _mainboardMH3_y = 19.24 + (3.5/2.0)
    def mainboardMH3_y(self):
        return HDMIConverterDims._mainboardMH3_y
    _mainboardMH4_x = 18.07 + (3.5/2.0)
    def mainboardMH4_x(self):
        return HDMIConverterDims._mainboardMH4_x
    _mainboardMH4_y = 47.32 + (3.5/2.0)
    def mainboardMH4_y(self):
        return HDMIConverterDims._mainboardMH4_y
    _buttonboardWidth = 104.13
    def buttonboardWidth(self):
        return HDMIConverterDims._buttonboardWidth
    _buttonboardHeight = 21.87
    def buttonboardHeight(self):
        return HDMIConverterDims._buttonboardHeight
    _buttonboardMHDia = 3.32
    def buttonboardMHDia(self):
        return HDMIConverterDims._buttonboardMHDia
    _buttonboardMH1_x = 8.2 + (3.32/2.0)
    def buttonboardMH1_x(self):
        return HDMIConverterDims._buttonboardMH1_x
    _buttonboardMH1_y = 6 + (3.32/2.0)
    def buttonboardMH1_y(self):
        return HDMIConverterDims._buttonboardMH1_y
    _buttonboardMH2_x = 92.7 + (3.32/2.0)
    def buttonboardMH2_x(self):
        return HDMIConverterDims._buttonboardMH2_x
    _buttonboardMH2_y = 6 + (3.32/2.0)
    def buttonboardMH2_y(self):
        return HDMIConverterDims._buttonboardMH2_y
    _hvpowerboardWidth = 119.73
    def hvpowerboardWidth(self):
        return HDMIConverterDims._hvpowerboardWidth
    _hvpowerboardHeight = 23.24
    def hvpowerboardHeight(self):
        return HDMIConverterDims._hvpowerboardHeight
    _hvpowerboardMHDia = 3.5
    def hvpowerboardMHDia(self):
        return HDMIConverterDims._hvpowerboardMHDia
    _hvpowerboardMH2_x = 114.22 + (3.5/2.0)
    def hvpowerboardMH2_x(self):
        return HDMIConverterDims._hvpowerboardMH2_x
    _hvpowerboardMH2_y = 2.2 + (3.5/2.0)
    def hvpowerboardMH2_y(self):
        return HDMIConverterDims._hvpowerboardMH2_y
    _hvpowerboardMH1_x1 = 2.73
    def hvpowerboardMH1_x1(self):
        return HDMIConverterDims._hvpowerboardMH1_x1
    _hvpowerboardMH1_wide = 14.25
    def hvpowerboardMH1_wide(self):
        return HDMIConverterDims._hvpowerboardMH1_wide
    _hvpowerboardMH1_y = 2.0
    def hvpowerboardMH1_y(self):
        return HDMIConverterDims._hvpowerboardMH1_y
    _boardthickness = 1.5
    def boardthickness(self):
        return HDMIConverterDims._boardthickness
    def __init__(self):
        raise RuntimeError("No Instances allowed for HDMIConverterDims!")

class HDMIConverterMainBoard(HDMIConverterDims):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        boardthick = Base.Vector(0,0,self.boardthickness())
        self.board = Part.makePlane(self.mainboardWidth(),
                                    self.mainboardHeight(),
                                    origin).extrude(boardthick)
        self.mh = dict()
        self.mh[1] = Base.Vector(origin.x+self.mainboardMH1_x(),
                                 origin.y+self.mainboardMH1_y(),
                                 origin.z)
        self.mh[2] = Base.Vector(origin.x+self.mainboardMH2_x(),
                                 origin.y+self.mainboardMH2_y(),
                                 origin.z)
        self.mh[3] = Base.Vector(origin.x+self.mainboardMH3_x(),
                                 origin.y+self.mainboardMH3_y(),
                                 origin.z)
        self.mh[4] = Base.Vector(origin.x+self.mainboardMH4_x(),
                                 origin.y+self.mainboardMH4_y(),
                                 origin.z)
        mrad = self.mainBoardMHDia()/2.0
        for i in [1,2,3,4]:
            mhFace = Part.Face(Part.Wire(Part.makeCircle(mrad,self.mh[i])))
            self.board = self.board.cut(mhFace.extrude(boardthick))
    def show(self):
        doc = App.activeDocument()                                              
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.board
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        thick = Base.Vector(0,0,panelThick)
        mrad = self.mainBoardMHDia()/2.0
        return Part.Face(Part.Wire(Part.makeCircle(mrad,mh))).extrude(thick)
    def Standoff(self,i,zBase,height,diameter):
        soff = self.mh[i] 
        soff = Base.Vector(soff.x,soff.y,zBase)
        stall = Base.Vector(0,0,height)
        srad = diameter/2.0
        return Part.Face(Part.Wire(Part.makeCircle(srad,soff))).extrude(stall)

class HDMIButtonBoard_Upsidedown(HDMIConverterDims):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        boardthick = Base.Vector(0,0,-self.boardthickness())
        self.board = Part.makePlane(self.buttonboardWidth(),
                                    self.buttonboardHeight(),
                                    origin).extrude(boardthick)
        self.mh = dict()
        self.mh[1] = Base.Vector(origin.x+self.buttonboardMH1_x(),
                                 (origin.y+self.buttonboardHeight())-self.buttonboardMH1_y(),
                                 origin.z)
        self.mh[2] = Base.Vector(origin.x+self.buttonboardMH2_x(),
                                 (origin.y+self.buttonboardHeight())-self.buttonboardMH2_y(),
                                 origin.z)
        mrad = self.buttonboardMHDia()/2.0
        for i in [1,2]:
            mhFace = Part.Face(Part.Wire(Part.makeCircle(mrad,self.mh[i])))
            self.board = self.board.cut(mhFace.extrude(boardthick))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.board
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([255/255.0,165/255.0,79/255.0])
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        thick = Base.Vector(0,0,panelThick)
        mrad = self.buttonboardMHDia()/2.0
        return Part.Face(Part.Wire(Part.makeCircle(mrad,mh))).extrude(thick)
    def Standoff(self,i,zBase,height,diameter):
        soff = self.mh[i] 
        soff = Base.Vector(soff.x,soff.y,zBase)
        stall = Base.Vector(0,0,height)
        srad = diameter/2.0
        return Part.Face(Part.Wire(Part.makeCircle(srad,soff))).extrude(stall)


        
class HDMIHVPowerBoard_Upsidedown(HDMIConverterDims):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        boardthick = Base.Vector(0,0,-self.boardthickness())
        self.board = Part.makePlane(self.hvpowerboardWidth(),
                                    self.hvpowerboardHeight(),
                                    origin).extrude(boardthick)
        self.mh = dict()
        mrad = self.hvpowerboardMHDia()/2.0
        slot_x = origin.x+self.hvpowerboardMH1_x1()
        slot_y = (origin.y+self.hvpowerboardHeight())-self.hvpowerboardMH1_y()-self.hvpowerboardMHDia()
        self.mh[1] = Base.Vector(slot_x+(self.hvpowerboardMH1_wide()/2.0),
                                 slot_y+mrad,
                                 origin.z)
        self.mh[2]= Base.Vector(origin.x+self.hvpowerboardMH2_x(),
                                (origin.y+self.hvpowerboardHeight())-self.hvpowerboardMH2_y(),
                                origin.z)
        slotorig=Base.Vector(slot_x,slot_y,origin.z)
        slot=Part.makePlane(self.hvpowerboardMH1_wide(),
                            self.hvpowerboardMHDia(),
                            slotorig).extrude(boardthick)
        self.board = self.board.cut(slot)
        mh2Face = Part.Face(Part.Wire(Part.makeCircle(mrad,self.mh[2])))
        self.board = self.board.cut(mh2Face.extrude(boardthick))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.board
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def MountingHole(self,i,zBase,panelThick):
        mh = self.mh[i]
        mh = Base.Vector(mh.x,mh.y,zBase)
        thick = Base.Vector(0,0,panelThick)
        mrad = self.hvpowerboardMHDia()/2.0
        return Part.Face(Part.Wire(Part.makeCircle(mrad,mh))).extrude(thick)
    def Standoff(self,i,zBase,height,diameter):
        soff = self.mh[i] 
        soff = Base.Vector(soff.x,soff.y,zBase)
        stall = Base.Vector(0,0,height)
        srad = diameter/2.0
        return Part.Face(Part.Wire(Part.makeCircle(srad,soff))).extrude(stall)
        
                                

