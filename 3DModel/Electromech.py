#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon Jun 1 10:34:36 2020
#  Last Modified : <200814.1428>
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

class Inlet(object):
    _flangewidth = 30.7
    _flangeheight = 23.7
    _flangedepth = 3.2
    _bodywidth = 27
    _bodyheight = 20
    _bodydepth = 16
    _lugwidth = 24
    _lugheight = 16
    _lugdepth = 7
    def Flange(self,yBase,yThick):
        flangeyoff = (Inlet._flangewidth - Inlet._bodywidth)/2.0
        flangexoff = (Inlet._flangeheight- Inlet._bodyheight)/2.0
        flangeorig = Base.Vector(self.origin.x-flangexoff,yBase,self.origin.z-flangeyoff)
        return Part.makePlane(Inlet._flangeheight,
                              Inlet._flangewidth,
                              flangeorig,Base.Vector(0,1,0)).extrude(Base.Vector(0,yThick,0))
    def bodyCutout(self,yBase,yThick):
        cutoutorig = Base.Vector(self.origin.x,yBase,self.origin.z)
        return Part.makePlane(Inlet._bodyheight,
                              Inlet._bodywidth,
                              cutoutorig,Base.Vector(0,1,0)
                              ).extrude(Base.Vector(0,yThick,0))
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        flange = self.Flange(oy,Inlet._flangedepth)
        body = Part.makePlane(Inlet._bodyheight,
                              Inlet._bodywidth,
                              origin,Base.Vector(0,1,0)
                              ).extrude(Base.Vector(0,-Inlet._bodydepth,0))
        self.body = body.fuse(flange)
        lugyoff = (Inlet._bodywidth - Inlet._lugwidth) / 2.0
        lugxoff = (Inlet._bodyheight - Inlet._lugheight) / 2.0
        lugorigin = Base.Vector(ox+lugxoff,oy-Inlet._bodydepth,
                                oz+lugyoff)
        self.solderlugs = Part.makePlane(Inlet._lugheight,
                                         Inlet._lugwidth,
                                         lugorigin,
                                         Base.Vector(0,1,0)
                                         ).extrude(Base.Vector(0,-Inlet._lugdepth))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_body')
        obj.Shape = self.body
        obj.Label=self.name+'_body'
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_solderlugs')
        obj.Shape = self.solderlugs
        obj.Label=self.name+'_solderlugs'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])

# 561-MP3P4

class DCStrainRelief(object):
    _holedia = (.437*25.4)
    _flangedia = (.484*25.4)
    _flangedepth = (.41*25.4)-6.75
    _bodydia = (.437*25.4)
    _bodydepth = 6.75 # Measured
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        YNorm=Base.Vector(0,1,0)
        flangerad = DCStrainRelief._flangedia/2.0
        flangeextrude = Base.Vector(0,-DCStrainRelief._flangedepth,0)
        flange = Part.Face(Part.Wire(Part.makeCircle(flangerad,origin,YNorm))
                          ).extrude(flangeextrude)
        bodyrad = DCStrainRelief._bodydia/2.0
        bodyextrude = Base.Vector(0,DCStrainRelief._bodydepth,0)
        body = Part.Face(Part.Wire(Part.makeCircle(bodyrad,origin,YNorm))
                        ).extrude(bodyextrude)
        self.body = body.fuse(flange)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.body
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
    def MountHole(self,yBase,yDepth):
        holerad = DCStrainRelief._holedia/2.0
        holeorig = Base.Vector(self.origin.x,yBase,self.origin.z)
        holeextrude = Base.Vector(0,yDepth,0)
        YNorm=Base.Vector(0,1,0)
        return Part.Face(Part.Wire(Part.makeCircle(holerad,holeorig,YNorm))
                        ).extrude(holeextrude)


