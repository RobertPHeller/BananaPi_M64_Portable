#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri May 15 08:45:36 2020
#  Last Modified : <200515.0854>
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

snit::macro LCDDims {} {
    typevariable _LCDWidth 344
    typevariable _LCDHeight 222
    typevariable _LCDThickness 6.5
    typevariable _LCDM1_y 11.85
    typevariable _LCDM2_y [expr {11.85 + 54.0}]
    typevariable _LCDM3_y [expr {11.85 + 144.3}]
    typevariable _LCDM4_y [expr {11.85 + 198.0}]
    typevariable _LCDM_x  [expr {3.7 + (6.5 / 2.0)}]
    typevariable _LCDM_r  [expr {2.5 / 2.0}]
}

snit::type LCDScreen {
    LCDDims
    Common
    component screen
    delegate method * to screen
    constructor {args} {
        $self configurelist $args
        install screen using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_LCDWidth 0 0] \
                        -vec2 [list 0 $_LCDHeight 0]] \
              -vector [list 0 0 $_LCDThickness] \
              -color  {250 250 250}
    }
}

package provide LCDScreen 1.0
