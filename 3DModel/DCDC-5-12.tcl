#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon May 11 15:59:56 2020
#  Last Modified : <200523.2047>
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

# DCDC 5V to 12V power converter

snit::macro DCDC_5_12Dims {} {
    typevariable _dcdc_5_12_width 31.75
    typevariable _dcdc_5_12_height 45.720
    typevariable _dcdc_5_12_holeEdgeOffset 3.81
    typevariable _dcdc_5_12_holeHSpacing 29.21
    typevariable _dcdc_5_12_holeWSpacing 24.13
    typevariable _dcdc_5_12_holeDia 2.7
    typevariable _dcdc_5_12_boardthickness 1.6
}

snit::type DCDC_5_12_Vert12Down {
    Common
    DCDC_5_12Dims
    component board
    component mh1
    component mh2
    component mh3
    component mh4
    constructor {args} {
        $self configurelist $args
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list 0 $_dcdc_5_12_height 0] \
                        -vec2 [list $_dcdc_5_12_width 0 0]] \
              -vector [list 0 0 $_dcdc_5_12_boardthickness] \
              -color {210 180 140}
        lassign $options(-origin) ox oy oz
        set mh1x [expr {$ox + $_dcdc_5_12_holeEdgeOffset}]
        set mh1y [expr {$oy + $_dcdc_5_12_holeEdgeOffset}]
        install mh1 using Cylinder %AUTO% \
              -bottom [list $mh1x $mh1y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
        set mh2x [expr {$mh1x + $_dcdc_5_12_holeWSpacing}]
        set mh2y $mh1y
        install mh2 using Cylinder %AUTO% \
              -bottom [list $mh2x $mh2y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
        set mh3x $mh2x
        set mh3y [expr {$mh2y + $_dcdc_5_12_holeWSpacing}]
        install mh3 using Cylinder %AUTO% \
              -bottom [list $mh3x $mh3y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
        set mh4x $mh1x
        set mh4y $mh3y
        install mh4 using Cylinder %AUTO% \
              -bottom [list $mh4x $mh4y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
    }
    method MountingHole {name i zBase height} {
        lassign [[set mh$i] cget -bottom] x y z
        return [Cylinder create $name \
                -bottom [list $x $y $zBase] \
                -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
                -direction Z \
                -height $height \
                -color {255 255 255}]
    }
    method Standoff {name i zBase height {diameter 6.35}} {
        lassign [[set mh$i] cget -bottom] x y z
        return [Cylinder create $name \
                -bottom [list $x $y $zBase] \
                -radius [expr {$diameter / 2.0}] \
                -direction Z \
                -height $height \
                -color {255 255 0}]
    }
    method print {{fp stdout}} { 
        $board print $fp
        $mh1   print $fp
        $mh2   print $fp
        $mh3   print $fp
        $mh4   print $fp
    }
}


snit::type DCDC_5_12_Horiz12Right {
    Common
    DCDC_5_12Dims
    component board
    component mh1
    component mh2
    component mh3
    component mh4
    constructor {args} {
        $self configurelist $args
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_dcdc_5_12_height 0 0] \
                        -vec2 [list 0 $_dcdc_5_12_width 0]] \
              -vector [list 0 0 $_dcdc_5_12_boardthickness] \
              -color {210 180 140}
        lassign $options(-origin) ox oy oz
        set mh1x [expr {$ox + ($_dcdc_5_12_height - $_dcdc_5_12_holeEdgeOffset) - $_dcdc_5_12_holeHSpacing}]
        set mh1y [expr {$oy + $_dcdc_5_12_holeEdgeOffset}]
        install mh1 using Cylinder %AUTO% \
              -bottom [list $mh1x $mh1y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
        set mh2x [expr {$mh1x + $_dcdc_5_12_holeHSpacing}]
        set mh2y $mh1y
        install mh2 using Cylinder %AUTO% \
              -bottom [list $mh2x $mh2y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
        set mh3x $mh2x
        set mh3y [expr {$mh2y + $_dcdc_5_12_holeWSpacing}]
        install mh3 using Cylinder %AUTO% \
              -bottom [list $mh3x $mh3y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
        set mh4x $mh1x
        set mh4y $mh3y
        install mh4 using Cylinder %AUTO% \
              -bottom [list $mh4x $mh4y $oz] \
              -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
              -direction Z \
              -height $_dcdc_5_12_boardthickness \
              -color {255 255 255}
    }
    method MountingHole {name i zBase height} {
        lassign [[set mh$i] cget -bottom] x y z
        return [Cylinder create $name \
                -bottom [list $x $y $zBase] \
                -radius [expr {$_dcdc_5_12_holeDia / 2.0}] \
                -direction Z \
                -height $height \
                -color {255 255 255}]
    }
    method Standoff {name i zBase height {diameter 6.35}} {
        lassign [[set mh$i] cget -bottom] x y z
        return [Cylinder create $name \
                -bottom [list $x $y $zBase] \
                -radius [expr {$diameter / 2.0}] \
                -direction Z \
                -height $height \
                -color {255 255 0}]
    }
    method print {{fp stdout}} { 
        $board print $fp
        $mh1   print $fp
        $mh2   print $fp
        $mh3   print $fp
        $mh4   print $fp
    }
}

package provide DCDC_5_12 1.0

