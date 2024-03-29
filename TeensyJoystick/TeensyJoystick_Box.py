#!/usr/local/bin/FreeCAD019
#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri Jul 30 11:03:18 2021
#  Last Modified : <210731.1146>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
#    Copyright (C) 2021  Robert Heller D/B/A Deepwoods Software
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


import FreeCAD as App
import Part
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))

class TactileSwitch(object):
    _Width = 5.99
    _Length = 5.99
    _PinSpaceX = 6.5
    _PinSpaceY = 4.5
    _BaseHeight = 3.61
    _BaseColor = tuple([0.0,0.0,0.0])
    _ButtonHeight = 4.40
    _ButtonDiameter = 3.51
    _ButtonColor = tuple([1.0,1.0,1.0])
    def ButtonTop(self):
        return self.origin.z+self._BaseHeight+self._ButtonHeight
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        corner = Base.Vector(ox-(self._Width/2.0),oy-(self._Length/2.0),oz)
        self.body = Part.makePlane(self._Width,self._Length,corner)\
                    .extrude(Base.Vector(0,0,self._BaseHeight))
        buttonO = Base.Vector(ox,oy,oz+self._BaseHeight)
        self.button = Part.Face(Part.Wire(Part.makeCircle(\
                            self._ButtonDiameter/2.0,buttonO)))\
                            .extrude(Base.Vector(0,0,self._ButtonHeight))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_Base")
        obj.Shape = self.body
        obj.Label=self.name+'_Base'
        obj.ViewObject.ShapeColor=self._BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_Button")
        obj.Shape = self.button
        obj.Label=self.name+'_Button'
        obj.ViewObject.ShapeColor=self._ButtonColor

