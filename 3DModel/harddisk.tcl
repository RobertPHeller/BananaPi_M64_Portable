#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon May 25 18:05:27 2020
#  Last Modified : <200526.1011>
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

snit::macro Disk25_2HDims {} {
    typevariable _Disk25_2H_Width 69.85
    typevariable _Disk25_2H_Length 100.29
    typevariable _Disk25_2H_Height 9.38
    typevariable _Disk25_2H_MH1X [expr {2.8   + (2.7/2.0)}]
    typevariable _Disk25_2H_MH1Y [expr {12.67 + (2.7/2.0)}]
    typevariable _Disk25_2H_MH2X [expr {2.8   + (2.7/2.0)}]
    typevariable _Disk25_2H_MH2Y [expr {89.33 + (2.7/2.0)}]
    typevariable _Disk25_2H_MH3X [expr {64.79 + (2.7/2.0)}]
    typevariable _Disk25_2H_MH3Y [expr {12.67 + (2.7/2.0)}]
    typevariable _Disk25_2H_MH4X [expr {64.79 + (2.7/2.0)}]
    typevariable _Disk25_2H_MH4Y [expr {89.33 + (2.7/2.0)}]
    typevariable _Disk25_2H_MHDia 2.7
    typevariable _Disk25_2H_MHDepth 4.67
}

snit::type Disk25_2H {
    Common
    Disk25_2HDims
    component body
    component mh1
    component mh2
    component mh3
    component mh4
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_Disk25_2H_Width 0 0] \
                        -vec2 [list 0 $_Disk25_2H_Length 0]] \
              -vector [list 0 0 $_Disk25_2H_Height] \
              -color {200 200 200}
        lassign $options(-origin) ox oy oz
        install mh1 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_Disk25_2H_MH1X}] \
                       [expr {$oy + $_Disk25_2H_MH1Y}] $oz] \
              -radius [expr {$_Disk25_2H_MHDia / 2.0}] \
              -height $_Disk25_2H_MHDepth \
              -direction Z \
              -color {255 255 255}
        install mh2 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_Disk25_2H_MH2X}] \
                       [expr {$oy + $_Disk25_2H_MH2Y}] $oz] \
              -radius [expr {$_Disk25_2H_MHDia / 2.0}] \
              -height $_Disk25_2H_MHDepth \
              -direction Z \
              -color {255 255 255}
        install mh3 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_Disk25_2H_MH3X}] \
                       [expr {$oy + $_Disk25_2H_MH3Y}] $oz] \
              -radius [expr {$_Disk25_2H_MHDia / 2.0}] \
              -height $_Disk25_2H_MHDepth \
              -direction Z \
              -color {255 255 255}
        install mh4 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_Disk25_2H_MH4X}] \
                       [expr {$oy + $_Disk25_2H_MH4Y}] $oz] \
              -radius [expr {$_Disk25_2H_MHDia / 2.0}] \
              -height $_Disk25_2H_MHDepth \
              -direction Z \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $mh1  print $fp
        $mh2  print $fp
        $mh3  print $fp
        $mh4  print $fp
    }
    method MountingHole {name i baseZ height} {
        lassign [[set mh$i] cget -bottom] x y z
        set bottom [list $x $y $baseZ]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [[set mh$i] cget -radius] \
                -height $height \
                -color {255 255 255}]
    }
}
    
package provide harddisk 1.0    