class Fan02510SS_05P_AT00(object):
    _fanwidth_height = 25
    _fandepth = 10
    _fanmholespacing = 20
    _fanmholedia = 2.8
    _fanholedia = 24.3
    def mhxyoff(self):
        return (Fan02510SS_05P_AT00._fanwidth_height-\
                Fan02510SS_05P_AT00._fanmholespacing)/2.0
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        forig = Base.Vector(ox,oy+Fan02510SS_05P_AT00._fanwidth_height,oz)
        XNorm=Base.Vector(1,0,0)
        fanextrude = Base.Vector(Fan02510SS_05P_AT00._fandepth,0,0)
        self.body = Part.makePlane(Fan02510SS_05P_AT00._fanwidth_height,
                                   Fan02510SS_05P_AT00._fanwidth_height,
                                   forig,XNorm
                                  ).extrude(fanextrude)
        mhXYoff = self.mhxyoff()
        self.mh = dict()
        self.mh[1] = Base.Vector(ox,oy+mhXYoff,oz+mhXYoff)
        self.mh[2] = Base.Vector(ox,
                               oy+mhXYoff+
                                 Fan02510SS_05P_AT00._fanmholespacing,
                               oz+mhXYoff)
        self.mh[3] = Base.Vector(ox,
                               oy+mhXYoff,
                               oz+mhXYoff+
                                 Fan02510SS_05P_AT00._fanmholespacing)
        self.mh[4] = Base.Vector(ox,
                               oy+mhXYoff+
                                 Fan02510SS_05P_AT00._fanmholespacing,
                               oz+mhXYoff+
                                 Fan02510SS_05P_AT00._fanmholespacing)
        fanmhrad = Fan02510SS_05P_AT00._fanmholedia/2.0
        #fanextrude = Base.Vector(-Fan02510SS_05P_AT00._fandepth,0,0)
        for i in [1,2,3,4]:
            self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(fanmhrad,self.mh[i],XNorm))).extrude(fanextrude))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.body
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
    def MountingHole(self,i,xBase,xDepth):
        mh = Base.Vector(xBase,self.mh[i].y,self.mh[i].z)
        fanmhrad = Fan02510SS_05P_AT00._fanmholedia/2.0
        XNorm=Base.Vector(1,0,0)
        extrude = Base.Vector(xDepth,0,0)
        return Part.Face(Part.Wire(Part.makeCircle(fanmhrad,mh,XNorm))
                        ).extrude(extrude)
    def RoundFanHole(self,xBase,height):
        ox=xBase
        oy=self.origin.y+(Fan02510SS_05P_AT00._fanwidth_height/2.0)
        oz=self.origin.z+(Fan02510SS_05P_AT00._fanwidth_height/2.0)
        holeorig=Base.Vector(ox,oy,oz)
        holerad=Fan02510SS_05P_AT00._fanholedia/2.0
        XNorm=Base.Vector(1,0,0)
        extrude = Base.Vector(height,0,0)
        return Part.Face(Part.Wire(Part.makeCircle(holerad,holeorig,XNorm))
                        ).extrude(extrude)
    def SquareFanHole(self,xBase,height):
        ox=xBase
        oy=self.origin.y+Fan02510SS_05P_AT00._fanwidth_height
        oz=self.origin.z
        holeorig=Base.Vector(ox,oy,oz)
        holeside=Fan02510SS_05P_AT00._fanwidth_height
        XNorm=Base.Vector(1,0,0)
        extrude = Base.Vector(height,0,0)
        return Part.makePlane(holeside,holeside,holeorig,XNorm).extrude(extrude)
    def DrillGrillHoles(self,xBase,height,hdia,hspace,panel):
        ox=xBase
        oy=self.origin.y
        oz=self.origin.z
        hrad = hdia/2.0
        holeside=Fan02510SS_05P_AT00._fanwidth_height
        extrude = Base.Vector(height,0,0)
        XNorm=Base.Vector(1,0,0)
        x = hspace/2.0
        while x < holeside:
            y = hspace/2.0
            while y < holeside:
                holeorig=Base.Vector(ox,oy+x,oz+y)
                panel = panel.cut(Part.Face(Part.Wire(Part.makeCircle(hrad,holeorig,XNorm))
                                           ).extrude(extrude))
                y += hspace
            x += hspace
        return panel

