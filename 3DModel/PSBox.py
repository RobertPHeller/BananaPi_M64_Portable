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
#  Created       : Sat May 30 19:30:31 2020
#  Last Modified : <210418.1358>
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


from PSPCB import *
from Electromech import *
from Case import *



## Al. box:      Mouser #563-CU-3002A
# Base: 2.125in wide, 4.000in long, 1.625in high
# Cover 2.031in wide, 3.906in long, 1.562in high

class CU_3002A_(object):
    _basewidth = 2.125*25.4
    def baseWidth(self):
        return CU_3002A_._basewidth
    _baselength = 4.000*25.4
    def baseLength(self):
        return CU_3002A_._baselength
    _baseheight = 1.625*25.4
    def baseHeight(self):
        return CU_3002A_._baseheight
    _baseflangewidth =  0.375*25.4
    def baseFlangeWidth(self):
        return CU_3002A_._baseflangewidth
    _baseholeoffset = 0.172*25.4
    def baseHoleOffset(self):
        return CU_3002A_._baseholeoffset
    _baseholeheightoffset = 0.594*25.4
    def baseHoleHeightOffset(self):
        return CU_3002A_._baseholeheightoffset
    _baseholediameter = (5.0/32.0)*25.4
    def baseHoleDiameter(self):
        return CU_3002A_._baseholediameter
    def baseHoleRadius(self):
        return CU_3002A_._baseholediameter/2.0
    _coverwidth = 2.031*25.4
    def coverWidth(self):
        return CU_3002A_._coverwidth
    _coverlength = 3.906*25.4
    def coverLength(self):
        return CU_3002A_._coverlength
    _coverheight = 1.562*25.4
    def coverHeight(self):
        return CU_3002A_._coverheight
    _coverholeoffset = 0.156*25.4
    def coverHoleOffset(self):
        return CU_3002A_._coverholeoffset
    _coverholeheightoffset = 0.968*25.4
    def coverHoleHeightOffset(self):
        return CU_3002A_._coverholeheightoffset
    _coverholediameter = (3.0/32.0)*25.4
    def coverHoleDiameter(self):
        return CU_3002A_._coverholediameter
    def coverHoleRadius(self):
        return CU_3002A_._coverholediameter/2.0
    _thickness = 0.04*25.4
    def thickness(self):
        return CU_3002A_._thickness
    def __init__(self):
        raise RuntimeError("No Instances allowed for CU_3002A_!")

class CU_3002A_Base(CU_3002A_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        XNorm=Base.Vector(1,0,0)
        XThick=Base.Vector(self.thickness(),0,0)
        XThick_=Base.Vector(-self.thickness(),0,0)
        YNorm=Base.Vector(0,1,0)
        YThick=Base.Vector(0,self.thickness(),0)
        YThick_=Base.Vector(0,-self.thickness(),0)
        ZNorm=Base.Vector(0,0,1)
        ZThick=Base.Vector(0,0,self.thickness())
        base = Part.makePlane(self.baseWidth(),self.baseLength(),origin,ZNorm
                             ).extrude(ZThick)
        front = Part.makePlane(self.baseHeight(),self.baseWidth(),origin,YNorm
                              ).extrude(YThick)
        backorig = Base.Vector(ox,oy+self.baseLength(),oz)
        back =  Part.makePlane(self.baseHeight(),self.baseWidth(),backorig,YNorm
                              ).extrude(YThick_)
        lfforig=Base.Vector(ox+self.baseWidth(),oy+self.baseFlangeWidth(),oz)
        lffholeorig=Base.Vector(lfforig.x,lfforig.y-self.baseHoleOffset(),
                                (lfforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        lffhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),lffholeorig,XNorm)))
        leftfrontflange = Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),lfforig,XNorm
                                        ).cut(lffhole).extrude(XThick_)
        front = front.fuse(leftfrontflange)
        lbforig=Base.Vector(ox+self.baseWidth(),oy+self.baseLength(),oz)
        leftbottomflange = Part.makePlane(self.baseFlangeWidth(),self.baseLength(),lbforig,XNorm
                                         ).extrude(XThick_)
        base = base.fuse(leftbottomflange)
        lbforig=Base.Vector(ox+self.baseWidth(),oy+self.baseLength(),oz)
        lbfholeorig=Base.Vector(lbforig.x,lbforig.y-self.baseHoleOffset(),
                                (lbforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        lbfhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),lbfholeorig,XNorm)))
        leftbackflange = Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),lbforig,XNorm
                                        ).cut(lbfhole).extrude(XThick_)
        back = back.fuse(leftbackflange)
        rfforig=Base.Vector(ox,oy+self.baseFlangeWidth(),oz)
        rffholeorig=Base.Vector(rfforig.x,
                                (rfforig.y)-self.baseHoleOffset(),
                                (rfforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        rffhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),rffholeorig,XNorm)))
        rightfrontflange=Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),rfforig,XNorm
                                        ).cut(rffhole).extrude(XThick_)
        front = front.fuse(rightfrontflange)
        rbforig=Base.Vector(ox,oy+self.baseLength(),oz)
        rightbottomflange=Part.makePlane(self.baseFlangeWidth(),self.baseLength(),rbforig,XNorm
                                         ).extrude(XThick_)
        base = base.fuse(rightbottomflange)
        rbforig=Base.Vector(ox,oy+self.baseLength(),oz)
        rbfholeorig=Base.Vector(rbforig.x,rbforig.y-self.baseHoleOffset(),
                                (rbforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        rbfhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),rbfholeorig,XNorm)))
        rightbackflange = Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),rbforig,XNorm
                                        ).cut(rbfhole).extrude(XThick_)
        back = back.fuse(rightbackflange)
        
        self.base = base.fuse(front).fuse(back)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_CU3002ABase')
        obj.Shape = self.base        
        obj.Label=self.name+'_CU3002ABase'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])

class CU_3002A_Cover(CU_3002A_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        XNorm=Base.Vector(1,0,0)
        XThick=Base.Vector(self.thickness(),0,0)
        XThick_=Base.Vector(-self.thickness(),0,0)
        YNorm=Base.Vector(0,1,0)
        YThick=Base.Vector(0,self.thickness(),0)
        YThick_=Base.Vector(0,-self.thickness(),0)
        ZNorm=Base.Vector(0,0,1)
        ZThick=Base.Vector(0,0,self.thickness())
        ZThick_=Base.Vector(0,0,-self.thickness())
        toporig = Base.Vector(ox+self.thickness(),oy+self.thickness(),oz+self.thickness()+self.coverHeight())
        top = Part.makePlane(self.coverWidth(),self.coverLength(),toporig).extrude(ZThick_)
        leftorig = Base.Vector(ox+self.thickness(),oy+self.thickness()+self.coverLength(),oz+self.thickness())
        left = Part.makePlane(self.coverHeight(),self.coverLength(),leftorig,XNorm).extrude(XThick_)
        lx = leftorig.x
        ly = leftorig.y
        lz = leftorig.z
        frontholeorig = Base.Vector(lx,ly-self.coverHoleOffset(),lz+self.coverHoleHeightOffset())
        fronthole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,frontholeorig,XNorm))).extrude(XThick_)
        left = left.cut(fronthole)
        backholeorig = Base.Vector(lx,ly-self.coverLength()+self.coverHoleOffset(),lz+self.coverHoleHeightOffset())
        backhole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,backholeorig,XNorm))).extrude(XThick_)
        left = left.cut(backhole)
        rightorig = Base.Vector(ox+self.thickness()+self.coverWidth(),oy+self.thickness()+self.coverLength(),oz+self.thickness())
        right = Part.makePlane(self.coverHeight(),self.coverLength(),rightorig,XNorm).extrude(XThick_)
        rx = rightorig.x
        ry = rightorig.y
        rz = rightorig.z
        frontholeorig = Base.Vector(rx,ry-self.coverHoleOffset(),rz+self.coverHoleHeightOffset())
        fronthole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,frontholeorig,XNorm))).extrude(XThick_)
        right = right.cut(fronthole)
        backholeorig = Base.Vector(rx,ry-self.coverLength()+self.coverHoleOffset(),rz+self.coverHoleHeightOffset())
        backhole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,backholeorig,XNorm))).extrude(XThick_)
        right = right.cut(backhole)
        self.cover = top.fuse(left).fuse(right)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_CU3002ACover')
        obj.Shape = self.cover
        obj.Label=self.name+'_CU3002ACover'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])
        

class CU_3002A(CU_3002A_Base,CU_3002A_Cover):
    def __init__(self,name,origin):
        CU_3002A_Base.__init__(self,name,origin)
        CU_3002A_Cover.__init__(self,name,origin)
    def show(self):
        CU_3002A_Base.show(self)
        CU_3002A_Cover.show(self)

class CU_3006A_(object):
    _basewidth = 3.000*25.4
    def baseWidth(self):
        return CU_3006A_._basewidth
    _baselength = 5.250*25.4
    def baseLength(self):
        return CU_3006A_._baselength
    _baseheight = 2.125*25.4
    def baseHeight(self):
        return CU_3006A_._baseheight
    _baseflangewidth =  0.375*25.4
    def baseFlangeWidth(self):
        return CU_3006A_._baseflangewidth
    _baseholeoffset = 0.172*25.4
    def baseHoleOffset(self):
        return CU_3006A_._baseholeoffset
    _baseholeheightoffset = 1.094*25.4
    def baseHoleHeightOffset(self):
        return CU_3006A_._baseholeheightoffset
    _baseholediameter = (5.0/32.0)*25.4
    def baseHoleDiameter(self):
        return CU_3006A_._baseholediameter
    def baseHoleRadius(self):
        return CU_3006A_._baseholediameter/2.0
    _coverwidth = 2.906*25.4
    def coverWidth(self):
        return CU_3006A_._coverwidth
    _coverlength = 5.156*25.4
    def coverLength(self):
        return CU_3006A_._coverlength
    _coverheight = 2.062*25.4
    def coverHeight(self):
        return CU_3006A_._coverheight
    _coverholeoffset = 0.156*25.4
    def coverHoleOffset(self):
        return CU_3006A_._coverholeoffset
    _coverholeheightoffset = 0.968*25.4
    def coverHoleHeightOffset(self):
        return CU_3006A_._coverholeheightoffset
    _coverholediameter = (3.0/32.0)*25.4
    def coverHoleDiameter(self):
        return CU_3006A_._coverholediameter
    def coverHoleRadius(self):
        return CU_3006A_._coverholediameter/2.0
    _thickness = 0.04*25.4
    def thickness(self):
        return CU_3006A_._thickness
    def __init__(self):
        raise RuntimeError("No Instances allowed for CU_3006A_!")

