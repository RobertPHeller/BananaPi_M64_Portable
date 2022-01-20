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
#  Created       : Tue Jun 2 22:09:55 2020
#  Last Modified : <200819.0948>
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
import FreeCADGui
from FreeCAD import Console
from FreeCAD import Base
import FreeCAD as App
import os
import sys
sys.path.append(os.path.dirname(__file__))

import datetime



from abc import ABCMeta, abstractmethod, abstractproperty

class HDMIConverterDims(object):
    __metaclass__ = ABCMeta
    _mainboardWidth = 139
    @staticmethod
    def mainboardWidth():
        return HDMIConverterDims._mainboardWidth
    _mainboardHeight = 58
    @staticmethod
    def mainboardHeight():
        return HDMIConverterDims._mainboardHeight
    _mainBoardMHDia = 3.5
    @staticmethod
    def mainBoardMHDia():
        return HDMIConverterDims._mainBoardMHDia
    _mainboardMH1_x = 124.47 + (3.5/2.0)
    @staticmethod
    def mainboardMH1_x():
        return HDMIConverterDims._mainboardMH1_x
    _mainboardMH1_y = 19.24 + (3.5/2.0)
    @staticmethod
    def mainboardMH1_y():
        return HDMIConverterDims._mainboardMH1_y
    _mainboardMH2_x = 123.03 + (3.5/2.0)
    @staticmethod
    def mainboardMH2_x():
        return HDMIConverterDims._mainboardMH2_x
    _mainboardMH2_y = 47.32 + (3.5/2.0)
    @staticmethod
    def mainboardMH2_y():
        return HDMIConverterDims._mainboardMH2_y
    _mainboardMH3_x = 12.36 + (3.5/2.0)
    @staticmethod
    def mainboardMH3_x():
        return HDMIConverterDims._mainboardMH3_x
    _mainboardMH3_y = 19.24 + (3.5/2.0)
    @staticmethod
    def mainboardMH3_y():
        return HDMIConverterDims._mainboardMH3_y
    _mainboardMH4_x = 18.07 + (3.5/2.0)
    @staticmethod
    def mainboardMH4_x():
        return HDMIConverterDims._mainboardMH4_x
    _mainboardMH4_y = 47.32 + (3.5/2.0)
    @staticmethod
    def mainboardMH4_y():
        return HDMIConverterDims._mainboardMH4_y
    _buttonboardWidth = 104.13
    @staticmethod
    def buttonboardWidth():
        return HDMIConverterDims._buttonboardWidth
    _buttonboardHeight = 21.87
    @staticmethod
    def buttonboardHeight():
        return HDMIConverterDims._buttonboardHeight
    _buttonboardMHDia = 3.32
    @staticmethod
    def buttonboardMHDia():
        return HDMIConverterDims._buttonboardMHDia
    _buttonboardMH1_x = 8.2 + (3.32/2.0)
    @staticmethod
    def buttonboardMH1_x():
        return HDMIConverterDims._buttonboardMH1_x
    _buttonboardMH1_y = 6 + (3.32/2.0)
    @staticmethod
    def buttonboardMH1_y():
        return HDMIConverterDims._buttonboardMH1_y
    _buttonboardMH2_x = 92.7 + (3.32/2.0)
    @staticmethod
    def buttonboardMH2_x():
        return HDMIConverterDims._buttonboardMH2_x
    _buttonboardMH2_y = 6 + (3.32/2.0)
    @staticmethod
    def buttonboardMH2_y():
        return HDMIConverterDims._buttonboardMH2_y
    _hvpowerboardWidth = 119.73
    @staticmethod
    def hvpowerboardWidth():
        return HDMIConverterDims._hvpowerboardWidth
    _hvpowerboardHeight = 23.24
    @staticmethod
    def hvpowerboardHeight():
        return HDMIConverterDims._hvpowerboardHeight
    _hvpowerboardMHDia = 3.5
    @staticmethod
    def hvpowerboardMHDia():
        return HDMIConverterDims._hvpowerboardMHDia
    _hvpowerboardMH2_x = 114.22 + (3.5/2.0)
    @staticmethod
    def hvpowerboardMH2_x():
        return HDMIConverterDims._hvpowerboardMH2_x
    _hvpowerboardMH2_y = 2.2 + (3.5/2.0)
    @staticmethod
    def hvpowerboardMH2_y():
        return HDMIConverterDims._hvpowerboardMH2_y
    _hvpowerboardMH1_x1 = 2.73
    @staticmethod
    def hvpowerboardMH1_x1():
        return HDMIConverterDims._hvpowerboardMH1_x1
    _hvpowerboardMH1_wide = 14.25
    @staticmethod
    def hvpowerboardMH1_wide():
        return HDMIConverterDims._hvpowerboardMH1_wide
    _hvpowerboardMH1_y = 2.0
    @staticmethod
    def hvpowerboardMH1_y():
        return HDMIConverterDims._hvpowerboardMH1_y
    _boardthickness = 1.5
    @staticmethod
    def boardthickness():
        return HDMIConverterDims._boardthickness
    _bracketthickness = .125*25.4
    @staticmethod
    def bracketthinkness():
        return HDMIConverterDims._bracketthickness
    @staticmethod
    def bracketwidth():
        w1 = (HDMIConverterDims._mainboardMH1_x - HDMIConverterDims._mainboardMH2_x) + 10.16
        w2 = (HDMIConverterDims._mainboardMH4_x - HDMIConverterDims._mainboardMH3_x) + 10.16
        if w1 > w2: return w1
        else:       return w2
    @staticmethod
    def brackethorizlen():
        return HDMIConverterDims._mainboardHeight
    @staticmethod
    def bracketvertlen():
        return (HDMIConverterDims._mainboardHeight)*.25
    _bracketholedia = 3.5
    @staticmethod
    def bracketholedia():
        return HDMIConverterDims._bracketholedia
        
