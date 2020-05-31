#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun May 31 08:03:12 2020
#  Last Modified : <200531.0806>
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

## Power Supply: Mouser #490-PSK-S15C-5
# PCB mount, 28.8mm wide 53.8mm long, 23.5mm high

class PSK_S15C(object):
    _pswidth = 28.8
    _pslength = 53.8
    _psheight = 23.5
    _pspindia = 1.0
    _pspinlength = 6.0
    _pspin1Xoff = ((53.8-45.72)/2.0)+45.72
    _pspin1Yoff = ((28.8-20.32)/2.0)+20.32
    _pspin2Xoff = ((53.8-45.72)/2.0)+45.72
    _pspin2Yoff = (28.8-20.32)/2.0
    _pspin3Xoff = (53.8-45.72)/2.0
    _pspin3Yoff = ((28.8-20.32)/2.0)+10.16
    _pspin4Xoff = (53.8-45.72)/2.0
    _pspin4Yoff = ((28.8-20.32)/2.0)+20.32
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        ox = origin.x
        oy = origin.y
        oz = origin.z