class Fan02510SS_05P_AT00_TopMount(object):
    _fanwidth_height = 25
    _fandepth = 10
    _fanmholespacing = 20
    _fanmholedia = 2.8
    _fanholedia = 24.3
    _grilholesize = (3/32)*25.4
    @classmethod
    def _hspace(cls):
        return cls._fanwidth_height/8
    def mhxyoff(self):
        return (self._fanwidth_height-\
                self._fanmholespacing)/2.0
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        forig = Base.Vector(ox,oy,oz)
        ZNorm=Base.Vector(0,0,1)
        fanextrude = Base.Vector(0,0,-self._fandepth)
        self.body = Part.makePlane(self._fanwidth_height,
                                   self._fanwidth_height,
                                   forig,ZNorm
                                  ).extrude(fanextrude)
        mhXYoff = self.mhxyoff()
        self.mh = dict()
        self.mh[1] = Base.Vector(ox+mhXYoff,oy+mhXYoff,oz)
        self.mh[2] = Base.Vector(ox+mhXYoff,
                               oy+mhXYoff+
                                 self._fanmholespacing,
                               oz)
        self.mh[3] = Base.Vector(ox+mhXYoff+self._fanmholespacing,
                               oy+mhXYoff,
                               oz)
        self.mh[4] = Base.Vector(ox+mhXYoff+
                                 self._fanmholespacing,
                               oy+mhXYoff+
                                 self._fanmholespacing,
                               oz)
        fanmhrad = self._fanmholedia/2.0
        for i in [1,2,3,4]:
            self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(fanmhrad,self.mh[i],ZNorm))).extrude(fanextrude))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.body
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
    def MountingHole(self,i,zBase,zDepth):
        mh = Base.Vector(self.mh[i].x,self.mh[i].y,zBase)
        fanmhrad = self._fanmholedia/2.0
        ZNorm=Base.Vector(0,0,1)
        extrude = Base.Vector(0,0,zDepth)
        return Part.Face(Part.Wire(Part.makeCircle(fanmhrad,mh,ZNorm))
                        ).extrude(extrude)
    def RoundFanHole(self,zBase,height):
        ox=self.origin.x+(self._fanwidth_height/2.0)
        oy=self.origin.y+(self._fanwidth_height/2.0)
        oz=zBase
        holeorig=Base.Vector(ox,oy,oz)
        holerad=self._fanholedia/2.0
        ZNorm=Base.Vector(0,0,1)
        extrude = Base.Vector(0,0,height)
        return Part.Face(Part.Wire(Part.makeCircle(holerad,holeorig,ZNorm))
                        ).extrude(extrude)
    def RoundFanGrill(self,zBase,height,panel):
        hdia = self._grilholesize
        hrad = hdia/2.0
        hspace = self._hspace()
        rowholespaces = [0,1,2,3]
        ox=self.origin.x
        oy=self.origin.y
        oz=zBase
        center = self._fanwidth_height/2
        for hs in rowholespaces:
            if hs == 0:
                panel = panel.cut(self._cutgrillhole(ox+center,oy+center,oz,\
                                                    hrad,height))
            else:
                rxy = hs*hspace
                panel = panel.cut(self._cutgrillhole(ox+center,oy+(center+rxy),\
                                                     oz,hrad,height))
                panel = panel.cut(self._cutgrillhole(ox+center,oy+(center-rxy),\
                                                     oz,hrad,height))
                panel = panel.cut(self._cutgrillhole(ox+(center+rxy),oy+center,\
                                                     oz,hrad,height))
                panel = panel.cut(self._cutgrillhole(ox+(center-rxy),oy+center,\
                                                     oz,hrad,height))
                if hs == 1:
                    panel = panel.cut(self._cutgrillhole(ox+(center+rxy),\
                                                         oy+(center+rxy),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center-rxy),\
                                                         oy+(center-rxy),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center+rxy),\
                                                         oy+(center-rxy),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center-rxy),\
                                                         oy+(center+rxy),oz,\
                                                         hrad,height))
                elif hs == 2:
                    panel = panel.cut(self._cutgrillhole(ox+(center+hspace),\
                                                         oy+(center+rxy),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center-hspace),\
                                                         oy+(center+rxy),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center+hspace),\
                                                         oy+(center-rxy),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center-hspace),\
                                                         oy+(center-rxy),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center-rxy),\
                                                         oy+(center+hspace),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center-rxy),\
                                                         oy+(center-hspace),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center+rxy),\
                                                         oy+(center+hspace),oz,\
                                                         hrad,height))
                    panel = panel.cut(self._cutgrillhole(ox+(center+rxy),\
                                                         oy+(center-hspace),oz,\
                                                         hrad,height))
        return panel
    def _cutgrillhole(self,xh,yh,zh,rad,height):
        horig=Base.Vector(xh,yh,zh)
        hthick = Base.Vector(0,0,height)
        ZNorm=Base.Vector(0,0,1)
        return Part.Face(Part.Wire(Part.makeCircle(rad,horig,ZNorm))).extrude(hthick)
    def SquareFanHole(self,zBase,height):
        ox=self.origin.x
        oy=self.origin.y+self._fanwidth_height
        oz=zBase
        holeorig=Base.Vector(ox,oy,oz)
        holeside=self._fanwidth_height
        ZNorm=Base.Vector(0,0,1)
        extrude = Base.Vector(0,0,height)
        return Part.makePlane(holeside,holeside,holeorig,ZNorm).extrude(extrude)
    def DrillGrillHoles(self,zBase,height,hdia,hspace,panel):
        ox=self.origin.x
        oy=self.origin.y
        oz=zBase
        hrad = hdia/2.0
        holeside=self._fanwidth_height
        extrude = Base.Vector(0,0,height)
        ZNorm=Base.Vector(0,0,1)
        x = hspace/2.0
        while x < holeside:
            y = hspace/2.0
            while y < holeside:
                holeorig=Base.Vector(ox+y,oy+x,oz)
                panel = panel.cut(Part.Face(Part.Wire(Part.makeCircle(hrad,holeorig,XNorm))
                                           ).extrude(extrude))
                y += hspace
            x += hspace
        return panel

