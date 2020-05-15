#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri May 15 14:20:43 2020
#  Last Modified : <200515.1852>
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

snit::macro HDMIConverterDims {} {
    typevariable _HDMIConv_mainboardWidth 139
    typevariable _HDMIConv_mainboardHeight 58
    typevariable _HDMIConv_mainBoardMHDia 3.5
    typevariable _HDMIConv_mainboardMH1_x [expr {124.47 + (3.5/2.0)}]
    typevariable _HDMIConv_mainboardMH1_y [expr {19.24 + (3.5/2.0)}]
    typevariable _HDMIConv_mainboardMH2_x [expr {123.03 + (3.5/2.0)}]
    typevariable _HDMIConv_mainboardMH2_y [expr {47.32 + (3.5/2.0)}]
    typevariable _HDMIConv_mainboardMH3_x [expr {12.36 + (3.5/2.0)}]
    typevariable _HDMIConv_mainboardMH3_y [expr {19.24 + (3.5/2.0)}]
    typevariable _HDMIConv_mainboardMH4_x [expr {18.07 + (3.5/2.0)}]
    typevariable _HDMIConv_mainboardMH4_y [expr {47.32 + (3.5/2.0)}]
    typevariable _HDMIConv_buttonboardWidth 104.13
    typevariable _HDMIConv_buttonboardHeight 21.87
    typevariable _HDMIConv_buttonboardMHDia 3.32
    typevariable _HDMIConv_buttonboardMH1_x [expr {8.2 + (3.32/2.0)}]
    typevariable _HDMIConv_buttonboardMH1_y [expr {6 + (3.32/2.0)}]
    typevariable _HDMIConv_buttonboardMH2_x [expr {92.7 + (3.32/2.0)}]
    typevariable _HDMIConv_buttonboardMH2_y [expr {6 + (3.32/2.0)}]
    typevariable _HDMIConv_hvpowerboardWidth 119.73
    typevariable _HDMIConv_hvpowerboardHeight 23.24
    typevariable _HDMIConv_hvpowerboardMHDia 3.5
    typevariable _HDMIConv_hvpowerboardMH2_x [expr {114.22 + (3.5/2.0)}]
    typevariable _HDMIConv_hvpowerboardMH2_y [expr {2.2 + (3.5/2.0)}]
    typevariable _HDMIConv_hvpowerboardMH1_x1 2.73
    typevariable _HDMIConv_hvpowerboardMH1_wide 14.25
    typevariable _HDMIConv_hvpowerboardMH1_y 2.0
    typevariable _HDMIConv_boardthickness 1.5
}


snit::type HDMIConverterMainBoard {
    Common
    HDMIConverterDims
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
                        -vec1 [list $_HDMIConv_mainboardWidth 0 0] \
                        -vec2 [list 0 $_HDMIConv_mainboardHeight 0]] \
              -vector [list 0 0 $_HDMIConv_boardthickness] \
              -color  {0 255 0}
        lassign $options(-origin) ox oy oz
        install mh1 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_HDMIConv_mainboardMH1_x}] \
                       [expr {$oy + $_HDMIConv_mainboardMH1_y}] \
                       $oz] \
              -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
              -height $_HDMIConv_boardthickness \
              -direction Z \
              -color {255 255 255}
        install mh2 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_HDMIConv_mainboardMH2_x}] \
                       [expr {$oy + $_HDMIConv_mainboardMH2_y}] \
                       $oz] \
              -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
              -height $_HDMIConv_boardthickness \
              -direction Z \
              -color {255 255 255}
        install mh3 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_HDMIConv_mainboardMH3_x}] \
                       [expr {$oy + $_HDMIConv_mainboardMH3_y}] \
                       $oz] \
              -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
              -height $_HDMIConv_boardthickness \
              -direction Z \
              -color {255 255 255}
        install mh4 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_HDMIConv_mainboardMH4_x}] \
                       [expr {$oy + $_HDMIConv_mainboardMH4_y}] \
                       $oz] \
              -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
              -height $_HDMIConv_boardthickness \
              -direction Z \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $board print $fp
        $mh1 print $fp
        $mh2 print $fp
        $mh3 print $fp
        $mh4 print $fp
    }
    method MountingHole {name i zBase height} {
        lassign [[set mh$i] cget -bottom] bx by bz
        return [Cylinder create $name \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
                -height $height \
                -direction Z -color {255 255 255}]
    }
    method Standoff {name i zBase height diameter color} {
        lassign [[set mh$i] cget -bottom] bx by bz
        return [Cylinder create $name \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$diameter / 2.0}] \
                -height $height \
                -direction Z -color $color]
    }
}