class ThumbStick(object):
    _Width = 25.4
    _Length = 25.4
    _BoardOffZ = 2.54
    _BoardThick = 1.6
    _boardColor = tuple([0.0,0.0,1.0])
    _Pin4X = -3.81 # from center
    _Pin3X = -1.27 # from center
    _Pin2X =  1.27 # from center
    _Pin1X =  3.81 # from center
    _PinsY = 11.43 # +/- from center
    _Pinshole = 0.762
    _HeaderBodySize = 2.54
    _headerColor = tuple([0.0,0.0,0.0])
    _BodyXY = 17.5
    _BodyZ = 5.66
    _BodyColor = tuple([0.85,0.85,0.85])
    _StickXY = 4
    _StickZ = 3.18
    _StickColor = tuple([0.0,0.0,0.0])
    _KnobBodyZoff = 1
    _KnobBodyDia = 16
    _KnobTopDia = 18
    @classmethod
    def CutoutDiameter(cls):
        return (cls._KnobTopDia*1.25)
    _KnobBodyHeight = 6
    _KnobTopHeight = 3
    _KnobColor = tuple([0.4,.4,1.0])
    _MholeOff = 10.13
    _Mhole    = 2
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        corner = Base.Vector(ox-(self._Width/2.0),oy-(self._Length/2.0),oz)
        boardOrig = corner.add(Base.Vector(0,0,self._BoardOffZ))
        boardsurf = Part.makePlane(self._Width,self._Length,boardOrig)
        MholeRad = self._Mhole/2.0
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(MholeRad,Base.Vector(ox-self._MholeOff,\
                                                         oy-self._MholeOff,\
                                                         oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(MholeRad,Base.Vector(ox+self._MholeOff,\
                                                         oy-self._MholeOff,\
                                                         oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(MholeRad,Base.Vector(ox-self._MholeOff,\
                                                         oy+self._MholeOff,\
                                                         oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(MholeRad,Base.Vector(ox+self._MholeOff,\
                                                         oy+self._MholeOff,\
                                                         oz+self._BoardOffZ)))))
        pinrad = self._Pinshole/2.0
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin4X,
                                                       oy+self._PinsY,
                                                       oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin3X,
                                                       oy+self._PinsY,
                                                       oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin2X,
                                                       oy+self._PinsY,
                                                       oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin1X,
                                                       oy+self._PinsY,
                                                       oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin4X,
                                                       oy-self._PinsY,
                                                       oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin3X,
                                                       oy-self._PinsY,
                                                       oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin2X,
                                                       oy-self._PinsY,
                                                       oz+self._BoardOffZ)))))
        boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                    Part.makeCircle(pinrad,Base.Vector(ox+self._Pin1X,
                                                       oy-self._PinsY,
                                                       oz+self._BoardOffZ)))))
        self.board = boardsurf.extrude(Base.Vector(0,0,self._BoardThick))
        bodyrad = self._HeaderBodySize/2
        upperHBody = Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin4X,
                                                        oy+self._PinsY,
                                                        oz))))
        upperHBody = upperHBody.fuse(Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin3X,
                                                        oy+self._PinsY,
                                                        oz)))))
        upperHBody = upperHBody.fuse(Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin2X,
                                                        oy+self._PinsY,
                                                        oz)))))
        upperHBody = upperHBody.fuse(Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin1X,
                                                        oy+self._PinsY,
                                                        oz)))))
        self.ubody = upperHBody.extrude(Base.Vector(0,0,self._BoardOffZ))
        lowerHBody = Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin4X,
                                                        oy-self._PinsY,
                                                        oz))))
        lowerHBody = lowerHBody.fuse(Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin3X,
                                                        oy-self._PinsY,
                                                        oz)))))
        lowerHBody = lowerHBody.fuse(Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin2X,
                                                        oy-self._PinsY,
                                                        oz)))))
        lowerHBody = lowerHBody.fuse(Part.Face(Part.Wire(\
                     Part.makeCircle(bodyrad,Base.Vector(ox+self._Pin1X,
                                                        oy-self._PinsY,
                                                        oz)))))
        self.lbody = lowerHBody.extrude(Base.Vector(0,0,self._BoardOffZ))
        bodyCorner = Base.Vector(ox-(self._BodyXY/2),oy-(self._BodyXY/2),\
                                 oz+self._BoardOffZ+self._BoardThick)
        self.body = Part.makePlane(self._BodyXY,self._BodyXY,bodyCorner)\
                    .extrude(Base.Vector(0,0,self._BodyZ))
        
        stickOff = self._StickXY/2
        stickOrig = Base.Vector(ox-stickOff,oy-stickOff,\
                                oz+self._BoardOffZ+self._BoardThick+self._BodyZ)
        
        self.stick = Part.makePlane(self._StickXY,\
                                    self._StickXY,\
                                    stickOrig).extrude(Base.Vector(0,0,\
                                                                 self._StickZ))
        knob = Part.Face(Part.Wire(Part.makeCircle(self._KnobBodyDia/2,\
                                             Base.Vector(ox,oy,stickOrig.z+\
                                                        self._KnobBodyZoff))))\
                     .extrude(Base.Vector(0,0,self._KnobBodyHeight))
        knob = knob.cut(self.stick)
        self.knob = knob.fuse(Part.Face(Part.Wire(Part.makeCircle(\
                                        self._KnobTopDia/2.0,
                                        Base.Vector(ox,oy,\
                                                    stickOrig.z+\
                                                      self._KnobBodyHeight+\
                                                      self._KnobBodyZoff))))\
                                .extrude(Base.Vector(0,0,self._KnobTopHeight)))
    @staticmethod
    def knobSTL(filename):
        knob = Part.Face(Part.Wire(Part.makeCircle(
                            ThumbStick._KnobTopDia/2,
                            Base.Vector(0,0,0))))\
                        .extrude(Base.Vector(0,0,ThumbStick._KnobTopHeight))
        knob = knob.fuse(Part.Face(Part.Wire(Part.makeCircle(
                            ThumbStick._KnobBodyDia/2,
                            Base.Vector(0,0,ThumbStick._KnobTopHeight))))\
                        .extrude(Base.Vector(0,0,ThumbStick._KnobBodyHeight)))
        stick = Part.makePlane(ThumbStick._StickXY,\
                               ThumbStick._StickXY,\
                               Base.Vector(-ThumbStick._StickXY/2,
                                           -ThumbStick._StickXY/2,
                                           (ThumbStick._KnobTopHeight+\
                                            ThumbStick._KnobBodyHeight+\
                                            ThumbStick._KnobBodyZoff)-ThumbStick._StickZ))\
                    .extrude(Base.Vector(0,0,ThumbStick._StickZ))
        knob = knob.cut(stick)
        return knob.exportStl(filename)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_board")
        obj.Shape = self.board
        obj.Label=self.name+'_board'
        obj.ViewObject.ShapeColor=self._boardColor
        obj = doc.addObject("Part::Feature",self.name+"_ubody")
        obj.Shape = self.ubody
        obj.Label=self.name+'_ubody'
        obj.ViewObject.ShapeColor=self._headerColor
        obj = doc.addObject("Part::Feature",self.name+"_lbody")
        obj.Shape = self.lbody
        obj.Label=self.name+'_lbody'
        obj.ViewObject.ShapeColor=self._headerColor
        obj = doc.addObject("Part::Feature",self.name+"_body")
        obj.Shape = self.body
        obj.Label=self.name+'_body'
        obj.ViewObject.ShapeColor=self._BodyColor
        obj = doc.addObject("Part::Feature",self.name+"_stick")
        obj.Shape = self.stick
        obj.Label=self.name+'_stick'
        obj.ViewObject.ShapeColor=self._StickColor
        obj = doc.addObject("Part::Feature",self.name+"_knob")
        obj.Shape = self.knob
        obj.Label=self.name+'_knob'
        obj.ViewObject.ShapeColor=self._KnobColor
        