class CU_3006A_Base(CU_3006A_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        XNorm=Base.Vector(1,0,0)
        XThick=Base.Vector(self.thickness(),0,0)
        XThick_=Base.Vector(-self.thickness(),0,0)
        YNorm=Base.Vector(0,1,0)
        YThick=Base.Vector(0,self.thickness(),0)
        YThick_=Base.Vector(0,-self.thickness(),0)
        ZNorm=Base.Vector(0,0,1)
        ZThick=Base.Vector(0,0,self.thickness())
        base = Part.makePlane(self.baseWidth(),self.baseLength(),origin,ZNorm
                             ).extrude(ZThick)
        front = Part.makePlane(self.baseHeight(),self.baseWidth(),origin,YNorm
                              ).extrude(YThick)
        backorig = Base.Vector(ox,oy+self.baseLength(),oz)
        back =  Part.makePlane(self.baseHeight(),self.baseWidth(),backorig,YNorm
                              ).extrude(YThick_)
        lfforig=Base.Vector(ox+self.baseWidth(),oy+self.baseFlangeWidth(),oz)
        lffholeorig=Base.Vector(lfforig.x,lfforig.y-self.baseHoleOffset(),
                                (lfforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        lffhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),lffholeorig,XNorm)))
        leftfrontflange = Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),lfforig,XNorm
                                        ).cut(lffhole).extrude(XThick_)
        front = front.fuse(leftfrontflange)
        lbforig=Base.Vector(ox+self.baseWidth(),oy+self.baseLength(),oz)
        leftbottomflange = Part.makePlane(self.baseFlangeWidth(),self.baseLength(),lbforig,XNorm
                                         ).extrude(XThick_)
        base = base.fuse(leftbottomflange)
        lbforig=Base.Vector(ox+self.baseWidth(),oy+self.baseLength(),oz)
        lbfholeorig=Base.Vector(lbforig.x,lbforig.y-self.baseHoleOffset(),
                                (lbforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        lbfhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),lbfholeorig,XNorm)))
        leftbackflange = Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),lbforig,XNorm
                                        ).cut(lbfhole).extrude(XThick_)
        back = back.fuse(leftbackflange)
        rfforig=Base.Vector(ox,oy+self.baseFlangeWidth(),oz)
        rffholeorig=Base.Vector(rfforig.x,
                                (rfforig.y)-self.baseHoleOffset(),
                                (rfforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        rffhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),rffholeorig,XNorm)))
        rightfrontflange=Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),rfforig,XNorm
                                        ).cut(rffhole).extrude(XThick_)
        front = front.fuse(rightfrontflange)
        rbforig=Base.Vector(ox,oy+self.baseLength(),oz)
        rightbottomflange=Part.makePlane(self.baseFlangeWidth(),self.baseLength(),rbforig,XNorm
                                         ).extrude(XThick_)
        base = base.fuse(rightbottomflange)
        rbforig=Base.Vector(ox,oy+self.baseLength(),oz)
        rbfholeorig=Base.Vector(rbforig.x,rbforig.y-self.baseHoleOffset(),
                                (rbforig.z+self.baseHeight())-self.baseHoleHeightOffset())
        rbfhole=Part.Face(Part.Wire(Part.makeCircle(self.baseHoleRadius(),rbfholeorig,XNorm)))
        rightbackflange = Part.makePlane(self.baseHeight(),self.baseFlangeWidth(),rbforig,XNorm
                                        ).cut(rbfhole).extrude(XThick_)
        back = back.fuse(rightbackflange)
        
        self.base = base.fuse(front).fuse(back)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_CU3002ABase')
        obj.Shape = self.base        
        obj.Label=self.name+'_CU3006ABase'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])

class CU_3006A_Cover(CU_3006A_):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        XNorm=Base.Vector(1,0,0)
        XThick=Base.Vector(self.thickness(),0,0)
        XThick_=Base.Vector(-self.thickness(),0,0)
        YNorm=Base.Vector(0,1,0)
        YThick=Base.Vector(0,self.thickness(),0)
        YThick_=Base.Vector(0,-self.thickness(),0)
        ZNorm=Base.Vector(0,0,1)
        ZThick=Base.Vector(0,0,self.thickness())
        ZThick_=Base.Vector(0,0,-self.thickness())
        toporig = Base.Vector(ox+self.thickness(),oy+self.thickness(),oz+self.thickness()+self.coverHeight())
        top = Part.makePlane(self.coverWidth(),self.coverLength(),toporig).extrude(ZThick_)
        leftorig = Base.Vector(ox+self.thickness(),oy+self.thickness()+self.coverLength(),oz+self.thickness())
        left = Part.makePlane(self.coverHeight(),self.coverLength(),leftorig,XNorm).extrude(XThick_)
        lx = leftorig.x
        ly = leftorig.y
        lz = leftorig.z
        frontholeorig = Base.Vector(lx,ly-self.coverHoleOffset(),lz+self.coverHoleHeightOffset())
        fronthole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,frontholeorig,XNorm))).extrude(XThick_)
        left = left.cut(fronthole)
        backholeorig = Base.Vector(lx,ly-self.coverLength()+self.coverHoleOffset(),lz+self.coverHoleHeightOffset())
        backhole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,backholeorig,XNorm))).extrude(XThick_)
        left = left.cut(backhole)
        rightorig = Base.Vector(ox+self.thickness()+self.coverWidth(),oy+self.thickness()+self.coverLength(),oz+self.thickness())
        right = Part.makePlane(self.coverHeight(),self.coverLength(),rightorig,XNorm).extrude(XThick_)
        rx = rightorig.x
        ry = rightorig.y
        rz = rightorig.z
        frontholeorig = Base.Vector(rx,ry-self.coverHoleOffset(),rz+self.coverHoleHeightOffset())
        fronthole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,frontholeorig,XNorm))).extrude(XThick_)
        right = right.cut(fronthole)
        backholeorig = Base.Vector(rx,ry-self.coverLength()+self.coverHoleOffset(),rz+self.coverHoleHeightOffset())
        backhole = Part.Face(Part.Wire(Part.makeCircle(self.coverHoleDiameter()/2.0,backholeorig,XNorm))).extrude(XThick_)
        right = right.cut(backhole)
        self.cover = top.fuse(left).fuse(right)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_CU3002ACover')
        obj.Shape = self.cover
        obj.Label=self.name+'_CU3006ACover'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])
        

class CU_3006A(CU_3006A_Base,CU_3006A_Cover):
    def __init__(self,name,origin):
        CU_3006A_Base.__init__(self,name,origin)
        CU_3006A_Cover.__init__(self,name,origin)
    def show(self):
        CU_3006A_Base.show(self)
        CU_3006A_Cover.show(self)

from abc import ABCMeta, abstractmethod, abstractproperty

class Bud_AC(object):
    __metaclass__ = ABCMeta
    @staticmethod
    def A():
        pass
    @staticmethod
    def B():
        pass
    @staticmethod
    def C():
        pass
    @staticmethod
    def TYPE():
        pass
    @staticmethod
    def GUAGE():
        pass
    @staticmethod
    def BRACKETHOLES():
        return False
    def _buildbox(self):
        ox = self.origin.x
        oy = self.origin.y
        oz = self.origin.z
        XNorm=Base.Vector(1,0,0)
        XThick=Base.Vector(self.GUAGE(),0,0)
        XThick_=Base.Vector(-self.GUAGE(),0,0)
        YNorm=Base.Vector(0,1,0)
        YThick=Base.Vector(0,self.GUAGE(),0)
        YThick_=Base.Vector(0,-self.GUAGE(),0)
        ZNorm=Base.Vector(0,0,1)
        ZThick=Base.Vector(0,0,self.GUAGE())
        ZThick_=Base.Vector(0,0,-self.GUAGE())
        base = Part.makePlane(self.A(),self.B(),self.origin,ZNorm).extrude(ZThick)
        front = Part.makePlane(self.C()-self.GUAGE(),self.A(),self.origin,YNorm).extrude(YThick)
        frontflange = Part.makePlane(self.A(),.5*25.4,self.origin.add(Base.Vector(0,0,self.C()-self.GUAGE())),ZNorm).extrude(ZThick_)
        if (self.TYPE() == 'A'):
            center = self.A()/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(center,(.5-.187)*25.4,self.C()-self.GUAGE())),ZNorm))).extrude(ZThick_)
            frontflange = frontflange.cut(h)
        elif (self.TYPE() == 'B'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(2.969*25.4,(.5*25.4)-(0.187*25.4),self.C())),ZNorm))).extrude(ZThick_)
            frontflange = frontflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(self.A()-2.969*25.4,(.5*25.4)-(0.187*25.4),self.C())),ZNorm))).extrude(ZThick_)
            frontflange = frontflange.cut(h2)
        elif (self.TYPE() == 'C'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(0.812*25.4,.25*25.4,self.C())),ZNorm))).extrude(ZThick_)
            frontflange = frontflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(self.A()-0.812*25.4,.25*25.4,self.C())),ZNorm))).extrude(ZThick_)
            frontflange = frontflange.cut(h2)
        front = front.fuse(frontflange)
        backorig = Base.Vector(ox,oy+self.B(),0)
        back  = Part.makePlane(self.C()-self.GUAGE(),self.A(),backorig,YNorm).extrude(YThick_)
        backflange = Part.makePlane(self.A(),.5*25.4,self.origin.add(Base.Vector(0,0+self.B()-(.5*25.4),self.C()-self.GUAGE())),ZNorm).extrude(ZThick_)
        if (self.TYPE() == 'A'):
            center = self.A()/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(center,.187*25.4,self.C()-self.GUAGE())),ZNorm))).extrude(ZThick_)
            backflange = backflange.cut(h)
        elif (self.TYPE() == 'B'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(2.969*25.4,(-.5+0.187)*25.4,self.C())),ZNorm))).extrude(ZThick_)
            backflange = backflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(self.A()-2.969*25.4,(-.5+0.187)*25.4,self.C())),ZNorm))).extrude(ZThick_)
            backflange = backflange.cut(h2)
        elif (self.TYPE() == 'C'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(0.812*25.4,-.25*25.4,self.C())),ZNorm))).extrude(ZThick_)
            backflange = backflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(self.A()-0.812*25.4,-.25*25.4,self.C())),ZNorm))).extrude(ZThick_)
            backflange = backflange.cut(h2)
        back = back.fuse(backflange)
        sidelen = self.B()-2*self.GUAGE()
        leftorig = Base.Vector(ox,oy+sidelen+self.GUAGE(),oz)
        left  = Part.makePlane(self.C(),sidelen,leftorig,XNorm).extrude(XThick)
        leftflange = Part.makePlane(.5*25.4,sidelen,leftorig.add(Base.Vector(0,-sidelen,self.C())),ZNorm).extrude(ZThick_)
        if (self.TYPE() == 'A'):
            center = sidelen/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,leftorig.add(Base.Vector((.5-.187)*25.4,-center,self.C())),ZNorm))).extrude(ZThick_)
            leftflange = leftflange.cut(h)
        left = left.fuse(leftflange)
        if (self.BRACKETHOLES()):
            bh1 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,leftorig.add(Base.Vector(0,-(25.4-self.GUAGE()),self.C()-25.4)),XNorm))).extrude(XThick)
            left = left.cut(bh1)
            bh2 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,leftorig.add(Base.Vector(0,-((sidelen+self.GUAGE())-25.4),self.C()-25.4)),XNorm))).extrude(XThick)
            left = left.cut(bh2)
        rightorig = Base.Vector(ox+self.A(),oy+sidelen+self.GUAGE(),oz)
        right = Part.makePlane(self.C(),sidelen,rightorig,XNorm).extrude(XThick_)
        rightflange = Part.makePlane(.5*25.4,sidelen,rightorig.add(Base.Vector(-.5*25.4,-sidelen,self.C())),ZNorm).extrude(ZThick_)
        if (self.TYPE() == 'A'):
            center = sidelen/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,rightorig.add(Base.Vector((-.5+.187)*25.4,-center,self.C())),ZNorm))).extrude(ZThick_)
            rightflange = rightflange.cut(h)
        right = right.fuse(rightflange)
        if (self.BRACKETHOLES()):
            bh1 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,rightorig.add(Base.Vector(0,-(25.4-self.GUAGE()),self.C()-25.4)),XNorm))).extrude(XThick)
            right = right.cut(bh1)
            bh2 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,rightorig.add(Base.Vector(0,-((sidelen+self.GUAGE())-25.4),self.C()-25.4)),XNorm))).extrude(XThick)
            right = right.cut(bh2)
        self.box = base.fuse(front).fuse(back).fuse(left).fuse(right)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_ACBox')
        obj.Shape = self.box
        obj.Label=self.name+'_ACBox'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])
        
