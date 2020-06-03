#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Jun 2 09:21:27 2020
#  Last Modified : <200603.1156>
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

from M64 import *
from PSBox import *
from Electromech import *
from DCDC_5_12 import *
from LCDScreen import *
from LCDMountingBracket import * 
from HDMIConverter import * 
#package require TeensyThumbStick
#package require Speaker
#package require Battery
#package require USBHub
#package require OTGAdaptor
#package require USB_SATA_Adapter
#package require harddisk
#package require PianoHinge
#package require SVGOutput

import csv

class CutList(object):
    _cutList = dict()
    @classmethod
    def AddCut(cls,width,height,length):
        key = (width,height,length)
        if key in cls._cutList:
            cls._cutList[key] += 1
        else:
            cls._cutList[key] = 1
    @staticmethod
    def _normPartSizeMM(t):
        return ("%.3fx%.3fx%.3f" % t)
    @staticmethod
    def _inch(mm):
        return mm / 25.4
    @staticmethod
    def _normPartSizeIN(t):
        X, Y, Z = t
        return ("%.4fx%.4fx%.4f" % (CutList._inch(X), CutList._inch(Y), CutList._inch(Z)))
    _units = 'in'
    @classmethod
    def SetUnits(cls,units):
        if units == 'in' or units == 'mm':
            cls._units = units
        else:
            raise RuntimeError("Unsupport units!")
    @classmethod
    def GetUnits(cls):
        return cls._units
    @classmethod
    def _normPartSize(cls,t):
        if cls._units == 'in':
            return CutList._normPartSizeIN(t)
        elif cls._units == 'mm':
            return CutList._normPartSizeMM(t)
        else:
            raise RuntimeError("Unsupport units!")
    @classmethod
    def ListCuts(cls,filename):
        keys = cls._cutList.keys()
        keys.sort()
        f = open(filename,"w")
        w = csv.writer(f)
        w.writerow([("Size (%s)" % cls._units),"Count"])
        for key in keys:
            w.writerow([cls._normPartSize(key),cls._cutList[key]])
        f.close()
    def __init__(self):
        raise RuntimeError("No Instances allowed for CutList!")

class PortableM64CaseCommon(object):
    _Width = 15.5 * 25.4
    def Width(self):
        return PortableM64CaseCommon._Width
    _Height = 11 * 25.4
    def Height(self):
        return PortableM64CaseCommon._Height
    _BottomDepth = 1.75 * 25.4
    def BottomDepth(self):
        return PortableM64CaseCommon._BottomDepth
    _MiddleTotalDepth = 1.5 * 25.4
    def MiddleTotalDepth(self):
        return PortableM64CaseCommon._MiddleTotalDepth
    _MiddleLowerDepth = .5 * 25.4
    def MiddleLowerDepth(self):
        return PortableM64CaseCommon._MiddleLowerDepth
    _TopDepth = (.5+.125) * 25.4
    def TopDepth(self):
        return PortableM64CaseCommon._TopDepth
    _WallThickness = .125 * 25.4
    def WallThickness(self):
        return PortableM64CaseCommon._WallThickness
    _ShelfHeight = ((1.75-.125) * 25.4)-23
    def ShelfHeight(self):
        return PortableM64CaseCommon._ShelfHeight
    _ShelfBlockThick = 23
    def ShelfBlockThick(self):
        return PortableM64CaseCommon._ShelfBlockThick
    _ShelfLength = 6 * 25.4
    def ShelfLength(self):
        return PortableM64CaseCommon._ShelfLength
    _BlockThick = .375*25.4
    def BlockThick(self):
        return PortableM64CaseCommon._BlockThick
    _BlockWidth = .5*25.4
    def BlockWidth(self):
        return PortableM64CaseCommon._BlockWidth
    _TeensyThumbStickDrop = .25*25.4
    def TeensyThumbStickDrop(self):
        return PortableM64CaseCommon._TeensyThumbStickDrop
    def __init__(self):
        raise RuntimeError("No Instances allowed for PortableM64CaseCommon!")