class Teensy(object):
    _Width  = 8.509+9.271   # Y dim
    _Length = 18.542+17.018 # X dim (board is rotated 90)
    _Thick = 1.6
    _YOff = 8.509
    _XOFF = 17.018
    _BoardOffZ = 2.54
    _BoardThick = 1.6
    _boardColor = tuple([0.0,1.0,0.0])
    USBWidth = 5.78
    _USBLength = 7.54
    _USBYOff = 8.509-5.25
    _USBXOff = 17.018+1.62
    USBZ = 1.87
    _USBColor = tuple([0.85,0.85,0.85])
    _PinG1X = -15.748
    _PinG1Y = -7.239
    _PinVINY = 8.001
    _PinSpace = 2.54
    _PinDia = 1.016
    _HeaderBodySize = 2.54
    _headerColor = tuple([0.0,0.0,0.0])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x 
        oy = origin.y
        oz = origin.z
        boardOrig = Base.Vector(ox-self._XOFF,oy-self._YOff,oz+self._BoardOffZ)
        boardsurf = Part.makePlane(self._Length,self._Width,boardOrig)
        pinrad = self._PinDia/2.0
        bodyrad = self._HeaderBodySize/2
        header1 = None
        header2 = None
        pinY1 = oy+self._PinG1Y
        pinY2 = oy+self._PinVINY
        pinZ = oz+self._BoardOffZ
        for px in range(14):
            pxoff = px*self._PinSpace
            pinX = ox+self._PinG1X+pxoff
            boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                            Part.makeCircle(pinrad,\
                                            Base.Vector(pinX,pinY1,pinZ)))))
            if header1 == None:
                header1 = Part.Face(Part.Wire(\
                            Part.makeCircle(bodyrad,\
                                            Base.Vector(pinX,pinY1,oz))))
            else:
                header1 = header1.fuse(Part.Face(Part.Wire(\
                                            Part.makeCircle(bodyrad,\
                                                            Base.Vector(pinX,\
                                                                        pinY1,\
                                                                        oz)))))
            boardsurf = boardsurf.cut(Part.Face(Part.Wire(\
                            Part.makeCircle(pinrad,\
                                            Base.Vector(pinX,pinY2,pinZ)))))
                                                        
            if header2 == None:
                header2 = Part.Face(Part.Wire(\
                            Part.makeCircle(bodyrad,\
                                            Base.Vector(pinX,pinY2,oz))))
            else:
                header2 = header2.fuse(Part.Face(Part.Wire(\
                                            Part.makeCircle(bodyrad,\
                                                            Base.Vector(pinX,\
                                                                        pinY2,\
                                                                        oz)))))
        self.board = boardsurf.extrude(Base.Vector(0,0,self._BoardThick))
        self.ubody = header1.extrude(Base.Vector(0,0,self._BoardOffZ))
        self.lbody = header2.extrude(Base.Vector(0,0,self._BoardOffZ))
        self.usbOrig = Base.Vector(ox-self._USBXOff,oy-self._USBYOff,\
                                oz+self._BoardOffZ+self._BoardThick)
        self.usb = Part.makePlane(self._USBLength,self.USBWidth,self.usbOrig)\
                        .extrude(Base.Vector(0,0,self.USBZ))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_board")
        obj.Shape = self.board
        obj.Label=self.name+'_board'
        obj.ViewObject.ShapeColor=self._boardColor
        obj = doc.addObject("Part::Feature",self.name+"_ubody")
        obj.Shape = self.ubody
        obj.Label=self.name+'_ubody'
        obj.ViewObject.ShapeColor=self._headerColor
        obj = doc.addObject("Part::Feature",self.name+"_lbody")
        obj.Shape = self.lbody
        obj.Label=self.name+'_lbody'
        obj.ViewObject.ShapeColor=self._headerColor
        obj = doc.addObject("Part::Feature",self.name+"_usb")
        obj.Shape = self.usb
        obj.Label=self.name+'_usb'
        obj.ViewObject.ShapeColor=self._USBColor
        