snit::type HDMIButtonBoard_Upsidedown {
    Common
    HDMIConverterDims
    component board
    component mh1
    component mh2
    constructor {args} {
        $self configurelist $args
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_HDMIConv_buttonboardWidth 0 0] \
                        -vec2 [list 0 $_HDMIConv_buttonboardHeight 0]] \
              -vector [list 0 0 $_HDMIConv_boardthickness] \
              -color  {255 165  79}
        lassign $options(-origin) ox oy oz
        install mh1 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_HDMIConv_buttonboardMH1_x}] \
                       [expr {($oy+$_HDMIConv_buttonboardHeight) - $_HDMIConv_buttonboardMH1_y}] \
                       $oz] \
              -radius [expr {$_HDMIConv_buttonboardMHDia / 2.0}] \
              -height $_HDMIConv_boardthickness \
              -direction Z \
              -color {255 255 255}
        install mh2 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_HDMIConv_buttonboardMH2_x}] \
                       [expr {($oy + $_HDMIConv_buttonboardHeight) - $_HDMIConv_buttonboardMH2_y}] \
                       $oz] \
              -radius [expr {$_HDMIConv_buttonboardMHDia / 2.0}] \
              -height $_HDMIConv_boardthickness \
              -direction Z \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $board print $fp
        $mh1 print $fp
        $mh2 print $fp
    }
    method MountingHole {name i zBase height} {
        lassign [[set mh$i] cget -bottom] bx by bz
        return [Cylinder create $name \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
                -height $height \
                -direction Z -color {255 255 255}]
    }
    method Standoff {name i zBase height diameter color} {
        lassign [[set mh$i] cget -bottom] bx by bz
        return [Cylinder create $name \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$diameter / 2.0}] \
                -height $height \
                -direction Z -color $color]
    }
}

snit::type HDMIHVPowerBoard_Upsidedown {
Common
    HDMIConverterDims
    component board
    component mh1
    component mh2
    constructor {args} {
        $self configurelist $args
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_HDMIConv_hvpowerboardWidth 0 0] \
                        -vec2 [list 0 $_HDMIConv_hvpowerboardHeight 0]] \
              -vector [list 0 0 $_HDMIConv_boardthickness] \
              -color  {0 255 0}
        lassign $options(-origin) ox oy oz
        install mh1 using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$ox + $_HDMIConv_hvpowerboardMH1_x1}] \
                                      [expr {($oy + $_HDMIConv_hvpowerboardHeight) - $_HDMIConv_hvpowerboardMH1_y}] \
                                      $oz] \
                        -vec1 [list $_HDMIConv_hvpowerboardMH1_wide 0 0] \
                        -vec2 [list 0 -$_HDMIConv_hvpowerboardMHDia 0]] \
              -vector [list 0 0 $_HDMIConv_boardthickness] \
              -color {255 255 255}
        install mh2 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_HDMIConv_hvpowerboardMH2_x}] \
                       [expr {($oy + $_HDMIConv_hvpowerboardHeight) - $_HDMIConv_hvpowerboardMH2_y}] \
                       $oz] \
              -radius [expr {$_HDMIConv_hvpowerboardMHDia / 2.0}] \
              -height $_HDMIConv_boardthickness \
              -direction Z \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $board print $fp
        $mh1 print $fp
        $mh2 print $fp
    }
    method MountingHole {name i zBase height} {
        if {$i == 1} {
            set holesurf [$mh1 cget -surface]
            lassign [$holesurf cget -cornerpoint] cx cy cz
            set bottom [list [expr {$ox + $_HDMIConv_hvpowerboardMH1_x1 + ($_HDMIConv_hvpowerboardMH1_wide / 2.0)}] \
                        [expr {($cy + $_HDMIConv_hvpowerboardHeight) - ($_HDMIConv_hvpowerboardMHDia/2.a0)}] \
                        $zBase]
            return [Cylinder create $name \
                    -bottom $bottom \
                    -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
                    -height $height \
                    -direction Z -color {255 255 255}]
        } else {
            lassign [[set mh$i] cget -bottom] bx by bz
            return [Cylinder create $name \
                    -bottom [list $bx $by $zBase] \
                    -radius [expr {$_HDMIConv_mainBoardMHDia / 2.0}] \
                    -height $height \
                    -direction Z -color {255 255 255}]
        }
    }
    method Standoff {name i zBase height diameter color} {
        if {$i == 1} {
            set holesurf [$mh1 cget -surface]
            lassign [$holesurf cget -cornerpoint] cx cy cz
            set bottom [list [expr {$ox + $_HDMIConv_hvpowerboardMH1_x1 + ($_HDMIConv_hvpowerboardMH1_wide / 2.0)}] \
                        [expr {($cy + $_HDMIConv_hvpowerboardHeight) - ($_HDMIConv_hvpowerboardMHDia/2.a0)}] \
                        $zBase]
            return [Cylinder create $name \
                    -bottom $bottom \
                    -radius [expr {$diameter / 2.0}] \
                    -height $height \
                    -direction Z -color $color]
        } else {
            lassign [[set mh$i] cget -bottom] bx by bz
            return [Cylinder create $name \
                    -bottom [list $bx $by $zBase] \
                    -radius [expr {$diameter / 2.0}] \
                    -height $height \
                    -direction Z -color $color]
        }
    }
}    

package provide HDMIConverter 1.0
