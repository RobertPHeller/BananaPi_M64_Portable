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
#  Last Modified : <200610.1310>
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

from PSPCB import *
from Electromech import *

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

class PSBox(CU_3002A):
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
        CU_3002A.__init__(self,name,origin)
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
        f2y = oy+self._fan2Yoff()
        f2origin = Base.Vector(fx,f2y,fz)
        self.fan2 = Fan02510SS_05P_AT00(self.name+"_fan2",f2origin)
        c = self.cover
        for i in [1,2,3,4]:
            c = c.cut(self.fan1.MountingHole(i,fx,-self.thickness()))
            c = c.cut(self.fan2.MountingHole(i,fx,-self.thickness()))
        c = c.cut(self.fan1.RoundFanHole(fx,-self.thickness()))
        c = c.cut(self.fan2.RoundFanHole(fx,-self.thickness()))
        c = self.fan1.DrillGrillHoles(ox+self.thickness(),-self.thickness(),2.5,3.5,c)
        c = self.fan2.DrillGrillHoles(ox+self.thickness(),-self.thickness(),2.5,3.5,c)
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
        CU_3002A.show(self)
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
    


if __name__ == '__main__':
    doc = App.newDocument("PowerSupplyBox")
    App.setActiveDocument ( "PowerSupplyBox" )
    o = Base.Vector(0,0,0)
    psbox = PSBox("psbox",o)
    psbox.show()
    Gui.SendMsgToActiveView("ViewFit")
    
