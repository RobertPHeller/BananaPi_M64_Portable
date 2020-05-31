#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 30 11:16:52 2020
#  Last Modified : <200531.0048>
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

class M64Board(object):  
    _m64_m1_relpos = [ (96.4-93.64472), (59.9-57.15) ]
    _m64_m2_relpos = [ (96.4-7.79526), (59.9-57.15) ]
    _m64_m3_relpos = [ (96.4-93.64472), (59.9-2.794) ]
    _m64_m4_relpos = [ (96.4-7.79526), (59.9-8.0772) ]
    _m64_mh_dia = 2.750
    _m64XOff = 0
    _m64YOff = 1*25.4
    _m64YMin = 0
    _m64YMax = 59.90082
    _m64XMin = 5.00126
    _m64XMax = 96.40062
    _m64Width = 59.90082
    _m64Length = 96.40062-5.00126
    _m64Thickness = .06125*25.4
    _m64Standoff = .25*25.4
    _m64StandoffDia = 6
    _PlateHeight = 16
    _DualUSBHeight = 15.60
    _DualUSBWidth = 14.40
    _DualUSBLength = 100.93452-79.34452
    _DualUSBXMin = 79.34452
    _DualUSBXMax = 100.93452
    _DualUSBYMin = 10.96518
    _DualUSBYMax = 26.45918
    _RJ45YMin = 30.83814
    _RJ45YMax = 45.23994
    _RJ45XMin = 83.55584
    _RJ45XMax = 100.90404
    _RJ45Height = 13.35
    _RJ45Width = 16
    _RJ45Length = 100.90404 - 83.55584
    _AudioYMinBody = 47.55642
    _AudioYMaxBody = 53.15458
    _AudioDiameter = 5.6
    _AudioXMinBody = 84.29244
    _AudioXMaxBody = 96.393
    _AudioBodyLength = 14.0 - 2.0
    _AudioBodyWidth =  6.0
    _AudioBodyHeight = 5.0
    _AudioXMinBarrel = 96.393
    _AudioXMaxBarrel = 98.39198
    _gpioHeaderXOffset = 26.16962-3.57
    _gpioHeaderLength = 55.4
    _gpioHeaderHeight = 16.1
    _OTG_XMin = 6.99516
    _OTG_XMax = 14.59484
    _OTG_YMin = -1.6891
    _OTG_YMax = 4.31038
    _OTG_Width = 7.57
    _OTG_Length = 5.59
    _OTG_Thick = 2.62
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z
        boardsurf = Part.makePlane(M64Board._m64Length,M64Board._m64Width,origin)
        dualusb_x = ox + (M64Board._m64XMax - M64Board._DualUSBXMax)
        dualusb_y = oy + (M64Board._m64YMax - M64Board._DualUSBYMax)
        dualusb_z = oz + M64Board._m64Thickness
        dualusbsurf = Part.makePlane(M64Board._DualUSBLength,
                                     M64Board._DualUSBWidth,
                                     Base.Vector(dualusb_x,dualusb_y,dualusb_z))
        self.dualusb = dualusbsurf.extrude(Base.Vector(0,0,M64Board._DualUSBHeight))
        rj45_x = ox + (M64Board._m64XMax - M64Board._RJ45XMax)
        rj45_y = oy + (M64Board._m64YMax - M64Board._RJ45YMax)
        rj45_z = oz + M64Board._m64Thickness
        rj45surf = Part.makePlane(M64Board._RJ45Length,
                                  M64Board._RJ45Width,
                                  Base.Vector(rj45_x,rj45_y,rj45_z))
        self.rj45 = rj45surf.extrude(Base.Vector(0,0,M64Board._RJ45Height))
        audiobody_x = ox + (M64Board._m64XMax - M64Board._AudioXMaxBody)
        audiobody_y = oy + (M64Board._m64YMax - M64Board._AudioYMaxBody)
        audiobody_z = oz + M64Board._m64Thickness
        audiobodysurf = Part.makePlane(M64Board._AudioBodyLength,
                                       M64Board._AudioBodyWidth,
                                       Base.Vector(audiobody_x,audiobody_y,audiobody_z))
        self.audiobody = audiobodysurf.extrude(Base.Vector(0,0,M64Board._AudioBodyHeight))
        audiobarrel_x = ox 
        audiobarrel_y = oy + (M64Board._m64YMax - M64Board._AudioYMaxBody + (M64Board._AudioBodyWidth/2.0))
        audiobarrel_z = oz + (M64Board._m64Thickness + (M64Board._AudioBodyHeight / 2.0))
        audiobarrelcirc = Part.makeCircle((M64Board._AudioDiameter/2.0),
                                          Base.Vector(audiobarrel_x,audiobarrel_y,audiobarrel_z),
                                          Base.Vector(1,0,0))
        audiobarrelwire = Part.Wire(audiobarrelcirc)
        audiobarrelsurf = Part.Face(audiobarrelwire)
        self.audiobarrel = audiobarrelsurf.extrude(Base.Vector(M64Board._AudioXMinBarrel-M64Board._AudioXMaxBarrel,0,0))
        otg_x = ox + (M64Board._m64XMax - M64Board._OTG_XMax)
        otg_y = oy + (M64Board._m64YMax - M64Board._OTG_YMax)
        otg_z = oz + M64Board._m64Thickness
        otgsurf = Part.makePlane(M64Board._OTG_Width,M64Board._OTG_Length,
                                 Base.Vector(otg_x,otg_y,otg_z))
        self.otg = otgsurf.extrude(Base.Vector(0,0,M64Board._OTG_Thick))
        self.mhvector = {
            1: Base.Vector(ox+M64Board._m64_m1_relpos[0],
                                               oy+M64Board._m64_m1_relpos[1],
                                               oz),
            2: Base.Vector(ox+M64Board._m64_m2_relpos[0],
                                               oy+M64Board._m64_m2_relpos[1],
                                               oz),
            3: Base.Vector(ox+M64Board._m64_m3_relpos[0],
                                               oy+M64Board._m64_m3_relpos[1],
                                               oz),
            4: Base.Vector(ox+M64Board._m64_m4_relpos[0],
                                               oy+M64Board._m64_m4_relpos[1],
                                               oz)
        }
        mh1circ = Part.makeCircle(M64Board._m64_mh_dia/2.0,
                                  self.mhvector[1])
        mh1wire = Part.Wire(mh1circ)
        mh1 = Part.Face(mh1wire)
        boardsurf = boardsurf.cut(mh1)
        mh2circ = Part.makeCircle(M64Board._m64_mh_dia/2.0,
                                   self.mhvector[2])
        mh2wire = Part.Wire(mh2circ)
        mh2 = Part.Face(mh2wire)
        boardsurf = boardsurf.cut(mh2)
        mh3circ = Part.makeCircle(M64Board._m64_mh_dia/2.0,
                                   self.mhvector[3])
        mh3wire = Part.Wire(mh3circ)
        mh3 = Part.Face(mh3wire)
        boardsurf = boardsurf.cut(mh3)
        mh4circ = Part.makeCircle(M64Board._m64_mh_dia/2.0,
                                   self.mhvector[4])
        mh4wire = Part.Wire(mh4circ)
        mh4 = Part.Face(mh4wire)
        boardsurf = boardsurf.cut(mh4)
        self.board = boardsurf.extrude(Base.Vector(0,0,M64Board._m64Thickness))
        self.standoff1 = self.Standoff("stoff1",1,oz,-M64Board._m64Standoff,M64Board._m64StandoffDia,[255,244,0])
        self.standoff2 = self.Standoff("stoff2",2,oz,-M64Board._m64Standoff,M64Board._m64StandoffDia,[255,244,0])
        self.standoff3 = self.Standoff("stoff3",3,oz,-M64Board._m64Standoff,M64Board._m64StandoffDia,[255,244,0])
        self.standoff4 = self.Standoff("stoff4",4,oz,-M64Board._m64Standoff,M64Board._m64StandoffDia,[255,244,0])
        Part.show(self.board)
        doc = App.activeDocument()
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':M64Board'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,1.0,0.0])        
        Part.show(self.dualusb)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Dual USB'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.9,.9,.9])
        Part.show(self.rj45)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Ethernet Jack'
        doc.Objects[last].ViewObject.ShapeColor=tuple([.9,.9,.9])
        Part.show(self.audiobody)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Audio Body'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        Part.show(self.audiobarrel)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':Audio Barrel'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        Part.show(self.otg)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':OTG Jack'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.9,0.9,0.9])
        Part.show(self.standoff1)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':StandOff 1'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.9,0.9,0.0])
        Part.show(self.standoff2)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':StandOff 2'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.9,0.9,0.0])
        Part.show(self.standoff3)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':StandOff 3'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.9,0.9,0.0])
        Part.show(self.standoff4)
        last = len(doc.Objects)-1
        doc.Objects[last].Label=name+':StandOff 4'
        doc.Objects[last].ViewObject.ShapeColor=tuple([0.9,0.9,0.0])
    def MountingHole(self,name,i,zBase):
        mhv = self.mhvector[i]
        mhz = Base.Vector(mhv.x,mhv.y,zBase);
        mhcirc = Part.makeCircle(M64Board._m64_mh_dia/2.0,mhv);
        mhwire = Part.Wire(mhcirc)
        return Part.Face(mhwire)
    def Standoff(self,name,i,zBase,height,diameter,color):
        stofv = self.mhvector[i]
        stofv = Base.Vector(stofv.x,stofv.y,zBase)
        stofcirc = Part.makeCircle(diameter/2.0,stofv)
        stofwire = Part.Wire(stofcirc)
        stofface = Part.Face(stofwire)
        result = stofface.extrude(Base.Vector(0,0,height))
        return result
        







    
if __name__ == '__main__':
    board = M64Board("board",Base.Vector(0,0,0))
