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
#  Last Modified : <200724.0935>
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

from M64 import *
from PSBox import *
from Electromech import *
from DCDC_5_12 import *
from LCDScreen import *
from LCDMountingBracket import * 
from HDMIConverter import * 
from TeensyThumbStick import *
from Speaker import *
from Battery import *
from USBHub import *
from OTGAdaptor import *
from USB_SATA_Adapter import *
from harddisk import *
from PianoHinge import *

from SectionList import *

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
        keys = list(cls._cutList.keys())
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
    _BottomDepth = 2.5 * 25.4
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
    _ShelfHeight = ((2.25-.125) * 25.4)-23
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
        self.block = Part.makePlane(thickness,width,offset,XNorm)\
                         .extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.block
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
        self.block = Part.makePlane(thickness,width,origin,YNorm)\
                         .extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.block
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
        self.block = Part.makePlane(thickness,width,origin,ZNorm)\
                         .extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.block
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
        self.block = Part.makePlane(width,thickness,origin,ZNorm)\
                         .extrude(lvect)
        CutList.AddCut(width,thickness,length)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.block
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.panel
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
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
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.panel
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
        self.panel =  Part.makePlane(depth,pheight,corner,XNorm)\
                          .extrude(thickvect)
        CutList.AddCut(depth,pheight,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.panel
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
        self.panel =  Part.makePlane(depth,pwidth,origin,YNorm)\
                          .extrude(thickvect)
        CutList.AddCut(depth,pwidth,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.panel
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
        corner = origin.add(Base.Vector(0,self.Height()-\
                                          self.WallThickness(),0))
        self.corner = corner
        thickvect = Base.Vector(0,self.WallThickness(),0)
        self.thickness = thickvect
        YNorm=Base.Vector(0,1,0)
        self.panel =  Part.makePlane(depth,pwidth,corner,YNorm
                                    ).extrude(thickvect)
        CutList.AddCut(depth,pwidth,self.WallThickness())
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.panel
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
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
    def __init__(self,name,origin,backhinge=None,keyboardhinge=None):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.panel = PortableM64CasePanel(name+"_panel",origin)
        ax = M64Board._m64XOff
        ay = M64Board._m64YOff
        az = M64Board._m64Standoff+self.panel.PanelThickness()
        ao = Base.Vector(ax,ay,az)
        self.m64 = M64Board(name+"_M64",self.panel.corner.add(ao))
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
        xoff = self.Width() - Fan02510SS_05P_AT00._fandepth - \
                              self.WallThickness() - CU_3002A_._basewidth
        yoff = self.Height() - CU_3002A_._baselength - \
                               self.panel.PanelThickness()
        zoff = self.WallThickness()
        psboxorigin = origin.add(Base.Vector(xoff,yoff,zoff))
        self.psbox = PSBox(name+"_psbox",psboxorigin)
        self.panel.cutfrom(self.psbox.MountingHole(1,self.panel.corner.z)\
                              .extrude(self.panel.thickness))
        self.panel.cutfrom(self.psbox.MountingHole(2,self.panel.corner.z)\
                              .extrude(self.panel.thickness))
        self.panel.cutfrom(self.psbox.MountingHole(3,self.panel.corner.z)\
                              .extrude(self.panel.thickness))
        self.panel.cutfrom(self.psbox.MountingHole(4,self.panel.corner.z)\
                              .extrude(self.panel.thickness))
        dcdc512_dx = PortableM64CaseBottom._dcdc512Xoff+self.WallThickness()
        dcdc512_dy = PortableM64CaseBottom._dcdc512Yoff+self.WallThickness()
        dcdc512_dz = PortableM64CaseBottom._dcdc512StandoffHeight+self.WallThickness()
        dcdc512origin = origin.add(Base.Vector(dcdc512_dx,dcdc512_dy,dcdc512_dz))
        self.dcdc512 = DCDC_5_12_Horiz12Right(name+"_dcdc512",dcdc512origin)
        self.dcdc512_standoff1 = self.dcdc512.Standoff(1,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.dcdc512_standoff2 = self.dcdc512.Standoff(2,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.dcdc512_standoff3 = self.dcdc512.Standoff(3,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.dcdc512_standoff4 = self.dcdc512.Standoff(4,standoffZ,PortableM64CaseBottom._dcdc512StandoffHeight,PortableM64CaseBottom._dcdc512StandoffDiameter)
        self.panel.cutfrom(self.dcdc512.MountingHole(1,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.dcdc512.MountingHole(2,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.dcdc512.MountingHole(3,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.dcdc512.MountingHole(4,self.panel.corner.z,self.WallThickness()))
        hdorig = self.panel.corner.add(Base.Vector(12.7 + HDMIConverterDims._mainboardWidth + 6.35,
                                                   self.panel.pheight-(12.7+Disk25_2H._Length),
                                                   self.panel.PanelThickness()))
        self.harddisk = Disk25_2H(name+"_harddisk",hdorig)
        self.panel.cutfrom(self.harddisk.MountingHole(1,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.harddisk.MountingHole(2,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.harddisk.MountingHole(3,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.harddisk.MountingHole(4,self.panel.corner.z,self.WallThickness()))
        usbsataadaptordelta = Base.Vector(12.7 + 50.8,
                                          self.panel.pheight-(12.7+Disk25_2H._Length + 12.7),
                                          self.panel.PanelThickness()+2.54)
        usbsataadaptororig = self.panel.corner.add(usbsataadaptordelta)
        self.usbsataadaptor = USB_SATA_Adapter_Horiz(name+"_usbsataadaptor",
                                                     usbsataadaptororig)
        cradleorig = usbsataadaptororig.add(Base.Vector(self.usbsataadaptor._USBPlug_XOff+1,
                                                        3.5,-2.54))
        self.usbsataadaptorcradle = USB_SATA_Adapter_BoardCradleHoriz(name+"_cradle",cradleorig)
        self.panel.cutfrom(self.usbsataadaptorcradle.MountingHole(1,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.usbsataadaptorcradle.MountingHole(2,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.usbsataadaptorcradle.MountingHole(3,self.panel.corner.z,self.WallThickness()))
        otgadaptor_dx = ((M64Board._OTG_Width - OTGAdaptor._MicroB_Width)/2.0) - OTGAdaptor._MicroB_XOff
        otgadaptor_dy = OTGAdaptor._MicroB_Length
        otgadaptor_dz = ((M64Board._OTG_Thick - OTGAdaptor._MicroB_Thick)/2.0) - OTGAdaptor._MicroB_ZOff
        otgadaptor_delta = Base.Vector(otgadaptor_dx,otgadaptor_dy,otgadaptor_dz)
        otgadaptororig = self.m64.otg_origin.add(otgadaptor_delta)
        self.otgadaptor = OTGAdaptor(name+"_otgadapter",otgadaptororig)
        hmiconvertermainboardorig=Base.Vector(self.panel.corner.x+12.7,
                                             self.panel.corner.y+self.panel.pheight-(12.7+HDMIConverterDims._mainboardHeight),
                                             self.panel.corner.z+6.35+self.panel.PanelThickness())
        self.hdmiconvertermainboard = HDMIConverterMainBoard(name+"_hdmiconvertermainboard",hmiconvertermainboardorig)
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(1,self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(2,self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(3,self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmiconvertermainboard.MountingHole(4,self.panel.corner.z,self.panel.PanelThickness()))
        self.hdmiconvertermainboard_standoff1 = self.hdmiconvertermainboard.Standoff(1,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        self.hdmiconvertermainboard_standoff2 = self.hdmiconvertermainboard.Standoff(2,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        self.hdmiconvertermainboard_standoff3 = self.hdmiconvertermainboard.Standoff(3,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        self.hdmiconvertermainboard_standoff4 = self.hdmiconvertermainboard.Standoff(4,self.panel.corner.z+self.panel.PanelThickness(),6.35,6.35)
        borig = self.panel.corner.add(Base.Vector(self.panel.pwidth-Battery._Length-BlockY._BlockWidth,
                                       BlockX._BlockWidth,self.panel.PanelThickness()))
        self.battery = Battery(name+"_battery",borig)
        usbo_x = 12.7+HDMIConverterDims._mainboardWidth+6.35
        usbo_x += Disk25_2H._Width+6.35
        usbo_y = self.panel.pheight - USBHub_._Length
        usbo_z = self.panel.PanelThickness()
        usbhorg = self.panel.corner.add(Base.Vector(usbo_x,usbo_y,usbo_z))
        self.usbhub = USBHub270(name+"_usbhub",usbhorg)
        self.left  = PortableM64CaseLeftPanel(name+"_left",origin,
                                              self.BottomDepth())
        self.left.cutfrom(self.m64.DualUSBCutout(self.left.corner.x,self.left.PanelThickness()))
        self.left.cutfrom(self.m64.RJ45Cutout(self.left.corner.x,self.left.PanelThickness()))
        self.left.cutfrom(self.m64.AudioCutout(self.left.corner.x,self.left.PanelThickness()))
        self.right = PortableM64CaseRightPanel(name+"_right",origin,
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
        self.front = PortableM64CaseFrontPanel(name+"_front",origin,
                                              self.BottomDepth())
        self.front.cutfrom(self.m64.GPIOCutout(self.front.corner.y,self.front.PanelThickness()))
        if keyboardhinge != None:
            for i in range(1,7):
                self.front.cutfrom(keyboardhinge.MountingHole(1,i,self.front.corner.y,self.front.PanelThickness()))
        self.back = PortableM64CaseBackPanel(name+"_back",origin,
                                              self.BottomDepth())
        self.back.cutfrom(self.psbox.InletFlangeCutout(self.back.corner.y,self.back.PanelThickness()))
        if backhinge != None:
            for i in range(1,7):
                self.back.cutfrom(backhinge.MountingHole(1,i,self.back.corner.y,self.back.PanelThickness()))
        blocko = self.panel.corner.add(Base.Vector(0,0,
                                                 self.panel.PanelThickness()))
        blockl = self.panel.pwidth
        self.frontblock = BlockX(name+"_frontblock",blocko,length=blockl)
        blocko = borig.add(Base.Vector(-BlockY._BlockWidth,0,0))
        blockl = Battery._Width - 6.35
        self.batteryblock1 = BlockY(name+"_batteryblock1",blocko,length=blockl)
        blocko = borig.add(Base.Vector(-BlockY._BlockWidth,Battery._Width,0))
        blockl = Battery._Length+BlockY._BlockWidth
        self.batteryblock2 = BlockX(name+"_batteryblock2",blocko,length=blockl)
        bpanelorig = borig.add(Base.Vector(-BlockY._BlockWidth,-BlockX._BlockWidth,BlockY._BlockThick))
        bpanellength = Battery._Length+(2*BlockY._BlockWidth)
        bpanelwidth  = Battery._Width+(2*BlockX._BlockWidth)
        self.bpanel = Part.makePlane(bpanellength,bpanelwidth,bpanelorig)\
                        .extrude(Base.Vector(0,0,self.WallThickness()))
        CutList.AddCut(bpanelwidth,bpanellength,self.WallThickness())
        bpanelMH1_x = bpanelorig.x + 38.1
        bpanelMH2_x = (bpanelorig.x + bpanellength)- 38.1
        bpanelMH1_y = bpanelorig.y + 6.35
        bpanelMH2_y = (bpanelorig.y+bpanelwidth)-6.35
        bpanelMHShapes = dict()
        bpanelMHRad = (.125*25.4)/2.0
        bpanelMHDepth = Base.Vector(0,0,bpanelorig.z+self.WallThickness())
        bpanelMHShapes[1] = Part.Face(Part.Wire(Part.makeCircle(bpanelMHRad,\
                    Base.Vector(bpanelMH1_x,bpanelMH1_y,0))))\
                    .extrude(bpanelMHDepth)
        bpanelMHShapes[2] = Part.Face(Part.Wire(Part.makeCircle(bpanelMHRad,\
                    Base.Vector(bpanelMH2_x,bpanelMH1_y,0))))\
                    .extrude(bpanelMHDepth)
        bpanelMHShapes[3] = Part.Face(Part.Wire(Part.makeCircle(bpanelMHRad,\
                    Base.Vector(bpanelMH1_x,bpanelMH2_y,0))))\
                    .extrude(bpanelMHDepth)
        bpanelMHShapes[4] = Part.Face(Part.Wire(Part.makeCircle(bpanelMHRad,\
                    Base.Vector(bpanelMH2_x,bpanelMH2_y,0))))\
                    .extrude(bpanelMHDepth)
        for i in [1,2,3,4]:
            self.panel.cutfrom(bpanelMHShapes[i])
            self.bpanel = self.bpanel.cut(bpanelMHShapes[i])
            if i == 1 or i == 2:
                self.frontblock.cutfrom(bpanelMHShapes[i])
            else:
                self.batteryblock2.cutfrom(bpanelMHShapes[i])
        ventholeRad = ((3.0/16.0)*25.4)/2.0
        ventholeSpace = (1.0/4.0)*25.4
        xleft = bpanelorig.x+BlockY._BlockWidth+(ventholeSpace/2.0)
        xleftend = bpanelMH1_x
        xright = bpanelMH2_x+(ventholeSpace/2.0)
        ybottom = bpanelorig.y+BlockY._BlockWidth+(ventholeSpace/2.0)
        holeextrude = Base.Vector(0,0,self.WallThickness())
        while xleft < xleftend:
            yhole = ybottom
            while yhole < (bpanelMH2_y-ventholeSpace):
                holeorig = Base.Vector(xleft,yhole,bpanelorig.z)
                hole = Part.Face(Part.Wire(Part.makeCircle(ventholeRad,\
                                                            holeorig)))\
                          .extrude(holeextrude)
                self.bpanel = self.bpanel.cut(hole)
                holeorig = Base.Vector(xright,yhole,bpanelorig.z)
                hole = Part.Face(Part.Wire(Part.makeCircle(ventholeRad,\
                                                            holeorig)))\
                          .extrude(holeextrude)
                self.bpanel = self.bpanel.cut(hole)
                yhole += ventholeSpace
            xleft += ventholeSpace
            xright += ventholeSpace
        blocko = self.panel.corner.add(Base.Vector(0,self.panel.pheight-BlockX._BlockWidth,self.panel.PanelThickness()))
        self.backblock = BlockX(name+"_backblock",blocko,length=usbo_x)
        blocko = self.panel.corner.add(Base.Vector(0,
                                           M64Board._m64YOff+M64Board._m64YMax,
                                           self.panel.PanelThickness()))
        blockl = self.panel.pheight-(M64Board._m64YOff+M64Board._m64YMax+BlockY._BlockWidth)
        self.leftblock = BlockY(name+"_leftblock",blocko,length=blockl) 
        blocko = self.panel.corner.add(Base.Vector(
                                          self.panel.pwidth-BlockY._BlockWidth,
                                          BlockY._BlockWidth,
                                          self.panel.PanelThickness()))
        self.rightblock = BlockY(name+"_rightblock",blocko,
                                 length=self.panel.pheight-BlockY._BlockWidth-PSBox._baselength)
        blocko = self.panel.corner.add(Base.Vector(0,0,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        blockl = self._ShelfHeight-(self.panel.PanelThickness()+BlockZa._BlockThick)
        self.leftfrontcorner = BlockZa(name+"_leftfrontcorner",blocko,
                                       length=blockl)
        blocko = self.panel.corner.add(Base.Vector(self.panel.pwidth-BlockY._BlockThick,0,self.panel.PanelThickness()+BlockX._BlockThick))
        blockl = self._ShelfHeight-(self.panel.PanelThickness()+BlockZa._BlockWidth)
        self.rightfrontcorner = BlockZa(name+"_rightfrontcorner",blocko,
                                       length=blockl)
        self.bpanel = self.bpanel.cut(self.rightfrontcorner.block)
        blocko = self.panel.corner.add(Base.Vector(0,
                              self.panel.pheight-BlockZa._BlockWidth,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        blockl = self._BottomDepth-(self.panel.PanelThickness()+BlockZa._BlockThick)
        self.leftbackcorner = BlockZa(name+"_leftbackcorner",blocko,
                                      length=blockl)
        blocko = self.panel.corner.add(Base.Vector(
                              self.panel.pwidth-BlockZa._BlockThick,
                              self.panel.pheight-BlockZa._BlockWidth,
                              self.panel.PanelThickness()))
        blockl = self._BottomDepth-self.panel.PanelThickness()
        self.rightbackcorner=BlockZa(name+"_rightbackcorner",blocko,
                                     length=blockl)
        blocko = self.panel.corner.add(Base.Vector(0,
                              self.ShelfLength()-BlockZa._BlockWidth,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        blockl = self._ShelfHeight-(self.panel.PanelThickness()+BlockZa._BlockThick)
        self.leftshelfsupport = BlockZa(name+"_leftshelfsupport",blocko,
                                        length=blockl)
        blocko = self.panel.corner.add(Base.Vector(
                                         self.panel.pwidth-BlockZa._BlockThick,
                                         self.ShelfLength()-BlockZa._BlockWidth,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        self.rightshelfsupport = BlockZa(name+"_rightshelfsupport",blocko,
                                        length=blockl)
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
        self.battery.show()
        self.usbhub.show()
        self.otgadaptor.show()
        self.harddisk.show()
        self.usbsataadaptor.show()
        self.usbsataadaptorcradle.show()
        self.frontblock.show()
        self.batteryblock1.show()
        self.batteryblock2.show()
        self.backblock.show()
        self.leftblock.show()
        self.rightblock.show()
        self.leftfrontcorner.show()
        self.rightfrontcorner.show()
        self.leftbackcorner.show()
        self.rightbackcorner.show()
        self.leftshelfsupport.show()
        self.rightshelfsupport.show()
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_M64Standoff1')
        obj.Shape = self.m64standoff1
        obj.Label=self.name+'_M64Standoff1'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_M64Standoff2')
        obj.Shape = self.m64standoff2
        obj.Label=self.name+'_M64Standoff2'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_M64Standoff3')
        obj.Shape = self.m64standoff3
        obj.Label=self.name+'_M64Standoff3'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'M64Standoff4')
        obj.Shape = self.m64standoff4
        obj.Label=self.name+'_M64Standoff4'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_dcdc512Standoff1')
        obj.Shape = self.dcdc512_standoff1
        obj.Label=self.name+'_dcdc512Standoff1'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_dcdc512Standoff2')
        obj.Shape = self.dcdc512_standoff2
        obj.Label=self.name+'_dcdc512Standoff2'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_dcdc512Standoff3')
        obj.Shape = self.dcdc512_standoff3
        obj.Label=self.name+'_dcdc512Standoff3'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_dcdc512Standoff4')
        obj.Shape = self.dcdc512_standoff4
        obj.Label=self.name+'_dcdc512Standoff4'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+'_psgrill')
        obj.Shape = self.grillpanel
        obj.Label=self.name+'_psgrill'
        obj.ViewObject.ShapeColor=tuple([.9,.9,.9])
        obj = doc.addObject("Part::Feature",self.name+'_hdmiconvertermainboard_standoff1')
        obj.Shape = self.hdmiconvertermainboard_standoff1
        obj.Label=self.name+'_hdmiconvertermainboard_standoff1'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_hdmiconvertermainboard_standoff2')
        obj.Shape = self.hdmiconvertermainboard_standoff2
        obj.Label=self.name+'_hdmiconvertermainboard_standoff2'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_hdmiconvertermainboard_standoff3')
        obj.Shape = self.hdmiconvertermainboard_standoff3
        obj.Label=self.name+'_hdmiconvertermainboard_standoff3'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_hdmiconvertermainboard_standoff4')
        obj.Shape = self.hdmiconvertermainboard_standoff4
        obj.Label=self.name+'_hdmiconvertermainboard_standoff4'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_batterypanel')
        obj.Shape = self.bpanel
        obj.Label=self.name+'_batterypanel'
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
                

class PortableM64CaseMiddle(PortableM64CaseCommon):
    def __init__(self,name,origin,bottombackhinge=None,topbackhinge=None):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        morigin = origin.add(Base.Vector(0,0,self.BottomDepth()))
        mporigin = morigin.add(Base.Vector(0,0,self.MiddleLowerDepth()))
        self.panel = PortableM64CasePanel(name+"_panel",mporigin)
        cx = self.panel.corner.x
        cy = self.panel.corner.y
        cz = self.panel.corner.z
        panelWidth = self.panel.pwidth
        panelLength = self.panel.pheight
        wOffset = (panelWidth/2.0)-(LCDDims._Width/2.0)
        leftbracketorig = Base.Vector(cx+wOffset,cy + 25.4,cz)
        self.leftbracket = LCDMountingBracket(name+"_LCDLeftBracket",leftbracketorig,"L")
        self.panel.cutfrom(self.leftbracket.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftbracket.MountingHole(2,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftbracket.MountingHole(3,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftbracket.MountingHole(4,cz,self.panel.PanelThickness()))
        rightbracketorig = leftbracketorig.add(Base.Vector(LCDDims._Width,0,0))
        self.rightbracket = LCDMountingBracket(name+"_LCDRightBracket",rightbracketorig,"R")
        self.panel.cutfrom(self.rightbracket.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightbracket.MountingHole(2,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightbracket.MountingHole(3,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightbracket.MountingHole(4,cz,self.panel.PanelThickness()))
        self.screen = LCDScreen(name+"_screen",Base.Vector(cx+wOffset,cy + 25.4,cz-((6.5/2.0)+(((1.0/2.0)*25.4)/2.0))))
        hdmibuttonboardorig = Base.Vector(cx+12.7,
                                          (cy+panelLength)-HDMIConverterDims._buttonboardHeight,
                                          cz - 6.35)
        
        self.hdmibuttonboard = HDMIButtonBoard_Upsidedown(name+"_hdmibuttonboard",hdmibuttonboardorig)
        self.panel.cutfrom(self.hdmibuttonboard.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmibuttonboard.MountingHole(2,cz,self.panel.PanelThickness()))
        self.hdmibuttonboard_standoff1 = self.hdmibuttonboard.Standoff(1,cz,-6.35,6.35)
        self.hdmibuttonboard_standoff2 = self.hdmibuttonboard.Standoff(2,cz,-6.35,6.35)
        hdmihvpowerboardorig = Base.Vector((cx+panelWidth)-(12.7+HDMIConverterDims._hvpowerboardWidth),
                                           (cy+panelLength)-HDMIConverterDims._hvpowerboardHeight,
                                           cz - 6.35)
        self.hdmihvpowerboard = HDMIHVPowerBoard_Upsidedown(name+"_hdmihvpowerboard",hdmihvpowerboardorig)
        self.panel.cutfrom(self.hdmihvpowerboard.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmihvpowerboard.MountingHole(2,cz,self.panel.PanelThickness()))
        self.hdmihvpowerboard_standoff1 = self.hdmihvpowerboard.Standoff(1,cz,-6.35,6.35)
        self.hdmihvpowerboard_standoff2 = self.hdmihvpowerboard.Standoff(2,cz,-6.35,6.35)
        leftspeakerorig = self.panel.corner.add(Base.Vector(0,(panelLength-Speaker_._Length)/2.0,-(6.35-Speaker_._StandoffRecessDepth)))
        self.leftspeaker = SpeakerLeft_UpsideDown(name+"_leftspeaker",leftspeakerorig)
        self.panel.cutfrom(self.leftspeaker.MountingHole("top",self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftspeaker.MountingHole("bottom",self.panel.corner.z,self.panel.PanelThickness()))
        self.leftspeaker_standofftop = self.leftspeaker.Standoff("top",self.panel.corner.z,-6.35,6)
        self.leftspeaker_standoffbottom = self.leftspeaker.Standoff("bottom",self.panel.corner.z,-6.35,6)
        rightspeakerorig = self.panel.corner.add(Base.Vector(panelWidth-Speaker_._Width,(panelLength-Speaker_._Length)/2.0,-(6.35-Speaker_._StandoffRecessDepth)))
        self.rightspeaker = SpeakerRight_UpsideDown(name+"_rightspeaker",rightspeakerorig)
        
        self.panel.cutfrom(self.rightspeaker.MountingHole("top",self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightspeaker.MountingHole("bottom",self.panel.corner.z,self.panel.PanelThickness()))
        self.rightspeaker_standofftop = self.rightspeaker.Standoff("top",self.panel.corner.z,-6.35,6)
        self.rightspeaker_standoffbottom = self.rightspeaker.Standoff("bottom",self.panel.corner.z,-6.35,6)
        self.left  = PortableM64CaseLeftPanel(name+"_left",morigin,
                                              self.MiddleTotalDepth())
        self.right = PortableM64CaseRightPanel(name+"_right",morigin,
                                              self.MiddleTotalDepth())
        self.front = PortableM64CaseFrontPanel(name+"_front",morigin,
                                              self.MiddleTotalDepth())
        self.back = PortableM64CaseBackPanel(name+"_back",morigin,
                                              self.MiddleTotalDepth())
        if bottombackhinge != None:
            for i in range(1,7):
                self.back.cutfrom(bottombackhinge.MountingHole(2,i,self.back.corner.y,self.back.PanelThickness()))
        if topbackhinge != None:
            for i in range(1,7):
                self.back.cutfrom(topbackhinge.MountingHole(1,i,self.back.corner.y,self.back.PanelThickness()))
        w = self.panel.pwidth
        h = self.panel.pheight
        pcorner = self.panel.corner
        pthick = self.panel.PanelThickness()
        blocko = pcorner.add(Base.Vector(0,0,pthick))
        blockl = w
        self.frontblock = BlockX(name+"_frontblock",blocko,length=blockl)
        blocko =  pcorner.add(Base.Vector(0,h-BlockX._BlockWidth,pthick))
        self.backblock = BlockX(name+"_backblock",blocko,length=blockl)
        self.backblock.cutfrom(self.hdmibuttonboard.MountingHole(1,pcorner.z+pthick,BlockX._BlockThick))
        self.backblock.cutfrom(self.hdmibuttonboard.MountingHole(2,pcorner.z+pthick,BlockX._BlockThick))
        self.backblock.cutfrom(self.hdmihvpowerboard.MountingHole(1,pcorner.z+pthick,BlockX._BlockThick))
        self.backblock.cutfrom(self.hdmihvpowerboard.MountingHole(2,pcorner.z+pthick,BlockX._BlockThick))
        blocko = pcorner.add(Base.Vector(0,BlockY._BlockWidth,pthick))
        blockl = h - (BlockY._BlockWidth*2)
        self.leftblock = BlockY(name+"_leftblock",blocko,length=blockl)
        self.leftblock.cutfrom(self.leftspeaker.MountingHole("top",pcorner.z+pthick,BlockX._BlockThick))
        self.leftblock.cutfrom(self.leftspeaker.MountingHole("bottom",pcorner.z+pthick,BlockX._BlockThick))
        blocko = pcorner.add(Base.Vector(w-BlockY._BlockWidth,BlockY._BlockWidth,pthick))
        self.rightblock = BlockY(name+"_rightblock",blocko,length=blockl)
        self.rightblock.cutfrom(self.rightspeaker.MountingHole("top",pcorner.z+pthick,BlockX._BlockThick))
        self.rightblock.cutfrom(self.rightspeaker.MountingHole("bottom",pcorner.z+pthick,BlockX._BlockThick))
        blocko = pcorner.add(Base.Vector(0,0,pthick+BlockZa._BlockThick))
        blockl = self._MiddleTotalDepth - (self._MiddleLowerDepth + pthick + BlockZa._BlockThick)
        self.leftfrontcorner = BlockZa(name+"_leftfrontcorner",blocko,
                                       length=blockl)
        blocko = pcorner.add(Base.Vector(w-BlockZa._BlockThick,0,
                                         pthick+BlockZa._BlockThick))
        self.rightfrontcorner = BlockZa(name+"_rightfrontcorner",blocko,
                                       length=blockl)
        blocko = pcorner.add(Base.Vector(0,h-BlockZa._BlockWidth,
                                         pthick+BlockZa._BlockThick))
        self.leftbackcorner = BlockZa(name+"_rightbackcorner",blocko,
                                       length=blockl)
        blocko = pcorner.add(Base.Vector(w-BlockZa._BlockThick,
                                         h-BlockZa._BlockWidth,
                                         pthick+BlockZa._BlockThick))
        self.rightbackcorner = BlockZa(name+"_leftbackcorner",blocko,
                                       length=blockl)

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
        self.leftspeaker.show()
        self.rightspeaker.show()
        self.frontblock.show()
        self.backblock.show()
        self.leftblock.show()
        self.rightblock.show()
        self.leftfrontcorner.show()
        self.rightfrontcorner.show()
        self.leftbackcorner.show()
        self.rightbackcorner.show()
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_hdmibuttonboard_standoff1')
        obj.Shape = self.hdmibuttonboard_standoff1
        obj.Label=self.name+'_hdmibuttonboard_standoff1'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_hdmibuttonboard_standoff2')
        obj.Shape = self.hdmibuttonboard_standoff2
        obj.Label=self.name+'_hdmibuttonboard_standoff2'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_hdmihvpowerboard_standoff1')
        obj.Shape = self.hdmihvpowerboard_standoff1
        obj.Label=self.name+'_hdmihvpowerboard_standoff1'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_hdmihvpowerboard_standoff2')
        obj.Shape = self.hdmihvpowerboard_standoff2
        obj.Label=self.name+'_hdmihvpowerboard_standoff2'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_leftspeaker_standofftop')
        obj.Shape = self.leftspeaker_standofftop
        obj.Label=self.name+'_leftspeaker_standofftop'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_leftspeaker_standoffbottom')
        obj.Shape = self.leftspeaker_standoffbottom
        obj.Label=self.name+'_leftspeaker_standoffbottom'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_rightspeaker_standofftop')
        obj.Shape = self.rightspeaker_standofftop
        obj.Label=self.name+'_rightspeaker_standofftop'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_rightspeaker_standoffbottom')
        obj.Shape = self.rightspeaker_standoffbottom
        obj.Label=self.name+'_rightspeaker_standoffbottom'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        

class PortableM64CaseTop(PortableM64CaseCommon):
    def __init__(self,name,origin,hinge=None):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        torigin = origin.add(Base.Vector(0,0,self.BottomDepth()+self.MiddleTotalDepth()))
        tporigin = torigin.add(Base.Vector(0,0,self.TopDepth()-self.WallThickness()))
        self.panel = PortableM64CasePanel(name+"_panel",tporigin)
        self.left  = PortableM64CaseLeftPanel(name+"_left",torigin,
                                              self.TopDepth())
        self.right = PortableM64CaseRightPanel(name+"_right",torigin,
                                              self.TopDepth())
        self.front = PortableM64CaseFrontPanel(name+"_front",torigin,
                                              self.TopDepth())
        self.back = PortableM64CaseBackPanel(name+"_back",torigin,
                                              self.TopDepth())
        corner = self.panel.corner
        panelWidth = self.panel.pwidth
        panelLength = self.panel.pheight
        panelThick = self.panel.PanelThickness()
        blocko = corner.add(Base.Vector(0,0,-BlockX._BlockThick))
        blockl = panelWidth
        self.frontblock = BlockX(name+"_frontblock",blocko,length=blockl)
        blocko = corner.add(Base.Vector(0,panelLength-BlockX._BlockWidth,
                                        -BlockX._BlockThick))
        self.backblock = BlockX(name+"_backblock",blocko,length=blockl)
        if hinge != None:
            for i in range(1,7):
                self.back.cutfrom(hinge.MountingHole(2,i,self.back.corner.y,self.back.PanelThickness()))
                self.backblock.cutfrom(hinge.MountingHole(2,i,blocko.y,BlockX._BlockWidth))
        blocko = corner.add(Base.Vector(0,BlockX._BlockWidth,
                                        -BlockX._BlockThick))
        blockl = panelLength - (2*BlockY._BlockWidth)
        self.leftblock = BlockY(name+"_leftblock",blocko,length=blockl)
        blocko = corner.add(Base.Vector(panelWidth-BlockY._BlockWidth,
                                        BlockX._BlockWidth,
                                        -BlockX._BlockThick))
        self.rightblock = BlockY(name+"_rightblock",blocko,length=blockl)
    def show(self):
        self.panel.show()
        self.left.show()
        self.right.show()
        self.front.show()
        self.back.show()
        self.frontblock.show()
        self.backblock.show()
        self.leftblock.show()
        self.rightblock.show()

class PortableM64CaseKeyboardShelf(PortableM64CaseCommon):
    def __init__(self,name,origin,hinge=None):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        shelforig = origin.add(Base.Vector(self.WallThickness(),
                                           self.WallThickness()+PianoHinge_._PinDia,
                                           self.ShelfHeight()))
        shelfthick = Base.Vector(0,0,self.WallThickness())
        shelfwidth = self.Width()-(self.WallThickness()*2)
        self.shelf = Part.makePlane(shelfwidth,
                                    self.ShelfLength(),
                                    shelforig).extrude(shelfthick)
        CutList.AddCut(shelfwidth,self.ShelfLength(),self.WallThickness())
        self.hingeblock = BlockX(name+"_hingeblock",
                                 shelforig.add(shelfthick),
                                 thickness=self.ShelfBlockThick(),
                                 length=shelfwidth)
        if hinge != None:
            for i in range(1,7):
                self.hingeblock.cutfrom(hinge.MountingHole(2,i,shelforig.y,self.ShelfBlockThick()))
        teensythumbstickO = shelforig.add(
                Base.Vector(shelfwidth - (TeensyThumbStick_._Width + 12.7),
                            self._ShelfLength - (TeensyThumbStick_._Height + 12.7),
                            -(self._TeensyThumbStickDrop + TeensyThumbStick_._BoardThick)))
        self.teensythumbstick = TeensyThumbStick(name+"_teensythumbstick",
                                                 teensythumbstickO)
        self.shelf = self.shelf.cut(self.teensythumbstick.Cutout(shelforig.z,
                                                        self.WallThickness()))
        self.shelf = self.shelf.cut(self.teensythumbstick.MountingHole(1,shelforig.z,
                                                        self.WallThickness()))
        self.shelf = self.shelf.cut(self.teensythumbstick.MountingHole(2,shelforig.z,
                                                        self.WallThickness()))
        self.shelf = self.shelf.cut(self.teensythumbstick.MountingHole(3,shelforig.z,
                                                        self.WallThickness()))
        self.shelf = self.shelf.cut(self.teensythumbstick.MountingHole(4,shelforig.z,
                                                        self.WallThickness()))
        self.teensythumbstick_standoff1 = self.teensythumbstick.Standoff(1,shelforig.z,-self._TeensyThumbStickDrop,.25*25.4)
        self.teensythumbstick_standoff2 = self.teensythumbstick.Standoff(2,shelforig.z,-self._TeensyThumbStickDrop,.25*25.4)
        self.teensythumbstick_standoff3 = self.teensythumbstick.Standoff(3,shelforig.z,-self._TeensyThumbStickDrop,.25*25.4)
        self.teensythumbstick_standoff4 = self.teensythumbstick.Standoff(4,shelforig.z,-self._TeensyThumbStickDrop,.25*25.4)
        teensythumbstickcoverO = teensythumbstickO.add(
                Base.Vector(0,0,
                (self._TeensyThumbStickDrop + TeensyThumbStick_._BoardThick + self.WallThickness())))
        self.teensythumbstickcover = TeensyThumbStickCover(name+"_teensythumbstickcover",
                                                       teensythumbstickcoverO)
        drop = Base.Vector(0,0,-self.TeensyThumbStickDrop())
        self.teensythumbstickbuttons = dict()
        for h in ['left','middle','right']:
            horig = self.teensythumbstickcover.buttonholes[h]
            porig = horig.add(drop)
            self.teensythumbstickbuttons[h] = TeensyThumbStickButtonPlunger(name+"_teensythumbstick_"+h,porig)
    def show(self):
        self.hingeblock.show()
        self.teensythumbstick.show()
        self.teensythumbstickcover.show()
        for h in ['left','middle','right']:
            self.teensythumbstickbuttons[h].show()
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_shelf')
        obj.Shape = self.shelf
        obj.Label=self.name+'_shelf'
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_teensythumbstick_standoff1')
        obj.Shape = self.teensythumbstick_standoff1
        obj.Label=self.name+'_teensythumbstick_standoff1'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_teensythumbstick_standoff2')
        obj.Shape = self.teensythumbstick_standoff2
        obj.Label=self.name+'_teensythumbstick_standoff2'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_teensythumbstick_standoff3')
        obj.Shape = self.teensythumbstick_standoff3
        obj.Label=self.name+'_teensythumbstick_standoff3'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_teensythumbstick_standoff4')
        obj.Shape = self.teensythumbstick_standoff4
        obj.Label=self.name+'_teensythumbstick_standoff4'
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
                        

class PortableM64Case(PortableM64CaseCommon):
    def __init__(self,name,origin,sections=SectionList("all")):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        if not isinstance(sections,SectionList):
            raise RuntimeError("sections is not a SectionList!")
        self.sections = sections
        self.keyboardshelfhinge = PianoHingeFlatInsideClosedFront(
          name+"_keyboardshelfhinge",
          origin.add(Base.Vector(((self._Width - PianoHinge_._Length)/2.0),
                 self._WallThickness,self._BottomDepth-PianoHinge_._FoldHeight)))
        self.bottommiddlehinge = PianoHingeFlatOutsideBack(
          name+"_bottommiddlehinge",
          origin.add(Base.Vector(
                   ((self._Width - PianoHinge_._Length)/2.0)-25.4,
                   self._Height,
                   self._BottomDepth - (PianoHinge_._FlangeWidth + PianoHinge_._PinOff + (PianoHinge_._PinDia / 2.0)))))
        self.middletophinge = PianoHingeFlatOutsideBack(
          name+"_middletophinge",
          origin.add(Base.Vector(
              ((self._Width - PianoHinge_._Length)/2.0),
              self._Height,
              (self._BottomDepth+self._MiddleTotalDepth) - (PianoHinge_._FlangeWidth + PianoHinge_._PinOff + (PianoHinge_._PinDia / 2.0)))))
        self.bottom = PortableM64CaseBottom(name+"_bottom",origin,
                                            backhinge=self.bottommiddlehinge,
                                            keyboardhinge=self.keyboardshelfhinge)
        self.middle = PortableM64CaseMiddle(name+"_middle",origin,
                                       bottombackhinge=self.bottommiddlehinge,
                                       topbackhinge=self.middletophinge)
        self.top    = PortableM64CaseTop(name+"_top",origin,
                                       hinge=self.middletophinge)
        self.keyboardshelf = PortableM64CaseKeyboardShelf(
                    name+"_keyboardshelf",
                    origin,
                    hinge=self.keyboardshelfhinge)


    def show(self):
        if self.sections.sectionP("Bottom"):
            self.bottom.show()
        if self.sections.sectionP("Middle"):
            self.middle.show()
        if self.sections.sectionP("Top"):
            self.top.show()
        if self.sections.sectionP("KeyboardShelf"):
            self.keyboardshelf.show()
        if self.sections.sectionP("KeyboardShelf") and self.sections.sectionP("Bottom"):
            self.keyboardshelfhinge.show()
        if self.sections.sectionP("Bottom") and self.sections.sectionP("Middle"):
            self.bottommiddlehinge.show()
        if self.sections.sectionP("Middle") and self.sections.sectionP("Top"):
            self.middletophinge.show()

if __name__ == '__main__':
    doc = None
    for docname in App.listDocuments():
        lddoc = App.getDocument(docname)
        if lddoc.Label == 'BananaPiM64Model':
            doc = lddoc
            break
    if doc == None:
        App.open("/home/heller/BananaPi_M64_Portable/3DModel/BananaPiM64Model.fcstd")
        doc = App.getDocument('BananaPiM64Model')
    App.ActiveDocument=doc
    Gui.ActiveDocument=doc
    #Gui.SendMsgToActiveView("ViewFit")
    #Gui.activeDocument().activeView().viewIsometric()
    for g in doc.findObjects('TechDraw::DrawSVGTemplate'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('TechDraw::DrawPage'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('Spreadsheet::Sheet'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('TechDraw::DrawViewPart'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('TechDraw::DrawViewDimension'):
        doc.removeObject(g.Name)
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = doc.USLetterTemplate.EditableTexts
    doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = doc.USLetterTemplate.EditableTexts
    edt['CompanyName'] = "Deepwoods Software"
    edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA'    
    edt['DrawingTitle1']= 'Block Drill Sheets'
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
    #*****
    # Top blocks -- hinge mounting holes
    doc.addObject('TechDraw::DrawPage','TopBackBlockDrillSheetPage')
    doc.TopBackBlockDrillSheetPage.Template = doc.USLetterTemplate
    edt = doc.TopBackBlockDrillSheetPage.Template.EditableTexts
    edt['DrawingTitle2']= "Top Back"
    edt['Scale'] = '.5'
    edt['Sheet'] = "Sheet 1 of 7"
    doc.TopBackBlockDrillSheetPage.Template.EditableTexts = edt
    doc.TopBackBlockDrillSheetPage.ViewObject.show()
    topbacksheet = doc.addObject('Spreadsheet::Sheet','TopBackDimensionTable')
    topbacksheet.set("A1",'%-11.11s'%"Dim")
    topbacksheet.set("B1",'%10.10s'%"inch")
    topbacksheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','TopBackView')
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackView)
    doc.TopBackView.Source = doc.M64Case_top_backblock
    doc.TopBackView.Direction=(0.0,1.0,0.0)
    doc.TopBackView.Scale = .5
    doc.TopBackView.X = 140
    doc.TopBackView.Y = 180
    
    blockShape = doc.M64Case_top_backblock.Shape
    minX = 999999999
    minZ = 999999999
    maxX = 0
    maxZ = 0
    for v in blockShape.Vertexes:
       if v.X < minX:
           minX = v.X
       if v.X > maxX:
           maxX = v.X    
       if v.Z < minZ:
           minZ = v.Z
       if v.Z > maxZ:
           maxZ = v.Z
    length = maxX - minX
    height = maxZ - minZ
    #print ('*** TopBack: origin (%g,%g), length = %g, height = %g'%(minX,minZ,length,height))    
    #i = 0
    #for e in blockShape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        #print('*** TopBack: Edges[%d].Curve is a %s'%(i,type(e.Curve)))
    #        circ = e.Curve
    #        print('*** TopBack: Edges[%d].Curve %g at (%g,%g)'%\
    #              (i,circ.Radius*2,circ.Location.x,circ.Location.z))
    #    i += 1
    holediameter = blockShape.Edges[11].Curve.Radius*2
    holezoff = blockShape.Edges[11].Curve.Location.z-minZ
    holez1off = height-holezoff
    #print ('*** TopBack: holezoff=%g,holez1off=%g'%(holezoff,holez1off))
    holeoff1 = blockShape.Edges[11].Curve.Location.x-minX
    holeoff2 = blockShape.Edges[12].Curve.Location.x-minX
    holeoff3 = blockShape.Edges[7].Curve.Location.x-minX
    holeoff4 = blockShape.Edges[8].Curve.Location.x-minX
    holeoff5 = blockShape.Edges[10].Curve.Location.x-minX
    holeoff6 = blockShape.Edges[9].Curve.Location.x-minX
    #print ('*** TopBack: holeoff1=%g,holeoff2=%g,holeoff3=%g,holeoff4=%g,holeoff5=%g,holeoff6=%g'%\
    #       (holeoff1,holeoff2,holeoff3,holeoff4,holeoff5,holeoff6))
    # Edge6    -- For diameter (holediameter)
    doc.addObject('TechDraw::DrawViewDimension','TopBackHDia')
    doc.TopBackHDia.Type = 'Diameter'
    doc.TopBackHDia.References2D=[(doc.TopBackView,'Edge6')]
    doc.TopBackHDia.FormatSpec='HDia (6x)'
    doc.TopBackHDia.Arbitrary = True
    doc.TopBackHDia.X = -30
    doc.TopBackHDia.Y = 10
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackHDia)
    topbacksheet.set("A%d"%ir,'%-11.11s'%"HDia")
    topbacksheet.set("B%d"%ir,'%10.6f'%(holediameter/25.4))
    topbacksheet.set("C%d"%ir,'%10.6f'%holediameter)
    ir += 1
    # Vertex1  -- Origin (ll)
    # Vertex2  -- Extent (ur) (length,height)
    doc.addObject('TechDraw::DrawViewDimension','TopBackLength')
    doc.TopBackLength.Type = 'DistanceX'
    doc.TopBackLength.References2D=[(doc.TopBackView,'Vertex1'),\
                                    (doc.TopBackView,'Vertex2')]
    doc.TopBackLength.FormatSpec='l'
    doc.TopBackLength.Arbitrary = True
    doc.TopBackLength.X = 0
    doc.TopBackLength.Y = -5
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackLength)
    topbacksheet.set("A%d"%ir,'%-11.11s'%"l")
    topbacksheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    topbacksheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','TopBackHeight')
    doc.TopBackHeight.Type = 'DistanceY'
    doc.TopBackHeight.References2D=[(doc.TopBackView,'Vertex1'),\
                                    (doc.TopBackView,'Vertex2')]
    doc.TopBackHeight.FormatSpec='h'
    doc.TopBackHeight.Arbitrary = True
    doc.TopBackHeight.X =105
    doc.TopBackLength.Y =-11 
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackHeight)
    topbacksheet.set("A%d"%ir,'%-11.11s'%"h")
    topbacksheet.set("B%d"%ir,'%10.6f'%(height/25.4))
    topbacksheet.set("C%d"%ir,'%10.6f'%height)
    ir += 1
    # Vertex12 -- Hole 1 (holezoff,holeoff1)
    doc.addObject('TechDraw::DrawViewDimension','TopBackHoleZ')
    doc.TopBackHoleZ.Type = 'DistanceY'
    doc.TopBackHoleZ.References2D=[(doc.TopBackView,'Vertex1'),\
                                   (doc.TopBackView,'Vertex12')]
    doc.TopBackHoleZ.FormatSpec='z'
    doc.TopBackHoleZ.Arbitrary = True
    doc.TopBackHoleZ.X = -105
    doc.TopBackHoleZ.Y = -5
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackHoleZ)
    topbacksheet.set("A%d"%ir,'%-11.11s'%"z")
    topbacksheet.set("B%d"%ir,'%10.6f'%(holezoff/25.4))
    topbacksheet.set("C%d"%ir,'%10.6f'%holezoff)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','TopBackHole1')
    doc.TopBackHole1.Type = 'DistanceX'
    doc.TopBackHole1.References2D=[(doc.TopBackView,'Vertex1'),\
                                   (doc.TopBackView,'Vertex12')]
    doc.TopBackHole1.FormatSpec='a'
    doc.TopBackHole1.Arbitrary = True
    doc.TopBackHole1.X = -80
    doc.TopBackHole1.Y = -6
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackHole1)
    topbacksheet.set("A%d"%ir,'%-11.11s'%"a")
    topbacksheet.set("B%d"%ir,'%10.6f'%(holeoff1/25.4))
    topbacksheet.set("C%d"%ir,'%10.6f'%holeoff1)
    ir += 1
    # Vertex15 -- Hole 2 (holeoff2)
    doc.addObject('TechDraw::DrawViewDimension','TopBackHolePitch')
    doc.TopBackHolePitch.Type = 'DistanceX'
    doc.TopBackHolePitch.References2D=[(doc.TopBackView,'Vertex12'),\
                                       (doc.TopBackView,'Vertex15')]
    doc.TopBackHolePitch.FormatSpec='p (5x)'
    doc.TopBackHolePitch.Arbitrary = True
    doc.TopBackHolePitch.X = -50
    doc.TopBackHolePitch.Y = -6
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackHolePitch)
    topbacksheet.set("A%d"%ir,'%-11.11s'%"p")
    topbacksheet.set("B%d"%ir,'%10.6f'%((holeoff2-holeoff1)/25.4))
    topbacksheet.set("C%d"%ir,'%10.6f'%(holeoff2-holeoff1))
    ir += 1
    # Vertex9  -- Hole 3 (holeoff3)
    # Vertex6  -- Hole 4 (holeoff4)
    # Vertex21 -- Hole 5 (holeoff5)
    # Vertex18 -- Hole 6 (holeoff6)

    doc.addObject('TechDraw::DrawViewSpreadsheet','TopBackDimBlock')
    doc.TopBackBlockDrillSheetPage.addView(doc.TopBackDimBlock)
    doc.TopBackDimBlock.Source = topbacksheet
    doc.TopBackDimBlock.TextSize = 8
    doc.TopBackDimBlock.CellEnd = "C%d"%(ir-1) 
    doc.TopBackDimBlock.recompute()
    doc.TopBackDimBlock.X = 82
    doc.TopBackDimBlock.Y = 140
    doc.TopBackBlockDrillSheetPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.TopBackBlockDrillSheetPage,"BananaPiM64Model_TopBackBlockDrillSheet.pdf")
    #*****
    # Middle blocks (various mounting holes)
    # Back (HDMI aux boards: buttons and HV PS)
    doc.addObject('TechDraw::DrawPage','MiddleBackBlockDrillSheetPage')
    doc.MiddleBackBlockDrillSheetPage.Template = doc.USLetterTemplate
    edt = doc.MiddleBackBlockDrillSheetPage.Template.EditableTexts
    edt['DrawingTitle2']= "Middle Back"
    edt['Scale'] = '.5'
    edt['Sheet'] = "Sheet 2 of 7"
    doc.MiddleBackBlockDrillSheetPage.Template.EditableTexts = edt
    doc.MiddleBackBlockDrillSheetPage.ViewObject.show()
    middlebacksheet = doc.addObject('Spreadsheet::Sheet','MiddleBackDimensionTable')
    middlebacksheet.set("A1",'%-11.11s'%"Dim")
    middlebacksheet.set("B1",'%10.10s'%"inch")
    middlebacksheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','MiddleBackView')
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackView)
    doc.MiddleBackView.Source = doc.M64Case_middle_backblock
    doc.MiddleBackView.Direction=(0.0,0.0,-1.0)
    doc.MiddleBackView.Scale = .5
    doc.MiddleBackView.Rotation = 180
    doc.MiddleBackView.X = 140
    doc.MiddleBackView.Y = 180
    blockShape = doc.M64Case_middle_backblock.Shape
    minX = 999999999
    minY = 999999999
    maxX = 0
    maxY = 0
    for v in blockShape.Vertexes:
       if v.X < minX:
           minX = v.X
       if v.X > maxX:
           maxX = v.X    
       if v.Y < minY:
           minY = v.Y
       if v.Y > maxY:
           maxY = v.Y
    length = maxX - minX
    height = maxY - minY
    #print ('*** MiddleBack: origin (%g,%g), length = %g, height = %g'%(minX,minY,length,height))    
    #i = 0
    #for e in blockShape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        #print('*** MiddleBack: Edges[%d].Curve is a %s'%(i,type(e.Curve)))
    #        circ = e.Curve
    #        print('*** MiddleBack: Edges[%d].Curve %g at (%g,%g)'%\
    #              (i,circ.Radius*2,circ.Location.x-minX,circ.Location.y-minY))
    #    i += 1
    
    # Vertex0  -- origin (ur)
    # Vertex3  -- extent (ll) (height,length)
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackLength')
    doc.MiddleBackLength.Type = 'DistanceX'
    doc.MiddleBackLength.References2D = [(doc.MiddleBackView,'Vertex0'),\
                                         (doc.MiddleBackView,'Vertex3')]
    doc.MiddleBackLength.FormatSpec='l'
    doc.MiddleBackLength.Arbitrary = True
    doc.MiddleBackLength.X = 0
    doc.MiddleBackLength.Y = -12
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackLength)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"l")
    middlebacksheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackHeight')
    doc.MiddleBackHeight.Type = 'DistanceY'
    doc.MiddleBackHeight.References2D = [(doc.MiddleBackView,'Vertex0'),\
                                         (doc.MiddleBackView,'Vertex3')]
    doc.MiddleBackHeight.FormatSpec='h'
    doc.MiddleBackHeight.Arbitrary = True
    doc.MiddleBackHeight.X = 105
    doc.MiddleBackHeight.Y = 0
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackHeight)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"h")
    middlebacksheet.set("B%d"%ir,'%10.6f'%(height/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%height)
    ir += 1

    # Edge7    -- button board MH diameter
    doc.addObject('TechDraw::DrawViewDimension','MiddleBBMHDia')
    doc.MiddleBBMHDia.Type = 'Diameter'
    doc.MiddleBBMHDia.References2D = [(doc.MiddleBackView,'Edge7')]
    doc.MiddleBBMHDia.FormatSpec='BBDia (2x)'
    doc.MiddleBBMHDia.Arbitrary = True
    doc.MiddleBBMHDia.X = 60
    doc.MiddleBBMHDia.Y = 13
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBBMHDia)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"BBDia")
    middlebacksheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims._buttonboardMHDia/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims._buttonboardMHDia)
    ir += 1
    
    # Vertex15 -- button board MH 1 (right) (nearest Vertex0) blockShape.Edges[7] 
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackBBMH1Yoff')
    doc.MiddleBackBBMH1Yoff.Type = 'DistanceY'
    doc.MiddleBackBBMH1Yoff.References2D = [(doc.MiddleBackView,'Vertex2'),\
                                         (doc.MiddleBackView,'Vertex15')]
    doc.MiddleBackBBMH1Yoff.FormatSpec='E'
    doc.MiddleBackBBMH1Yoff.Arbitrary = True
    doc.MiddleBackBBMH1Yoff.X = 70
    doc.MiddleBackBBMH1Yoff.Y = -6
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackBBMH1Yoff)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"E")
    E = blockShape.Edges[7].Curve.Location.y - minY
    middlebacksheet.set("B%d"%ir,'%10.6f'%(E/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%E)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackBBMH1Xoff')
    doc.MiddleBackBBMH1Xoff.Type = 'DistanceX'
    doc.MiddleBackBBMH1Xoff.References2D = [(doc.MiddleBackView,'Vertex0'),\
                                         (doc.MiddleBackView,'Vertex15')]
    doc.MiddleBackBBMH1Xoff.FormatSpec='A'
    doc.MiddleBackBBMH1Xoff.Arbitrary = True
    doc.MiddleBackBBMH1Xoff.X = 92
    doc.MiddleBackBBMH1Xoff.Y = -7
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackBBMH1Xoff)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"A")
    A = blockShape.Edges[7].Curve.Location.x - minX
    middlebacksheet.set("B%d"%ir,'%10.6f'%(A/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%A)
    ir += 1
    # Vertex12 -- button board MH 2 (left) blockShape.Edges[6]
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackBBMH12Xoff')
    doc.MiddleBackBBMH12Xoff.Type = 'DistanceX'
    doc.MiddleBackBBMH12Xoff.References2D = [(doc.MiddleBackView,'Vertex15'),\
                                         (doc.MiddleBackView,'Vertex12')]
    doc.MiddleBackBBMH12Xoff.FormatSpec='B'
    doc.MiddleBackBBMH12Xoff.Arbitrary = True
    doc.MiddleBackBBMH12Xoff.X = 61
    doc.MiddleBackBBMH12Xoff.Y = -7
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackBBMH12Xoff)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"B")
    bbmh12X = HDMIConverterDims._buttonboardMH2_x - \
                HDMIConverterDims._buttonboardMH1_x
    middlebacksheet.set("B%d"%ir,'%10.6f'%(bbmh12X/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%bbmh12X)
    ir += 1

    # Edge5    -- HV PS board MH diameter
    doc.addObject('TechDraw::DrawViewDimension','MiddleHVMHDia')
    doc.MiddleHVMHDia.Type = 'Diameter'
    doc.MiddleHVMHDia.References2D = [(doc.MiddleBackView,'Edge5')]
    doc.MiddleHVMHDia.FormatSpec='HVDia (2x)'
    doc.MiddleHVMHDia.Arbitrary = True
    doc.MiddleHVMHDia.X = -60
    doc.MiddleHVMHDia.Y = 13
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleHVMHDia)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"HVDia")
    middlebacksheet.set("B%d"%ir,'%10.6f'%(HDMIConverterDims._hvpowerboardMHDia/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%HDMIConverterDims._hvpowerboardMHDia)
    ir += 1

    # Vertex6  -- HV PS Board MH 2 (right) blockShape.Edges[4]
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackHVMH2Xoff')
    doc.MiddleBackHVMH2Xoff.Type = 'DistanceX'
    doc.MiddleBackHVMH2Xoff.References2D = [(doc.MiddleBackView,'Vertex6'),\
                                         (doc.MiddleBackView,'Vertex9')]
    doc.MiddleBackHVMH2Xoff.FormatSpec='D'
    doc.MiddleBackHVMH2Xoff.Arbitrary = True
    doc.MiddleBackHVMH2Xoff.X = -50
    doc.MiddleBackHVMH2Xoff.Y = -7
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackHVMH2Xoff)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"D")
    D = HDMIConverterDims._hvpowerboardMH2_x - (HDMIConverterDims._hvpowerboardMH1_x1+(HDMIConverterDims._hvpowerboardMH1_wide/2.0))
    middlebacksheet.set("B%d"%ir,'%10.6f'%(D/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%D)
    ir += 1
    # Vertex9  -- HV PS Board MH 1 (left) (nearest Vertex3) blockShape.Edges[5]
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackHVMH1Yoff')
    doc.MiddleBackHVMH1Yoff.Type = 'DistanceY'
    doc.MiddleBackHVMH1Yoff.References2D = [(doc.MiddleBackView,'Vertex3'),\
                                         (doc.MiddleBackView,'Vertex9')]
    doc.MiddleBackHVMH1Yoff.FormatSpec='F'
    doc.MiddleBackHVMH1Yoff.Arbitrary = True
    doc.MiddleBackHVMH1Yoff.X = -70
    doc.MiddleBackHVMH1Yoff.Y = -6
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackHVMH1Yoff)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"F")
    F = blockShape.Edges[5].Curve.Location.y - minY
    middlebacksheet.set("B%d"%ir,'%10.6f'%(F/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%F)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleBackHVMH1Xoff')
    doc.MiddleBackHVMH1Xoff.Type = 'DistanceX'
    doc.MiddleBackHVMH1Xoff.References2D = [(doc.MiddleBackView,'Vertex3'),\
                                         (doc.MiddleBackView,'Vertex9')]
    doc.MiddleBackHVMH1Xoff.FormatSpec='C'
    doc.MiddleBackHVMH1Xoff.Arbitrary = True
    doc.MiddleBackHVMH1Xoff.X = -92
    doc.MiddleBackHVMH1Xoff.Y = -7
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackHVMH1Xoff)
    middlebacksheet.set("A%d"%ir,'%-11.11s'%"C")
    C = maxX - blockShape.Edges[5].Curve.Location.x
    middlebacksheet.set("B%d"%ir,'%10.6f'%(C/25.4))
    middlebacksheet.set("C%d"%ir,'%10.6f'%C)
    ir += 1

    doc.addObject('TechDraw::DrawViewSpreadsheet','MiddleBackDimBlock')
    doc.MiddleBackBlockDrillSheetPage.addView(doc.MiddleBackDimBlock)
    doc.MiddleBackDimBlock.Source = middlebacksheet
    doc.MiddleBackDimBlock.TextSize = 8
    doc.MiddleBackDimBlock.CellEnd = "C%d"%(ir-1) 
    doc.MiddleBackDimBlock.recompute()
    doc.MiddleBackDimBlock.X = 82
    doc.MiddleBackDimBlock.Y = 120
    doc.MiddleBackBlockDrillSheetPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.MiddleBackBlockDrillSheetPage,"BananaPiM64Model_MiddleBackBlockDrillSheet.pdf")
    # Left (Speaker)
    doc.addObject('TechDraw::DrawPage','MiddleLeftBlockDrillSheetPage')
    doc.MiddleLeftBlockDrillSheetPage.Template = doc.USLetterTemplate
    edt = doc.MiddleLeftBlockDrillSheetPage.Template.EditableTexts
    edt['DrawingTitle2']= "Middle Left"
    edt['Scale'] = '.75'
    edt['Sheet'] = "Sheet 3 of 7"
    doc.MiddleLeftBlockDrillSheetPage.Template.EditableTexts = edt
    doc.MiddleLeftBlockDrillSheetPage.ViewObject.show()
    middleleftsheet = doc.addObject('Spreadsheet::Sheet','MiddleLeftDimensionTable')
    middleleftsheet.set("A1",'%-11.11s'%"Dim")
    middleleftsheet.set("B1",'%10.10s'%"inch")
    middleleftsheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','MiddleLeftView')
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftView)
    doc.MiddleLeftView.Source = doc.M64Case_middle_leftblock
    doc.MiddleLeftView.Direction=(0.0,0.0,-1.0)
    doc.MiddleLeftView.Scale = .75
    doc.MiddleLeftView.Rotation = 90
    doc.MiddleLeftView.X = 140
    doc.MiddleLeftView.Y = 180
    blockShape = doc.M64Case_middle_leftblock.Shape
    minX = 999999999
    minY = 999999999
    maxX = 0
    maxY = 0
    for v in blockShape.Vertexes:
       if v.X < minX:
           minX = v.X
       if v.X > maxX:
           maxX = v.X    
       if v.Y < minY:
           minY = v.Y
       if v.Y > maxY:
           maxY = v.Y
    length = maxY - minY
    height = maxX - minX
    #print ('*** MiddleLeft: origin (%g,%g), length = %g, height = %g'%(minX,minY,length,height))    
    #i = 0
    #for e in blockShape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        #print('*** MiddleLeft: Edges[%d].Curve is a %s'%(i,type(e.Curve)))
    #        circ = e.Curve
    #        print('*** MiddleLeft: Edges[%d].Curve %g at (%g,%g)'%\
    #              (i,circ.Radius*2,circ.Location.x-minX,circ.Location.y-minY))
    #    i += 1
    # Vertex0  UR (minX, maxY)
    # Vertex1  UL (maxX, maxY)
    # Vertex2  LR (minX, minY
    # Vertex3  LL (maxX, minY)
    doc.addObject('TechDraw::DrawViewDimension','MiddleLeftLength')
    doc.MiddleLeftLength.Type = 'DistanceX'
    doc.MiddleLeftLength.References2D = [(doc.MiddleLeftView,'Vertex0'),\
                                         (doc.MiddleLeftView,'Vertex3')]
    doc.MiddleLeftLength.FormatSpec='l'
    doc.MiddleLeftLength.Arbitrary = True
    doc.MiddleLeftLength.X = 0
    doc.MiddleLeftLength.Y = -12
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftLength)
    middleleftsheet.set("A%d"%ir,'%-11.11s'%"l")
    middleleftsheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    middleleftsheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleLeftHeight')
    doc.MiddleLeftHeight.Type = 'DistanceY'
    doc.MiddleLeftHeight.References2D = [(doc.MiddleLeftView,'Vertex0'),\
                                         (doc.MiddleLeftView,'Vertex3')]
    doc.MiddleLeftHeight.FormatSpec='h'
    doc.MiddleLeftHeight.Arbitrary = True
    doc.MiddleLeftHeight.X = 105
    doc.MiddleLeftHeight.Y = 0
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftHeight)
    middleleftsheet.set("A%d"%ir,'%-11.11s'%"h")
    middleleftsheet.set("B%d"%ir,'%10.6f'%(height/25.4))
    middleleftsheet.set("C%d"%ir,'%10.6f'%height)
    ir += 1
    
    # Edge4 / Vertex6 (right) [speaker top] blockShape.Edges[4].Curve
    doc.addObject('TechDraw::DrawViewDimension','MiddleLeftSpeakerMHDia')
    doc.MiddleLeftSpeakerMHDia.Type = 'Diameter'
    doc.MiddleLeftSpeakerMHDia.References2D = [(doc.MiddleLeftView,'Edge5')]
    doc.MiddleLeftSpeakerMHDia.FormatSpec='EDia (2x)'
    doc.MiddleLeftSpeakerMHDia.Arbitrary = True
    doc.MiddleLeftSpeakerMHDia.X = -60
    doc.MiddleLeftSpeakerMHDia.Y = 13
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftSpeakerMHDia)
    middleleftsheet.set("A%d"%ir,'%-11.11s'%"EDia")
    middleleftsheet.set("B%d"%ir,'%10.6f'%(Speaker_._MHoleDia/25.4))
    middleleftsheet.set("C%d"%ir,'%10.6f'%Speaker_._MHoleDia)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleLeftTopMHXoff')
    doc.MiddleLeftTopMHXoff.Type = 'DistanceX'
    doc.MiddleLeftTopMHXoff.References2D = [(doc.MiddleLeftView,'Vertex6'),\
                                         (doc.MiddleLeftView,'Vertex0')]
    doc.MiddleLeftTopMHXoff.FormatSpec='A'
    doc.MiddleLeftTopMHXoff.Arbitrary = True
    doc.MiddleLeftTopMHXoff.X = 54
    doc.MiddleLeftTopMHXoff.Y = -7
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftTopMHXoff)
    middleleftsheet.set("A%d"%ir,'%-11.11s'%"A")
    A = blockShape.Edges[4].Curve.Location.y - minY
    middleleftsheet.set("B%d"%ir,'%10.6f'%(A/25.4))
    middleleftsheet.set("C%d"%ir,'%10.6f'%A)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleLeftTopMHYoff')
    doc.MiddleLeftTopMHYoff.Type = 'DistanceY'
    doc.MiddleLeftTopMHYoff.References2D = [(doc.MiddleLeftView,'Vertex6'),\
                                         (doc.MiddleLeftView,'Vertex0')]
    doc.MiddleLeftTopMHYoff.FormatSpec='B'
    doc.MiddleLeftTopMHYoff.Arbitrary = True
    doc.MiddleLeftTopMHYoff.X = 16
    doc.MiddleLeftTopMHYoff.Y = 8
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftTopMHYoff)
    middleleftsheet.set("A%d"%ir,'%-11.11s'%"B")
    B = blockShape.Edges[4].Curve.Location.x - minX
    middleleftsheet.set("B%d"%ir,'%10.6f'%(B/25.4))
    middleleftsheet.set("C%d"%ir,'%10.6f'%B)
    ir += 1
    
    # Edge5 / Vertex9 (left)  [speaker bottom] blockShape.Edges[5].Curve
    doc.addObject('TechDraw::DrawViewDimension','MiddleLeftBottomMHXoff')
    doc.MiddleLeftBottomMHXoff.Type = 'DistanceX'
    doc.MiddleLeftBottomMHXoff.References2D = [(doc.MiddleLeftView,'Vertex9'),\
                                         (doc.MiddleLeftView,'Vertex3')]
    doc.MiddleLeftBottomMHXoff.FormatSpec='C'
    doc.MiddleLeftBottomMHXoff.Arbitrary = True
    doc.MiddleLeftBottomMHXoff.X = -63
    doc.MiddleLeftBottomMHXoff.Y = -7
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftBottomMHXoff)
    middleleftsheet.set("A%d"%ir,'%-11.11s'%"C")
    C = maxY - blockShape.Edges[5].Curve.Location.y
    middleleftsheet.set("B%d"%ir,'%10.6f'%(C/25.4))
    middleleftsheet.set("C%d"%ir,'%10.6f'%C)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleLeftBottomMHYoff')
    doc.MiddleLeftBottomMHYoff.Type = 'DistanceY'
    doc.MiddleLeftBottomMHYoff.References2D = [(doc.MiddleLeftView,'Vertex9'),\
                                         (doc.MiddleLeftView,'Vertex1')]
    doc.MiddleLeftBottomMHYoff.FormatSpec='D'
    doc.MiddleLeftBottomMHYoff.Arbitrary = True
    doc.MiddleLeftBottomMHYoff.X = -50
    doc.MiddleLeftBottomMHYoff.Y = 1.5
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftBottomMHYoff)
    middleleftsheet.set("A%d"%ir,'%-11.11s'%"D")
    D = blockShape.Edges[5].Curve.Location.x - minX
    middleleftsheet.set("B%d"%ir,'%10.6f'%(D/25.4))
    middleleftsheet.set("C%d"%ir,'%10.6f'%D)
    ir += 1

    doc.addObject('TechDraw::DrawViewSpreadsheet','MiddleLeftDimBlock')
    doc.MiddleLeftBlockDrillSheetPage.addView(doc.MiddleLeftDimBlock)
    doc.MiddleLeftDimBlock.Source = middleleftsheet
    doc.MiddleLeftDimBlock.TextSize = 8
    doc.MiddleLeftDimBlock.CellEnd = "C%d"%(ir-1) 
    doc.MiddleLeftDimBlock.recompute()
    doc.MiddleLeftDimBlock.X = 87
    doc.MiddleLeftDimBlock.Y = 130
    doc.MiddleLeftBlockDrillSheetPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.MiddleLeftBlockDrillSheetPage,"BananaPiM64Model_MiddleLeftBlockDrillSheet.pdf")


    # Right (Speaker)
    doc.addObject('TechDraw::DrawPage','MiddleRightBlockDrillSheetPage')
    doc.MiddleRightBlockDrillSheetPage.Template = doc.USLetterTemplate
    edt = doc.MiddleRightBlockDrillSheetPage.Template.EditableTexts
    edt['DrawingTitle2']= "Middle Right"
    edt['Scale'] = '.75'
    edt['Sheet'] = "Sheet 4 of 7"
    doc.MiddleRightBlockDrillSheetPage.Template.EditableTexts = edt
    doc.MiddleRightBlockDrillSheetPage.ViewObject.show()
    middlerightsheet = doc.addObject('Spreadsheet::Sheet','MiddleRightDimensionTable')
    middlerightsheet.set("A1",'%-11.11s'%"Dim")
    middlerightsheet.set("B1",'%10.10s'%"inch")
    middlerightsheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','MiddleRightView')
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightView)
    doc.MiddleRightView.Source = doc.M64Case_middle_rightblock
    doc.MiddleRightView.Direction=(0.0,0.0,-1.0)
    doc.MiddleRightView.Scale = .75
    #doc.MiddleRightView.Scale = 2
    doc.MiddleRightView.Rotation = 90
    doc.MiddleRightView.X = 140
    doc.MiddleRightView.Y = 180
    blockShape = doc.M64Case_middle_rightblock.Shape
    minX = 999999999
    minY = 999999999
    maxX = 0
    maxY = 0
    for v in blockShape.Vertexes:
       if v.X < minX:
           minX = v.X
       if v.X > maxX:
           maxX = v.X    
       if v.Y < minY:
           minY = v.Y
       if v.Y > maxY:
           maxY = v.Y
    height = maxX - minX
    length = maxY - minY
    #print ('*** MiddleRight: origin (%g,%g), length = %g, height = %g'%(minX,minY,length,height))    
    #i = 0
    #for e in blockShape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        #print('*** MiddleRight: Edges[%d].Curve is a %s'%(i,type(e.Curve)))
    #        circ = e.Curve
    #        print('*** MiddleRight: Edges[%d].Curve %g at (%g,%g)'%\
    #              (i,circ.Radius*2,circ.Location.x-minX,circ.Location.y-minY))
    #    i += 1

    # Vertex0 UR  minX,maxY
    # Vertex1 UL  minX,minY
    # Vertex2 LR  maxX,maxY
    # Vertex3 LL  maxX,minY

    doc.addObject('TechDraw::DrawViewDimension','MiddleRightLength')
    doc.MiddleRightLength.Type = 'DistanceX'
    doc.MiddleRightLength.References2D = [(doc.MiddleRightView,'Vertex0'),\
                                         (doc.MiddleRightView,'Vertex3')]
    doc.MiddleRightLength.FormatSpec='l'
    doc.MiddleRightLength.Arbitrary = True
    doc.MiddleRightLength.X = 0
    doc.MiddleRightLength.Y = -12
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightLength)
    middlerightsheet.set("A%d"%ir,'%-11.11s'%"l")
    middlerightsheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    middlerightsheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleRightHeight')
    doc.MiddleRightHeight.Type = 'DistanceY'
    doc.MiddleRightHeight.References2D = [(doc.MiddleRightView,'Vertex0'),\
                                         (doc.MiddleRightView,'Vertex3')]
    doc.MiddleRightHeight.FormatSpec='h'
    doc.MiddleRightHeight.Arbitrary = True
    doc.MiddleRightHeight.X = 105
    doc.MiddleRightHeight.Y = 0
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightHeight)
    middlerightsheet.set("A%d"%ir,'%-11.11s'%"h")
    middlerightsheet.set("B%d"%ir,'%10.6f'%(height/25.4))
    middlerightsheet.set("C%d"%ir,'%10.6f'%height)
    ir += 1

    # Edge4 / Vertex6 (right) [Speaker top] Edges[5]
    doc.addObject('TechDraw::DrawViewDimension','MiddleRightTopMHXoff')
    doc.MiddleRightTopMHXoff.Type = 'DistanceX'
    doc.MiddleRightTopMHXoff.References2D = [(doc.MiddleRightView,'Vertex6'),\
                                         (doc.MiddleRightView,'Vertex2')]
    doc.MiddleRightTopMHXoff.FormatSpec='A'
    doc.MiddleRightTopMHXoff.Arbitrary = True
    doc.MiddleRightTopMHXoff.X = 54
    doc.MiddleRightTopMHXoff.Y = -7
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightTopMHXoff)
    middlerightsheet.set("A%d"%ir,'%-11.11s'%"A")
    A = blockShape.Edges[4].Curve.Location.y - minY
    middlerightsheet.set("B%d"%ir,'%10.6f'%(A/25.4))
    middlerightsheet.set("C%d"%ir,'%10.6f'%A)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleRightTopMHYoff')
    doc.MiddleRightTopMHYoff.Type = 'DistanceY'
    doc.MiddleRightTopMHYoff.References2D = [(doc.MiddleRightView,'Vertex6'),\
                                         (doc.MiddleRightView,'Vertex0')]
    doc.MiddleRightTopMHYoff.FormatSpec='B'
    doc.MiddleRightTopMHYoff.Arbitrary = True
    doc.MiddleRightTopMHYoff.X = 42
    doc.MiddleRightTopMHYoff.Y = 12
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightTopMHYoff)
    middlerightsheet.set("A%d"%ir,'%-11.11s'%"B")
    B = blockShape.Edges[4].Curve.Location.x - minX
    middlerightsheet.set("B%d"%ir,'%10.6f'%(B/25.4))
    middlerightsheet.set("C%d"%ir,'%10.6f'%B)
    ir += 1
    
    # Edge5 / Vertex9 (left) [Speaker bottom] Edges[4]
    doc.addObject('TechDraw::DrawViewDimension','MiddleRightBottomMHXoff')
    doc.MiddleRightBottomMHXoff.Type = 'DistanceX'
    doc.MiddleRightBottomMHXoff.References2D = [(doc.MiddleRightView,'Vertex9'),\
                                         (doc.MiddleRightView,'Vertex3')]
    doc.MiddleRightBottomMHXoff.FormatSpec='C'
    doc.MiddleRightBottomMHXoff.Arbitrary = True
    doc.MiddleRightBottomMHXoff.X = -63
    doc.MiddleRightBottomMHXoff.Y = -7
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightBottomMHXoff)
    middlerightsheet.set("A%d"%ir,'%-11.11s'%"C")
    C = maxY - blockShape.Edges[5].Curve.Location.y
    middlerightsheet.set("B%d"%ir,'%10.6f'%(C/25.4))
    middlerightsheet.set("C%d"%ir,'%10.6f'%C)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','MiddleRightBottomMHYoff')
    doc.MiddleRightBottomMHYoff.Type = 'DistanceY'
    doc.MiddleRightBottomMHYoff.References2D = [(doc.MiddleRightView,'Vertex9'),\
                                         (doc.MiddleRightView,'Vertex1')]
    doc.MiddleRightBottomMHYoff.FormatSpec='D'
    doc.MiddleRightBottomMHYoff.Arbitrary = True
    doc.MiddleRightBottomMHYoff.X = -50
    doc.MiddleRightBottomMHYoff.Y = 1.5
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightBottomMHYoff)
    middlerightsheet.set("A%d"%ir,'%-11.11s'%"D")
    D = blockShape.Edges[5].Curve.Location.x - minX
    middlerightsheet.set("B%d"%ir,'%10.6f'%(D/25.4))
    middlerightsheet.set("C%d"%ir,'%10.6f'%D)
    ir += 1

    doc.addObject('TechDraw::DrawViewDimension','MiddleRightSpeakerMHDia')
    doc.MiddleRightSpeakerMHDia.Type = 'Diameter'
    doc.MiddleRightSpeakerMHDia.References2D = [(doc.MiddleRightView,'Edge5')]
    doc.MiddleRightSpeakerMHDia.FormatSpec='EDia (2x)'
    doc.MiddleRightSpeakerMHDia.Arbitrary = True
    doc.MiddleRightSpeakerMHDia.X = -60
    doc.MiddleRightSpeakerMHDia.Y = 13
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightSpeakerMHDia)
    middlerightsheet.set("A%d"%ir,'%-11.11s'%"EDia")
    middlerightsheet.set("B%d"%ir,'%10.6f'%(Speaker_._MHoleDia/25.4))
    middlerightsheet.set("C%d"%ir,'%10.6f'%Speaker_._MHoleDia)
    ir += 1


    doc.addObject('TechDraw::DrawViewSpreadsheet','MiddleRightDimBlock')
    doc.MiddleRightBlockDrillSheetPage.addView(doc.MiddleRightDimBlock)
    doc.MiddleRightDimBlock.Source = middlerightsheet
    doc.MiddleRightDimBlock.TextSize = 8
    doc.MiddleRightDimBlock.CellEnd = "C%d"%(ir-1) 
    doc.MiddleRightDimBlock.recompute()
    doc.MiddleRightDimBlock.X = 82
    doc.MiddleRightDimBlock.Y = 120
    doc.MiddleRightBlockDrillSheetPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.MiddleRightBlockDrillSheetPage,"BananaPiM64Model_MiddleRightBlockDrillSheet.pdf")

    #*****
    # Keyboard shelf hinge block -- hinge mounting holes
    doc.addObject('TechDraw::DrawPage','KeyboardHingeBlockDrillSheetPage')
    doc.KeyboardHingeBlockDrillSheetPage.Template = doc.USLetterTemplate
    edt = doc.KeyboardHingeBlockDrillSheetPage.Template.EditableTexts
    edt['DrawingTitle2']= "Keyboard Hinge"
    edt['Scale'] = '.5'
    edt['Sheet'] = "Sheet 5 of 7"
    doc.KeyboardHingeBlockDrillSheetPage.Template.EditableTexts = edt
    doc.KeyboardHingeBlockDrillSheetPage.ViewObject.show()
    keyboardhingesheet = doc.addObject('Spreadsheet::Sheet','KeyboardHingeDimensionTable')
    keyboardhingesheet.set("A1",'%-11.11s'%"Dim")
    keyboardhingesheet.set("B1",'%10.10s'%"inch")
    keyboardhingesheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','KeyboardHingeView')
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeView)
    doc.KeyboardHingeView.Source = doc.M64Case_keyboardshelf_hingeblock
    doc.KeyboardHingeView.Direction=(0.0,1.0,0.0)
    doc.KeyboardHingeView.Scale = .5
    doc.KeyboardHingeView.X = 140
    doc.KeyboardHingeView.Y = 180
    
    blockShape = doc.M64Case_keyboardshelf_hingeblock.Shape
    minX = 999999999
    minZ = 999999999
    maxX = 0
    maxZ = 0
    for v in blockShape.Vertexes:
       if v.X < minX:
           minX = v.X
       if v.X > maxX:
           maxX = v.X    
       if v.Z < minZ:
           minZ = v.Z
       if v.Z > maxZ:
           maxZ = v.Z
    length = maxX - minX
    height = maxZ - minZ
    #print ('*** KeyboardHinge: origin (%g,%g), length = %g, height = %g'%(minX,minZ,length,height))    
    #i = 0
    #for e in blockShape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        #print('*** KeyboardHinge: Edges[%d].Curve is a %s'%(i,type(e.Curve)))
    #        circ = e.Curve
    #        print('*** KeyboardHinge: Edges[%d].Curve %g at (%g,%g)'%\
    #              (i,circ.Radius*2,circ.Location.x,circ.Location.z))
    #    i += 1

    holediameter = blockShape.Edges[11].Curve.Radius*2
    holezoff = blockShape.Edges[11].Curve.Location.z-minZ
    holez1off = height-holezoff
    #print ('*** TopBack: holezoff=%g,holez1off=%g'%(holezoff,holez1off))
    holeoff1 = blockShape.Edges[11].Curve.Location.x-minX
    holeoff2 = blockShape.Edges[12].Curve.Location.x-minX
    holeoff3 = blockShape.Edges[7].Curve.Location.x-minX
    holeoff4 = blockShape.Edges[8].Curve.Location.x-minX
    holeoff5 = blockShape.Edges[10].Curve.Location.x-minX
    holeoff6 = blockShape.Edges[9].Curve.Location.x-minX

    # Edge6 (for Diameter)
    doc.addObject('TechDraw::DrawViewDimension','KeyboardHingeHDia')
    doc.KeyboardHingeHDia.Type = 'Diameter'
    doc.KeyboardHingeHDia.References2D=[(doc.KeyboardHingeView,'Edge6')]
    doc.KeyboardHingeHDia.FormatSpec='HDia (6x)'
    doc.KeyboardHingeHDia.Arbitrary = True
    doc.KeyboardHingeHDia.X = -30
    doc.KeyboardHingeHDia.Y = 10
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeHDia)
    keyboardhingesheet.set("A%d"%ir,'%-11.11s'%"HDia")
    keyboardhingesheet.set("B%d"%ir,'%10.6f'%(holediameter/25.4))
    keyboardhingesheet.set("C%d"%ir,'%10.6f'%holediameter)
    ir += 1

    # Vertex0 LR (minY,maxX)
    # Vertex1 LL (minY,minX)
    # Vertex2 UR (maxY,maxX)
    # Vertex3 UL (maxY,minX)
    doc.addObject('TechDraw::DrawViewDimension','KeyboardHingeLength')
    doc.KeyboardHingeLength.Type = 'DistanceX'
    doc.KeyboardHingeLength.References2D=[(doc.KeyboardHingeView,'Vertex1'),\
                                    (doc.KeyboardHingeView,'Vertex2')]
    doc.KeyboardHingeLength.FormatSpec='l'
    doc.KeyboardHingeLength.Arbitrary = True
    doc.KeyboardHingeLength.X = 0
    doc.KeyboardHingeLength.Y = -5
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeLength)
    keyboardhingesheet.set("A%d"%ir,'%-11.11s'%"l")
    keyboardhingesheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    keyboardhingesheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','KeyboardHingeHeight')
    doc.KeyboardHingeHeight.Type = 'DistanceY'
    doc.KeyboardHingeHeight.References2D=[(doc.KeyboardHingeView,'Vertex1'),\
                                    (doc.KeyboardHingeView,'Vertex2')]
    doc.KeyboardHingeHeight.FormatSpec='h'
    doc.KeyboardHingeHeight.Arbitrary = True
    doc.KeyboardHingeHeight.X =105
    doc.KeyboardHingeLength.Y =-11 
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeHeight)
    keyboardhingesheet.set("A%d"%ir,'%-11.11s'%"h")
    keyboardhingesheet.set("B%d"%ir,'%10.6f'%(height/25.4))
    keyboardhingesheet.set("C%d"%ir,'%10.6f'%height)
    ir += 1

    # Vertex12 hole1 (leftmost)  Edges[11]
    doc.addObject('TechDraw::DrawViewDimension','KeyboardHingeHoleZ')
    doc.KeyboardHingeHoleZ.Type = 'DistanceY'
    doc.KeyboardHingeHoleZ.References2D=[(doc.KeyboardHingeView,'Vertex1'),\
                                   (doc.KeyboardHingeView,'Vertex12')]
    doc.KeyboardHingeHoleZ.FormatSpec='z'
    doc.KeyboardHingeHoleZ.Arbitrary = True
    doc.KeyboardHingeHoleZ.X = -105
    doc.KeyboardHingeHoleZ.Y = -5
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeHoleZ)
    keyboardhingesheet.set("A%d"%ir,'%-11.11s'%"z")
    keyboardhingesheet.set("B%d"%ir,'%10.6f'%(holezoff/25.4))
    keyboardhingesheet.set("C%d"%ir,'%10.6f'%holezoff)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','KeyboardHingeHole1')
    doc.KeyboardHingeHole1.Type = 'DistanceX'
    doc.KeyboardHingeHole1.References2D=[(doc.KeyboardHingeView,'Vertex1'),\
                                   (doc.KeyboardHingeView,'Vertex12')]
    doc.KeyboardHingeHole1.FormatSpec='a'
    doc.KeyboardHingeHole1.Arbitrary = True
    doc.KeyboardHingeHole1.X = -80
    doc.KeyboardHingeHole1.Y = -6
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeHole1)
    keyboardhingesheet.set("A%d"%ir,'%-11.11s'%"a")
    keyboardhingesheet.set("B%d"%ir,'%10.6f'%(holeoff1/25.4))
    keyboardhingesheet.set("C%d"%ir,'%10.6f'%holeoff1)
    ir += 1
    # Vertex15 hole2             Edges[12]
    doc.addObject('TechDraw::DrawViewDimension','KeyboardHingeHolePitch')
    doc.KeyboardHingeHolePitch.Type = 'DistanceX'
    doc.KeyboardHingeHolePitch.References2D=[(doc.KeyboardHingeView,'Vertex12'),\
                                       (doc.KeyboardHingeView,'Vertex15')]
    doc.KeyboardHingeHolePitch.FormatSpec='p (5x)'
    doc.KeyboardHingeHolePitch.Arbitrary = True
    doc.KeyboardHingeHolePitch.X = -50
    doc.KeyboardHingeHolePitch.Y = -6
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeHolePitch)
    keyboardhingesheet.set("A%d"%ir,'%-11.11s'%"p")
    keyboardhingesheet.set("B%d"%ir,'%10.6f'%((holeoff2-holeoff1)/25.4))
    keyboardhingesheet.set("C%d"%ir,'%10.6f'%(holeoff2-holeoff1))
    ir += 1
    # Vertex9  hole3             Edges[7]
    # Vertex6  hole4             Edges[8]
    # Vertex21 hole5             Edges[10]
    # Vertex18 hole6 (rightmost) Edges[9]
    
    


    doc.addObject('TechDraw::DrawViewSpreadsheet','KeyboardHingeDimBlock')
    doc.KeyboardHingeBlockDrillSheetPage.addView(doc.KeyboardHingeDimBlock)
    doc.KeyboardHingeDimBlock.Source = keyboardhingesheet
    doc.KeyboardHingeDimBlock.TextSize = 8
    doc.KeyboardHingeDimBlock.CellEnd = "C%d"%(ir-1) 
    doc.KeyboardHingeDimBlock.recompute()
    doc.KeyboardHingeDimBlock.X = 82
    doc.KeyboardHingeDimBlock.Y = 120
    doc.KeyboardHingeBlockDrillSheetPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.KeyboardHingeBlockDrillSheetPage,"BananaPiM64Model_KeyboardHingeBlockDrillSheet.pdf")

    #*****
    # Battery cover mounting holes:
    # in frontblock and batteryblock2:
    # doc.M64Case_bottom_frontblock
    # doc.M64Case_bottom_batteryblock2
    #
    doc.addObject('TechDraw::DrawPage','BottomFrontBlockDrillSheetPage')
    doc.BottomFrontBlockDrillSheetPage.Template = doc.USLetterTemplate
    edt = doc.BottomFrontBlockDrillSheetPage.Template.EditableTexts
    edt['DrawingTitle2']= "Bottom Front Block"
    edt['Scale'] = '.5'
    edt['Sheet'] = "Sheet 6 of 7"
    doc.BottomFrontBlockDrillSheetPage.Template.EditableTexts = edt
    doc.BottomFrontBlockDrillSheetPage.ViewObject.show()
    frontblocksheet = doc.addObject('Spreadsheet::Sheet','BottomFrontDimensionTable')
    frontblocksheet.set("A1",'%-11.11s'%"Dim")
    frontblocksheet.set("B1",'%10.10s'%"inch")
    frontblocksheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','BottomFrontView')
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontView)
    doc.BottomFrontView.Source = doc.M64Case_bottom_frontblock
    doc.BottomFrontView.Direction=(0.0,0.0,1.0)
    doc.BottomFrontView.Scale = .5
    doc.BottomFrontView.X = 140
    doc.BottomFrontView.Y = 180
    
    blockShape = doc.M64Case_bottom_frontblock.Shape
    minX = 999999999
    minY = 999999999
    maxX = 0
    maxY = 0
    for v in blockShape.Vertexes:
       if v.X < minX:
           minX = v.X
       if v.X > maxX:
           maxX = v.X    
       if v.Y < minY:
           minY = v.Y
       if v.Y > maxY:
           maxY = v.Y
    length = maxX - minX
    height = maxY - minY
    #print ('*** BottomFront: origin (%g,%g), length = %g, height = %g'%(minX,minY,length,height))    
    #i = 0
    #for e in blockShape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        #print('*** BottomFront: Edges[%d].Curve is a %s'%(i,type(e.Curve)))
    #        circ = e.Curve
    #        print('*** BottomFront: Edges[%d].Curve %g at (%g,%g)'%\
    #              (i,circ.Radius*2,circ.Location.x,circ.Location.y))
    #    i += 1

    # Vertex0 UL minX,maxY
    # Vertex1 UR maxX,maxY
    # Vertex2 LL minX,minY
    # Vertex3 LR maxX,minY
    doc.addObject('TechDraw::DrawViewDimension','BottomFrontLength')
    doc.BottomFrontLength.Type = 'DistanceX'
    doc.BottomFrontLength.References2D=[(doc.BottomFrontView,'Vertex1'),\
                                    (doc.BottomFrontView,'Vertex2')]
    doc.BottomFrontLength.FormatSpec='l'
    doc.BottomFrontLength.Arbitrary = True
    doc.BottomFrontLength.X = 0
    doc.BottomFrontLength.Y = -5
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontLength)
    frontblocksheet.set("A%d"%ir,'%-11.11s'%"l")
    frontblocksheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    frontblocksheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BottomFrontHeight')
    doc.BottomFrontHeight.Type = 'DistanceY'
    doc.BottomFrontHeight.References2D=[(doc.BottomFrontView,'Vertex1'),\
                                    (doc.BottomFrontView,'Vertex2')]
    doc.BottomFrontHeight.FormatSpec='h'
    doc.BottomFrontHeight.Arbitrary = True
    doc.BottomFrontHeight.X =105
    doc.BottomFrontLength.Y =-11 
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontHeight)
    frontblocksheet.set("A%d"%ir,'%-11.11s'%"h")
    frontblocksheet.set("B%d"%ir,'%10.6f'%(height/25.4))
    frontblocksheet.set("C%d"%ir,'%10.6f'%height)
    ir += 1
    
    # Edge4   For diameter
    doc.addObject('TechDraw::DrawViewDimension','BottomFrontHDia')
    doc.BottomFrontHDia.Type = 'Diameter'
    doc.BottomFrontHDia.References2D=[(doc.BottomFrontView,'Edge4')]
    doc.BottomFrontHDia.FormatSpec='HDia (2x)'
    doc.BottomFrontHDia.Arbitrary = True
    doc.BottomFrontHDia.X = 20
    doc.BottomFrontHDia.Y = 12
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontHDia)
    holediameter = blockShape.Edges[4].Curve.Radius*2
    frontblocksheet.set("A%d"%ir,'%-11.11s'%"HDia")
    frontblocksheet.set("B%d"%ir,'%10.6f'%(holediameter/25.4))
    frontblocksheet.set("C%d"%ir,'%10.6f'%holediameter)
    ir += 1
    
    # Vertex6 left hole Edges[4]
    doc.addObject('TechDraw::DrawViewDimension','BottomFrontHoleY')
    doc.BottomFrontHoleY.Type = 'DistanceY'
    doc.BottomFrontHoleY.References2D=[(doc.BottomFrontView,'Vertex2'),\
                                   (doc.BottomFrontView,'Vertex6')]
    doc.BottomFrontHoleY.FormatSpec='y'
    doc.BottomFrontHoleY.Arbitrary = True
    doc.BottomFrontHoleY.X = 50
    doc.BottomFrontHoleY.Y = 12
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontHoleY)
    holeyoff = blockShape.Edges[4].Curve.Location.y - minY
    frontblocksheet.set("A%d"%ir,'%-11.11s'%"y")
    frontblocksheet.set("B%d"%ir,'%10.6f'%(holeyoff/25.4))
    frontblocksheet.set("C%d"%ir,'%10.6f'%holeyoff)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','BottomFrontHoleLeft')
    doc.BottomFrontHoleLeft.Type = 'DistanceX'
    doc.BottomFrontHoleLeft.References2D=[(doc.BottomFrontView,'Vertex2'),\
                                   (doc.BottomFrontView,'Vertex6')]
    doc.BottomFrontHoleLeft.FormatSpec='a'
    doc.BottomFrontHoleLeft.Arbitrary = True
    doc.BottomFrontHoleLeft.X = -80
    doc.BottomFrontHoleLeft.Y = -6
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontHoleLeft)
    holeoff = blockShape.Edges[4].Curve.Location.x - minX
    frontblocksheet.set("A%d"%ir,'%-11.11s'%"a")
    frontblocksheet.set("B%d"%ir,'%10.6f'%(holeoff/25.4))
    frontblocksheet.set("C%d"%ir,'%10.6f'%holeoff)
    ir += 1

    # Vertex9 (right) Edges[5]
    doc.addObject('TechDraw::DrawViewDimension','BottomFrontHoleSpacing')
    doc.BottomFrontHoleSpacing.Type = 'DistanceX'
    doc.BottomFrontHoleSpacing.References2D=[(doc.BottomFrontView,'Vertex6'),\
                                       (doc.BottomFrontView,'Vertex9')]
    doc.BottomFrontHoleSpacing.FormatSpec='s'
    doc.BottomFrontHoleSpacing.Arbitrary = True
    doc.BottomFrontHoleSpacing.X = 60
    doc.BottomFrontHoleSpacing.Y = -6
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontHoleSpacing)
    holespacing = blockShape.Edges[5].Curve.Location.x - \
                  blockShape.Edges[4].Curve.Location.x
    frontblocksheet.set("A%d"%ir,'%-11.11s'%"s")
    frontblocksheet.set("B%d"%ir,'%10.6f'%(holespacing/25.4))
    frontblocksheet.set("C%d"%ir,'%10.6f'%holespacing)
    ir += 1
    

    doc.addObject('TechDraw::DrawViewSpreadsheet','BottomFrontDimBlock')
    doc.BottomFrontBlockDrillSheetPage.addView(doc.BottomFrontDimBlock)
    doc.BottomFrontDimBlock.Source = frontblocksheet
    doc.BottomFrontDimBlock.TextSize = 8
    doc.BottomFrontDimBlock.CellEnd = "C%d"%(ir-1) 
    doc.BottomFrontDimBlock.recompute()
    doc.BottomFrontDimBlock.X = 82
    doc.BottomFrontDimBlock.Y = 140
    doc.BottomFrontBlockDrillSheetPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.BottomFrontBlockDrillSheetPage,"BananaPiM64Model_BottomFrontBlockDrillSheet.pdf")


    doc.addObject('TechDraw::DrawPage','Battery2BlockDrillSheetPage')
    doc.Battery2BlockDrillSheetPage.Template = doc.USLetterTemplate
    edt = doc.Battery2BlockDrillSheetPage.Template.EditableTexts
    edt['DrawingTitle2']= "Battery Block 2"
    edt['Scale'] = '1:1'
    edt['Sheet'] = "Sheet 7 of 7"
    doc.Battery2BlockDrillSheetPage.Template.EditableTexts = edt
    doc.Battery2BlockDrillSheetPage.ViewObject.show()
    batteryblock2sheet = doc.addObject('Spreadsheet::Sheet','Battery2DimensionTable')
    batteryblock2sheet.set("A1",'%-11.11s'%"Dim")
    batteryblock2sheet.set("B1",'%10.10s'%"inch")
    batteryblock2sheet.set("C1",'%10.10s'%"mm")
    ir = 2
    doc.addObject('TechDraw::DrawViewPart','Battery2View')
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2View)
    doc.Battery2View.Source = doc.M64Case_bottom_batteryblock2
    doc.Battery2View.Direction=(0.0,0.0,1.0)
    doc.Battery2View.Scale = 1
    doc.Battery2View.X = 140
    doc.Battery2View.Y = 180
    
    blockShape = doc.M64Case_bottom_batteryblock2.Shape
    minX = 999999999
    minY = 999999999
    maxX = 0
    maxY = 0
    for v in blockShape.Vertexes:
       if v.X < minX:
           minX = v.X
       if v.X > maxX:
           maxX = v.X    
       if v.Y < minY:
           minY = v.Y
       if v.Y > maxY:
           maxY = v.Y
    length = maxX - minX
    height = maxY - minY
    #print ('*** Battery2: origin (%g,%g), length = %g, height = %g'%(minX,minY,length,height))    
    #i = 0
    #for e in blockShape.Edges:
    #    if isinstance(e.Curve,Part.Circle):
    #        #print('*** Battery2: Edges[%d].Curve is a %s'%(i,type(e.Curve)))
    #        circ = e.Curve
    #        print('*** Battery2: Edges[%d].Curve %g at (%g,%g)'%\
    #              (i,circ.Radius*2,circ.Location.x,circ.Location.y))
    #    i += 1
    
    # Vertex0 UL minX,maxY
    # Vertex1 UR maxX,maxY
    # Vertex2 LL minX,minY
    # Vertex3 LR maxX,minY
    doc.addObject('TechDraw::DrawViewDimension','Battery2Length')
    doc.Battery2Length.Type = 'DistanceX'
    doc.Battery2Length.References2D=[(doc.Battery2View,'Vertex1'),\
                                    (doc.Battery2View,'Vertex2')]
    doc.Battery2Length.FormatSpec='l'
    doc.Battery2Length.Arbitrary = True
    doc.Battery2Length.X = 0
    doc.Battery2Length.Y = -5
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2Length)
    batteryblock2sheet.set("A%d"%ir,'%-11.11s'%"l")
    batteryblock2sheet.set("B%d"%ir,'%10.6f'%(length/25.4))
    batteryblock2sheet.set("C%d"%ir,'%10.6f'%length)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Battery2Height')
    doc.Battery2Height.Type = 'DistanceY'
    doc.Battery2Height.References2D=[(doc.Battery2View,'Vertex1'),\
                                    (doc.Battery2View,'Vertex2')]
    doc.Battery2Height.FormatSpec='h'
    doc.Battery2Height.Arbitrary = True
    doc.Battery2Height.X =105
    doc.Battery2Length.Y =-11 
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2Height)
    batteryblock2sheet.set("A%d"%ir,'%-11.11s'%"h")
    batteryblock2sheet.set("B%d"%ir,'%10.6f'%(height/25.4))
    batteryblock2sheet.set("C%d"%ir,'%10.6f'%height)
    ir += 1
    # Edge4   For diameter
    doc.addObject('TechDraw::DrawViewDimension','Battery2HDia')
    doc.Battery2HDia.Type = 'Diameter'
    doc.Battery2HDia.References2D=[(doc.Battery2View,'Edge4')]
    doc.Battery2HDia.FormatSpec='HDia (2x)'
    doc.Battery2HDia.Arbitrary = True
    doc.Battery2HDia.X = -5
    doc.Battery2HDia.Y = 15
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2HDia)
    holediameter = blockShape.Edges[4].Curve.Radius*2
    batteryblock2sheet.set("A%d"%ir,'%-11.11s'%"HDia")
    batteryblock2sheet.set("B%d"%ir,'%10.6f'%(holediameter/25.4))
    batteryblock2sheet.set("C%d"%ir,'%10.6f'%holediameter)
    ir += 1
        # Vertex6 left hole Edges[4]
    doc.addObject('TechDraw::DrawViewDimension','Battery2HoleY')
    doc.Battery2HoleY.Type = 'DistanceY'
    doc.Battery2HoleY.References2D=[(doc.Battery2View,'Vertex2'),\
                                   (doc.Battery2View,'Vertex6')]
    doc.Battery2HoleY.FormatSpec='y'
    doc.Battery2HoleY.Arbitrary = True
    doc.Battery2HoleY.X = -45
    doc.Battery2HoleY.Y = 12
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2HoleY)
    holeyoff = blockShape.Edges[4].Curve.Location.y - minY
    batteryblock2sheet.set("A%d"%ir,'%-11.11s'%"y")
    batteryblock2sheet.set("B%d"%ir,'%10.6f'%(holeyoff/25.4))
    batteryblock2sheet.set("C%d"%ir,'%10.6f'%holeyoff)
    ir += 1
    doc.addObject('TechDraw::DrawViewDimension','Battery2HoleLeft')
    doc.Battery2HoleLeft.Type = 'DistanceX'
    doc.Battery2HoleLeft.References2D=[(doc.Battery2View,'Vertex2'),\
                                   (doc.Battery2View,'Vertex6')]
    doc.Battery2HoleLeft.FormatSpec='a'
    doc.Battery2HoleLeft.Arbitrary = True
    doc.Battery2HoleLeft.X = -45
    doc.Battery2HoleLeft.Y = -8
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2HoleLeft)
    holeoff = blockShape.Edges[4].Curve.Location.x - minX
    batteryblock2sheet.set("A%d"%ir,'%-11.11s'%"a")
    batteryblock2sheet.set("B%d"%ir,'%10.6f'%(holeoff/25.4))
    batteryblock2sheet.set("C%d"%ir,'%10.6f'%holeoff)
    ir += 1

    # Vertex9 (right) Edges[5]
    doc.addObject('TechDraw::DrawViewDimension','Battery2HoleSpacing')
    doc.Battery2HoleSpacing.Type = 'DistanceX'
    doc.Battery2HoleSpacing.References2D=[(doc.Battery2View,'Vertex6'),\
                                       (doc.Battery2View,'Vertex9')]
    doc.Battery2HoleSpacing.FormatSpec='s'
    doc.Battery2HoleSpacing.Arbitrary = True
    doc.Battery2HoleSpacing.X =  0
    doc.Battery2HoleSpacing.Y = -8
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2HoleSpacing)
    holespacing = blockShape.Edges[5].Curve.Location.x - \
                  blockShape.Edges[4].Curve.Location.x
    batteryblock2sheet.set("A%d"%ir,'%-11.11s'%"s")
    batteryblock2sheet.set("B%d"%ir,'%10.6f'%(holespacing/25.4))
    batteryblock2sheet.set("C%d"%ir,'%10.6f'%holespacing)
    ir += 1

    doc.addObject('TechDraw::DrawViewSpreadsheet','Battery2DimBlock')
    doc.Battery2BlockDrillSheetPage.addView(doc.Battery2DimBlock)
    doc.Battery2DimBlock.Source = batteryblock2sheet
    doc.Battery2DimBlock.TextSize = 8
    doc.Battery2DimBlock.CellEnd = "C%d"%(ir-1) 
    doc.Battery2DimBlock.recompute()
    doc.Battery2DimBlock.X = 110
    doc.Battery2DimBlock.Y = 140
    doc.Battery2BlockDrillSheetPage.recompute()
    doc.recompute()
    TechDrawGui.exportPageAsPdf(doc.Battery2BlockDrillSheetPage,"BananaPiM64Model_Battery2BlockDrillSheet.pdf")
    sys.exit(0)
