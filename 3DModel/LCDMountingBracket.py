#!/usr/local/bin/FreeCAD018
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
#  Last Modified : <200610.1632>
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



import Part, TechDraw
from FreeCAD import Base
import FreeCAD as App

import os
import sys
sys.path.append(os.path.dirname(__file__))

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
        self.bracketPoly = bracketPoly
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
        self._mapPolyVerts()
        self._mapBMHoleEdges()
        self._mapLCDMHoleEdges()
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.bracket
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])
    def MountingHole(self,i,zBase,height):
        bracketmh = self.bracketmh[i]
        bracketmh = Base.Vector(bracketmh.x,bracketmh.y,zBase)
        extrude_mh = Base.Vector(0,0,height)
        return Part.Face(Part.Wire(Part.makeCircle(self.BRACKET_r(),bracketmh))).extrude(extrude_mh)
    def _mapPolyVerts(self):
        self.polyVertexMap = list()
        for p in self.bracketPoly:
            i = 0
            for v in self.bracket.Vertexes:
                if v.X == p.x and v.Y == p.y and v.Z == p.z:
                   self.polyVertexMap.append(i)
                   break
                i += 1
    def _mapBMHoleEdges(self):
        self.BMHoleEdgeMap = dict()
        for i in [1,2,3,4]:
            ie = 0
            print ("*** LCDMountingBracket::_mapBMHoleEdges(): self.bracketmh[",i,"] is ",self.bracketmh[i])
            for e in self.bracket.Edges:
                c = e.Curve
                print ("*** LCDMountingBracket::_mapBMHoleEdges(): type(c) is ",type(c))
                print ("*** LCDMountingBracket::_mapBMHoleEdges(): type(Part.Circle()) is ",type(Part.Circle()))
                if type(c) is type(Part.Circle()):
                    print ("*** LCDMountingBracket::_mapBMHoleEdges(): c.Center is ",c.Center)
                    if c.Center.x == self.bracketmh[i].x and \
                       c.Center.y == self.bracketmh[i].y and \
                       c.Center.z == self.bracketmh[i].z:
                        self.BMHoleEdgeMap[i] = ie
                        break
                ie += 1
    def _mapLCDMHoleEdges(self):
        self.LCDMHoleEdgeMap = dict()
        for i in [1,2,3,4]:
            ie = 0
            for e in self.bracket.Edges:
                if type(e) is type(Part.Circle):
                    if e.Center.x == self.lcdmh[i].x and \
                       e.Center.y == self.lcdmh[i].y and \
                       e.Center.z == self.lcdmh[i].z:
                        self.LCDMHoleEdgeMap[i] = ie
                        break
                ie += 1
    def dumpVerts(self):
        i = 0
        for v in self.bracket.Vertexes:
            print ('%d (%g,%g,%g)' % (i,v.X,v.Y,v.Z))
            i += 1
    def findLCDMHolesAsVerts(self):
        for i in [1,2,3,4]:
            vi = 0
            for v in bracket.bracket.Vertexes:
                if v.Y == self.lcdmh[i].y:
                    print ("Y match for %d (%g,%g,%g): %d (%g,%g,%g)" % \
                        (i,self.lcdmh[i].x,self.lcdmh[i].y,self.lcdmh[i].z,\
                         vi,v.X,v.Y,v.Z))
                vi += 1
            i += 1
    def findBMHolesAsVerts(self):
        for i in [1,2,3,4]:
            vi = 0
            for v in bracket.bracket.Vertexes:
                if v.Y == self.bracketmh[i].y:
                    print ("Y match for %d (%g,%g,%g): %d (%g,%g,%g)" % \
                        (i,self.bracketmh[i].x,self.bracketmh[i].y,self.bracketmh[i].z,\
                         vi,v.X,v.Y,v.Z))
                vi += 1
            i += 1

