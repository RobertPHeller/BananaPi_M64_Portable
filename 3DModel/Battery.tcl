#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Wed May 20 15:47:14 2020
#  Last Modified : <200520.1559>
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


package require Common

snit::macro BatteryDims {} {
    typevariable _Battery_Length [expr {12.1*10}]
    typevariable _Battery_Width  [expr {6.5*10}]
    typevariable _Battery_Height [expr {.75*10}]
}

snit::type Battery {
    Common
    BatteryDims
    component battery
    delegate method * to battery
    delegate option * to battery
    constructor {args} {
        $self configurelist $args
        install battery using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_Battery_Length 0 0] \
                        -vec2 [list 0 $_Battery_Width 0]] \
              -vector [list 0 0 $_Battery_Height] \
              -color {192 192 192}
    }
}


package provide Battery 1.0
