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
#  Last Modified : <200605.1349>
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
    _BottomDepth = 2.25 * 25.4
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
    def __init__(self,name,origin,backhinge=None,keyboardhinge=None):
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
        hdorig = self.panel.corner.add(Base.Vector(12.7 + HDMIConverterDims._mainboardWidth + 6.35,
                                                   self.panel.pheight-(12.7+Disk25_2H._Length),
                                                   self.panel.PanelThickness()))
        self.harddisk = Disk25_2H(name+":harddisk",hdorig)
        self.panel.cutfrom(self.harddisk.MountingHole(1,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.harddisk.MountingHole(2,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.harddisk.MountingHole(3,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.harddisk.MountingHole(4,self.panel.corner.z,self.WallThickness()))
        usbsataadaptordelta = Base.Vector(12.7 + 50.8,
                                          self.panel.pheight-(12.7+Disk25_2H._Length + 12.7),
                                          self.panel.PanelThickness()+2.54)
        usbsataadaptororig = self.panel.corner.add(usbsataadaptordelta)
        self.usbsataadaptor = USB_SATA_Adapter_Horiz(name+":usbsataadaptor",
                                                     usbsataadaptororig)
        cradleorig = usbsataadaptororig.add(Base.Vector(self.usbsataadaptor._USBPlug_XOff+1,
                                                        3.5,-2.54))
        self.usbsataadaptorcradle = USB_SATA_Adapter_BoardCradleHoriz(name+":cradle",cradleorig)
        self.panel.cutfrom(self.usbsataadaptorcradle.MountingHole(1,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.usbsataadaptorcradle.MountingHole(2,self.panel.corner.z,self.WallThickness()))
        self.panel.cutfrom(self.usbsataadaptorcradle.MountingHole(3,self.panel.corner.z,self.WallThickness()))
        otgadaptor_dx = ((M64Board._OTG_Width - OTGAdaptor._MicroB_Width)/2.0) - OTGAdaptor._MicroB_XOff
        otgadaptor_dy = OTGAdaptor._MicroB_Length
        otgadaptor_dz = ((M64Board._OTG_Thick - OTGAdaptor._MicroB_Thick)/2.0) - OTGAdaptor._MicroB_ZOff
        otgadaptor_delta = Base.Vector(otgadaptor_dx,otgadaptor_dy,otgadaptor_dz)
        otgadaptororig = self.m64.otg_origin.add(otgadaptor_delta)
        self.otgadaptor = OTGAdaptor(name+":otgadapter",otgadaptororig)
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
        borig = self.panel.corner.add(Base.Vector(self.panel.pwidth-Battery._Length-BlockY._BlockWidth,
                                       BlockX._BlockWidth,self.panel.PanelThickness()))
        self.battery = Battery(name+":battery",borig)
        usbo_x = 12.7+HDMIConverterDims._mainboardWidth+6.35
        usbo_x += Disk25_2H._Width+6.35
        usbo_y = self.panel.pheight - USBHub_._Length
        usbo_z = self.panel.PanelThickness()
        usbhorg = self.panel.corner.add(Base.Vector(usbo_x,usbo_y,usbo_z))
        self.usbhub = USBHub270(name+":usbhub",usbhorg)
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
        if keyboardhinge != None:
            for i in range(1,7):
                self.front.cutfrom(keyboardhinge.MountingHole(1,i,self.front.corner.y,self.front.PanelThickness()))
        self.back = PortableM64CaseBackPanel(name+":back",origin,
                                              self.BottomDepth())
        self.back.cutfrom(self.psbox.InletFlangeCutout(self.back.corner.y,self.back.PanelThickness()))
        if backhinge != None:
            for i in range(1,7):
                self.back.cutfrom(backhinge.MountingHole(1,i,self.back.corner.y,self.back.PanelThickness()))
        blocko = self.panel.corner.add(Base.Vector(0,0,
                                                 self.panel.PanelThickness()))
        blockl = self.panel.pwidth
        self.frontblock = BlockX(name+":frontblock",blocko,length=blockl)
        blocko = self.panel.corner.add(Base.Vector(0,self.panel.pheight-BlockX._BlockWidth,self.panel.PanelThickness()))
        self.backblock = BlockX(name+":backblock",blocko,length=usbo_x)
        blocko = self.panel.corner.add(Base.Vector(0,
                                           M64Board._m64YOff+M64Board._m64YMax,
                                           self.panel.PanelThickness()))
        blockl = self.panel.pheight-(M64Board._m64YOff+M64Board._m64YMax+BlockY._BlockWidth)
        self.leftblock = BlockY(name+":leftblock",blocko,length=blockl) 
        blocko = self.panel.corner.add(Base.Vector(
                                          self.panel.pwidth-BlockY._BlockWidth,
                                          BlockY._BlockWidth,
                                          self.panel.PanelThickness()))
        self.rightblock = BlockY(name+":rightblock",blocko,
                                 length=self.panel.pheight-BlockY._BlockWidth-PSBox._baselength)
        blocko = self.panel.corner.add(Base.Vector(0,0,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        blockl = self._ShelfHeight-(self.panel.PanelThickness()+BlockZa._BlockThick)
        self.leftfrontcorner = BlockZa(name+":leftfrontcorner",blocko,
                                       length=blockl)
        blocko = self.panel.corner.add(Base.Vector(self.panel.pwidth-BlockY._BlockThick,0,self.panel.PanelThickness()+Battery._Height))
        blockl = self._ShelfHeight-(self.panel.PanelThickness()+BlockZa._BlockWidth)
        self.rightfrontcorner = BlockZa(name+":rightfrontcorner",blocko,
                                       length=blockl)
        blocko = self.panel.corner.add(Base.Vector(0,
                              self.panel.pheight-BlockZa._BlockWidth,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        blockl = self._BottomDepth-(self.panel.PanelThickness()+BlockZa._BlockThick)
        self.leftbackcorner = BlockZa(name+":leftbackcorner",blocko,
                                      length=blockl)
        blocko = self.panel.corner.add(Base.Vector(
                              self.panel.pwidth-BlockZa._BlockThick,
                              self.panel.pheight-BlockZa._BlockWidth,
                              self.panel.PanelThickness()))
        blockl = self._BottomDepth-self.panel.PanelThickness()
        self.rightbackcorner=BlockZa(name+":rightbackcorner",blocko,
                                     length=blockl)
        blocko = self.panel.corner.add(Base.Vector(0,
                              self.ShelfLength()-BlockZa._BlockWidth,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        blockl = self._ShelfHeight-(self.panel.PanelThickness()+BlockZa._BlockThick)
        self.leftshelfsupport = BlockZa(name+":leftshelfsupport",blocko,
                                        length=blockl)
        blocko = self.panel.corner.add(Base.Vector(
                                         self.panel.pwidth-BlockZa._BlockThick,
                                         self.ShelfLength()-BlockZa._BlockWidth,
                              self.panel.PanelThickness()+BlockZa._BlockThick))
        self.rightshelfsupport = BlockZa(name+":rightshelfsupport",blocko,
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
    def __init__(self,name,origin,bottombackhinge=None,topbackhinge=None):
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
                                          cz - 6.35)
        
        self.hdmibuttonboard = HDMIButtonBoard_Upsidedown(name+":hdmibuttonboard",hdmibuttonboardorig)
        self.panel.cutfrom(self.hdmibuttonboard.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmibuttonboard.MountingHole(2,cz,self.panel.PanelThickness()))
        self.hdmibuttonboard_standoff1 = self.hdmibuttonboard.Standoff(1,cz,-6.35,6.35)
        self.hdmibuttonboard_standoff2 = self.hdmibuttonboard.Standoff(2,cz,-6.35,6.35)
        hdmihvpowerboardorig = Base.Vector((cx+panelWidth)-(12.7+HDMIConverterDims._hvpowerboardWidth),
                                           (cy+panelLength)-HDMIConverterDims._hvpowerboardHeight,
                                           cz - 6.35)
        self.hdmihvpowerboard = HDMIHVPowerBoard_Upsidedown(name+":hdmihvpowerboard",hdmihvpowerboardorig)
        self.panel.cutfrom(self.hdmihvpowerboard.MountingHole(1,cz,self.panel.PanelThickness()))
        self.panel.cutfrom(self.hdmihvpowerboard.MountingHole(2,cz,self.panel.PanelThickness()))
        self.hdmihvpowerboard_standoff1 = self.hdmihvpowerboard.Standoff(1,cz,-6.35,6.35)
        self.hdmihvpowerboard_standoff2 = self.hdmihvpowerboard.Standoff(2,cz,-6.35,6.35)
        leftspeakerorig = self.panel.corner.add(Base.Vector(0,(panelLength-Speaker_._Length)/2.0,-(6.35-Speaker_._StandoffRecessDepth)))
        self.leftspeaker = SpeakerLeft_UpsideDown(name+":leftspeaker",leftspeakerorig)
        self.panel.cutfrom(self.leftspeaker.MountingHole("top",self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.leftspeaker.MountingHole("bottom",self.panel.corner.z,self.panel.PanelThickness()))
        self.leftspeaker_standofftop = self.leftspeaker.Standoff("top",self.panel.corner.z,-6.35,6)
        self.leftspeaker_standoffbottom = self.leftspeaker.Standoff("bottom",self.panel.corner.z,-6.35,6)
        rightspeakerorig = self.panel.corner.add(Base.Vector(panelWidth-Speaker_._Width,(panelLength-Speaker_._Length)/2.0,-(6.35-Speaker_._StandoffRecessDepth)))
        self.rightspeaker = SpeakerRight_UpsideDown(name+":rightspeaker",rightspeakerorig)
        
        self.panel.cutfrom(self.rightspeaker.MountingHole("top",self.panel.corner.z,self.panel.PanelThickness()))
        self.panel.cutfrom(self.rightspeaker.MountingHole("bottom",self.panel.corner.z,self.panel.PanelThickness()))
        self.rightspeaker_standofftop = self.rightspeaker.Standoff("top",self.panel.corner.z,-6.35,6)
        self.rightspeaker_standoffbottom = self.rightspeaker.Standoff("bottom",self.panel.corner.z,-6.35,6)
        self.left  = PortableM64CaseLeftPanel(name+":left",morigin,
                                              self.MiddleTotalDepth())
        self.right = PortableM64CaseRightPanel(name+":right",morigin,
                                              self.MiddleTotalDepth())
        self.front = PortableM64CaseFrontPanel(name+":front",morigin,
                                              self.MiddleTotalDepth())
        self.back = PortableM64CaseBackPanel(name+":back",morigin,
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
        self.frontblock = BlockX(name+":frontblock",blocko,length=blockl)
        blocko =  pcorner.add(Base.Vector(0,h-BlockX._BlockWidth,pthick))
        self.backblock = BlockX(name+":backblock",blocko,length=blockl)
        self.backblock.cutfrom(self.hdmibuttonboard.MountingHole(1,pcorner.z+pthick,BlockX._BlockThick))
        self.backblock.cutfrom(self.hdmibuttonboard.MountingHole(2,pcorner.z+pthick,BlockX._BlockThick))
        self.backblock.cutfrom(self.hdmihvpowerboard.MountingHole(1,pcorner.z+pthick,BlockX._BlockThick))
        self.backblock.cutfrom(self.hdmihvpowerboard.MountingHole(2,pcorner.z+pthick,BlockX._BlockThick))
        blocko = pcorner.add(Base.Vector(0,BlockY._BlockWidth,pthick))
        blockl = h - (BlockY._BlockWidth*2)
        self.leftblock = BlockY(name+":leftblock",blocko,length=blockl)
        self.leftblock.cutfrom(self.leftspeaker.MountingHole("top",pcorner.z+pthick,BlockX._BlockThick))
        self.leftblock.cutfrom(self.leftspeaker.MountingHole("bottom",pcorner.z+pthick,BlockX._BlockThick))
        blocko = pcorner.add(Base.Vector(w-BlockY._BlockWidth,BlockY._BlockWidth,pthick))
        self.rightblock = BlockY(name+":rightblock",blocko,length=blockl)
        self.rightblock.cutfrom(self.rightspeaker.MountingHole("top",pcorner.z+pthick,BlockX._BlockThick))
        self.rightblock.cutfrom(self.rightspeaker.MountingHole("bottom",pcorner.z+pthick,BlockX._BlockThick))
        blocko = pcorner.add(Base.Vector(0,0,pthick+BlockZa._BlockThick))
        blockl = self._MiddleTotalDepth - (self._MiddleLowerDepth + pthick + BlockZa._BlockThick)
        self.leftfrontcorner = BlockZa(name+":leftfrontcorner",blocko,
                                       length=blockl)
        blocko = pcorner.add(Base.Vector(w-BlockZa._BlockThick,0,
                                         pthick+BlockZa._BlockThick))
        self.rightfrontcorner = BlockZa(name+":rightfrontcorner",blocko,
                                       length=blockl)
        blocko = pcorner.add(Base.Vector(0,h-BlockZa._BlockWidth,
                                         pthick+BlockZa._BlockThick))
        self.leftbackcorner = BlockZa(name+":rightbackcorner",blocko,
                                       length=blockl)
        blocko = pcorner.add(Base.Vector(w-BlockZa._BlockThick,
                                         h-BlockZa._BlockWidth,
                                         pthick+BlockZa._BlockThick))
        self.rightbackcorner = BlockZa(name+":leftbackcorner",blocko,
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
        Part.show(self.leftspeaker_standofftop)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':leftspeaker_standofftop'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.leftspeaker_standoffbottom)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':leftspeaker_standoffbottom'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.rightspeaker_standofftop)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':rightspeaker_standofftop'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.rightspeaker_standoffbottom)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':rightspeaker_standoffbottom'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        

class PortableM64CaseTop(PortableM64CaseCommon):
    def __init__(self,name,origin,hinge=None):
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
        corner = self.panel.corner
        panelWidth = self.panel.pwidth
        panelLength = self.panel.pheight
        panelThick = self.panel.PanelThickness()
        blocko = corner.add(Base.Vector(0,0,-BlockX._BlockThick))
        blockl = panelWidth
        self.frontblock = BlockX(name+":frontblock",blocko,length=blockl)
        blocko = corner.add(Base.Vector(0,panelLength-BlockX._BlockWidth,
                                        -BlockX._BlockThick))
        self.backblock = BlockX(name+":backblock",blocko,length=blockl)
        if hinge != None:
            for i in range(1,7):
                self.back.cutfrom(hinge.MountingHole(2,i,self.back.corner.y,self.back.PanelThickness()))
                self.backblock.cutfrom(hinge.MountingHole(2,i,blocko.y,BlockX._BlockWidth))
        blocko = corner.add(Base.Vector(0,BlockX._BlockWidth,
                                        -BlockX._BlockThick))
        blockl = panelLength - (2*BlockY._BlockWidth)
        self.leftblock = BlockY(name+":leftblock",blocko,length=blockl)
        blocko = corner.add(Base.Vector(panelWidth-BlockY._BlockWidth,
                                        BlockX._BlockWidth,
                                        -BlockX._BlockThick))
        self.rightblock = BlockY(name+":rightblock",blocko,length=blockl)
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
        self.hingeblock = BlockX(name+":hingeblock",
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
        self.teensythumbstick = TeensyThumbStick(name+":teensythumbstick",
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
        self.teensythumbstickcover = TeensyThumbStickCover(name+":teensythumbstickcover",
                                                       teensythumbstickcoverO)
    def show(self):
        self.hingeblock.show()
        self.teensythumbstick.show()
        self.teensythumbstickcover.show()
        doc = App.activeDocument()
        Part.show(self.shelf)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':shelf'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
        Part.show(self.teensythumbstick_standoff1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':teensythumbstick_standoff1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.teensythumbstick_standoff2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':teensythumbstick_standoff2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.teensythumbstick_standoff3)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':teensythumbstick_standoff3'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        Part.show(self.teensythumbstick_standoff4)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':teensythumbstick_standoff4'
        doc.Objects[last].ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
                        

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
          name+":keyboardshelfhinge",
          origin.add(Base.Vector(((self._Width - PianoHinge_._Length)/2.0),
                 self._WallThickness,self._BottomDepth-PianoHinge_._FoldHeight)))
        self.bottommiddlehinge = PianoHingeFlatOutsideBack(
          name+":bottommiddlehinge",
          origin.add(Base.Vector(
                   ((self._Width - PianoHinge_._Length)/2.0)-25.4,
                   self._Height,
                   self._BottomDepth - (PianoHinge_._FlangeWidth + PianoHinge_._PinOff + (PianoHinge_._PinDia / 2.0)))))
        self.middletophinge = PianoHingeFlatOutsideBack(
          name+":middletophinge",
          origin.add(Base.Vector(
              ((self._Width - PianoHinge_._Length)/2.0),
              self._Height,
              (self._BottomDepth+self._MiddleTotalDepth) - (PianoHinge_._FlangeWidth + PianoHinge_._PinOff + (PianoHinge_._PinDia / 2.0)))))
        self.bottom = PortableM64CaseBottom(name+":bottom",origin,
                                            backhinge=self.bottommiddlehinge,
                                            keyboardhinge=self.keyboardshelfhinge)
        self.middle = PortableM64CaseMiddle(name+":middle",origin,
                                       bottombackhinge=self.bottommiddlehinge,
                                       topbackhinge=self.middletophinge)
        self.top    = PortableM64CaseTop(name+":top",origin,
                                       hinge=self.middletophinge)
        self.keyboardshelf = PortableM64CaseKeyboardShelf(
                    name+":keyboardshelf",
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