class BlockX(PortableM64CaseCommon):
    def __init__(self,name,origin,length=0,
                 thickness=PortableM64CaseCommon._BlockThick,
                 width=PortableM64CaseCommon._BlockWidth):
        self.name = name
        if length==0:
            raise RuntimeError("Lenth cannot be zero!")
        self.length = length
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.thickness = thickness
        self.width = width
        offset = origin.add(Base.Vector(0,width,0))
        XNorm=Base.Vector(1,0,0)
        lvect=Base.Vector(length,0,0)
        self.block = Part.makePlane(thickness,width,offset,XNorm).extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        Part.show(self.block)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def cutfrom(self,other):
        self.block = self.block.cut(other)
    def fuseto(self,other):
        self.block = self.block.fuse(other)
        


class BlockY(PortableM64CaseCommon):
    def __init__(self,name,origin,length=0,
                 thickness=PortableM64CaseCommon._BlockThick,
                 width=PortableM64CaseCommon._BlockWidth):
        self.name = name
        if length==0:
            raise RuntimeError("Lenth cannot be zero!")
        self.length = length
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.thickness = thickness
        self.width = width
        YNorm=Base.Vector(0,1,0)
        lvect=Base.Vector(0,length,0)
        self.block = Part.makePlane(thickness,width,origin,YNorm).extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        Part.show(self.block)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def cutfrom(self,other):
        self.block = self.block.cut(other)
    def fuseto(self,other):
        self.block = self.block.fuse(other)

class BlockZa(PortableM64CaseCommon):
    def __init__(self,name,origin,length=0,
                 thickness=PortableM64CaseCommon._BlockThick,
                 width=PortableM64CaseCommon._BlockWidth):
        self.name = name
        if length==0:
            raise RuntimeError("Lenth cannot be zero!")
        self.length = length
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.thickness = thickness
        self.width = width
        ZNorm=Base.Vector(0,0,1)
        lvect=Base.Vector(0,0,length)
        self.block = Part.makePlane(thickness,width,origin,ZNorm).extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        Part.show(self.block)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def cutfrom(self,other):
        self.block = self.block.cut(other)
    def fuseto(self,other):
        self.block = self.block.fuse(other)
        
class BlockZb(PortableM64CaseCommon):
    def __init__(self,name,origin,length=0,
                 thickness=PortableM64CaseCommon._BlockThick,
                 width=PortableM64CaseCommon._BlockWidth):
        self.name = name
        if length==0:
            raise RuntimeError("Lenth cannot be zero!")
        self.length = length
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.thickness = thickness
        self.width = width
        ZNorm=Base.Vector(0,0,1)
        lvect=Base.Vector(0,0,length)
        self.block = Part.makePlane(width,thickness,origin,ZNorm).extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        Part.show(self.block)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def cutfrom(self,other):
        self.block = self.block.cut(other)
    def fuseto(self,other):
        self.block = self.block.fuse(other)