class Grommet(object):
    _OutsideDiameter = 8.71
    _InsideDiameter  = 3.18
    _HoleDiameter    = 6.35
    _Height          = 4.75
    _PanelThick      = 1.59
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        borig = origin.add(Base.Vector(-(self._Height/2.0),0,0))
        XNorm = Base.Vector(1,0,0)
        Thick = Base.Vector(self._Height,0,0)
        self.body = Part.Face(Part.Wire(Part.makeCircle(\
                          self._OutsideDiameter/2,borig,XNorm))).extrude(Thick)
        self.body = self.body.cut(Part.Face(Part.Wire(Part.makeCircle(\
                          self._InsideDiameter/2,borig,XNorm))).extrude(Thick))
        panelorigin = origin.add(Base.Vector(-(self._PanelThick/2),-self._OutsideDiameter/2,-self._OutsideDiameter/2))
        panelthick  = Base.Vector(self._PanelThick,0,0)
        panel = Part.makePlane(self._OutsideDiameter,self._OutsideDiameter,\
                               panelorigin,XNorm).extrude(panelthick)
        self.horig = origin.add(Base.Vector(-(self._PanelThick/2),0,0))
        panel = panel.cut(Part.Face(Part.Wire(Part.makeCircle(self._HoleDiameter/2,self.horig,XNorm))).extrude(panelthick))
        self.body = self.body.cut(panel)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.body
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
    def CutHole(self,panel):
        XNorm = Base.Vector(1,0,0)
        panelthick  = Base.Vector(self._PanelThick,0,0)
        return panel.cut(Part.Face(Part.Wire(Part.makeCircle(self._HoleDiameter/2,self.horig,XNorm))).extrude(panelthick))