class HDMIConverterMainBoardBracket(HDMIConverterDims):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        hthick = Base.Vector(0,0,-self.bracketthinkness())
        vthick = Base.Vector(0,-self.bracketthinkness(),0)
        ZNorm  = Base.Vector(0,0,1)
        YNorm  = Base.Vector(0,1,0)
        vorig  = self.origin.add(Base.Vector(0,self.brackethorizlen(),-self.bracketvertlen()))
        hpart  = Part.makePlane(self.bracketwidth(),self.brackethorizlen(),self.origin,ZNorm).extrude(hthick)
        vpart  = Part.makePlane(self.bracketvertlen(),self.bracketwidth(),vorig,YNorm).extrude(vthick)
        self.holeorig = vorig.add(Base.Vector(self.bracketwidth()/2,0,self.bracketvertlen()/2))
        hole   = Part.Face(Part.Wire(Part.makeCircle(self.bracketholedia()/2,self.holeorig,YNorm))).extrude(vthick)
        self.bracket = hpart.fuse(vpart.cut(hole))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.bracket
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.85,.85,0.85])        
    def MountingHole(self,yBase,yHeight):
        mhorig = Base.Vector(self.holeorig.x,yBase,self.holeorig.z)
        vthick = Base.Vector(0,yHeight,0)
        YNorm  = Base.Vector(0,1,0)
        hole   = Part.Face(Part.Wire(Part.makeCircle(self.bracketholedia()/2,mhorig,YNorm))).extrude(vthick)
        return hole
    def cutFrom(self,shape):
        self.bracket = self.bracket.cut(shape)        

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
        
                                

