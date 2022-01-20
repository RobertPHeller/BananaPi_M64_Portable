#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Jun 2 22:07:22 2020
#  Last Modified : <200606.1858>
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

class LCDDims(object):
    _Width = 344
    def Width(self):
        return LCDDims._Width
    _Height = 222
    def Height(self):
        return LCDDims._Height
    _Thickness = 6.5
    def Thickness(self):
        return LCDDims._Thickness
    _M1_y = 11.85
    def M1_y(self):
        return LCDDims._M1_y
    _M2_y = 11.85 + 54.0
    def M2_y(self):
        return LCDDims._M2_y
    _M3_y = 11.85 + 144.3
    def M3_y(self):
        return LCDDims._M3_y
    _M4_y = 11.85 + 198.0
    def M4_y(self):
        return LCDDims._M4_y
    _M_x =  3.7 + (6.5 / 2.0)
    def M_x(self):
        return LCDDims._M_x
    _M_r =  2.5 / 2.0
    def M_r(self):
        return LCDDims._M_r
    def __init__(self):
        raise RuntimeError("No Instances allowed for LCDDims!")

class LCDScreen(LCDDims):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        surf = Part.makePlane(self.Width(),self.Height(),origin)
        thick=Base.Vector(0,0,self.Thickness())
        self.screen = surf.extrude(thick)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.screen
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([250/255.0,250/255.0,250/255.0])

        
