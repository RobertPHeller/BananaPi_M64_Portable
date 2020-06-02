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
#  Last Modified : <200602.0537>
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
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        Part.show(self.solderlugs)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':solderlugs'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.75,.75,.75])


class DCStrainRelief(object):
    _holedia = 11.40
    _flangedia = 13.40
    _flangedepth = 4.0
    _bodydia = 13.31
    _bodydepth = 6.0
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
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
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
        mhXYoff = (Fan02510SS_05P_AT00._fanwidth_height-
                   Fan02510SS_05P_AT00._fanmholespacing)/2.0
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
        Part.show(self.body)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=self.name+':body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
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
        oy=self.origin.y
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