class Bud_BPA(object):
    __metaclass__ = ABCMeta
    @staticmethod
    def AA():
        pass
    @staticmethod
    def BB():
        pass
    @staticmethod
    def TYPE():
        pass
    def _buildbottom(self,C):
        ZNorm=Base.Vector(0,0,1)
        ZThick=Base.Vector(0,0,.040*25.4)
        borig = self.origin.add(Base.Vector((.812-.750)*25.4,(.250-.187)*25.4,C))
        bottom = Part.makePlane(self.BB(),self.AA(),borig).extrude(ZThick)
        if self.TYPE() == 'A':
            centerA = self.AA()/2.0
            centerB = self.BB()/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(centerB,0.219*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(0.219*25.4,centerA,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(centerB,self.AA()-0.219*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-0.219*25.4,centerA,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
        elif self.TYPE() == 'B':
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(2.875*25.4,0.219*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-2.875*25.4,0.219*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(2.875*25.4,self.AA()-0.219*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-2.875*25.4,self.AA()-0.219*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
        elif self.TYPE() == 'C':
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(.750*25.4,0.187*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-.750*25.4,0.187*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(.750*25.4,self.AA()-0.187*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
            h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-.750*25.4,self.AA()-0.187*25.4,0)),ZNorm))).extrude(ZThick)
            bottom = bottom.cut(h)
        self.bottom = bottom
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_BPABottom')
        obj.Shape = self.bottom
        obj.Label=self.name+'_BPABottom'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])



class AC_1404(Bud_AC):
    @staticmethod
    def A():
        return(5.000*25.4)
    @staticmethod
    def B():
        return(4.000*25.4)
    @staticmethod
    def C():
        return(2.000*25.4)
    @staticmethod
    def TYPE():
        return 'C'
    @staticmethod
    def GUAGE():
        return(.040*25.4)
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self._buildbox()

class BPA_1504(Bud_BPA):
    @staticmethod
    def AA():
        return(3.875*25.4)
    @staticmethod
    def BB():
        return(4.875*25.4)
    @staticmethod
    def TYPE():
        return 'C'
    @staticmethod
    def _C():
        return(2.0*25.4)
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self._buildbottom(self._C())
        
class PSBoxOrig(CU_3006A):
    _standoff_height = 9.0
    _standoff_dia = 5
    _inletXoff =  1.27
    _inletZoff =  19
    _dcstrainXoff = 26.9875
    _dcstrainZoff = 20.6375
    def _fanXoff(self):
        return self.thickness()+self.coverWidth()
    def _fanZoff(self):
        return self.baseFlangeWidth()+self.thickness()
    def _fan1Yoff(self):
        return (self.coverLength()-(2*Fan02510SS_05P_AT00._fanwidth_height))/2.0
    def _fan2Yoff(self):
        return self._fan1Yoff()+Fan02510SS_05P_AT00._fanwidth_height
    def InletFlangeCutout(self,yBase,yThick):
        return self.inlet.Flange(yBase,yThick)
    def __init__(self,name,origin):
        CU_3006A.__init__(self,name,origin)
        ox = origin.x
        oy = origin.y
        oz = origin.z
        pcborig=Base.Vector(ox+((self.baseWidth()-PCBwithStrips._psPCBwidth)/2.0),
                            oy+((self.baseLength()-PCBwithStrips._psPCBlength)/2.0),
                            oz+self.thickness()+PSBox._standoff_height)
        self.pspcb = PSOnPCB(self.name+'_pcb',pcborig)
        self.standoffs = list()
        for i in [1,2,3,4]:
            self.standoffs.append(self.pspcb.Standoff(i,oz+self.thickness(),
                                                      PSBox._standoff_height,
                                                      PSBox._standoff_dia))
        mhthick = Base.Vector(0,0,self.thickness())
        b = self.base
        for i in [1,2,3,4]:
            mh = self.pspcb.MountingHole(i,oz).extrude(mhthick)
            b = b.cut(mh)
        self.base = b
        self.inlet = Inlet(self.name+"_inlet",Base.Vector(ox+PSBox._inletXoff,
                                                        oy+self.baseLength(),
                                                        oz+PSBox._inletZoff))
        b = self.base.cut(self.inlet.bodyCutout(oy+self.baseLength(),-self.thickness()))
        self.base = b  
        self.dcstrainrelief = DCStrainRelief(self.name+"_dcstrain",Base.Vector(ox+PSBox._dcstrainXoff,oy,oz+PSBox._dcstrainZoff))
        b = self.base.cut(self.dcstrainrelief.MountHole(oy,self.thickness()))
        self.base = b
        fx = ox+self._fanXoff()
        f1y = oy+self._fan1Yoff()
        fz = oz+self._fanZoff()
        f1origin = Base.Vector(fx,f1y,fz)
        self.fan1 = Fan02510SS_05P_AT00(self.name+"_fan1",f1origin)
        g1origin = Base.Vector(fx-CU_3006A_._thickness/2.0,f1y-9,fz+25)
        self.grommet1 = Grommet(self.name+"_grommet1",g1origin)
        f2y = oy+self._fan2Yoff()
        f2origin = Base.Vector(fx,f2y,fz)
        self.fan2 = Fan02510SS_05P_AT00(self.name+"_fan2",f2origin)
        g2origin = Base.Vector(fx-CU_3006A_._thickness/2.0,f2y+25+9,fz+25)
        self.grommet2 = Grommet(self.name+"_grommet2",g2origin)
        c = self.cover
        for i in [1,2,3,4]:
            c = c.cut(self.fan1.MountingHole(i,fx,-self.thickness()))
            c = c.cut(self.fan2.MountingHole(i,fx,-self.thickness()))
        c = c.cut(self.fan1.RoundFanHole(fx,-self.thickness()))
        c = c.cut(self.fan2.RoundFanHole(fx,-self.thickness()))
        c = self.fan1.DrillGrillHoles(ox+self.thickness(),-self.thickness(),2.5,3.5,c)
        c = self.fan2.DrillGrillHoles(ox+self.thickness(),-self.thickness(),2.5,3.5,c)
        c = self.grommet1.CutHole(c)
        c = self.grommet2.CutHole(c)
        self.cover = c
    def MountingHole(self,i,zBase):
        return self.pspcb.MountingHole(i,zBase)
    def RoundFanHole1(self,xBase,height):
        return self.fan1.RoundFanHole(xBase,height)
    def RoundFanHole2(self,xBase,height):
        return self.fan2.RoundFanHole(xBase,height)
    def SquareFanHole1(self,xBase,height):
        return self.fan1.SquareFanHole(xBase,height)
    def SquareFanHole2(self,xBase,height):
        return self.fan2.SquareFanHole(xBase,height)
    def DrillGrillHoles1(self,xBase,height,hdia,hspace,panel):
        return self.fan1.DrillGrillHoles(xBase,height,hdia,hspace,panel)
    def DrillGrillHoles2(self,xBase,height,hdia,hspace,panel):
        return self.fan2.DrillGrillHoles(xBase,height,hdia,hspace,panel)
    def show(self):
        doc = App.activeDocument()
        CU_3006A.show(self)
        self.pspcb.show()
        i = 1
        for standoff in self.standoffs:
            obj = doc.addObject("Part::Feature",self.name+('_Standoff%d' % i))
            obj.Shape = standoff
            obj.Label=self.name+('_Standoff%d' % i)
            obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
            i = i + 1
        self.inlet.show()
        self.dcstrainrelief.show()
        self.fan1.show()
        self.fan2.show()
        self.grommet1.show()    
        self.grommet2.show()    

class PSBox(AC_1404,BPA_1504):
    _standoff_height = 9.0
    _standoff_dia = 5
    def InletFlangeCutout(self,yBase,yThick):
        return self.inlet.Flange(yBase,yThick)
    def __init__(self,name,origin):
        AC_1404.__init__(self,name,origin)
        BPA_1504.__init__(self,name,origin)
        ox = origin.x
        oy = origin.y
        oz = origin.z
        pcb1orig=Base.Vector(ox+PS2OnPCB._psPCBwidth+5.08+5.08,
                            oy+((self.B()-PSOnPCB._psPCBlength)/2.0),
                            oz+self.GUAGE()+self._standoff_height)
        self.pspcb1 = PSOnPCB(self.name+'_pcb1',pcb1orig)
        self.standoffs = list()
        for i in [1,2,3,4]:
            self.standoffs.append(self.pspcb1.Standoff(i,oz+self.GUAGE(),
                                                      self._standoff_height,
                                                      self._standoff_dia))
        mhthick = Base.Vector(0,0,self.GUAGE())
        b = self.box
        for i in [1,2,3,4]:
            mh = self.pspcb1.MountingHole(i,oz).extrude(mhthick)
            b = b.cut(mh)
        self.box = b
        pcb2orig = pcb1orig.add(Base.Vector(-(PS2OnPCB._psPCBwidth+5.08),0,0))
        self.pspcb2 = PS2OnPCB(self.name+'_pcb2',pcb2orig)
        for i in [1,2,3,4]:
            self.standoffs.append(self.pspcb2.Standoff(i,oz+self.GUAGE(),
                                                       self._standoff_height,
                                                       self._standoff_dia))
        b = self.box
        for i in [1,2,3,4]:
            mh = self.pspcb2.MountingHole(i,oz).extrude(mhthick)
            b = b.cut(mh)
        self.box = b
        # 120VAC inlet
        inletXoff = self.A()-(Inlet._bodywidth+5.08+(PSOnPCB._psPCBwidth-7.62))
        inletZoff = self.C()-(Inlet._bodyheight+5.08)
        self.inlet = Inlet(self.name+"_inlet",Base.Vector(ox+inletXoff,\
                                                          oy+self.B(),\
                                                          oz+inletZoff))
        b = self.box.cut(self.inlet.bodyCutout(oy+self.B(),-self.GUAGE()))
        self.box = b  
        # DC/Bat out strainreliefs
        M64_5VStrainOrig = Base.Vector(pcb1orig.x+(PSOnPCB._psPCBwidth/2),
                                       oy,
                                       oz+(self.C()-((DCStrainRelief._flangedia/2)+5.08)))
        self.m64_5vstrain = DCStrainRelief(self.name+"_m64_5vstrain",M64_5VStrainOrig)
        b = self.box.cut(self.m64_5vstrain.MountHole(oy,-self.GUAGE()))
        self.box = b
        LCD_12VStrainOrig = Base.Vector(ox+((DCStrainRelief._flangedia/2)+5.08),\
                                        oy,\
                                        oz+(self.C()-((DCStrainRelief._flangedia/2)+5.08)))
        self.lcd_12vstrain = DCStrainRelief(self.name+"_lcd_12vstrain",LCD_12VStrainOrig)
        b = self.box.cut(self.lcd_12vstrain.MountHole(oy,-self.GUAGE()))
        self.box = b
        AUX_BattStrainOrig = LCD_12VStrainOrig.add(Base.Vector(DCStrainRelief._flangedia+1.27,0,0))
        self.aux_battstrain = DCStrainRelief(self.name+"_aux_battstrain",AUX_BattStrainOrig)
        b = self.box.cut(self.aux_battstrain.MountHole(oy,-self.GUAGE()))
        self.box = b
        SATA_5VStrainOrig = AUX_BattStrainOrig.add(Base.Vector(DCStrainRelief._flangedia+1.27,0,0))
        self.sata_5vstrain = DCStrainRelief(self.name+"_sata_5vstrain",SATA_5VStrainOrig)
        b = self.box.cut(self.sata_5vstrain.MountHole(oy,-self.GUAGE()))
        self.box = b
        # Fans
        f1x = self.pspcb1.origin.x+(self.pspcb1._psPCBwidth/2)
        f1x -= Fan02510SS_05P_AT00_TopMount._fanwidth_height/2
        f1y = self.pspcb1.origin.y+(self.pspcb1._psPCBlength/2)
        f1y -= Fan02510SS_05P_AT00_TopMount._fanwidth_height/2
        fan1Orig = Base.Vector(f1x,f1y,oz+self.C())
        self.fan1 = Fan02510SS_05P_AT00_TopMount(self.name+'_fan1',fan1Orig)
        for i in [1,2,3,4]:
            b = self.bottom.cut(self.fan1.MountingHole(i,oz+self.C(),2*self.GUAGE()))
            self.bottom = b
        b = self.fan1.RoundFanGrill(oz+self.C(),2*self.GUAGE(),self.bottom)
        self.bottom = b
        f2x = self.pspcb2.origin.x+(self.pspcb2._psPCBwidth/2)
        f2x -= Fan02510SS_05P_AT00_TopMount._fanwidth_height/2
        f2y = self.pspcb2.origin.y+(self.pspcb2._psPCBlength/2)
        f2y -= Fan02510SS_05P_AT00_TopMount._fanwidth_height/2
        fan2Orig = Base.Vector(f2x,f2y,oz+self.C())
        self.fan2 = Fan02510SS_05P_AT00_TopMount(self.name+'_fan2',fan2Orig)
        for i in [1,2,3,4]:
            b = self.bottom.cut(self.fan2.MountingHole(i,oz+self.C(),2*self.GUAGE()))
            self.bottom = b
        b = self.fan2.RoundFanGrill(oz+self.C(),2*self.GUAGE(),self.bottom)
        self.bottom = b
        # Vent holes
        self._drillFanIntakeGrill(f1x)
        self._drillFanIntakeGrill(f2x)
        # VAdj hole
        VAdjHoleOrig = Base.Vector(ox,self.pspcb2.VAdjustY(),self.pspcb2.VAdjustZ())
        XNorm = Base.Vector(1,0,0)
        HoleExtrude = Base.Vector(self.GUAGE(),0,0)
        HoleRadius = .125*25.4
        b = self.box.cut(Part.Face(Part.Wire(Part.makeCircle(HoleRadius,VAdjHoleOrig,XNorm))).extrude(HoleExtrude))
        self.box = b
        # Key Switch hole
        KeyButtonOrig = Base.Vector(ox,self.pspcb2.KeyButtonY(),self.pspcb2.KeyButtonZ())
        b = self.box.cut(Part.Face(Part.Wire(Part.makeCircle(HoleRadius,KeyButtonOrig,XNorm))).extrude(HoleExtrude))
        self.box = b
        # LED View Hole
    def _drillFanIntakeGrill(self,ox):
        oy = self.origin.y
        oz = self.origin.z+self._standoff_height
        height = self.GUAGE()
        hdia = 2.5
        hspace = 3.5
        hrad = hdia/2.0
        holeside=self.fan1._fanwidth_height
        extrude = Base.Vector(0,height,0)
        YNorm=Base.Vector(0,1,0)
        x = hspace/2.0
        panel = self.box
        while x < holeside:
            y = hspace/2.0
            while y < holeside:
                holeorig=Base.Vector(ox+x,oy,oz+y)
                hole = Part.Face(Part.Wire(Part.makeCircle(hrad,holeorig,YNorm))).extrude(extrude)
                panel = panel.cut(hole)
                y += hspace
            x += hspace
        self.box = panel
    def MountingHole(self,i,Z):
        if i >= 1 and i <= 4:
            return self.pspcb1.MountingHole(i,Z)
        elif i >= 5 and i <= 8:
            return self.pspcb2.MountingHole(i-4,Z)
    def show(self):
        doc = App.activeDocument()
        AC_1404.show(self)
        BPA_1504.show(self)
        self.pspcb1.show()
        self.pspcb2.show()
        self.inlet.show()
        self.m64_5vstrain.show()
        self.lcd_12vstrain.show()
        self.aux_battstrain.show()
        self.sata_5vstrain.show()
        self.fan1.show()
        self.fan2.show()
        i = 1
        for standoff in self.standoffs:
            obj = doc.addObject("Part::Feature",self.name+('_Standoff%d' % i))
            obj.Shape = standoff
            obj.Label=self.name+('_Standoff%d' % i)
            obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
            i = i + 1