if __name__ == '__main__':
    if "HDMIMainBoardMountingBracket" in App.listDocuments().keys():
        App.closeDocument("HDMIMainBoardMountingBracket")
    App.ActiveDocument=App.newDocument("HDMIMainBoardMountingBracket")
    doc = App.activeDocument()
    _insulatedWasherThick = .065*25.4
    _insulatedWasherDiameter = .250*25.4
    hmiconvertermainboardorig = Base.Vector(0,0,0)
    hdmiconvertermainboard =  HDMIConverterMainBoard("mainboard",hmiconvertermainboardorig)
    hdmiconvertermainboard_washer1 = hdmiconvertermainboard.Standoff(1,hmiconvertermainboardorig.z,-_insulatedWasherThick,_insulatedWasherDiameter)
    hdmiconvertermainboard_washer2 = hdmiconvertermainboard.Standoff(2,hmiconvertermainboardorig.z,-_insulatedWasherThick,_insulatedWasherDiameter)
    hdmiconvertermainboard_washer3 = hdmiconvertermainboard.Standoff(3,hmiconvertermainboardorig.z,-_insulatedWasherThick,_insulatedWasherDiameter)
    hdmiconvertermainboard_washer4 = hdmiconvertermainboard.Standoff(4,hmiconvertermainboardorig.z,-_insulatedWasherThick,_insulatedWasherDiameter)
    c1 = (hdmiconvertermainboard.mh[1].x+hdmiconvertermainboard.mh[2].x)/2.0
    b1x = c1 - (hdmiconvertermainboard.bracketwidth()/2.0)
    c2 = (hdmiconvertermainboard.mh[3].x+hdmiconvertermainboard.mh[4].x)/2.0
    b2x = c2 - (hdmiconvertermainboard.bracketwidth()/2.0) 
    by = hmiconvertermainboardorig.y
    bz = hmiconvertermainboardorig.z - _insulatedWasherThick
    hdmiconvertermainboardRightBracket = HDMIConverterMainBoardBracket("_hdmiconvertermainboardRightBracket",Base.Vector(b1x,by,bz))
    hdmiconvertermainboardRightBracket.cutFrom(hdmiconvertermainboard.MountingHole(1,bz,-hdmiconvertermainboard.bracketthinkness()))
    hdmiconvertermainboardRightBracket.cutFrom(hdmiconvertermainboard.MountingHole(2,bz,-hdmiconvertermainboard.bracketthinkness()))
    hdmiconvertermainboardLeftBracket = HDMIConverterMainBoardBracket("_hdmiconvertermainboardLeftBracket",Base.Vector(b2x,by,bz))
    hdmiconvertermainboardLeftBracket.cutFrom(hdmiconvertermainboard.MountingHole(3,bz,-hdmiconvertermainboard.bracketthinkness()))
    hdmiconvertermainboardLeftBracket.cutFrom(hdmiconvertermainboard.MountingHole(4,bz,-hdmiconvertermainboard.bracketthinkness()))
    hdmiconvertermainboard.show()
    obj = doc.addObject("Part::Feature",'_hdmiconvertermainboard_washer1')
    obj.Shape = hdmiconvertermainboard_washer1
    obj.Label='_hdmiconvertermainboard_washer1'
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
    obj = doc.addObject("Part::Feature",'_hdmiconvertermainboard_washer2')
    obj.Shape = hdmiconvertermainboard_washer2
    obj.Label='_hdmiconvertermainboard_washer2'
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
    obj = doc.addObject("Part::Feature",'_hdmiconvertermainboard_washer3')
    obj.Shape = hdmiconvertermainboard_washer3
    obj.Label='_hdmiconvertermainboard_washer3'
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
    obj = doc.addObject("Part::Feature",'_hdmiconvertermainboard_washer4')
    obj.Shape = hdmiconvertermainboard_washer4
    obj.Label='_hdmiconvertermainboard_washer4'
    obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
    hdmiconvertermainboardLeftBracket.show()
    hdmiconvertermainboardRightBracket.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewIsometric()
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = doc.USLetterTemplate.EditableTexts
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = doc.USLetterTemplate.EditableTexts
    edt['CompanyName'] = "Deepwoods Software"
    edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA'    
    edt['DrawingTitle1']= 'HDMI Main Board Mounting Bracket'
    edt['DrawingTitle3']= ""
    edt['DrawnBy'] = "Robert Heller"
    edt['CheckedBy'] = ""
    edt['Approved1'] = ""
    edt['Approved2'] = ""
    edt['Code'] = ""
    edt['Weight'] = ''
    edt['DrawingNumber'] = datetime.datetime.now().ctime()
    edt['Revision'] = "A"
    doc.USLetterTemplate.EditableTexts = edt
    doc.addObject('TechDraw::DrawPage','HDMIMainBoardMountingBracketPage')
    doc.HDMIMainBoardMountingBracketPage.Template = doc.USLetterTemplate
    edt = doc.HDMIMainBoardMountingBracketPage.Template.EditableTexts
    edt['DrawingTitle2']= "Box (Bottom and Front)"
    edt['Scale'] = '1:2'
    edt['Sheet'] = "Sheet 1"
    doc.HDMIMainBoardMountingBracketPage.Template.EditableTexts = edt
    doc.HDMIMainBoardMountingBracketPage.ViewObject.show()
    bracketsheet = doc.addObject('Spreadsheet::Sheet','BracketDimensionTable1')
    bracketsheet.set("A1",'%-11.11s'%"Dim")
    bracketsheet.set("B1",'%10.10s'%"inch")
    bracketsheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','BracketTopView')
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketTopView)
    doc.BracketTopView.Source = [doc._hdmiconvertermainboardLeftBracket,doc._hdmiconvertermainboardRightBracket]
    doc.BracketTopView.X = 60
    doc.BracketTopView.Y = 140
    doc.BracketTopView.Scale = .5
    doc.BracketTopView.Direction=(0.0,0.0,1.0)
    doc.BracketTopView.Caption = "Top"
    
    doc.addObject('TechDraw::DrawViewDimension','BracketA')
    doc.BracketA.Type = 'DistanceX'
    doc.BracketA.References2D=[(doc.BracketTopView,"Vertex0"),\
                               (doc.BracketTopView,"Vertex11")]
    doc.BracketA.FormatSpec='A (2x)'
    doc.BracketA.Arbitrary = True
    doc.BracketA.X = -25
    doc.BracketA.Y =  25
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketA)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"A")
    bracketsheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims.bracketwidth()/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims.bracketwidth())
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketB')
    doc.BracketB.Type = 'DistanceY'
    doc.BracketB.References2D=[(doc.BracketTopView,"Vertex0"),\
                               (doc.BracketTopView,"Vertex11")]
    doc.BracketB.FormatSpec='B (2x)'
    doc.BracketB.Arbitrary = True
    doc.BracketB.X = -3
    doc.BracketB.Y = 0
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketB)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"B")
    bracketsheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims.brackethorizlen()/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims.brackethorizlen())
    ir += 1
    # Edge4 -- board mounting hole (for diameter)
    doc.addObject('TechDraw::DrawViewDimension','BracketC')
    doc.BracketC.Type = 'Diameter'
    doc.BracketC.References2D=[(doc.BracketTopView,"Edge4")]
    doc.BracketC.FormatSpec='CDia (4x)'
    doc.BracketC.Arbitrary = True
    doc.BracketC.X = -16.5
    doc.BracketC.Y = -20
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketC)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"CDia")
    bracketsheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims.mainBoardMHDia()/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims.mainBoardMHDia())
    ir += 1
    # Left bracket holes
    # orig Vert: Vertex0 (b2x,by,bz)
    # mainboard orig is hmiconvertermainboardorig
    # mainboard.mh[3] (Vertex6) and mainboard.mh[4] (Vertex9)
    doc.addObject('TechDraw::DrawViewDimension','BracketD')
    doc.BracketD.Type = 'DistanceX'
    doc.BracketD.References2D=[(doc.BracketTopView,"Vertex0"),\
                               (doc.BracketTopView,"Vertex6")]
    doc.BracketD.FormatSpec='D'
    doc.BracketD.Arbitrary = True
    doc.BracketD.X = -17
    doc.BracketD.Y = 6
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketD)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"D")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[3].x-b2x)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[3].x-b2x))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketE')
    doc.BracketE.Type = 'DistanceY'
    doc.BracketE.References2D=[(doc.BracketTopView,"Vertex0"),\
                               (doc.BracketTopView,"Vertex6")]
    doc.BracketE.FormatSpec='E'
    doc.BracketE.Arbitrary = True
    doc.BracketE.X = -22
    doc.BracketE.Y = -7
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketE)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"E")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[3].y-by)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[3].y-by))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketF')
    doc.BracketF.Type = 'DistanceX'
    doc.BracketF.References2D=[(doc.BracketTopView,"Vertex9"),\
                               (doc.BracketTopView,"Vertex6")]
    doc.BracketF.FormatSpec='F'
    doc.BracketF.Arbitrary = True
    doc.BracketF.X = -2
    doc.BracketF.Y = 22
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketF)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"F")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[4].x-hdmiconvertermainboard.mh[3].x)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[4].x-hdmiconvertermainboard.mh[3].x))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketG')
    doc.BracketG.Type = 'DistanceY'
    doc.BracketG.References2D=[(doc.BracketTopView,"Vertex9"),\
                               (doc.BracketTopView,"Vertex6")]
    doc.BracketG.FormatSpec='G'
    doc.BracketG.Arbitrary = True
    doc.BracketG.X = -13
    doc.BracketG.Y =  2
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketG)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"G")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[4].y-hdmiconvertermainboard.mh[3].y)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[4].y-hdmiconvertermainboard.mh[3].y))
    ir += 1
    # Right bracket holes
    # orig Vert: Vertex12 (b1x, by, bz)
    # mainboard orig is hmiconvertermainboardorig
    # mainboard.mh[1] (Vertex18) and mainboard.mh[2] (Vertex21)
    doc.addObject('TechDraw::DrawViewDimension','BracketH')
    doc.BracketH.Type = 'DistanceX'
    doc.BracketH.References2D=[(doc.BracketTopView,"Vertex12"),\
                               (doc.BracketTopView,"Vertex18")]
    doc.BracketH.FormatSpec='H'
    doc.BracketH.Arbitrary = True
    doc.BracketH.X = 31
    doc.BracketH.Y = -17
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketH)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"H")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[1].x-b1x)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[1].x-b1x))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketI')
    doc.BracketI.Type = 'DistanceY'
    doc.BracketI.References2D=[(doc.BracketTopView,"Vertex12"),\
                               (doc.BracketTopView,"Vertex18")]
    doc.BracketI.FormatSpec='I'
    doc.BracketI.Arbitrary = True
    doc.BracketI.X = 14
    doc.BracketI.Y = -9
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketI)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"I")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[1].y-by)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[1].y-by))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketJ')
    doc.BracketJ.Type = 'DistanceX'
    doc.BracketJ.References2D=[(doc.BracketTopView,"Vertex18"),\
                               (doc.BracketTopView,"Vertex21")]
    doc.BracketJ.FormatSpec='J'
    doc.BracketJ.Arbitrary = True
    doc.BracketJ.X = 33
    doc.BracketJ.Y = 21
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketJ)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"J")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[1].x-hdmiconvertermainboard.mh[2].x)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[1].x-hdmiconvertermainboard.mh[2].x))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketK')
    doc.BracketK.Type = 'DistanceY'
    doc.BracketK.References2D=[(doc.BracketTopView,"Vertex18"),\
                               (doc.BracketTopView,"Vertex21")]
    doc.BracketK.FormatSpec='K'
    doc.BracketK.Arbitrary = True
    doc.BracketK.X = 14
    doc.BracketK.Y =  4
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketK)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"K")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboard.mh[2].y-hdmiconvertermainboard.mh[1].y)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboard.mh[2].y-hdmiconvertermainboard.mh[1].y))
    ir += 1
    
    doc.BracketTopView.recompute()
    
    doc.addObject('TechDraw::DrawViewPart','BracketFrontView')
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketFrontView)
    doc.BracketFrontView.Source = [doc._hdmiconvertermainboardLeftBracket,doc._hdmiconvertermainboardRightBracket]
    doc.BracketFrontView.X = 60
    doc.BracketFrontView.Y = 185
    doc.BracketFrontView.Scale = .5
    doc.BracketFrontView.Direction=(0.0,1.0,0.0)
    doc.BracketFrontView.Caption = "Front"
    
    doc.addObject('TechDraw::DrawViewDimension','BracketL')
    doc.BracketL.Type = 'DistanceY'
    doc.BracketL.References2D=[(doc.BracketFrontView,"Vertex9"),\
                               (doc.BracketFrontView,"Vertex14")]
    doc.BracketL.FormatSpec='L (2x)'
    doc.BracketL.Arbitrary = True
    doc.BracketL.X = -15
    doc.BracketL.Y = -11
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketL)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"L")
    bracketsheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims.bracketvertlen()/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims.bracketvertlen())
    ir += 1
    # Edge15 -- for hole diameter (HDMIConverterDims.bracketholedia())
    # Vertex14 -- orig (hdmiconvertermainboardLeftBracket.origin)
    # Vertex17 -- holeorig (hdmiconvertermainboardLeftBracket.holeorig)
    doc.addObject('TechDraw::DrawViewDimension','BracketM')
    doc.BracketM.Type = 'Diameter'
    doc.BracketM.References2D=[(doc.BracketFrontView,"Edge15")]
    doc.BracketM.FormatSpec='MDia (2x)'
    doc.BracketM.Arbitrary = True
    doc.BracketM.X =  0
    doc.BracketM.Y = 11
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketM)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"MDia")
    bracketsheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims.bracketholedia()/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims.bracketholedia())
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketN')
    doc.BracketN.Type = 'DistanceX'
    doc.BracketN.References2D=[(doc.BracketFrontView,"Vertex14"),\
                               (doc.BracketFrontView,"Vertex17")]
    doc.BracketN.FormatSpec='N'
    doc.BracketN.Arbitrary = True
    doc.BracketN.X = -30
    doc.BracketN.Y =  13
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketN)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"N")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboardLeftBracket.holeorig.x-hdmiconvertermainboardLeftBracket.origin.x)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboardLeftBracket.holeorig.x-hdmiconvertermainboardLeftBracket.origin.x))
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BracketO')
    doc.BracketO.Type = 'DistanceY'
    doc.BracketO.References2D=[(doc.BracketFrontView,"Vertex14"),\
                               (doc.BracketFrontView,"Vertex17")]
    doc.BracketO.FormatSpec='O'
    doc.BracketO.Arbitrary = True 
    doc.BracketO.X = -38
    doc.BracketO.Y = -1
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketO)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"O")
    bracketsheet.set("B%d"%ir,'%10.6f'%((hdmiconvertermainboardLeftBracket.origin.z-hdmiconvertermainboardLeftBracket.holeorig.z)/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%(hdmiconvertermainboardLeftBracket.origin.z-hdmiconvertermainboardLeftBracket.holeorig.z))
    ir += 1


    doc.BracketFrontView.recompute()

    doc.addObject('TechDraw::DrawViewPart','BracketLeftView')
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketLeftView)
    doc.BracketLeftView.Source = [doc._hdmiconvertermainboardLeftBracket,doc._hdmiconvertermainboardRightBracket]
    doc.BracketLeftView.X = 130
    doc.BracketLeftView.Y = 185
    doc.BracketLeftView.Scale = .5
    doc.BracketLeftView.Direction=(1.0,0.0,0.0)
    doc.BracketLeftView.Caption = "Left"
    # Vertex0 -- upper left
    # Vertex2 -- lower left
    # HDMIConverterDims.bracketthinkness()
    doc.addObject('TechDraw::DrawViewDimension','BracketP')
    doc.BracketP.Type = 'DistanceY'
    doc.BracketP.References2D=[(doc.BracketLeftView,"Vertex0"),\
                               (doc.BracketLeftView,"Vertex2")]
    doc.BracketP.FormatSpec='P'
    doc.BracketP.Arbitrary = True 
    doc.BracketP.X = -5
    doc.BracketP.Y = -4
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketP)
    bracketsheet.set("A%d"%ir,'%-11.11s'%"P")
    bracketsheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims.bracketthinkness()/25.4))
    bracketsheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims.bracketthinkness())
    ir += 1
    
    
    
    
    doc.BracketLeftView.recompute()

    doc.addObject('TechDraw::DrawViewPart','BracketISOView')
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketISOView)
    doc.BracketISOView.Source = [doc.mainboard,\
                                 doc._hdmiconvertermainboard_washer1,\
                                 doc._hdmiconvertermainboard_washer2,\
                                 doc._hdmiconvertermainboard_washer3,\
                                 doc._hdmiconvertermainboard_washer4,\
                                 doc._hdmiconvertermainboardLeftBracket,\
                                 doc._hdmiconvertermainboardRightBracket]
    doc.BracketISOView.X = 67
    doc.BracketISOView.Y = 80
    doc.BracketISOView.Scale = .5
    doc.BracketISOView.Direction=(1.0,-1.0,-1.0)
    doc.BracketISOView.Caption = "ISOMetric"
    
    doc.BracketISOView.recompute()

    bracketsheet.recompute()
    doc.addObject('TechDraw::DrawViewSpreadsheet','BracketDimBlock')
    doc.BracketDimBlock.Source = bracketsheet
    doc.BracketDimBlock.TextSize = 8
    doc.BracketDimBlock.CellEnd = "C%d"%(ir-1)
    doc.HDMIMainBoardMountingBracketPage.addView(doc.BracketDimBlock)
    doc.BracketDimBlock.recompute()
    doc.BracketDimBlock.X = 210
    doc.BracketDimBlock.Y = 140    

    doc.HDMIMainBoardMountingBracketPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.HDMIMainBoardMountingBracketPage,"BananaPiM64Model_HDMIMainBoardMountingBracketPage.pdf")
    sys.exit(1)    