class LED(object):
    Diameter = 3
    _Height =   5.55
    def __init__(self,name,origin,color):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        self.led = Part.Face(Part.Wire(Part.makeCircle(self.Diameter/2,origin)))\
                    .extrude(Base.Vector(0,0,self._Height))
        self.color = color
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.led
        obj.Label=self.name
        obj.ViewObject.ShapeColor=self.color

class PCB(object):
    _PCBWidth = 43.180
    _PCBLength = 63.500
    PCBThickness = 1.6
    MHDiameter = 2.7
    _mhOffset = 2.54
    _mhXSpace = 38.100
    _mhYSpace = 58.420
    _boardColor = tuple([0.0,.7058,0.0])
    # XBoardOrig (left)   = 44.45
    # YBoardOrig (bottom) = 127
    # Switches (pin1)
    # 53.04,118.11  63.35,118.11 73.66,118.11
    _sw3X = (53.04-44.45)+(TactileSwitch._PinSpaceX/2.0)
    _sw2X = (63.35-44.45)+(TactileSwitch._PinSpaceX/2.0)
    _sw1X = (73.66-44.45)+(TactileSwitch._PinSpaceX/2.0)
    _swY  = (127-118.11)-(TactileSwitch._PinSpaceY/2.0)
    # ThumbStick: 66.04,101.6 (center)
    _ThumbStickX = 66.04-44.45
    _ThumbStickY = 127-101.6
    # Teensy at 65.278, 76.581
    _TeensyX = 65.278-44.45
    _TeensyY = 127-76.581
    # LEDS at 48.26,90.17 and 83.82,90.17
    _LED1X = 48.26-44.45
    _LED1Color = tuple([1.0,0.0,0.0])
    _LED2X = 83.82-44.45
    _LED2Color = tuple([0.0,1.0,0.0])
    _LEDY  = (127-90.17)+1.27
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        boardsurf = Part.makePlane(PCB._PCBWidth,PCB._PCBLength,origin)
        self.mhvector = {
            1 : Base.Vector(ox+PCB._mhOffset,oy+PCB._mhOffset,oz),
            2 : Base.Vector(ox+PCB._mhOffset+PCB._mhXSpace,
                            oy+PCB._mhOffset,oz),
            3 : Base.Vector(ox+PCB._mhOffset+PCB._mhXSpace,
                            oy+PCB._mhOffset+PCB._mhYSpace,oz),
            4 : Base.Vector(ox+PCB._mhOffset,
                            oy+PCB._mhOffset+PCB._mhYSpace,oz)
        }
        mhRadius = PCB.MHDiameter/2.0
        for i in range(1,5):
            mh = Part.Face(Part.Wire(Part.makeCircle(mhRadius,self.mhvector[i])))
            boardsurf = boardsurf.cut(mh)
        self.board = boardsurf.extrude(Base.Vector(0,0,PCB.PCBThickness))
        componentZ = oz+PCB.PCBThickness
        self.sw3Origin = Base.Vector(ox+PCB._sw3X,oy+PCB._swY,componentZ)
        self.sw3 = TactileSwitch(name+"_Sw3",self.sw3Origin)
        self.sw2Origin = Base.Vector(ox+PCB._sw2X,oy+PCB._swY,componentZ)
        self.sw2 = TactileSwitch(name+"_Sw2",self.sw2Origin)
        self.sw1Origin = Base.Vector(ox+PCB._sw1X,oy+PCB._swY,componentZ)
        self.sw1 = TactileSwitch(name+"_Sw1",self.sw1Origin)
        self.thumbStickOrigin = Base.Vector(ox+PCB._ThumbStickX,oy+PCB._ThumbStickY,\
                                        componentZ)
        self.thumbStick = ThumbStick(name+"_thumbStick",self.thumbStickOrigin)
        teensyOrogin = Base.Vector(ox+PCB._TeensyX,oy+PCB._TeensyY,componentZ)
        self.teensy = Teensy(name+"_teensy",teensyOrogin)
        self.led1origin = Base.Vector(ox+self._LED1X,oy+self._LEDY,componentZ)
        self.led1 = LED("XLED",self.led1origin,self._LED1Color)
        self.led2origin = Base.Vector(ox+self._LED2X,oy+self._LEDY,componentZ)
        self.led2 = LED("YLED",self.led2origin,self._LED2Color)
        
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_PCB")
        obj.Shape = self.board
        obj.Label=self.name+'_PCB'
        obj.ViewObject.ShapeColor=self._boardColor
        self.sw3.show()
        self.sw2.show()
        self.sw1.show()
        self.thumbStick.show()
        self.teensy.show()
        self.led1.show()
        self.led2.show()

