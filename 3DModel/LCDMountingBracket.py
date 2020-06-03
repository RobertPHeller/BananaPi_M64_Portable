#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Jun 2 22:09:45 2020
#  Last Modified : <200603.0146>
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

from LCDScreen import *

class BracketAngleDims(object):
    _AngleHeight = (1.0/2.0)*25.4
    def AngleHeight(self):
        return BracketAngleDims._AngleHeight
    _AngleWidth = (1.0/2.0)*25.4
    def AngleWidth(self):
        return BracketAngleDims._AngleWidth
    _AngleThickness = (1.0/16.0)*25.4
    def AngleThickness(self):
        return BracketAngleDims._AngleThickness
    _AngleLength = 222.0
    def AngleLength(self):
        return BracketAngleDims._AngleLength
    _BRACKET_r = 3.5 / 2.0
    def BRACKET_r(self):
        return BracketAngleDims._BRACKET_r
    _BRACKET_z = (1.0/4.0)*25.4
    def BRACKET_z(self):
        return BracketAngleDims._BRACKET_z
    def __init__(self):
        raise RuntimeError("No Instances allowed for BracketAngleDims!")

class LCDMountingBracket(LCDDims,BracketAngleDims):
    _AngleNotchDX = 4
    def AngleNotchDX(self):
        return LCDMountingBracket._AngleNotchDX
    _AngleNotchDY1 = LCDDims._M3_y+1.0
    def AngleNotchDY1(self):
        return LCDMountingBracket._AngleNotchDY1
    _AngleNotchDY2 = LCDDims._M2_y-2.0
    def AngleNotchDY2(self):
        return LCDMountingBracket._AngleNotchDY2
    def __init__(self,name,origin,side='L'):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        bracketPoly = list()
        bracketPoly.append(Base.Vector(ox,oy,oz))
        self.bracketmh = dict()
        if side == 'L':
            x = ox
            y = oy+self.AngleLength()
            bracketPoly.append(Base.Vector(x,y,oz))
            x -= self.AngleWidth()
            bracketPoly.append(Base.Vector(x,y,oz))
            y -= self.AngleNotchDY2()
            bracketPoly.append(Base.Vector(x,y,oz))
            x += self.AngleNotchDX()
            bracketPoly.append(Base.Vector(x,y,oz))
            y -= (self.AngleNotchDY1()-self.AngleNotchDY2())
            bracketPoly.append(Base.Vector(x,y,oz))
            x -= self.AngleNotchDX()
            bracketPoly.append(Base.Vector(x,y,oz))
            y -= (self.AngleLength() - self.AngleNotchDY1())
            bracketPoly.append(Base.Vector(x,y,oz))
            bracketPoly.append(Base.Vector(ox,oy,oz))
            angle_a = Part.Face(Part.Wire(Part.makePolygon(bracketPoly)))
            self.bracketmh[1] = origin.add(Base.Vector(-self.BRACKET_z(),self.M1_y(),0))
            self.bracketmh[2] = origin.add(Base.Vector(-self.BRACKET_z(),self.M2_y(),0))
            self.bracketmh[3] = origin.add(Base.Vector(-self.BRACKET_z(),self.M3_y(),0))
            self.bracketmh[4] = origin.add(Base.Vector(-self.BRACKET_z(),self.M4_y(),0))
            extrude_b = Base.Vector(-self.AngleThickness(),0,0)
        elif side == 'R':
            x = ox
            y = oy+self.AngleLength()
            bracketPoly.append(Base.Vector(x,y,oz))
            x += self.AngleWidth()
            bracketPoly.append(Base.Vector(x,y,oz))
            y -= self.AngleNotchDY2()
            bracketPoly.append(Base.Vector(x,y,oz))
            x -= self.AngleNotchDX()
            bracketPoly.append(Base.Vector(x,y,oz))
            y -= (self.AngleNotchDY1()-self.AngleNotchDY2())
            bracketPoly.append(Base.Vector(x,y,oz))
            x += self.AngleNotchDX()
            bracketPoly.append(Base.Vector(x,y,oz))
            y -= (self.AngleLength() - self.AngleNotchDY1())
            bracketPoly.append(Base.Vector(x,y,oz))
            bracketPoly.append(Base.Vector(ox,oy,oz))
            angle_a = Part.Face(Part.Wire(Part.makePolygon(bracketPoly)))
            self.bracketmh[1] = origin.add(Base.Vector(self.BRACKET_z(),self.M1_y(),0))
            self.bracketmh[2] = origin.add(Base.Vector(self.BRACKET_z(),self.M2_y(),0))
            self.bracketmh[3] = origin.add(Base.Vector(self.BRACKET_z(),self.M3_y(),0))
            self.bracketmh[4] = origin.add(Base.Vector(self.BRACKET_z(),self.M4_y(),0))
            extrude_b = Base.Vector(self.AngleThickness(),0,0)
        else:        
            raise RuntimeError("side must be L or R!")
        borig=origin.add(Base.Vector(0,self.AngleLength(),-self.AngleHeight()))
        angle_b = Part.makePlane(self.AngleHeight(),
                                 self.AngleLength(),
                                 borig,
                                 Base.Vector(1,0,0))
        self.lcdmh = dict()
        self.lcdmh[1] = origin.add(Base.Vector(0,self.M1_y(),-self.M_x()))
        self.lcdmh[2] = origin.add(Base.Vector(0,self.M2_y(),-self.M_x()))
        self.lcdmh[3] = origin.add(Base.Vector(0,self.M3_y(),-self.M_x()))
        self.lcdmh[4] = origin.add(Base.Vector(0,self.M4_y(),-self.M_x()))
        #self.mhFaces = dict()
        for i in [1,2,3,4]:
            bmhFace = Part.Face(Part.Wire(Part.makeCircle(self.BRACKET_r(),self.bracketmh[i])))
            angle_a = angle_a.cut(bmhFace)
            mhFace = Part.Face(Part.Wire(Part.makeCircle(self.M_r(),self.lcdmh[i],Base.Vector(1,0,0))))
            angle_b = angle_b.cut(mhFace)
            #self.mhFaces[i] = mhFace.extrude(extrude_b)
        extrude_a = Base.Vector(0,0,-self.AngleThickness())
        self.bracket = angle_a.extrude(extrude_a)
        self.bracket = self.bracket.fuse(angle_b.extrude(extrude_b))
    def show(self):
        #for i in [1,2,3,4]:
        #    Part.show(self.mhFaces[i])
        doc = App.activeDocument()
        Part.show(self.bracket)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([.75,.75,.75])
    def MountingHole(self,i,zBase,height):
        bracketmh = self.bracketmh[i]
        bracketmh = Base.Vector(bracketmh.x,bracketmh.y,zBase)
        extrude_mh = Base.Vector(0,0,height)
        return Part.Face(Part.Wire(Part.makeCircle(self.BRACKET_r(),bracketmh))).extrude(extrude_mh)