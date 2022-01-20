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
#  Last Modified : <200612.0842>
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



import Part, TechDraw, Spreadsheet, TechDrawGui
from FreeCAD import Base
import FreeCAD as App

import os
import sys
sys.path.append(os.path.dirname(__file__))
import datetime
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
            #print ("*** LCDMountingBracket::_mapBMHoleEdges(): self.bracketmh[",i,"] is ",self.bracketmh[i])
            for e in self.bracket.Edges:
                c = e.Curve
                #print ("*** LCDMountingBracket::_mapBMHoleEdges(): type(c) is ",type(c))
                #print ("*** LCDMountingBracket::_mapBMHoleEdges(): type(Part.Circle()) is ",type(Part.Circle()))
                if type(c) is type(Part.Circle()):
                    #print ("*** LCDMountingBracket::_mapBMHoleEdges(): c.Center is ",c.Center)
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
    if "LeftBracketTechDrawing" in App.listDocuments().keys():
        App.closeDocument("LeftBracketTechDrawing")
    App.ActiveDocument=App.newDocument("LeftBracketTechDrawing")
    doc = App.activeDocument()
    bracket = LCDMountingBracket("left",Base.Vector(0,0,0))
    bracket.show()
    Gui.SendMsgToActiveView("ViewFit")
    bounds = bracket.bracket.BoundBox
    ##
    ## 
    doc.addObject('TechDraw::DrawPage','LeftBracketPage')
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    doc.LeftBracketPage.Template = doc.USLetterTemplate
    edt = doc.LeftBracketPage.Template.EditableTexts
    #print (edt.keys())
    edt['CompanyName'] = "Deepwoods Software"
    edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA'    
    edt['DrawingTitle1']= 'Left LCD Mounting Bracket'
    edt['DrawingTitle2']= "(Right bracket is just a mirror image)"
    edt['DrawingTitle3']= ""
    edt['DrawnBy'] = "Robert Heller"
    edt['CheckedBy'] = ""
    edt['Approved1'] = ""
    edt['Approved2'] = ""
    edt['Scale'] = "1:1"
    edt['Weight'] = ""
    edt['Sheet'] = "Sheet 1 of 1"
    edt['Code'] = ""
    edt['DrawingNumber'] = datetime.datetime.now().ctime()
    edt['Revision'] = "A"
    doc.LeftBracketPage.Template.EditableTexts = edt
    doc.LeftBracketPage.ViewObject.show()
    #
    sheet = doc.addObject('Spreadsheet::Sheet','DimensionTable')
    
    sheet.set("A1",'%-11.11s'%"Dim")
    sheet.set("B1",'%10.10s'%"inch")
    sheet.set("C1",'%10.10s'%"mm")
    ir = 2
    #
    doc.addObject('TechDraw::DrawViewPart','EndView')
    doc.LeftBracketPage.addView(doc.EndView)
    doc.EndView.Source = doc.left
    doc.EndView.X = 35
    doc.EndView.Y = 180
    doc.EndView.Direction=(0.0,1.0,0.0)
    doc.addObject('TechDraw::DrawViewDimension','Thick1')
    doc.Thick1.Type = 'DistanceX'
    doc.Thick1.References2D=[(doc.EndView,"Vertex7"),(doc.EndView,"Vertex4")]
    doc.Thick1.Y = -10
    doc.Thick1.X = 0
    doc.Thick1.FormatSpec='t'
    doc.Thick1.Arbitrary = True
    doc.LeftBracketPage.addView(doc.Thick1)
    doc.addObject('TechDraw::DrawViewDimension','Thick2')
    doc.Thick2.Type = 'DistanceY'
    doc.Thick2.References2D=[(doc.EndView,"Vertex5"),(doc.EndView,"Vertex6")]
    doc.Thick2.Y = 0
    doc.Thick2.X = 10
    doc.Thick2.FormatSpec='t'
    doc.Thick2.Arbitrary = True
    doc.LeftBracketPage.addView(doc.Thick2)
    sheet.set("A%d"%ir,'%-11.11s'%"t")
    sheet.set("B%d"%ir,'%10.6f'%(BracketAngleDims._AngleThickness/25.4))
    sheet.set("C%d"%ir,'%10.6f'%BracketAngleDims._AngleThickness)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Height')
    doc.Height.Type = 'DistanceX'
    doc.Height.Y = 15
    doc.Height.X = 0
    doc.Height.References2D=[(doc.EndView,"Vertex0"),(doc.EndView,"Vertex5")]
    doc.Height.FormatSpec='h'
    doc.Height.Arbitrary = True
    doc.LeftBracketPage.addView(doc.Height)
    sheet.set("A%d"%ir,'%-11.11s'%"h")
    sheet.set("B%d"%ir,'%10.6f'%(BracketAngleDims._AngleHeight/25.4))
    sheet.set("C%d"%ir,'%10.6f'%BracketAngleDims._AngleHeight)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Width')
    doc.Width.Type = 'DistanceY'
    doc.Width.X = -15
    doc.Width.Y = 0
    doc.Width.References2D=[(doc.EndView,"Vertex4"),(doc.EndView,"Vertex0")]
    doc.Width.FormatSpec='w'
    doc.Width.Arbitrary = True
    doc.LeftBracketPage.addView(doc.Width)
    sheet.set("A%d"%ir,'%-11.11s'%"w")
    sheet.set("B%d"%ir,'%10.6f'%(BracketAngleDims._AngleWidth/25.4))
    sheet.set("C%d"%ir,'%10.6f'%BracketAngleDims._AngleWidth)
    ir += 1
    doc.EndView.recompute()
    
    #
    doc.addObject('TechDraw::DrawViewPart','SideView')
    doc.LeftBracketPage.addView(doc.SideView)
    doc.SideView.Source = doc.left
    doc.SideView.X = 140
    doc.SideView.Y = 155
    doc.SideView.Direction=(1.0,0.0,0.0)
    doc.addObject('TechDraw::DrawViewDimension','MDia')
    doc.MDia.Type = 'Diameter'
    doc.MDia.References2D=[(doc.SideView,"Edge10")]
    doc.MDia.FormatSpec='MDia (4x)'
    doc.MDia.Arbitrary = True
    doc.MDia.X = 85
    doc.MDia.Y = 18
    doc.LeftBracketPage.addView(doc.MDia)
    sheet.set("A%d"%ir,'%-11.11s'%"MDia")
    sheet.set("B%d"%ir,'%10.6f'%((LCDDims._M_r*2)/25.4))
    sheet.set("C%d"%ir,'%10.6f'%(LCDDims._M_r*2))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MX')
    doc.MX.Type = 'DistanceY'
    doc.MX.References2D=[(doc.SideView,"Vertex4"),(doc.SideView,"Vertex17")]
    doc.MX.FormatSpec='MX'
    doc.MX.Arbitrary = True
    doc.MX.X = 75
    doc.LeftBracketPage.addView(doc.MX)
    sheet.set("A%d"%ir,'%-11.11s'%"MX")
    sheet.set("B%d"%ir,'%10.6f'%(LCDDims._M_x/25.4))
    sheet.set("C%d"%ir,'%10.6f'%LCDDims._M_x)
    ir += 1
    doc.SideView.recompute()
    #
    doc.addObject('TechDraw::DrawViewPart','BottomView')
    doc.LeftBracketPage.addView(doc.BottomView)
    doc.BottomView.Source = doc.left
    doc.BottomView.Direction=(0.0,0.0,-1.0)
    doc.BottomView.Rotation = 90
    doc.BottomView.X = 140
    doc.BottomView.Y = 120
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
    #doc.Length.References2D=[(doc.BottomView,"Vertex%d"%(v1)),\
    #                         (doc.BottomView,"Vertex%d"%(v2))]
    doc.Length.References2D=[(doc.BottomView,"Vertex0"),\
                             (doc.BottomView,"Vertex1")]
    doc.Length.FormatSpec='L'
    doc.Length.Arbitrary = True
    doc.Length.X = 0
    doc.Length.Y = 25.4
    doc.LeftBracketPage.addView(doc.Length)
    sheet.set("A%d"%ir,'%-11.11s'%"L")
    length = bracket.bracket.Vertexes[v2].Y-bracket.bracket.Vertexes[v1].Y
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    v1 = v2
    v2 = bracket.polyVertexMap[2]
    #ty = bounds.YMax + 6.35
    #tx = (bracket.bracket.Vertexes[v1].X+bracket.bracket.Vertexes[v2].X)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d2 = Draft.makeDimension(doc.left,v1,v2,tv)
    #d2.ViewObject.FontSize=5
    #d2.ViewObject.Override="w"
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
    #doc.A.References2D=[(doc.BottomView,"Vertex%d"%(v1)),\
    #                    (doc.BottomView,"Vertex%d"%(v2))]
    doc.A.References2D=[(doc.BottomView,"Vertex3"),\
                        (doc.BottomView,"Vertex6")]
    doc.A.FormatSpec='A'
    doc.A.Arbitrary = True
    doc.A.Y = 15
    doc.A.X = 75
    doc.LeftBracketPage.addView(doc.A)
    sheet.set("A%d"%ir,'%-11.11s'%"A")
    length = bracket.bracket.Vertexes[v1].Y-bracket.bracket.Vertexes[v2].Y
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    v1 = v2
    v2 = bracket.polyVertexMap[4]
    #ty = bracket.bracket.Vertexes[v1].Y - 6.35
    #tx = (bracket.bracket.Vertexes[v1].X+bracket.bracket.Vertexes[v2].X)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d4 = Draft.makeDimension(doc.left,v1,v2,tv)
    #d4.ViewObject.FontSize=5
    #d4.ViewObject.Override="N"
    doc.addObject('TechDraw::DrawViewDimension','N')
    doc.N.Type = 'DistanceY'
    #doc.N.References2D=[(doc.BottomView,"Vertex%d"%(v1)),\
    #                    (doc.BottomView,"Vertex%d"%(v2))]
    doc.N.References2D=[(doc.BottomView,"Vertex6"),\
                        (doc.BottomView,"Vertex7")]
    doc.N.FormatSpec='N'
    doc.N.Arbitrary = True
    doc.LeftBracketPage.addView(doc.N)
    sheet.set("A%d"%ir,'%-11.11s'%"N")
    length = bracket.bracket.Vertexes[v2].X-bracket.bracket.Vertexes[v1].X
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    v1 = v2
    v2 = bracket.polyVertexMap[5]
    #tx = bounds.XMin - 6.35
    #ty = (bracket.bracket.Vertexes[v1].Y+bracket.bracket.Vertexes[v2].Y)/2.0
    #tv = Base.Vector(tx,ty,tz)
    #d5 = Draft.makeDimension(doc.left,v2,v1,tv)
    #d5.ViewObject.FontSize=5
    #d5.ViewObject.Override="B"
    doc.addObject('TechDraw::DrawViewDimension','B')
    doc.B.Type = 'DistanceX'
    #doc.B.References2D=[(doc.BottomView,"Vertex%d"%(v1)),\
    #                    (doc.BottomView,"Vertex%d"%(v2))]
    doc.B.References2D=[(doc.BottomView,"Vertex7"),\
                        (doc.BottomView,"Vertex8")]
    doc.B.FormatSpec='B'
    doc.B.Arbitrary = True
    doc.B.Y = 15
    doc.LeftBracketPage.addView(doc.B)
    sheet.set("A%d"%ir,'%-11.11s'%"B")
    length = bracket.bracket.Vertexes[v1].Y-bracket.bracket.Vertexes[v2].Y
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
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
    #doc.BMDia.References2D=[(doc.BottomView,"Edge%d"%(e1))]
    doc.BMDia.References2D=[(doc.BottomView,"Edge12")]
    doc.BMDia.FormatSpec='BMDia (4x)'
    doc.BMDia.Arbitrary = True
    doc.BMDia.X = 85
    doc.BMDia.Y = 18
    doc.LeftBracketPage.addView(doc.BMDia)
    sheet.set("A%d"%ir,'%-11.11s'%"BMDia")
    sheet.set("B%d"%ir,'%10.6f'%((BracketAngleDims._BRACKET_r*2)/25.4))
    sheet.set("C%d"%ir,'%10.6f'%(BracketAngleDims._BRACKET_r*2))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','M1')
    doc.M1.Type = 'DistanceX'
    doc.M1.References2D=[(doc.BottomView,"Vertex1"),
                         (doc.BottomView,"Vertex15")]
    doc.M1.FormatSpec='M1'
    doc.M1.Arbitrary = True
    doc.M1.Y = -15
    doc.M1.X = 105.5
    doc.LeftBracketPage.addView(doc.M1)
    sheet.set("A%d"%ir,'%-11.11s'%"M1")
    length = LCDDims._M1_y
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','M2')
    doc.M2.Type = 'DistanceX'
    doc.M2.References2D=[(doc.BottomView,"Vertex15"),
                         (doc.BottomView,"Vertex18")]
    doc.M2.FormatSpec='M2'
    doc.M2.Arbitrary = True
    doc.M2.Y = -15
    doc.M2.X = 73.5
    doc.LeftBracketPage.addView(doc.M2)
    sheet.set("A%d"%ir,'%-11.11s'%"M2")
    length = LCDDims._M2_y - LCDDims._M1_y
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','M3')
    doc.M3.Type = 'DistanceX'
    doc.M3.References2D=[(doc.BottomView,"Vertex18"),
                         (doc.BottomView,"Vertex12")]
    doc.M3.FormatSpec='M3'
    doc.M3.Arbitrary = True
    doc.M3.Y = -15
    doc.LeftBracketPage.addView(doc.M3)
    length = LCDDims._M3_y - LCDDims._M2_y
    sheet.set("A%d"%ir,'%-11.11s'%"M3")
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','M4')
    doc.M4.Type = 'DistanceX'
    doc.M4.References2D=[(doc.BottomView,"Vertex12"),
                         (doc.BottomView,"Vertex21")]
    doc.M4.FormatSpec='M4'
    doc.M4.Arbitrary = True
    doc.M4.Y = -15
    doc.M4.X = -73.5
    doc.LeftBracketPage.addView(doc.M4)
    length = LCDDims._M4_y - LCDDims._M3_y
    sheet.set("A%d"%ir,'%-11.11s'%"M4")
    sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.BottomView.recompute()

    
    sheet.recompute()
    doc.addObject('TechDraw::DrawViewSpreadsheet','DimBlock')
    doc.DimBlock.Source = sheet
    doc.DimBlock.TextSize = 8
    doc.DimBlock.CellEnd = "C%d"%(ir-1)
    doc.DimBlock.X = 67
    doc.DimBlock.Y = 58
    doc.LeftBracketPage.addView(doc.DimBlock)
    doc.DimBlock.recompute()    
    doc.DimBlock.X = 67
    doc.DimBlock.Y = 58
    doc.recompute()       
    TechDrawGui.exportPageAsPdf(doc.LeftBracketPage,"BananaPiM64Model_leftbracket_new.pdf")
    App.closeDocument("LeftBracketTechDrawing")
    sys.exit(1)