class Box(object):
    _ShellThick = 4
    _OuterWidth = PCB._PCBWidth+4+4+3+3
    _PCBXOff = 4+3
    _OuterLength = PCB._PCBLength+4+4+3+3
    _PCBYOff = 4+3
    _BottomHeight = 4+6
    _Color = tuple([0.0,0.0,0.0])
    _RidgeSize = 2
    _StandoffDiameter = 5
    _Number3Clear = .099*25.4
    _Number3TapHole = (5/64)*25.4
    _TopHeight = 15
    _PlungerShaftDia = 5
    _PlungerShaftHeight = 6
    _PlungerBaseDia  = 8
    _PlungerBaseHeight = 3
    _PlungerColor = tuple([1.0,0.0,0.0])
    _USBHoleYLength = 11
    _USBHomeZHeight = 8
    _USBZOff = (8-Teensy.USBZ)/2.0
    _USBYOff = (11-Teensy.USBWidth)/2.0
    _ScrewDepth = 12.7
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        XNorm=Base.Vector(1,0,0)
        XNormR=Base.Vector(-1,0,0)
        YNorm=Base.Vector(0,1,0)
        YNormR=Base.Vector(0,-1,0)
        self.board = PCB(name+"_board",Base.Vector(ox+self._PCBXOff,oy+self._PCBYOff,oz+self._BottomHeight))
        self.bottom = self.MakeBottom()
        self.top    = self.MakeTop(origin.add(Base.Vector(0,0,\
                                        self._BottomHeight+self._TopHeight)))
        
        plunger1Org=Base.Vector(origin.x+self.board.sw1Origin.x,origin.y+self.board.sw1Origin.y,self.board.sw1.ButtonTop())
        self.plunger1 = self.MakePlunger(plunger1Org)
        plunger2Org=Base.Vector(origin.x+self.board.sw2Origin.x,origin.y+self.board.sw2Origin.y,self.board.sw2.ButtonTop())
        self.plunger2 = self.MakePlunger(plunger2Org)
        plunger3Org=Base.Vector(origin.x+self.board.sw3Origin.x,origin.y+self.board.sw3Origin.y,self.board.sw3.ButtonTop())
        self.plunger3 = self.MakePlunger(plunger3Org)
    def MakePlunger(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        plunger = Part.Face(Part.Wire(Part.makeCircle(self._PlungerBaseDia/2,origin))).extrude(Base.Vector(0,0,self._PlungerBaseHeight))
        shaftOrigin = origin.add(Base.Vector(0,0,self._PlungerBaseHeight))
        plunger = \
            plunger.fuse(Part.Face(Part.Wire(Part.makeCircle(self._PlungerShaftDia/2,shaftOrigin))).extrude(Base.Vector(0,0,self._PlungerShaftHeight)))
        return plunger
    def MakeBottom(self):
        origin = self.origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        XNorm=Base.Vector(1,0,0)
        XNormR=Base.Vector(-1,0,0)
        YNorm=Base.Vector(0,1,0)
        YNormR=Base.Vector(0,-1,0)
        bottom = Part.makePlane(self._OuterWidth,self._OuterLength,origin)\
                    .extrude(Base.Vector(0,0,self._ShellThick))
        bottom = \
            bottom.fuse(Part.makePlane(self._BottomHeight-self._ShellThick,\
                                            self._OuterLength,\
                                            origin.add(Base.Vector(0,self._OuterLength,self._ShellThick)),XNorm)\
                  .extrude(Base.Vector(self._ShellThick,0,0)))
        bottom = \
            bottom.fuse(Part.makePlane(self._RidgeSize,\
                                            self._OuterLength,\
                                            origin.add(Base.Vector(0,self._OuterLength,self._BottomHeight)),XNorm)\
                  .extrude(Base.Vector(self._RidgeSize,0,0)))
        bottom = \
            bottom.fuse(Part.makePlane(self._BottomHeight-self._ShellThick,\
                                       self._OuterLength,\
                                       origin.add(Base.Vector(self._OuterWidth,\
                                                              self._OuterLength,\
                                                              self._BottomHeight)),\
                                       XNormR)\
                  .extrude(Base.Vector(-self._ShellThick,0,0)))
        bottom = \
            bottom.fuse(Part.makePlane(self._RidgeSize,\
                                            self._OuterLength,\
                                            origin.add(Base.Vector(self._OuterWidth,self._OuterLength,self._BottomHeight+self._RidgeSize)),XNormR)\
                  .extrude(Base.Vector(-self._RidgeSize,0,0)))
        bottom = \
            bottom.fuse(Part.makePlane(self._BottomHeight-self._ShellThick,
                                            self._OuterWidth-(self._ShellThick*2),\
                                            origin.add(Base.Vector(self._ShellThick,0,self._ShellThick)),\
                                            YNorm)\
                  .extrude(Base.Vector(0,self._ShellThick,0)))
        bottom = \
            bottom.fuse(Part.makePlane(self._RidgeSize,\
                                            self._OuterWidth-(self._RidgeSize*2),
                                            origin.add(Base.Vector(self._RidgeSize,0,self._BottomHeight)),
                                            YNorm)\
                   .extrude(Base.Vector(0,self._RidgeSize,0)))                         
        bottom = \
            bottom.fuse(Part.makePlane(self._BottomHeight-self._ShellThick,
                                            self._OuterWidth-(self._ShellThick*2),\
                                            origin.add(Base.Vector(self._ShellThick,self._OuterLength-self._ShellThick,self._BottomHeight)),\
                                            YNormR)\
                  .extrude(Base.Vector(0,self._ShellThick,0)))
        bottom = \
            bottom.fuse(Part.makePlane(self._RidgeSize,\
                                            self._OuterWidth-(self._RidgeSize*2),
                                            origin.add(Base.Vector(self._RidgeSize,self._OuterLength-self._RidgeSize,self._BottomHeight+self._RidgeSize)),
                                            YNormR)\
                   .extrude(Base.Vector(0,self._RidgeSize,0)))
        for i in [1,2,3,4]:
            h = self.board.mhvector[i]
            bottom = bottom.fuse(Part.Face(Part.Wire(\
                            Part.makeCircle(self._StandoffDiameter/2.0,
                                            Base.Vector(h.x,h.y,oz+self._ShellThick))))\
                                            .extrude(Base.Vector(0,0,self._BottomHeight-self._ShellThick)))
            bottom = bottom.cut(Part.Face(Part.Wire(\
                            Part.makeCircle(self._Number3Clear/2.0,
                                            Base.Vector(h.x,h.y,oz))))\
                                            .extrude(Base.Vector(0,0,self._BottomHeight)))
        return(bottom)
    def MakeTop(self,origin,deltaZ=-1):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        XNorm=Base.Vector(1,0,0)
        XNormR=Base.Vector(-1,0,0)
        YNorm=Base.Vector(0,1,0)
        YNormR=Base.Vector(0,-1,0)
        if deltaZ<0:
            toporigin = origin.add(Base.Vector(0,0,-self._ShellThick))
        else:
            toporigin = origin
        top  = Part.makePlane(self._OuterWidth,self._OuterLength,toporigin)\
                    .extrude(Base.Vector(0,0,self._ShellThick))
        plunger1Org=Base.Vector(origin.x+self.board.sw1Origin.x,origin.y+self.board.sw1Origin.y,toporigin.z)
        top = top.cut(Part.Face(Part.Wire(Part.makeCircle(self._PlungerShaftDia/2,plunger1Org))).extrude(Base.Vector(0,0,self._ShellThick)))
        plunger2Org=Base.Vector(origin.x+self.board.sw2Origin.x,origin.y+self.board.sw2Origin.y,toporigin.z)
        top = top.cut(Part.Face(Part.Wire(Part.makeCircle(self._PlungerShaftDia/2,plunger2Org))).extrude(Base.Vector(0,0,self._ShellThick)))
        plunger3Org=Base.Vector(origin.x+self.board.sw3Origin.x,origin.y+self.board.sw3Origin.y,toporigin.z)
        top = top.cut(Part.Face(Part.Wire(Part.makeCircle(self._PlungerShaftDia/2,plunger3Org))).extrude(Base.Vector(0,0,self._ShellThick)))
        thumbStickHoleOrigin=Base.Vector(origin.x+self.board.thumbStickOrigin.x,origin.y+self.board.thumbStickOrigin.y,toporigin.z)
        top = top.cut(Part.Face(Part.Wire(Part.makeCircle(ThumbStick.CutoutDiameter()/2,thumbStickHoleOrigin))).extrude(Base.Vector(0,0,self._ShellThick)))
        l1Org=Base.Vector(origin.x+self.board.led1origin.x,origin.y+self.board.led1origin.y,toporigin.z)
        top = top.cut(Part.Face(Part.Wire(Part.makeCircle(LED.Diameter/2,l1Org))).extrude(Base.Vector(0,0,self._ShellThick)))
        l2Org=Base.Vector(origin.x+self.board.led2origin.x,origin.y+self.board.led2origin.y,toporigin.z)
        top = top.cut(Part.Face(Part.Wire(Part.makeCircle(LED.Diameter/2,l2Org))).extrude(Base.Vector(0,0,self._ShellThick)))
        sideHeight = self._TopHeight-self._RidgeSize
        if deltaZ<0:
            origin1 = origin.add(Base.Vector(0,0,-sideHeight))
        else:
            origin1 = origin.add(Base.Vector(0,0,self._ShellThick))
        sideHeight -= self._ShellThick
        top = \
            top.fuse(Part.makePlane(sideHeight,self._OuterLength,\
                                        origin1.add(Base.Vector(0,\
                                                        self._OuterLength,0)),\
                                        XNorm)\
                  .extrude(Base.Vector(self._ShellThick,0,0)))
        if deltaZ<0:
            ridgeZ = -self._RidgeSize
        else:
            ridgeZ = sideHeight
        w = self._RidgeSize
        h = self._OuterLength-(self._RidgeSize*2)
        o = origin1.add(Base.Vector(self._RidgeSize,\
                                    self._OuterLength-(self._RidgeSize*1),\
                                    ridgeZ))
        e = Base.Vector(self._RidgeSize,0,0)
        top = \
            top.fuse(Part.makePlane(w,h,o,XNorm).extrude(e))
        top = \
            top.fuse(Part.makePlane(sideHeight,\
                                    self._OuterLength,\
                                    origin1.add(Base.Vector(self._OuterWidth,\
                                                            self._OuterLength,\
                                                            sideHeight)),\
                                    XNormR)\
                   .extrude(Base.Vector(-self._ShellThick,0,0)))
        w = self._RidgeSize
        h = self._OuterLength-(self._RidgeSize*2)
        o = origin1.add(Base.Vector(self._OuterWidth-self._RidgeSize*2,
                                    self._OuterLength-(self._RidgeSize*1),\
                                    ridgeZ+self._RidgeSize))
        e = Base.Vector(self._RidgeSize,0,0)
        top = \
            top.fuse(Part.makePlane(w,h,o,XNormR).extrude(e))
        
        h = self._USBHoleYLength
        w = self._USBHomeZHeight
        uz = self.board.teensy.usbOrig.z-self.board.origin.z
        o = origin1.add(Base.Vector(0,
                                    self.board.teensy.usbOrig.y-self._USBYOff+w,\
                                    uz-self._USBZOff))
        if deltaZ<0:
            o = o.add(Base.Vector(0,Teensy.USBWidth/2,-Teensy.USBZ))
            w += o.z-ridgeZ
            o = Base.Vector(o.x,o.y,ridgeZ)
        else:
            o = o.add(Base.Vector(self._OuterWidth-self._ShellThick,Teensy.USBWidth/2,Teensy.USBZ))
            w += ridgeZ
            o = Base.Vector(o.x,o.y,origin.z+self._ShellThick)
        e = Base.Vector(self._ShellThick,0)
        top = top.cut(Part.makePlane(w,h,o,XNorm).extrude(e))
        o = origin1.add(Base.Vector(self._ShellThick,0,0))
        top = \
            top.fuse(Part.makePlane(sideHeight,self._OuterWidth-(self._ShellThick*2),\
                                            o,\
                                            YNorm)\
                  .extrude(Base.Vector(0,self._ShellThick,0)))
        o = Base.Vector(o.x,o.y+self._RidgeSize,o.z+ridgeZ)
        w = self._RidgeSize
        h = self._OuterWidth-(self._ShellThick*2)
        e = Base.Vector(0,self._RidgeSize,0)
        top = \
            top.fuse(Part.makePlane(w,h,o,YNorm).extrude(e))
        o = origin1.add(Base.Vector(self._ShellThick,\
                                    self._OuterLength-self._ShellThick,\
                                    sideHeight))
        top = \
            top.fuse(Part.makePlane(sideHeight,\
                                    self._OuterWidth-(self._ShellThick*2),\
                                    o,YNormR)\
                      .extrude(Base.Vector(0,self._ShellThick,0)))
        if deltaZ<0:
            o = o.add(Base.Vector(0,0,-sideHeight))
        else:
            o = o.add(Base.Vector(0,0,self._RidgeSize))
        w = self._RidgeSize
        h = self._OuterWidth-(self._ShellThick*2)
        e = Base.Vector(0,self._RidgeSize,0)
        top = \
            top.fuse(Part.makePlane(w,h,o,YNormR).extrude(e))
        boardZExtra = self._RidgeSize-PCB.PCBThickness
        postExtrude = Base.Vector(0,0,sideHeight+boardZExtra)
        boardExtrude = Base.Vector(0,0,PCB.PCBThickness)
        screwExtrude = Base.Vector(0,0,self._ScrewDepth)
        if deltaZ<0:
            postZ = origin.z-(self._TopHeight-self._RidgeSize)-boardZExtra
            boardZ = origin.z-self._TopHeight
            screwZ = boardZ
        else:
            postZ = origin.z+self._ShellThick
            boardZ = origin.z+(self._TopHeight+boardZExtra)-self._RidgeSize
            screwZ = boardZ-self._ScrewDepth+self._RidgeSize
        for i in [1,2,3,4]:
            h = self.board.mhvector[i]
            oPost = Base.Vector(origin.x+h.x,origin.y+h.y,postZ)
            top = top.fuse(Part.Face(Part.Wire(\
                        Part.makeCircle(self._StandoffDiameter/2.0,\
                                        oPost))).extrude(postExtrude))
            oMHole = Base.Vector(origin.x+h.x,origin.y+h.y,boardZ)
            top = top.fuse(Part.Face(Part.Wire(\
                        Part.makeCircle(PCB.MHDiameter/2.0,\
                                        oMHole))).extrude(boardExtrude))
            oScrew = Base.Vector(origin.x+h.x,origin.y+h.y,screwZ)
            top = top.cut(Part.Face(Part.Wire(\
                        Part.makeCircle(self._Number3TapHole/2.0,\
                                        oScrew))).extrude(screwExtrude))
        return(top)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_bottom")
        obj.Shape = self.bottom
        obj.Label=self.name+'_bottom'
        obj.ViewObject.ShapeColor=self._Color
        obj = doc.addObject("Part::Feature",self.name+"_top")
        obj.Shape = self.top
        obj.Label=self.name+'_top'
        obj.ViewObject.ShapeColor=self._Color
        obj = doc.addObject("Part::Feature",self.name+"_plunger1")
        obj.Shape = self.plunger1
        obj.Label=self.name+'_plunger1'
        obj.ViewObject.ShapeColor=self._PlungerColor
        obj = doc.addObject("Part::Feature",self.name+"_plunger2")
        obj.Shape = self.plunger2
        obj.Label=self.name+'_plunger2'
        obj.ViewObject.ShapeColor=self._PlungerColor
        obj = doc.addObject("Part::Feature",self.name+"_plunger3")
        obj.Shape = self.plunger3
        obj.Label=self.name+'_plunger3'
        obj.ViewObject.ShapeColor=self._PlungerColor
        self.board.show()
    



if __name__ == '__main__':
    if "TeensyJoystick_Box" in App.listDocuments().keys():
        App.closeDocument("TeensyJoystick_Box")
    App.ActiveDocument=App.newDocument("TeensyJoystick_Box")
    doc = App.activeDocument()
    o = Base.Vector(0,0,0)
    box = Box("box",o)
    box.show()

    doc.saveAs("TeensyJoystick.FCStd")
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewRight()
    ThumbStick.knobSTL("ThumbStickKnob.stl")
    box.MakeTop(Base.Vector(0,0,0),1).exportStl("BoxTop.stl")
    box.bottom.exportStl("BoxBottom.stl")
    box.MakePlunger(Base.Vector(0,0,0)).exportStl("Plunger.stl")