if __name__ == '__main__':
    if "TestDimension" in App.listDocuments().keys():
        App.closeDocument("TestDimension")
    App.ActiveDocument=App.newDocument("TestDimension")
    doc = App.activeDocument()
    bracket = LCDMountingBracket("left",Base.Vector(0,0,0))
    bracket.show()
    Gui.SendMsgToActiveView("ViewFit")
    bounds = bracket.bracket.BoundBox
    ##
    ## 
    doc.addObject('TechDraw::DrawPage','Page1')
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    doc.Page1.Template = doc.USLetterTemplate
    edt = doc.Page1.Template.EditableTexts
    edt['CompanyName'] = "Deepwoods Software"
    edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA'    
    doc.Page1.Template.EditableTexts = edt
    #
    doc.addObject('TechDraw::DrawViewPart','EndView')
    doc.Page1.addView(doc.EndView)
    doc.EndView.Source = doc.left
    doc.EndView.X = 40
    doc.EndView.Y = 180
    doc.EndView.Direction=(0.0,1.0,0.0)
    doc.EndView.recompute()
    
    #
    doc.addObject('TechDraw::DrawViewPart','SideView')
    doc.Page1.addView(doc.SideView)
    doc.SideView.Source = doc.left
    doc.SideView.X = 140
    doc.SideView.Y = 130
    doc.SideView.Direction=(1.0,0.0,0.0)
    doc.SideView.recompute()
    #
    doc.addObject('TechDraw::DrawViewPart','BottomView')
    doc.Page1.addView(doc.BottomView)
    doc.BottomView.Source = doc.left
    doc.BottomView.Direction=(0.0,0.0,-1.0)
    doc.BottomView.Rotation = 90
    doc.BottomView.X = 140
    doc.BottomView.Y = 80
    #tz = bracket.bracket.Vertexes[0].Z
    #tx = bounds.XMin - 12.7
    v1 = bracket.polyVertexMap[0]
    v2 = bracket.polyVertexMap[1]
    #ty = (bracket.bracket.Vertexes[v1].Y+bracket.bracket.Vertexes[v2].Y)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d1 = Draft.makeDimension(doc.left,v1,v2,tv)
    #d1.ViewObject.FontSize=5
    #d1.ViewObject.Override="L"
    doc.addObject('TechDraw::DrawViewDimension','Length')
    doc.Length.Type = 'DistanceX'
    doc.Length.References2D=[(doc.BottomView,"Vertex%d"%v1),\
                             (doc.BottomView,"Vertex%d"%v2)]
    doc.Length.FormatSpec='L'
    doc.Length.Arbitrary = True
    doc.Length.X = 0
    doc.Length.Y = 32
    doc.Page1.addView(doc.Length)
    v1 = v2
    v2 = bracket.polyVertexMap[2]
    #ty = bounds.YMax + 6.35
    #tx = (bracket.bracket.Vertexes[v1].X+bracket.bracket.Vertexes[v2].X)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d2 = Draft.makeDimension(doc.left,v1,v2,tv)
    #d2.ViewObject.FontSize=5
    #d2.ViewObject.Override="w"
    doc.addObject('TechDraw::DrawViewDimension','Width')
    doc.Width.Type = 'DistanceY'
    doc.Width.References2D=[(doc.BottomView,"Vertex%d"%v1),\
                            (doc.BottomView,"Vertex%d"%v2)]
    doc.Width.FormatSpec='w'
    doc.Width.Arbitrary = True
    doc.Page1.addView(doc.Width)
    v1 = v2
    v2 = bracket.polyVertexMap[3]
    #tx = bounds.XMin - 6.35
    #ty = (bracket.bracket.Vertexes[v1].Y+bracket.bracket.Vertexes[v2].Y)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d3 = Draft.makeDimension(doc.left,v2,v1,tv)
    #d3.ViewObject.FontSize=5
    #d3.ViewObject.Override="A"
    doc.addObject('TechDraw::DrawViewDimension','A')
    doc.A.Type = 'DistanceX'
    doc.A.References2D=[(doc.BottomView,"Vertex%d"%v1),\
                        (doc.BottomView,"Vertex%d"%v2)]
    doc.A.FormatSpec='A'
    doc.A.Arbitrary = True
    doc.Page1.addView(doc.A)
    v1 = v2
    v2 = bracket.polyVertexMap[4]
    #ty = bracket.bracket.Vertexes[v1].Y - 6.35
    #tx = (bracket.bracket.Vertexes[v1].X+bracket.bracket.Vertexes[v2].X)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d4 = Draft.makeDimension(doc.left,v1,v2,tv)
    #d4.ViewObject.FontSize=5
    #d4.ViewObject.Override="N"
    doc.addObject('TechDraw::DrawViewDimension','N')
    doc.N.Type = 'Distance'
    doc.N.References2D=[(doc.BottomView,"Vertex%d"%v1),\
                        (doc.BottomView,"Vertex%d"%v2)]
    doc.N.FormatSpec='N'
    doc.N.Arbitrary = True
    doc.Page1.addView(doc.N)
    v1 = v2
    v2 = bracket.polyVertexMap[5]
    #tx = bounds.XMin - 6.35
    #ty = (bracket.bracket.Vertexes[v1].Y+bracket.bracket.Vertexes[v2].Y)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d5 = Draft.makeDimension(doc.left,v2,v1,tv)
    #d5.ViewObject.FontSize=5
    #d5.ViewObject.Override="B"
    doc.addObject('TechDraw::DrawViewDimension','B')
    doc.B.Type = 'Distance'
    doc.B.References2D=[(doc.BottomView,"Vertex%d"%v1),\
                        (doc.BottomView,"Vertex%d"%v2)]
    doc.B.FormatSpec='B'
    doc.B.Arbitrary = True
    doc.Page1.addView(doc.B)
    ##
    e1 = bracket.BMHoleEdgeMap[1]
    #ty = bracket.bracket.Edges[e1].Curve.Center.y
    #tx = bounds.XMin + 6.35
    #tv = Base.Vector(tx,ty,tz) 
    #d6 = Draft.makeDimension(doc.left,e1,"Diameter",tv)
    #d6.ViewObject.FontSize=5
    #d6.ViewObject.Override="BMDia"
    doc.addObject('TechDraw::DrawViewDimension','BMDia')
    doc.BMDia.Type = 'Diameter'
    doc.BMDia.References2D=[(doc.BottomView,"Edge%d"%e1)]
    doc.BMDia.FormatSpec='BMDia'
    doc.BMDia.Arbitrary = True
    doc.Page1.addView(doc.BMDia)
    doc.BottomView.recompute()
    doc.Page1.ViewObject.show()
    

    doc.recompute()       
    