class PortableM64CasePanel(PortableM64CaseCommon):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        offset = origin.add(Base.Vector(self.WallThickness(),
                                        self.WallThickness(),
                                        0))
        self.corner = offset
        pwidth = self.Width() - (self.WallThickness()*2.0)
        self.pwidth = pwidth
        pheight = self.Height() - (self.WallThickness()*2.0)
        self.pheight = pheight
        thickvect = Base.Vector(0,0,self.WallThickness())
        self.thickness = thickvect
        self.panel = Part.makePlane(pwidth,pheight,offset).extrude(thickvect)
        CutList.AddCut(pwidth,pheight,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        Part.show(self.panel)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
    def PanelCornerPoint(self):
        return self.corner
    def PanelThickness(self):
        return self.thickness.z
    def PanelDirection(self):
        return Base.Vector(0,0,1)
    def cutfrom(self,other):
        self.panel = self.panel.cut(other)
    def fuseto(self,other):
        self.panel = self.panel.fuse(other)

class PortableM64CaseLeftPanel(PortableM64CaseCommon):
    def __init__(self,name,origin,depth):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        if depth <= 0:
            raise RuntimeError("depth must be a positive and non-zero!")
        self.depth = depth
        pheight = self.Height() - (self.WallThickness()*2)
        self.pheight = pheight
        self.depth = depth
        corner = origin.add(Base.Vector(0,
                                        pheight+self.WallThickness(),
                                        0))
        self.corner = corner
        thickvect = Base.Vector(self.WallThickness(),0,0)
        self.thickness = thickvect
        XNorm=Base.Vector(1,0,0)
        self.panel =  Part.makePlane(depth,pheight,corner,XNorm
                                    ).extrude(thickvect)
        CutList.AddCut(depth,pheight,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        Part.show(self.panel)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def PanelCornerPoint(self):
        return self.corner
    def PanelThickness(self):
        return self.thickness.x
    def PanelDirection(self):
        return Base.Vector(1,0,0)
    def cutfrom(self,other):
        self.panel = self.panel.cut(other)
    def fuseto(self,other):
        self.panel = self.panel.fuse(other)

class PortableM64CaseRightPanel(PortableM64CaseCommon):
    def __init__(self,name,origin,depth):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        if depth <= 0:
            raise RuntimeError("depth must be a positive and non-zero!")
        self.depth = depth
        pheight = self.Height() - (self.WallThickness()*2)
        self.pheight = pheight
        corner = origin.add(Base.Vector(self.Width()-self.WallThickness(),
                                        pheight+self.WallThickness(),
                                        0))
        self.corner = corner
        thickvect = Base.Vector(self.WallThickness(),0,0)
        self.thickness = thickvect
        XNorm=Base.Vector(1,0,0)
        self.panel =  Part.makePlane(depth,pheight,corner,XNorm
                                    ).extrude(thickvect)
        CutList.AddCut(depth,pheight,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        Part.show(self.panel)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def PanelCornerPoint(self):
        return self.corner
    def PanelThickness(self):
        return self.thickness.x
    def PanelDirection(self):
        return Base.Vector(1,0,0)
    def cutfrom(self,other):
        self.panel = self.panel.cut(other)
    def fuseto(self,other):
        self.panel = self.panel.fuse(other)

class PortableM64CaseFrontPanel(PortableM64CaseCommon):
    def __init__(self,name,origin,depth):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        if depth <= 0:
            raise RuntimeError("depth must be a positive and non-zero!")
        self.depth = depth
        pwidth = self.Width()
        self.pwidth = pwidth
        self.corner = origin
        thickvect = Base.Vector(0,self.WallThickness(),0)
        self.thickness = thickvect
        YNorm=Base.Vector(0,1,0)
        self.panel =  Part.makePlane(depth,pwidth,origin,YNorm
                                    ).extrude(thickvect)
        CutList.AddCut(depth,pwidth,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        Part.show(self.panel)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def PanelCornerPoint(self):
        return self.corner
    def PanelThickness(self):
        return self.thickness.y
    def PanelDirection(self):
        return Base.Vector(0,1,0)
    def cutfrom(self,other):
        self.panel = self.panel.cut(other)
    def fuseto(self,other):
        self.panel = self.panel.fuse(other)

class PortableM64CaseBackPanel(PortableM64CaseCommon):
    def __init__(self,name,origin,depth):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        if depth <= 0:
            raise RuntimeError("depth must be a positive and non-zero!")
        self.depth = depth
        pwidth = self.Width()
        self.pwidth = pwidth
        corner = origin.add(Base.Vector(0,self.Height()-self.WallThickness(),0))
        self.corner = corner
        thickvect = Base.Vector(0,self.WallThickness(),0)
        self.thickness = thickvect
        YNorm=Base.Vector(0,1,0)
        self.panel =  Part.makePlane(depth,pwidth,corner,YNorm
                                    ).extrude(thickvect)
        CutList.AddCut(depth,pwidth,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        Part.show(self.panel)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    def PanelCornerPoint(self):
        return self.corner
    def PanelThickness(self):
        return self.thickness.y
    def PanelDirection(self):
        return Base.Vector(0,1,0)
    def cutfrom(self,other):
        self.panel = self.panel.cut(other)
    def fuseto(self,other):
        self.panel = self.panel.fuse(other)

class PortableM64CaseBottom(PortableM64CaseCommon):
    _dcdc512Xoff = 100
    _dcdc512Yoff = 2*25.4
    _dcdc512StandoffHeight = 6
    _dcdc512StandoffDiameter = 6.35
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.panel = PortableM64CasePanel(name+":panel",origin)
        ax = M64Board._m64XOff
        ay = M64Board._m64YOff
        az = M64Board._m64Standoff+self.panel.PanelThickness()
        ao = Base.Vector(ax,ay,az)
        self.m64 = M64Board(name+":M64",self.panel.corner.add(ao))
        mholez = self.panel.corner.z
        mholeext = self.panel.thickness
        self.panel.cutfrom(self.m64.MountingHole(1,mholez).extrude(mholeext))
        self.panel.cutfrom(self.m64.MountingHole(2,mholez).extrude(mholeext))
        self.panel.cutfrom(self.m64.MountingHole(3,mholez).extrude(mholeext))
        self.panel.cutfrom(self.m64.MountingHole(4,mholez).extrude(mholeext))
        standoffZ = self.panel.corner.z+self.panel.PanelThickness()
        self.m64standoff1 = self.m64.Standoff(1,standoffZ,
                                           M64Board._m64Standoff,
                                           M64Board._m64StandoffDia)
        self.m64standoff2 = self.m64.Standoff(2,standoffZ,
                                           M64Board._m64Standoff,
                                           M64Board._m64StandoffDia)
        self.m64standoff3 = self.m64.Standoff(3,standoffZ,
                                           M64Board._m64Standoff,
                                           M64Board._m64StandoffDia)
        self.m64standoff4 = self.m64.Standoff(4,standoffZ,
                                           M64Board._m64Standoff,
                                           M64Board._m64StandoffDia)
        xoff = self.Width() - Fan02510SS_05P_AT00._fandepth - self.WallThickness() - CU_3002A_._basewidth
        yoff = self.Height() - CU_3002A_._baselength - self.panel.PanelThickness()
        zoff = self.WallThickness()
        psboxorigin = origin.add(Base.Vector(xoff,yoff,zoff))
        self.psbox = PSBox(name+":psbox",psboxorigin)
        self.panel.cutfrom(self.psbox.MountingHole(1,self.panel.corner.z).extrude(self.panel.thickness))
        self.panel.cutfrom(self.psbox.MountingHole(2,self.panel.corner.z).extrude(self.panel.thickness))
        self.panel.cutfrom(self.psbox.MountingHole(3,self.panel.corner.z).extrude(self.panel.thickness))
        self.panel.cutfrom(self.psbox.MountingHole(4,self.panel.corner.z).extrude(self.panel.thickness))
        dcdc512_dx = PortableM64CaseBottom._dcdc512Xoff+self.WallThickness()
        dcdc512_dy = PortableM64CaseBottom._dcdc512Yoff+self.WallThickness()
        dcdc512_dz = PortableM64CaseBottom._dcdc512StandoffHeight+self.WallThickness()
        dcdc512origin = origin.add(Base.Vector(dcdc512_dx,dcdc512_dy,dcdc512_dz))
        self.dcdc512 = DCDC_5_12_Horiz12Right(name+":dcdc512",dcdc512origin)
        self.dcdc512_standoff1 = self.dcdc512.Standoff(1,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.dcdc512_standoff2 = self.dcdc512.Standoff(2,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.dcdc512_standoff3 = self.dcdc512.Standoff(3,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.dcdc512_standoff4 = self.dcdc512.Standoff(4,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.panel.cutfrom(self.dcdc512.MountingHole(1,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.dcdc512.MountingHole(2,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.dcdc512.MountingHole(3,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.dcdc512.MountingHole(4,self.panel.corner.z,self.WallThickness()))
        hmiconvertermainboardorig=Base.Vector(self.panel.corner.x+12.7,
                                             self.panel.corner.y+self.panel.pheight-(12.7+HDMIConverterDims._mainboardHeight),
                                             self.panel.corner.z+6.35+self.panel.PanelThickness())
        self.hdmiconvertermainboard = HDMIConverterMainBoard(name+":hdmiconvertermainboard",hmiconvertermainboardorig)
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(1,self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(2,self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(3,self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(4,self.panel.corner.z,self.panel.PanelThickness()))
        self.hdmiconvertermainboard_standoff1 = self.hdmiconvertermainboard.Standoff(1,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        self.hdmiconvertermainboard_standoff2 = self.hdmiconvertermainboard.Standoff(2,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        self.hdmiconvertermainboard_standoff3 = self.hdmiconvertermainboard.Standoff(3,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        self.hdmiconvertermainboard_standoff4 = self.hdmiconvertermainboard.Standoff(4,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        self.left  = PortableM64CaseLeftPanel(name+":left",origin,
                                              self.BottomDepth())
        self.left.cutfrom(self.m64.DualUSBCutout(self.left.corner.x,self.left.PanelThickness()))
        self.left.cutfrom(self.m64.RJ45Cutout(self.left.corner.x,self.left.PanelThickness()))
        self.left.cutfrom(self.m64.AudioCutout(self.left.corner.x,self.left.PanelThickness()))
        self.right = PortableM64CaseRightPanel(name+":right",origin,
                                              self.BottomDepth())
        self.right.cutfrom(self.psbox.SquareFanHole1(self.right.corner.x,self.right.PanelThickness()))
        self.right.cutfrom(self.psbox.SquareFanHole2(self.right.corner.x,self.right.PanelThickness()))
        grillz = self.psbox.fan1.origin.z-5
        grilly = self.psbox.fan2.origin.y+Fan02510SS_05P_AT00._fanwidth_height+5
        grillh = Fan02510SS_05P_AT00._fanwidth_height+10
        grillw = (Fan02510SS_05P_AT00._fanwidth_height*2)+10
        grillthick = .05*25.4
        grillx = self.right.corner.x+self.right.PanelThickness()-grillthick
        gporig = Base.Vector(grillx,grilly,grillz)
        gpextv = Base.Vector(grillthick,0,0)
        self.grillpanel = Part.makePlane(grillh,grillw,gporig,Base.Vector(1,0,0)).extrude(gpextv)
        self.right.cutfrom(self.grillpanel)
        self.grillpanel = self.psbox.DrillGrillHoles1(grillx,grillthick,2.5,3.5,self.grillpanel)
        self.grillpanel = self.psbox.DrillGrillHoles2(grillx,grillthick,2.5,3.5,self.grillpanel)
        self.front = PortableM64CaseFrontPanel(name+":front",origin,
                                              self.BottomDepth())
        self.front.cutfrom(self.m64.GPIOCutout(self.front.corner.y,self.front.PanelThickness()))
        self.back = PortableM64CaseBackPanel(name+":back",origin,
                                              self.BottomDepth())
        self.back.cutfrom(self.psbox.InletFlangeCutout(self.back.corner.y,self.back.PanelThickness()))
    def show(self):
        self.panel.show()
        self.left.show()
        self.right.show()
        self.front.show()
        self.back.show()
        self.m64.show()
        self.psbox.show()
        self.dcdc512.show()
        self.hdmiconvertermainboard.show()
        doc = App.activeDocument()
        Part.show(self.m64standoff1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':M64Standoff1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.m64standoff2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':M64Standoff2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.m64standoff3)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':M64Standoff3'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.m64standoff4)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':M64Standoff4'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.dcdc512_standoff1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':dcdc512Standoff1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.dcdc512_standoff2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':dcdc512Standoff2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.dcdc512_standoff3)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':dcdc512Standoff3'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.dcdc512_standoff4)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':dcdc512Standoff4'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        Part.show(self.grillpanel)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':psgrill'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.9,.9,.9])
        Part.show(self.hdmiconvertermainboard_standoff1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmiconvertermainboard_standoff1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.hdmiconvertermainboard_standoff2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmiconvertermainboard_standoff2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.hdmiconvertermainboard_standoff3)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmiconvertermainboard_standoff3'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.hdmiconvertermainboard_standoff4)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmiconvertermainboard_standoff4'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
                

class PortableM64CaseMiddle(PortableM64CaseCommon):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        morigin = origin.add(Base.Vector(0,0,self.BottomDepth()))
        mporigin = morigin.add(Base.Vector(0,0,self.MiddleLowerDepth()))
        self.panel = PortableM64CasePanel(name+":panel",mporigin)
        cx = self.panel.corner.x
        cy = self.panel.corner.y
        cz = self.panel.corner.z
        panelWidth = self.panel.pwidth
        panelLength = self.panel.pheight
        wOffset = (panelWidth/2.0)-(LCDDims._Width/2.0)
        leftbracketorig = Base.Vector(cx+wOffset,cy + 25.4,cz)
        self.leftbracket = LCDMountingBracket(name+":LCDLeftBracket",leftbracketorig,"L")
        self.panel.cutfrom(self.leftbracket.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftbracket.MountingHole(2,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftbracket.MountingHole(3,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftbracket.MountingHole(4,cz,self.panel.PanelThickness()))
        rightbracketorig = leftbracketorig.add(Base.Vector(LCDDims._Width,0,0))
        self.rightbracket = LCDMountingBracket(name+":LCDRightBracket",rightbracketorig,"R")
        self.panel.cutfrom(self.rightbracket.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightbracket.MountingHole(2,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightbracket.MountingHole(3,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightbracket.MountingHole(4,cz,self.panel.PanelThickness()))
        self.screen = LCDScreen(name+":screen",Base.Vector(cx+wOffset,cy + 25.4,cz-((6.5/2.0)+(((1.0/2.0)*25.4)/2.0))))
        hdmibuttonboardorig = Base.Vector(cx+12.7,
                                          (cy+panelLength)-HDMIConverterDims._buttonboardHeight,
                                          cz - 6.35 - HDMIConverterDims._boardthickness)
        
        self.hdmibuttonboard = HDMIButtonBoard_Upsidedown(name+":hdmibuttonboard",hdmibuttonboardorig)
        self.panel.cutfrom(self.hdmibuttonboard.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmibuttonboard.MountingHole(2,cz,self.panel.PanelThickness()))
        self.hdmibuttonboard_standoff1 = self.hdmibuttonboard.Standoff(1,cz,-6.35,6.35)
        self.hdmibuttonboard_standoff2 = self.hdmibuttonboard.Standoff(2,cz,-6.35,6.35)
        hdmihvpowerboardorig = Base.Vector((cx+panelWidth)-HDMIConverterDims._hvpowerboardWidth,
                                           (cy+panelLength)-HDMIConverterDims._hvpowerboardHeight,
                                           cz - 6.35 - HDMIConverterDims._boardthickness)
        self.hdmihvpowerboard = HDMIHVPowerBoard_Upsidedown(name+":hdmihvpowerboard",hdmihvpowerboardorig)
        self.panel.cutfrom(self.hdmihvpowerboard.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmihvpowerboard.MountingHole(2,cz,self.panel.PanelThickness()))
        self.hdmihvpowerboard_standoff1 = self.hdmihvpowerboard.Standoff(1,cz,-6.35,6.35)
        self.hdmihvpowerboard_standoff2 = self.hdmihvpowerboard.Standoff(2,cz,-6.35,6.35)
        self.left  = PortableM64CaseLeftPanel(name+":left",morigin,
                                              self.MiddleTotalDepth())
        self.right = PortableM64CaseRightPanel(name+":right",morigin,
                                              self.MiddleTotalDepth())
        self.front = PortableM64CaseFrontPanel(name+":front",morigin,
                                              self.MiddleTotalDepth())
        self.back = PortableM64CaseBackPanel(name+":back",morigin,
                                              self.MiddleTotalDepth())
    def show(self):
        self.panel.show()
        self.left.show()
        self.right.show()
        self.front.show()
        self.back.show()
        self.leftbracket.show()
        self.rightbracket.show()
        self.screen.show()
        self.hdmibuttonboard.show()
        self.hdmihvpowerboard.show()
        doc = App.activeDocument()
        Part.show(self.hdmibuttonboard_standoff1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmibuttonboard_standoff1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.hdmibuttonboard_standoff2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmibuttonboard_standoff2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.hdmihvpowerboard_standoff1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmihvpowerboard_standoff1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.hdmihvpowerboard_standoff2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':hdmihvpowerboard_standoff2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        

class PortableM64CaseTop(PortableM64CaseCommon):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        torigin = origin.add(Base.Vector(0,0,self.BottomDepth()+self.MiddleTotalDepth()))
        tporigin = torigin.add(Base.Vector(0,0,self.TopDepth()-self.WallThickness()))
        self.panel = PortableM64CasePanel(name+":panel",tporigin)
        self.left  = PortableM64CaseLeftPanel(name+":left",torigin,
                                              self.TopDepth())
        self.right = PortableM64CaseRightPanel(name+":right",torigin,
                                              self.TopDepth())
        self.front = PortableM64CaseFrontPanel(name+":front",torigin,
                                              self.TopDepth())
        self.back = PortableM64CaseBackPanel(name+":back",torigin,
                                              self.TopDepth())
    def show(self):
        self.panel.show()
        self.left.show()
        self.right.show()
        self.front.show()
        self.back.show()



class PortableM64Case(PortableM64CaseCommon):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.bottom = PortableM64CaseBottom(name+":bottom",origin)
        self.middle = PortableM64CaseMiddle(name+":middle",origin)
        self.top    = PortableM64CaseTop(name+":top",origin)
    def show(self):
        self.bottom.show()
        self.middle.show()
        self.top.show()