if __name__ == '__main__':
    if "PowerSupplyBoxTechDrawing" in App.listDocuments().keys():
        App.closeDocument("PowerSupplyBoxTechDrawing")
    App.ActiveDocument=App.newDocument("PowerSupplyBoxTechDrawing")
    doc = App.activeDocument()
    o = Base.Vector(0,0,0)
    psbox = PSBox("psbox",o)
    psbox.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewIsometric()
    boxbounds = psbox.box.BoundBox
    bottombounds = psbox.bottom.BoundBox
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = doc.USLetterTemplate.EditableTexts
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = doc.USLetterTemplate.EditableTexts
    edt['CompanyName'] = "Deepwoods Software"
    edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA'    
    edt['DrawingTitle1']= 'Power Supply Box'
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
    doc.addObject('TechDraw::DrawPage','PowerSupplyBoxPage1')
    doc.PowerSupplyBoxPage1.Template = doc.USLetterTemplate
    edt = doc.PowerSupplyBoxPage1.Template.EditableTexts
    edt['DrawingTitle2']= "Box (Bottom and Front)"
    edt['Scale'] = '1/2'
    edt['Sheet'] = "Sheet 1 of 3"
    doc.PowerSupplyBoxPage1.Template.EditableTexts = edt
    doc.PowerSupplyBoxPage1.ViewObject.show()
    boxsheet = doc.addObject('Spreadsheet::Sheet','BoxDimensionTable1')
    boxsheet.set("A1",'%-11.11s'%"Dim")
    boxsheet.set("B1",'%10.10s'%"inch")
    boxsheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','BoxBottomView')
    doc.PowerSupplyBoxPage1.addView(doc.BoxBottomView)
    doc.BoxBottomView.Source = doc.psbox_ACBox
    doc.BoxBottomView.X = 60
    doc.BoxBottomView.Y = 160
    doc.BoxBottomView.Scale = .5
    doc.BoxBottomView.Direction=(0.0,0.0,-1.0)
    doc.BoxBottomView.Caption = "Bottom"
    doc.addObject('TechDraw::DrawViewDimension','MHDia')
    doc.MHDia.Type = 'Diameter'
    doc.MHDia.References2D=[(doc.BoxBottomView,"Edge16")]
    doc.MHDia.FormatSpec='MHDia (8x)'
    doc.MHDia.Arbitrary = True
    doc.MHDia.X = 3
    doc.MHDia.Y = 1.5
    doc.PowerSupplyBoxPage1.addView(doc.MHDia)
    boxsheet.set("A%d"%ir,'%-11.11s'%"MHDia")
    boxsheet.set("B%d"%ir,'%10.6f'%(PSOnPCB._mhdia/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%PSOnPCB._mhdia)
    ir += 1
    # Vertex2 (upper left corner)
    # Vertex35 (lower right corner)
    # Vertex26 (upper left corner hole)
    # Vertex17 (upper second hole)
    # Vertex20 (upper third  hole)
    # Vertex29 (upper fourth hole)
    # Vertex23 (lower left   hole)
    boxshape = doc.psbox_ACBox.Shape
    #print('*** boxshape:',file=sys.__stderr__)
    #i = 0
    #for e in boxshape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        circ = e.Curve
    #        if circ.Location.z == 0:
    #            print('*** boxshape: Edges[%d].Curve %g at (%g,%g)'%\
    #                    (i,circ.Radius*2,circ.Location.x,circ.Location.y),
    #                    file=sys.__stderr__)
    #    i += 1
    #i = 0
    #for v in boxshape.Vertexes:
    #    if v.Z == 0:
    #        print('*** boxshape: Vertexes[%d] at (%g,%g)'%\
    #              (i,v.X,v.Y),file=sys.__stderr__)
    #    i += 1
    Vertex2 = boxshape.Vertexes[0]
    Vertex35 = boxshape.Vertexes[139]
    Vertex26 = boxshape.Vertexes[20]
    Vertex17 = boxshape.Vertexes[17]
    Vertex20 = boxshape.Vertexes[18]
    Vertex29 = boxshape.Vertexes[21]
    Vertex23 = boxshape.Vertexes[19]
    doc.addObject('TechDraw::DrawViewDimension','Box1A')
    doc.Box1A.Type = 'DistanceX'
    doc.Box1A.References2D=[(doc.BoxBottomView,"Vertex2"),(doc.BoxBottomView,"Vertex35")]
    doc.Box1A.FormatSpec='A'
    doc.Box1A.Arbitrary = True
    doc.Box1A.X = 0
    doc.Box1A.Y = 40
    doc.PowerSupplyBoxPage1.addView(doc.Box1A)
    boxsheet.set("A%d"%ir,'%-11.11s'%"A")
    ADist = Vertex35.X - Vertex2.X #psbox.A()
    boxsheet.set("B%d"%ir,'%10.6f'%(ADist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%ADist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1B')
    doc.Box1B.Type = 'DistanceY'
    doc.Box1B.References2D=[(doc.BoxBottomView,"Vertex2"),(doc.BoxBottomView,"Vertex35")]
    doc.Box1B.FormatSpec='B'
    doc.Box1B.Arbitrary = True
    doc.Box1B.X = 44
    doc.Box1B.Y = 0
    doc.PowerSupplyBoxPage1.addView(doc.Box1B)
    boxsheet.set("A%d"%ir,'%-11.11s'%"B")
    BDist = Vertex35.Y - Vertex2.Y #psbox.B()
    boxsheet.set("B%d"%ir,'%10.6f'%(BDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%BDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1C')
    doc.Box1C.Type = 'DistanceX'
    doc.Box1C.References2D=[(doc.BoxBottomView,"Vertex2"),(doc.BoxBottomView,"Vertex26")]
    doc.Box1C.FormatSpec='C'
    doc.Box1C.Arbitrary = True
    doc.Box1C.X = -25
    doc.Box1C.Y = 35
    doc.PowerSupplyBoxPage1.addView(doc.Box1C)
    boxsheet.set("A%d"%ir,'%-11.11s'%"C")
    CDist = Vertex26.X - Vertex2.X
    boxsheet.set("B%d"%ir,'%10.6f'%(CDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%CDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1D')
    doc.Box1D.Type = 'DistanceX'
    doc.Box1D.References2D=[(doc.BoxBottomView,"Vertex26"),(doc.BoxBottomView,"Vertex17")]
    doc.Box1D.FormatSpec='D'
    doc.Box1D.Arbitrary = True
    doc.Box1D.X = -10
    doc.Box1D.Y = 35
    doc.PowerSupplyBoxPage1.addView(doc.Box1D)
    boxsheet.set("A%d"%ir,'%-11.11s'%"D")
    DDist = Vertex17.X - Vertex26.X
    boxsheet.set("B%d"%ir,'%10.6f'%(DDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%DDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1E')
    doc.Box1E.Type = 'DistanceX'
    doc.Box1E.References2D=[(doc.BoxBottomView,"Vertex17"),(doc.BoxBottomView,"Vertex20")]
    doc.Box1E.FormatSpec='E'
    doc.Box1E.Arbitrary = True
    doc.Box1E.X = 4
    doc.Box1E.Y = 35
    doc.PowerSupplyBoxPage1.addView(doc.Box1E)
    boxsheet.set("A%d"%ir,'%-11.11s'%"E")
    EDist = Vertex20.X - Vertex17.X
    boxsheet.set("B%d"%ir,'%10.6f'%(EDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%EDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1F')
    doc.Box1F.Type = 'DistanceX'
    doc.Box1F.References2D=[(doc.BoxBottomView,"Vertex20"),(doc.BoxBottomView,"Vertex29")]
    doc.Box1F.FormatSpec='F'
    doc.Box1F.Arbitrary = True
    doc.Box1F.X = 15
    doc.Box1F.Y = 35
    doc.PowerSupplyBoxPage1.addView(doc.Box1F)
    boxsheet.set("A%d"%ir,'%-11.11s'%"F")
    FDist = Vertex29.X - Vertex20.X
    boxsheet.set("B%d"%ir,'%10.6f'%(FDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%FDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1G')
    doc.Box1G.Type = 'DistanceY'
    doc.Box1G.References2D=[(doc.BoxBottomView,"Vertex2"),(doc.BoxBottomView,"Vertex26")]
    doc.Box1G.FormatSpec='G'
    doc.Box1G.Arbitrary = True
    doc.Box1G.X = 36
    doc.Box1G.Y = 20
    doc.PowerSupplyBoxPage1.addView(doc.Box1G)
    boxsheet.set("A%d"%ir,'%-11.11s'%"G")
    GDist = Vertex26.Y - Vertex2.Y
    boxsheet.set("B%d"%ir,'%10.6f'%(GDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%GDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1H')
    doc.Box1H.Type = 'DistanceY'
    doc.Box1H.References2D=[(doc.BoxBottomView,"Vertex23"),(doc.BoxBottomView,"Vertex26")]
    doc.Box1H.FormatSpec='H'
    doc.Box1H.Arbitrary = True
    doc.Box1H.X = 36
    doc.Box1H.Y = 0
    doc.PowerSupplyBoxPage1.addView(doc.Box1H)
    boxsheet.set("A%d"%ir,'%-11.11s'%"H")
    HDist = Vertex23.Y - Vertex26.Y
    boxsheet.set("B%d"%ir,'%10.6f'%(HDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%HDist)
    ir += 1
    doc.BoxBottomView.recompute()
    
    doc.addObject('TechDraw::DrawViewPart','BoxFrontView')
    doc.PowerSupplyBoxPage1.addView(doc.BoxFrontView)
    doc.BoxFrontView.Source = doc.psbox_ACBox
    doc.BoxFrontView.X = 60
    doc.BoxFrontView.Y = 90
    doc.BoxFrontView.Scale = .5
    doc.BoxFrontView.Direction=(0.0,-1.0,0.0)
    doc.BoxFrontView.Caption = "Front"

    doc.addObject('TechDraw::DrawViewDimension','Box1I')
    doc.Box1I.Type = 'Diameter'
    doc.Box1I.References2D=[(doc.BoxFrontView,"Edge108")]
    doc.Box1I.FormatSpec='IDia (4x)'
    doc.Box1I.Arbitrary = True
    doc.Box1I.X = 0
    doc.Box1I.Y = 17
    doc.PowerSupplyBoxPage1.addView(doc.Box1I)
    boxsheet.set("A%d"%ir,'%-11.11s'%"IDia")
    boxsheet.set("B%d"%ir,'%10.6f'%(DCStrainRelief._bodydia/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%DCStrainRelief._bodydia)
    ir += 1

    # Vertex1 (lower left corner)
    # Vertex5 (upper right corner)
    # Vertex311 (left most strain relief)
    # Vertex305 (2nd strain relief)
    # Vertex308 (3rd strain relief)
    # Vertex302 (4th  strain relief)
    #
    # Edge97 Upper left most Grill Hole (for diameter)
    #
    # Left Batch grill holes:
    # Vertex278 Upper left most Grill Hole Center
    # Vertex257 Upper next Grill Hole
    # Vertex272 Next lower leftmost Grill Hole
    # Right Batch grill holes:
    # Vertex14  Upper Left Grill hole center
    boxshape = doc.psbox_ACBox.Shape
    #print('*** boxshape:',file=sys.__stderr__)
    #i = 0
    #for e in boxshape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        circ = e.Curve
    #        if circ.Location.y == 0:
    #            print('*** boxshape: Edges[%d].Curve %g at (%g,%g)'%\
    #                    (i,circ.Radius*2,circ.Location.x,circ.Location.z),
    #                    file=sys.__stderr__)
    #    i += 1
    #i = 0
    #for v in boxshape.Vertexes:
    #    if v.Y == 0:
    #        print('*** boxshape: Vertexes[%d] at (%g,%g)'%\
    #              (i,v.X,v.Z),file=sys.__stderr__)
    #    i += 1
    Vertex1 = boxshape.Vertexes[0]
    Vertex5 = boxshape.Vertexes[157]
    Vertex311 = boxshape.Vertexes[136]
    Vertex305 = boxshape.Vertexes[134]
    Vertex308 = boxshape.Vertexes[135]
    Vertex302 = boxshape.Vertexes[133]
    Vertex278 = boxshape.Vertexes[125]
    Vertex257 = boxshape.Vertexes[118]
    Vertex272 = boxshape.Vertexes[123]
    Vertex14  = boxshape.Vertexes[37]
    doc.addObject('TechDraw::DrawViewDimension','Box1J')
    doc.Box1J.Type = 'Diameter'
    doc.Box1J.References2D=[(doc.BoxFrontView,"Edge97")]
    doc.Box1J.FormatSpec='JDia (98x)'
    doc.Box1J.Arbitrary = True
    doc.Box1J.X = 23
    doc.Box1J.Y = -18
    doc.PowerSupplyBoxPage1.addView(doc.Box1J)
    boxsheet.set("A%d"%ir,'%-11.11s'%"JDia")
    JDia = 2.5 
    boxsheet.set("B%d"%ir,'%10.6f'%(JDia/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%JDia)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1K')
    doc.Box1K.Type = 'DistanceY'
    doc.Box1K.References2D=[(doc.BoxFrontView,"Vertex1"),\
                        (doc.BoxFrontView,"Vertex5")]
    doc.Box1K.FormatSpec='K'
    doc.Box1K.Arbitrary = True
    doc.Box1K.X = 36
    doc.Box1K.Y = 0
    doc.PowerSupplyBoxPage1.addView(doc.Box1K)
    boxsheet.set("A%d"%ir,'%-11.11s'%"K")
    KDist = Vertex5.Z - Vertex1.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(KDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%KDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1L')
    doc.Box1L.Type = 'DistanceX'
    doc.Box1L.References2D=[(doc.BoxFrontView,"Vertex1"),\
                        (doc.BoxFrontView,"Vertex5")]
    doc.Box1L.FormatSpec='L'
    doc.Box1L.Arbitrary = True
    doc.Box1L.X = 0
    doc.Box1L.Y = 35
    doc.PowerSupplyBoxPage1.addView(doc.Box1L)
    boxsheet.set("A%d"%ir,'%-11.11s'%"L")
    LDist = Vertex5.X - Vertex1.X
    boxsheet.set("B%d"%ir,'%10.6f'%(LDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%LDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1M')
    doc.Box1M.Type = 'DistanceX'
    doc.Box1M.References2D=[(doc.BoxFrontView,"Vertex1"),\
                        (doc.BoxFrontView,"Vertex311")]
    doc.Box1M.FormatSpec='M'
    doc.Box1M.Arbitrary = True
    doc.Box1M.X = -29
    doc.Box1M.Y = 25
    doc.PowerSupplyBoxPage1.addView(doc.Box1M)
    boxsheet.set("A%d"%ir,'%-11.11s'%"M")
    MDist = Vertex311.X - Vertex1.X
    boxsheet.set("B%d"%ir,'%10.6f'%(MDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%MDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1N')
    doc.Box1N.Type = 'DistanceX'
    doc.Box1N.References2D=[(doc.BoxFrontView,"Vertex305"),\
                        (doc.BoxFrontView,"Vertex311")]
    doc.Box1N.FormatSpec='N'
    doc.Box1N.Arbitrary = True
    doc.Box1N.X = -24
    doc.Box1N.Y = 25
    doc.PowerSupplyBoxPage1.addView(doc.Box1N)
    boxsheet.set("A%d"%ir,'%-11.11s'%"N")
    NDist = Vertex305.X - Vertex311.X
    boxsheet.set("B%d"%ir,'%10.6f'%(NDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%NDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1O')
    doc.Box1O.Type = 'DistanceX'
    doc.Box1O.References2D=[(doc.BoxFrontView,"Vertex305"),\
                        (doc.BoxFrontView,"Vertex308")]
    doc.Box1O.FormatSpec='O'
    doc.Box1O.Arbitrary = True
    doc.Box1O.X = -16
    doc.Box1O.Y = 25
    doc.PowerSupplyBoxPage1.addView(doc.Box1O)
    boxsheet.set("A%d"%ir,'%-11.11s'%"O")
    ODist = Vertex308.X - Vertex305.X
    boxsheet.set("B%d"%ir,'%10.6f'%(ODist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%ODist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1P')
    doc.Box1P.Type = 'DistanceX'
    doc.Box1P.References2D=[(doc.BoxFrontView,"Vertex308"),\
                        (doc.BoxFrontView,"Vertex302")]
    doc.Box1P.FormatSpec='P'
    doc.Box1P.Arbitrary = True
    doc.Box1P.X = 0
    doc.Box1P.Y = 25
    doc.PowerSupplyBoxPage1.addView(doc.Box1P)
    boxsheet.set("A%d"%ir,'%-11.11s'%"P")
    PDist = Vertex302.X - Vertex308.X
    boxsheet.set("B%d"%ir,'%10.6f'%(PDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%PDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1Q')
    doc.Box1Q.Type = 'DistanceY'
    doc.Box1Q.References2D=[(doc.BoxFrontView,"Vertex1"),\
                        (doc.BoxFrontView,"Vertex311")]
    doc.Box1Q.FormatSpec='Q'
    doc.Box1Q.Arbitrary = True
    doc.Box1Q.X = 45
    doc.Box1Q.Y = 0
    doc.PowerSupplyBoxPage1.addView(doc.Box1Q)
    boxsheet.set("A%d"%ir,'%-11.11s'%"Q")
    QDist = Vertex311.Z - Vertex1.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(QDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%QDist)
    ir += 1

    doc.addObject('TechDraw::DrawViewDimension','Box1R')
    doc.Box1R.Type = 'DistanceX'
    doc.Box1R.References2D=[(doc.BoxFrontView,"Vertex1"),\
                        (doc.BoxFrontView,"Vertex278")]
    doc.Box1R.FormatSpec='R'
    doc.Box1R.Arbitrary = True
    doc.Box1R.X = -26
    doc.Box1R.Y = -15
    doc.PowerSupplyBoxPage1.addView(doc.Box1R)
    boxsheet.set("A%d"%ir,'%-11.11s'%"R")
    RDist = Vertex278.X - Vertex1.X
    boxsheet.set("B%d"%ir,'%10.6f'%(RDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%RDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1S')
    doc.Box1S.Type = 'DistanceX'
    doc.Box1S.References2D=[(doc.BoxFrontView,"Vertex278"),\
                        (doc.BoxFrontView,"Vertex14")]
    doc.Box1S.FormatSpec='S'
    doc.Box1S.Arbitrary = True
    doc.Box1S.X = 0
    doc.Box1S.Y = -24
    doc.PowerSupplyBoxPage1.addView(doc.Box1S)
    boxsheet.set("A%d"%ir,'%-11.11s'%"S")
    SDist = Vertex14.X - Vertex278.X
    boxsheet.set("B%d"%ir,'%10.6f'%(SDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%SDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1T')
    doc.Box1T.Type = 'DistanceY'
    doc.Box1T.References2D=[(doc.BoxFrontView,"Vertex1"),\
                        (doc.BoxFrontView,"Vertex278")]
    doc.Box1T.FormatSpec='T'
    doc.Box1T.Arbitrary = True
    doc.Box1T.X = 54
    doc.Box1T.Y = 0
    doc.PowerSupplyBoxPage1.addView(doc.Box1T)
    boxsheet.set("A%d"%ir,'%-11.11s'%"T")
    TDist = Vertex278.Z - Vertex1.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(TDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%TDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1U')
    doc.Box1U.Type = 'DistanceX'
    doc.Box1U.References2D=[(doc.BoxFrontView,"Vertex278"),\
                        (doc.BoxFrontView,"Vertex257")]
    doc.Box1U.FormatSpec='U (12x)'
    doc.Box1U.Arbitrary = True
    doc.Box1U.X = -8
    doc.Box1U.Y = -31
    doc.PowerSupplyBoxPage1.addView(doc.Box1U)
    boxsheet.set("A%d"%ir,'%-11.11s'%"U")
    UDist = Vertex257.X - Vertex278.X
    boxsheet.set("B%d"%ir,'%10.6f'%(UDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%UDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box1V')
    doc.Box1V.Type = 'DistanceY'
    doc.Box1V.References2D=[(doc.BoxFrontView,"Vertex278"),\
                        (doc.BoxFrontView,"Vertex272")]
    doc.Box1V.FormatSpec='V (6x)'
    doc.Box1V.Arbitrary = True
    doc.Box1V.X = 3
    doc.Box1V.Y = -8
    doc.PowerSupplyBoxPage1.addView(doc.Box1V)
    boxsheet.set("A%d"%ir,'%-11.11s'%"V")
    VDist = Vertex278.Z - Vertex272.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(VDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%VDist)
    ir += 1

    doc.BoxFrontView.recompute()
    
    boxsheet.recompute()
    doc.addObject('TechDraw::DrawViewSpreadsheet','BoxDimBlock1')
    doc.BoxDimBlock1.Source = boxsheet
    doc.BoxDimBlock1.TextSize = 8
    doc.BoxDimBlock1.CellEnd = "C%d"%(ir-1)
    doc.PowerSupplyBoxPage1.addView(doc.BoxDimBlock1)
    doc.BoxDimBlock1.recompute()
    doc.BoxDimBlock1.X = 200
    doc.BoxDimBlock1.Y = 130
    doc.PowerSupplyBoxPage1.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.PowerSupplyBoxPage1,"BananaPiM64Model_PowerSupplyBoxPage1.pdf")
    
    

    doc.addObject('TechDraw::DrawPage','PowerSupplyBoxPage2')
    doc.PowerSupplyBoxPage2.Template = doc.USLetterTemplate
    edt = doc.PowerSupplyBoxPage1.Template.EditableTexts
    edt['DrawingTitle2']= "Box (Left and Back)"
    edt['Scale'] = '1/2'
    edt['Sheet'] = "Sheet 2 of 3"
    doc.PowerSupplyBoxPage2.Template.EditableTexts = edt
    doc.PowerSupplyBoxPage2.ViewObject.show()
    boxsheet = doc.addObject('Spreadsheet::Sheet','BoxDimensionTable2')
    boxsheet.set("A1",'%-11.11s'%"Dim")
    boxsheet.set("B1",'%10.10s'%"inch")
    boxsheet.set("C1",'%10.10s'%"mm")
    ir = 2


    doc.addObject('TechDraw::DrawViewPart','BoxLeftView')
    doc.PowerSupplyBoxPage2.addView(doc.BoxLeftView)
    doc.BoxLeftView.Source = doc.psbox_ACBox
    doc.BoxLeftView.X = 60
    doc.BoxLeftView.Y = 170
    doc.BoxLeftView.Scale = .5
    doc.BoxLeftView.Direction=(-1.0,0.0,0.0)
    doc.BoxLeftView.Caption = "Left"
    #
    # Edge19 -- for diameter
    #
    # Vertex3 -- lower right (0,0)
    # Vertex27 -- Upper Left (1,1)
    #
    # Vertex17 -- Vadjust hole
    # Vertex20 -- Key hole
    #
    boxshape = doc.psbox_ACBox.Shape
    #print('*** boxshape:',file=sys.__stderr__)
    #i = 0
    #for e in boxshape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        circ = e.Curve
    #        if circ.Location.x == 0:
    #            print('*** boxshape: Edges[%d].Curve %g at (%g,%g)'%\
    #                    (i,circ.Radius*2,circ.Location.y,circ.Location.z),
    #                    file=sys.__stderr__)
    #    i += 1
    #i = 0
    #for v in boxshape.Vertexes:
    #    if v.X == 0:
    #        print('*** boxshape: Vertexes[%d] at (%g,%g)'%\
    #              (i,v.Y,v.Z),file=sys.__stderr__)
    #    i += 1
    #
    Vertex3 = boxshape.Vertexes[0]
    Vertex27 = boxshape.Vertexes[275]
    #
    Edge19 = boxshape.Edges[42]
    #
    Vertex17 = boxshape.Vertexes[32]
    Vertex20 = boxshape.Vertexes[33]
    #
    doc.addObject('TechDraw::DrawViewDimension','Box2A')
    doc.Box2A.Type = 'Diameter'
    doc.Box2A.References2D=[(doc.BoxLeftView,"Edge19")]
    doc.Box2A.FormatSpec='ADia (2x)'
    doc.Box2A.Arbitrary = True
    doc.Box2A.X = 10
    doc.Box2A.Y = 20
    doc.PowerSupplyBoxPage2.addView(doc.Box2A)
    boxsheet.set("A%d"%ir,'%-11.11s'%"ADia")
    ADia = Edge19.Curve.Radius*2
    boxsheet.set("B%d"%ir,'%10.6f'%(ADia/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%ADia)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2B')
    doc.Box2B.Type = 'DistanceX'
    doc.Box2B.References2D=[(doc.BoxLeftView,"Vertex3"),\
                            (doc.BoxLeftView,"Vertex27")]
    doc.Box2B.FormatSpec='B'
    doc.Box2B.Arbitrary = True
    doc.Box2B.X = 0
    doc.Box2B.Y = 28
    doc.PowerSupplyBoxPage2.addView(doc.Box2B)
    boxsheet.set("A%d"%ir,'%-11.11s'%"B")
    BDist = Vertex27.Y - Vertex3.Y
    boxsheet.set("B%d"%ir,'%10.6f'%(BDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%BDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2C')
    doc.Box2C.Type = 'DistanceY'
    doc.Box2C.References2D=[(doc.BoxLeftView,"Vertex3"),\
                            (doc.BoxLeftView,"Vertex27")]
    doc.Box2C.FormatSpec='C'
    doc.Box2C.Arbitrary = True
    doc.Box2C.X = 38
    doc.Box2C.Y = 0
    doc.PowerSupplyBoxPage2.addView(doc.Box2C)
    boxsheet.set("A%d"%ir,'%-11.11s'%"C")
    CDist = Vertex27.Z - Vertex3.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(CDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%CDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2D')
    doc.Box2D.Type = 'DistanceX'
    doc.Box2D.References2D=[(doc.BoxLeftView,"Vertex3"),\
                            (doc.BoxLeftView,"Vertex20")]
    doc.Box2D.FormatSpec='D'
    doc.Box2D.Arbitrary = True
    doc.Box2D.X = 18
    doc.Box2D.Y = 6
    doc.PowerSupplyBoxPage2.addView(doc.Box2D)
    boxsheet.set("A%d"%ir,'%-11.11s'%"B")
    DDist = Vertex20.Y - Vertex3.Y
    boxsheet.set("B%d"%ir,'%10.6f'%(DDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%DDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2E')
    doc.Box2E.Type = 'DistanceX'
    doc.Box2E.References2D=[(doc.BoxLeftView,"Vertex20"),\
                            (doc.BoxLeftView,"Vertex17")]
    doc.Box2E.FormatSpec='E'
    doc.Box2E.Arbitrary = True
    doc.Box2E.X = -5
    doc.Box2E.Y = 6
    doc.PowerSupplyBoxPage2.addView(doc.Box2E)
    boxsheet.set("A%d"%ir,'%-11.11s'%"E")
    EDist = Vertex17.Y - Vertex20.Y
    boxsheet.set("B%d"%ir,'%10.6f'%(EDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%EDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2F')
    doc.Box2F.Type = 'DistanceY'
    doc.Box2F.References2D=[(doc.BoxLeftView,"Vertex3"),\
                            (doc.BoxLeftView,"Vertex20")]
    doc.Box2F.FormatSpec='F'
    doc.Box2F.Arbitrary = True
    doc.Box2F.X = 30
    doc.Box2F.Y = -7
    doc.PowerSupplyBoxPage2.addView(doc.Box2F)
    boxsheet.set("A%d"%ir,'%-11.11s'%"F")
    FDist = Vertex20.Z - Vertex3.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(FDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%FDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2Fa')
    doc.Box2Fa.Type = 'DistanceY'
    doc.Box2Fa.References2D=[(doc.BoxLeftView,"Vertex3"),\
                             (doc.BoxLeftView,"Vertex17")]
    doc.Box2Fa.FormatSpec='Fa'
    doc.Box2Fa.Arbitrary = True
    doc.Box2Fa.X = 48
    doc.Box2Fa.Y = -7
    doc.PowerSupplyBoxPage2.addView(doc.Box2Fa)
    boxsheet.set("A%d"%ir,'%-11.11s'%"Fa")
    FaDist = Vertex17.Z - Vertex3.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(FaDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%FaDist)
    ir += 1
    doc.BoxLeftView.recompute()

    #
    doc.addObject('TechDraw::DrawViewPart','BoxRearView')
    doc.PowerSupplyBoxPage2.addView(doc.BoxRearView)
    doc.BoxRearView.Source = doc.psbox_ACBox
    doc.BoxRearView.X = 60
    doc.BoxRearView.Y = 125
    doc.BoxRearView.Scale = .5
    doc.BoxRearView.Direction=(0.0,1.0,0.0)
    doc.BoxRearView.Caption = "Rear"
    ##Vertex1 -- origin
    ##Vertex21 -- size
    ##Vertex8 -- inlet.origin
    ##Vertex10 -- inlet size
    boxshape = doc.psbox_ACBox.Shape
    #print('*** boxshape:',file=sys.__stderr__)
    #i = 0
    #for v in boxshape.Vertexes:
    #    if v.Y == 101.6:
    #        print('*** boxshape: Vertexes[%d] at (%g,%g)'%\
    #              (i,v.X,v.Z),file=sys.__stderr__)
    #    i += 1
    Vertex1 = boxshape.Vertexes[0]
    Vertex21 = boxshape.Vertexes[305]
    Vertex8 = boxshape.Vertexes[271]
    Vertex10 = boxshape.Vertexes[273]
    doc.addObject('TechDraw::DrawViewDimension','Box2G')
    doc.Box2G.Type = 'DistanceX'
    doc.Box2G.References2D=[(doc.BoxRearView,"Vertex1"),\
                            (doc.BoxRearView,"Vertex21")]
    doc.Box2G.FormatSpec="G"
    doc.Box2G.Arbitrary = True
    doc.Box2G.X = 0
    doc.Box2G.Y = -4
    doc.PowerSupplyBoxPage2.addView(doc.Box2G)
    boxsheet.set("A%d"%ir,'%-11.11s'%"G")
    GDist = Vertex21.Y - Vertex1.Y
    boxsheet.set("B%d"%ir,'%10.6f'%(GDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%GDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2H')
    doc.Box2H.Type = 'DistanceY'
    doc.Box2H.References2D=[(doc.BoxRearView,"Vertex1"),\
                            (doc.BoxRearView,"Vertex21")]
    doc.Box2H.FormatSpec="H"
    doc.Box2H.Arbitrary = True
    doc.Box2H.X = 35
    doc.Box2H.Y = 0
    doc.PowerSupplyBoxPage2.addView(doc.Box2H)
    boxsheet.set("A%d"%ir,'%-11.11s'%"H")
    HDist = Vertex21.Z - Vertex1.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(HDist))
    boxsheet.set("C%d"%ir,'%10.6f'%HDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2I')
    doc.Box2I.Type = 'DistanceX'
    doc.Box2I.References2D=[(doc.BoxRearView,"Vertex1"),\
                             (doc.BoxRearView,"Vertex8")]
    doc.Box2I.FormatSpec="I"
    doc.Box2I.Arbitrary = True
    doc.Box2I.X = 18
    doc.Box2I.Y = 0
    doc.PowerSupplyBoxPage2.addView(doc.Box2I)
    boxsheet.set("A%d"%ir,'%-11.11s'%"I")
    IDist = Vertex8.X - Vertex1.X
    boxsheet.set("B%d"%ir,'%10.6f'%(IDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%IDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2J')
    doc.Box2J.Type = 'DistanceY'
    doc.Box2J.References2D=[(doc.BoxRearView,"Vertex1"),\
                            (doc.BoxRearView,"Vertex8")]
    doc.Box2J.FormatSpec="J"
    doc.Box2J.Arbitrary = True
    doc.Box2J.X = -12
    doc.Box2J.Y = -4
    doc.PowerSupplyBoxPage2.addView(doc.Box2J)
    boxsheet.set("A%d"%ir,'%-11.11s'%"J")
    JDist = Vertex8.Z - Vertex1.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(JDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%JDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2K')
    doc.Box2K.Type = 'DistanceX'
    doc.Box2K.References2D=[(doc.BoxRearView,"Vertex8"),\
                             (doc.BoxRearView,"Vertex10")]
    doc.Box2K.FormatSpec="K"
    doc.Box2K.Arbitrary = True
    doc.Box2K.X = -3
    doc.Box2K.Y = 8
    doc.PowerSupplyBoxPage2.addView(doc.Box2K)
    boxsheet.set("A%d"%ir,'%-11.11s'%"K")
    KDist = Vertex10.X - Vertex8.X
    boxsheet.set("B%d"%ir,'%10.6f'%(KDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%KDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Box2L')
    doc.Box2L.Type = 'DistanceY'
    doc.Box2L.References2D=[(doc.BoxRearView,"Vertex10"),\
                            (doc.BoxRearView,"Vertex8")]
    doc.Box2L.FormatSpec="L"
    doc.Box2L.Arbitrary = True
    doc.Box2L.X = 6
    doc.Box2L.Y = 4
    doc.PowerSupplyBoxPage2.addView(doc.Box2L)
    boxsheet.set("A%d"%ir,'%-11.11s'%"L")
    LDist = Vertex10.Z - Vertex8.Z
    boxsheet.set("B%d"%ir,'%10.6f'%(LDist/25.4))
    boxsheet.set("C%d"%ir,'%10.6f'%LDist)
    ir += 1
        

    doc.BoxRearView.recompute()
    



    
    doc.addObject('TechDraw::DrawViewPart','BoxISOView')
    doc.PowerSupplyBoxPage2.addView(doc.BoxISOView)
    doc.BoxISOView.Source = doc.psbox_ACBox
    doc.BoxISOView.Scale = .375
    doc.BoxISOView.X = 56
    doc.BoxISOView.Y = 60
    doc.BoxISOView.Direction=(1.0,-1.0,1.0)
    doc.BoxISOView.Caption = "ISOMetric"
    
    doc.BoxISOView.recompute()    
    
    
    boxsheet.recompute()
    doc.addObject('TechDraw::DrawViewSpreadsheet','BoxDimBlock2')
    doc.BoxDimBlock2.Source = boxsheet
    doc.BoxDimBlock2.TextSize = 8
    doc.BoxDimBlock2.CellEnd = "C%d"%(ir-1)
    doc.PowerSupplyBoxPage2.addView(doc.BoxDimBlock2)
    doc.BoxDimBlock2.recompute()
    doc.BoxDimBlock2.X = 200
    doc.BoxDimBlock2.Y = 160
    doc.PowerSupplyBoxPage2.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.PowerSupplyBoxPage2,"BananaPiM64Model_PowerSupplyBoxPage2.pdf")
    
    
    doc.addObject('TechDraw::DrawPage','PowerSupplyBoxCoverPage')
    doc.PowerSupplyBoxCoverPage.Template = doc.USLetterTemplate
    edt = doc.PowerSupplyBoxCoverPage.Template.EditableTexts
    edt['DrawingTitle2']= "Cover"
    edt['Sheet'] = "Sheet 3 of 3"
    doc.PowerSupplyBoxCoverPage.Template.EditableTexts = edt
    doc.PowerSupplyBoxCoverPage.ViewObject.show()
    coversheet = doc.addObject('Spreadsheet::Sheet','CoverDimensionTable')
    coversheet.set("A1",'%-11.11s'%"Dim")
    coversheet.set("B1",'%10.10s'%"inch")
    coversheet.set("C1",'%10.10s'%"mm")
    ir = 2
        
    doc.addObject('TechDraw::DrawViewPart','CoverTopView')
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverTopView)
    doc.CoverTopView.Source = doc.psbox_BPABottom
    doc.CoverTopView.X = 90
    doc.CoverTopView.Y = 140
    doc.CoverTopView.Direction=(0.0,0.0,1.0)
    doc.CoverTopView.Caption = "Top"
    doc.CoverTopView.Scale = 1
    covershape = doc.psbox_BPABottom.Shape
    #print('*** covershape:',file=sys.__stderr__)
    holes = list()
    i = 0
    for e in covershape.Edges:
        if isinstance(e.Curve,Part.Circle):
            circ = e.Curve
            if circ.Location.z == psbox._C()+psbox.origin.z:
                #print('*** covershape: Edges[%d].Curve %g at (%g,%g)'%\
                #        (i,circ.Radius*2,circ.Location.x,circ.Location.y),
                #        file=sys.__stderr__)
                holes.append(tuple([i,circ.Radius,circ.Location.x,circ.Location.y]))
        i += 1
    i = 0
    holeverts = dict()
    minV = None
    maxV = None
    for v in covershape.Vertexes:
        if v.Z == psbox._C()+psbox.origin.z:
            #print('*** covershape: Vertexes[%d] at (%g,%g)'%\
            #      (i,v.X,v.Y),file=sys.__stderr__)
            for h in holes:
                ie,rad,ex,ey = h
                #print('*** covershape: ey = %g, v.Y = %g, ex = %g, rad = %g, v.X = %g'%\
                #    (ey,v.Y,ex,rad,v.X),\
                #     file=sys.__stderr__)
                if closeto(ey,v.Y) and closeto(ex,v.X,fuzz=rad+.1):
                    holeverts[h] = tuple([i,v.X,v.Y])
                    break
            if minV == None:
                minV = v
            elif v.X < minV.X and v.Y < minV.Y:
                minV = v
            if maxV == None:
                maxV = v
            elif v.X > maxV.X and v.Y > maxV.Y:
                maxV = v
        i += 1
    FanMH_LeftTopLeft = None
    FanMH_LeftTopRight = None
    FanMH_LeftBottomLeft = None
    FanMH_RightTopLeft = None
    fanhm_rad = Fan02510SS_05P_AT00_TopMount._fanmholedia/2
    GrillHole_LeftTop = None
    GrillHole_RightTop = None
    GrillHole_LeftD1L1 = None
    grillhole_rad = Fan02510SS_05P_AT00_TopMount._grilholesize/2
    for holeedge in holeverts:
        ie,rad,ex,ey = holeedge
        iv,X,Y = holeverts[holeedge]
        if closeto(rad,fanhm_rad):
            #print('*** covershape (loop1): holeedge[%s] = %s'%(holeedge, holeverts[holeedge]), \
            #        file=sys.__stderr__)
            #print('*** covershape (loop1):: rad = %g, fanhm_rad = %g'%\
            #        (rad,fanhm_rad),\
            #        file=sys.__stderr__)
            if FanMH_LeftTopLeft == None:
                FanMH_LeftTopLeft = covershape.Vertexes[iv]
            elif X <= FanMH_LeftTopLeft.X and Y >= FanMH_LeftTopLeft.Y:
                FanMH_LeftTopLeft = covershape.Vertexes[iv]
            #print('*** covershape (loop): FanMH_LeftTopLeft = (%g,%g)'%\
            #            (FanMH_LeftTopLeft.X,FanMH_LeftTopLeft.Y),\
            #            file=sys.__stderr__)
            if FanMH_LeftBottomLeft == None:
                FanMH_LeftBottomLeft = covershape.Vertexes[iv]
            elif X <= FanMH_LeftBottomLeft.X and Y <= FanMH_LeftBottomLeft.Y:
                FanMH_LeftBottomLeft = covershape.Vertexes[iv]
        if closeto(rad,grillhole_rad):
            #print('*** covershape: holeedge[%s] = %s'%(holeedge, holeverts[holeedge]), \
            #        file=sys.__stderr__)
            #print('*** covershape: rad = %g, grillhole_rad = %g'%\
            #        (rad,grillhole_rad),\
            #        file=sys.__stderr__)
            if GrillHole_LeftTop == None:
                GrillHole_LeftTop = covershape.Vertexes[iv]
            elif X <= GrillHole_LeftTop.X and Y >= GrillHole_LeftTop.Y:
                GrillHole_LeftTop = covershape.Vertexes[iv]
            if GrillHole_RightTop == None:
                GrillHole_RightTop = covershape.Vertexes[iv]
            elif X >= GrillHole_RightTop.X and Y >= GrillHole_RightTop.Y:
                GrillHole_RightTop = covershape.Vertexes[iv]
    FanMH_LeftTopRight = FanMH_LeftTopLeft
    for holeedge in holeverts:
        ie,rad,ex,ey = holeedge
        iv,X,Y = holeverts[holeedge]
        if closeto(rad,fanhm_rad):
            #print('*** covershape (loop2): holeedge[%s] = %s'%(holeedge, holeverts[holeedge]), \
            #        file=sys.__stderr__)
            #print('*** covershape (loop2):: rad = %g, fanhm_rad = %g'%\
            #        (rad,fanhm_rad),\
            #        file=sys.__stderr__)
            if closeto(X,FanMH_LeftTopLeft.X + Fan02510SS_05P_AT00_TopMount._fanmholespacing) and \
               closeto(Y,FanMH_LeftTopLeft.Y):
                FanMH_LeftTopRight = covershape.Vertexes[iv]
            if FanMH_RightTopLeft == None:
                FanMH_RightTopLeft = covershape.Vertexes[iv]
            elif X <= FanMH_RightTopLeft.X and \
                 X > FanMH_LeftTopRight.X and \
                 closeto(Y,FanMH_LeftTopLeft.Y):
                FanMH_RightTopLeft = covershape.Vertexes[iv]
        if closeto(rad,grillhole_rad):
            #print('*** covershape: holeedge[%s] = %s'%(holeedge, holeverts[holeedge]), \
            #        file=sys.__stderr__)
            #print('*** covershape: rad = %g, grillhole_rad = %g'%\
            #        (rad,grillhole_rad),\
            #        file=sys.__stderr__)
            if GrillHole_LeftTop == None:
                GrillHole_LeftTop = covershape.Vertexes[iv]
            elif X <= GrillHole_LeftTop.X and Y >= GrillHole_LeftTop.Y:
                GrillHole_LeftTop = covershape.Vertexes[iv]
            if GrillHole_RightTop == None:
                GrillHole_RightTop = covershape.Vertexes[iv]
            elif X >= GrillHole_RightTop.X and Y >= GrillHole_RightTop.Y:
                GrillHole_RightTop = covershape.Vertexes[iv]
    f1center = (FanMH_LeftTopLeft.X+FanMH_LeftTopRight.X) / 2
    f1r2 = GrillHole_LeftTop.Y - Fan02510SS_05P_AT00_TopMount._hspace()
    f1c2 = GrillHole_LeftTop.X - Fan02510SS_05P_AT00_TopMount._hspace()
    for holeedge in holeverts:
        ie,rad,ex,ey = holeedge
        iv,X,Y = holeverts[holeedge]
        if closeto(rad,grillhole_rad):
            #print('*** covershape (loop3): holeedge[%s] = %s'%(holeedge, holeverts[holeedge]), \
            #        file=sys.__stderr__)
            #print('*** covershape (loop3): rad = %g, grillhole_rad = %g'%\
            #        (rad,grillhole_rad),\
            #        file=sys.__stderr__)
            if closeto(X,f1c2) and closeto(Y,f1r2):
                GrillHole_LeftD1L1 = covershape.Vertexes[iv]
                break
    #print('*** covershape: minV = (%g,%g)'%(minV.X,minV.Y),\
    #            file=sys.__stderr__)
    #print('*** covershape: maxV = (%g,%g)'%(maxV.X,maxV.Y),\
    #            file=sys.__stderr__)        
    #print('*** covershape: FanMH_LeftTopLeft = (%g,%g)'%\
    #        (FanMH_LeftTopLeft.X,FanMH_LeftTopLeft.Y),\
    #        file=sys.__stderr__)
    #print('*** covershape: FanMH_LeftTopRight = (%g,%g)'%\
    #        (FanMH_LeftTopRight.X,FanMH_LeftTopRight.Y),\
    #        file=sys.__stderr__)
    #print('*** covershape: FanMH_LeftBottomLeft = (%g,%g)'%\
    #        (FanMH_LeftBottomLeft.X,FanMH_LeftBottomLeft.Y),\
    #        file=sys.__stderr__)
    #print('*** covershape: FanMH_RightTopLeft = (%g,%g)'%\
    #        (FanMH_RightTopLeft.X,FanMH_RightTopLeft.Y),\
    #        file=sys.__stderr__)
    #print('*** covershape: GrillHole_LeftTop = (%g,%g)'%\
    #        (GrillHole_LeftTop.X,GrillHole_LeftTop.Y),\
    #        file=sys.__stderr__)
    #print('*** covershape: GrillHole_RightTop = (%g,%g)'%\
    #        (GrillHole_RightTop.X,GrillHole_RightTop.Y),\
    #        file=sys.__stderr__)
    #print('*** covershape: GrillHole_LeftD1L1 = (%g,%g)'%\
    #        (GrillHole_LeftD1L1.X,GrillHole_LeftD1L1.Y),\
    #        file=sys.__stderr__)
    # Edge62 -- Fan Mounting Hole (for diameter)
    # Edge58 -- Fan grill hole (for diameter)
    # Vertex0 -- origin
    Vertex0 = minV
    # Vertex3 -- max corner
    Vertex3 = maxV
    # Vertex180 -- Left Fan, top left mh
    Vertex180 = FanMH_LeftTopLeft
    # Vertex111 - Left Fan, top right mh
    Vertex111 = FanMH_LeftTopRight
    # Vertex177 - Left Fan, bottom left mh
    Vertex177 = FanMH_LeftBottomLeft
    # Vertex114 - Right fan, top left mh
    Vertex114 = FanMH_RightTopLeft
    # Vertex126 Left Fan top grill hole
    Vertex126 = GrillHole_LeftTop
    # Vertext36 Right Fan top grill hole
    Vertext36 = GrillHole_RightTop
    # Vertex132 Left Fan down one gril hole row, left one grill hole
    Vertex132 = GrillHole_LeftD1L1
    #
    doc.addObject('TechDraw::DrawViewDimension','CoverADia')
    doc.CoverADia.Type = 'Diameter'
    doc.CoverADia.References2D=[(doc.CoverTopView,'Edge62')]
    doc.CoverADia.FormatSpec='ADia (8x)'
    doc.CoverADia.Arbitrary = True
    doc.CoverADia.X = -7
    doc.CoverADia.Y = 40
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverADia)
    coversheet.set("A%d"%ir,'%-11.11s'%"ADia")
    coversheet.set("B%d"%ir,'%10.6f'%(Fan02510SS_05P_AT00_TopMount._fanmholedia/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%Fan02510SS_05P_AT00_TopMount._fanmholedia)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverBDia')
    doc.CoverBDia.Type = 'Diameter'
    doc.CoverBDia.References2D=[(doc.CoverTopView,'Edge58')]
    doc.CoverBDia.FormatSpec='BDia (50x)'
    doc.CoverBDia.Arbitrary = True
    doc.CoverBDia.X = -7
    doc.CoverBDia.Y = -35
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverBDia)
    coversheet.set("A%d"%ir,'%-11.11s'%"BDia")
    coversheet.set("B%d"%ir,'%10.6f'%(Fan02510SS_05P_AT00_TopMount._grilholesize/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%Fan02510SS_05P_AT00_TopMount._grilholesize)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverC')
    doc.CoverC.Type = 'DistanceX'
    doc.CoverC.References2D=[(doc.CoverTopView,'Vertex0'),\
                             (doc.CoverTopView,'Vertex3')]
    doc.CoverC.FormatSpec='C'
    doc.CoverC.Arbitrary = True
    doc.CoverC.X = 0
    doc.CoverC.Y = 60
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverC)
    CDist = Vertex3.X - Vertex0.X
    coversheet.set("A%d"%ir,'%-11.11s'%"C")
    coversheet.set("B%d"%ir,'%10.6f'%(CDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%CDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverD')
    doc.CoverD.Type = 'DistanceY'
    doc.CoverD.References2D=[(doc.CoverTopView,'Vertex0'),\
                             (doc.CoverTopView,'Vertex3')]
    doc.CoverD.FormatSpec='D'
    doc.CoverD.Arbitrary = True
    doc.CoverD.X = 67
    doc.CoverD.Y = 0
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverD)
    DDist =  Vertex3.Y - Vertex0.Y
    coversheet.set("A%d"%ir,'%-11.11s'%"D")
    coversheet.set("B%d"%ir,'%10.6f'%(DDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%DDist)
    ir += 1
    ## Fan Mounting Holes
    doc.addObject('TechDraw::DrawViewDimension','CoverE')
    doc.CoverE.Type = 'DistanceX'
    doc.CoverE.References2D=[(doc.CoverTopView,'Vertex0'),\
                             (doc.CoverTopView,'Vertex180')]
    doc.CoverE.FormatSpec='E'
    doc.CoverE.Arbitrary = True
    doc.CoverE.X = -45
    doc.CoverE.Y = -53
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverE)
    coversheet.set("A%d"%ir,'%-11.11s'%"E")
    EDist = Vertex180.X - Vertex0.X
    coversheet.set("B%d"%ir,'%10.6f'%(EDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%EDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverF')
    doc.CoverF.Type = 'DistanceY'
    doc.CoverF.References2D=[(doc.CoverTopView,'Vertex0'),\
                             (doc.CoverTopView,'Vertex180')]
    doc.CoverF.FormatSpec='F'
    doc.CoverF.Arbitrary = True
    doc.CoverF.X = -54
    doc.CoverF.Y = -15
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverF)
    coversheet.set("A%d"%ir,'%-11.11s'%"F")
    FDist = Vertex180.Y - Vertex0.Y
    coversheet.set("B%d"%ir,'%10.6f'%(FDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%FDist)
    ir += 1
    
    doc.addObject('TechDraw::DrawViewDimension','CoverG')
    doc.CoverG.Type = 'DistanceX'
    doc.CoverG.References2D=[(doc.CoverTopView,'Vertex180'),\
                             (doc.CoverTopView,'Vertex114')]
    doc.CoverG.FormatSpec='G'
    doc.CoverG.Arbitrary = True
    doc.CoverG.X = -10
    doc.CoverG.Y = -18
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverG)
    coversheet.set("A%d"%ir,'%-11.11s'%"G")
    GDist = Vertex114.X - Vertex180.X
    coversheet.set("B%d"%ir,'%10.6f'%(GDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%GDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverH')
    doc.CoverH.Type = 'DistanceX'
    doc.CoverH.References2D=[(doc.CoverTopView,'Vertex180'),\
                             (doc.CoverTopView,'Vertex111')]
    doc.CoverH.FormatSpec='H'
    doc.CoverH.Arbitrary = True
    doc.CoverH.X = 10
    doc.CoverH.Y = 23
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverH)
    coversheet.set("A%d"%ir,'%-11.11s'%"H")
    HDist = Vertex111.X - Vertex180.X
    coversheet.set("B%d"%ir,'%10.6f'%(HDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%HDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverI')
    doc.CoverI.Type = 'DistanceY'
    doc.CoverI.References2D=[(doc.CoverTopView,'Vertex180'),\
                             (doc.CoverTopView,'Vertex177')]
    doc.CoverI.FormatSpec='I'
    doc.CoverI.Arbitrary = True
    doc.CoverI.X = 50
    doc.CoverI.Y = 0
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverI)
    coversheet.set("A%d"%ir,'%-11.11s'%"I")
    IDist = Vertex180.Y - Vertex177.Y
    coversheet.set("B%d"%ir,'%10.6f'%(IDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%IDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverJ')
    doc.CoverJ.Type = 'DistanceX'
    doc.CoverJ.References2D=[(doc.CoverTopView,'Vertex0'),\
                             (doc.CoverTopView,'Vertex126')]
    doc.CoverJ.FormatSpec='J'
    doc.CoverJ.Arbitrary = True
    doc.CoverJ.X = -45
    doc.CoverJ.Y =  30
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverJ)
    coversheet.set("A%d"%ir,'%-11.11s'%"J")
    JDist = Vertex126.X - Vertex0.X
    coversheet.set("B%d"%ir,'%10.6f'%(JDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%JDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverK')
    doc.CoverK.Type = 'DistanceY'
    doc.CoverK.References2D=[(doc.CoverTopView,'Vertex0'),\
                             (doc.CoverTopView,'Vertex126')]
    doc.CoverK.FormatSpec='K'
    doc.CoverK.Arbitrary = True
    doc.CoverK.X =  54
    doc.CoverK.Y = -27
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverK)
    coversheet.set("A%d"%ir,'%-11.11s'%"K")
    KDist = Vertex126.Y - Vertex0.Y
    coversheet.set("B%d"%ir,'%10.6f'%(KDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%KDist)
    ir += 1

    doc.addObject('TechDraw::DrawViewDimension','CoverL')
    doc.CoverL.Type = 'DistanceX'
    doc.CoverL.References2D=[(doc.CoverTopView,'Vertex126'),\
                             (doc.CoverTopView,'Vertex132')]
    doc.CoverL.FormatSpec='L'
    doc.CoverL.Arbitrary = True
    doc.CoverL.X = -29
    doc.CoverL.Y =  20
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverL)
    coversheet.set("A%d"%ir,'%-11.11s'%"L")
    LDist = Vertex126.X - Vertex132.X
    coversheet.set("B%d"%ir,'%10.6f'%(LDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%LDist)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','CoverM')
    doc.CoverM.Type = 'DistanceY'
    doc.CoverM.References2D=[(doc.CoverTopView,'Vertex126'),\
                             (doc.CoverTopView,'Vertex132')]
    doc.CoverM.FormatSpec='M'
    doc.CoverM.Arbitrary = True
    doc.CoverM.X = -46
    doc.CoverM.Y =   9
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverM)
    coversheet.set("A%d"%ir,'%-11.11s'%"M")
    MDist = Vertex126.Y - Vertex132.Y
    coversheet.set("B%d"%ir,'%10.6f'%(MDist/25.4))
    coversheet.set("C%d"%ir,'%10.6f'%MDist)
    ir += 1
    #
    doc.CoverTopView.recompute()
    #
    #
    doc.addObject('TechDraw::DrawViewSpreadsheet','CoverDimBlock')
    doc.CoverDimBlock.Source = coversheet
    doc.CoverDimBlock.TextSize = 8
    doc.CoverDimBlock.CellEnd = "C%d"%(ir-1)
    doc.PowerSupplyBoxCoverPage.addView(doc.CoverDimBlock)
    doc.CoverDimBlock.recompute()
    doc.CoverDimBlock.X = 210
    doc.CoverDimBlock.Y = 140
    #
    #
    doc.PowerSupplyBoxCoverPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.PowerSupplyBoxCoverPage,"BananaPiM64Model_PowerSupplyBoxCoverPage.pdf")
    sys.exit(1)    
