#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon May 18 08:40:35 2020
#  Last Modified : <200518.1617>
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

snit::macro TeensyThumbStickDims {} {
    typevariable _TeensyThumbStick_Width 68.62
    typevariable _TeensyThumbStick_Height 65.35
    typevariable _TeensyThumbStick_BoardThick 1.6
    typevariable _TeensyThumbStick_ThumbHeight [expr {18.45-1.6}]
    typevariable _TeensyThumbStick_ThumbX 55.28
    typevariable _TeensyThumbStick_ThumbY 45.48
    typevariable _TeensyThumbStick_ThumbDia 14.22
    typevariable _TeensyThumbStick_TeensyHeight [expr {17-1.6}]
    typevariable _TeensyThumbStick_TeensyLength 35.57
    typevariable _TeensyThumbStick_TeensyWidth 17.77
    typevariable _TeensyThumbStick_TeensyX 0
    typevariable _TeensyThumbStick_TeensyY [expr {65.35-(8.63+17.77)}]
    typevariable _TeensyThumbStick_MHWidth 61.49
    typevariable _TeensyThumbStick_MHHeight 60.86
    typevariable _TeensyThumbStick_MHDia [expr {.125*25.4}]
    typevariable _TeensyThumbStick_CoverThick [expr {.0625*25.4}]
    typevariable _TeensyThumbStick_CoverCutoutX 0
    typevariable _TeensyThumbStick_CoverCutoutY 30.5
    typevariable _TeensyThumbStick_CoverCutoutWidth 68.62
    typevariable _TeensyThumbStick_CoverCutoutHeight [expr {34.39-6.35}]
    typevariable _TeensyThumbStick_CoverButtonHoleY 19.62
    typevariable _TeensyThumbStick_CoverButtonHole1X 48.59
    typevariable _TeensyThumbStick_CoverButtonHole2X 56.28
    typevariable _TeensyThumbStick_CoverButtonHole3X 63.94
    typevariable _TeensyThumbStick_CoverButtonHoleDia 5.08
}

snit::type TeensyThumbStick {
    Common
    TeensyThumbStickDims
    component board
    component thumbstick
    component teensy
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
                        -vec1 [list $_TeensyThumbStick_Width 0 0] \
                        -vec2 [list 0 $_TeensyThumbStick_Height 0]] \
              -vector [list 0 0 $_TeensyThumbStick_BoardThick] \
              -color {210 180 140}
        lassign $options(-origin) ox oy oz
        set z [expr {$oz + $_TeensyThumbStick_BoardThick}]
        install thumbstick using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_TeensyThumbStick_ThumbX}] \
                       [expr {$oy + $_TeensyThumbStick_ThumbY}] $z] \
              -radius [expr {$_TeensyThumbStick_ThumbDia / 2.0}] \
              -height $_TeensyThumbStick_ThumbHeight \
              -direction Z \
              -color {0 0 0}
        install teensy using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$ox + $_TeensyThumbStick_TeensyX}] \
                                      [expr {$oy + $_TeensyThumbStick_TeensyY}] $z] \
                        -vec1 [list $_TeensyThumbStick_TeensyLength 0 0] \
                        -vec2 [list 0 $_TeensyThumbStick_TeensyWidth 0]] \
              -vector [list 0 0 $_TeensyThumbStick_TeensyHeight] \
              -color  {0 192 0}
        set mh1X [expr {($_TeensyThumbStick_Width - $_TeensyThumbStick_MHWidth)/2.0}]
        set mh1Y [expr {($_TeensyThumbStick_Height - $_TeensyThumbStick_MHHeight) / 2.0}]
        install mh1 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh1X}] [expr {$oy + $mh1Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_BoardThick \
              -direction Z \
              -color {255 255 255}
        set mh2X [expr {$mh1X + $_TeensyThumbStick_MHWidth}]
        set mh2Y $mh1Y
        install mh2 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh2X}] [expr {$oy + $mh2Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_BoardThick \
              -direction Z \
              -color {255 255 255}
        set mh3X $mh2X
        set mh3Y [expr {$mh2Y + $_TeensyThumbStick_MHHeight}]
        install mh3 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh3X}] [expr {$oy + $mh3Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_BoardThick \
              -direction Z \
              -color {255 255 255}
        set mh4X $mh1X
        set mh4Y $mh3Y
        install mh4 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh4X}] [expr {$oy + $mh4Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_BoardThick \
              -direction Z \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $board print $fp
        $thumbstick print $fp
        $teensy print $fp
        $mh1 print $fp
        $mh2 print $fp
        $mh3 print $fp
        $mh4 print $fp
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
    method Standoff {name i baseZ height diameter color} {
        lassign [[set mh$i] cget -bottom] x y z
        set bottom [list $x $y $baseZ]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [expr {$diameter / 2.0}] \
                -height $height \
                -color $color]
    }
}        

snit::type TeensyThumbStickCover {
    Common
    TeensyThumbStickDims
    component coverpanel
    component mh1
    component mh2
    component mh3
    component mh4
    component button1hole
    component button2hole
    component button3hole
    component cutout
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) ox oy oz
        #puts stderr "*** $type create $self: options(-origin) is $options(-origin)"
        install coverpanel using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$ox - 6.35}] $oy $oz] \
                        -vec1 [list [expr {$_TeensyThumbStick_Width + 12.7}] 0 0] \
                        -vec2 [list 0 $_TeensyThumbStick_Height 0]] \
              -vector [list 0 0 $_TeensyThumbStick_CoverThick] \
              -color {240 240 240}
        #puts stderr "*** $type create $self: coverpanel := "
        #puts stderr "***    -surface := "
        #puts stderr "***        -rectangle   [[$coverpanel cget -surface] cget -rectangle]"
        #puts stderr "***        -cornerpoint [[$coverpanel cget -surface] cget -cornerpoint]"
        #puts stderr "***        -vec1        [[$coverpanel cget -surface] cget -vec1]"
        #puts stderr "***        -vec2        [[$coverpanel cget -surface] cget -vec2]"
        #puts stderr "***    -vector [$coverpanel cget -vector]"
        #puts stderr "***    -color  [$coverpanel cget -color]"
        set mh1X [expr {($_TeensyThumbStick_Width - $_TeensyThumbStick_MHWidth)/2.0}]
        set mh1Y [expr {($_TeensyThumbStick_Height - $_TeensyThumbStick_MHHeight) / 2.0}]
        install mh1 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh1X}] [expr {$oy + $mh1Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_CoverThick \
              -direction Z \
              -color {255 255 255}
        set mh2X [expr {$mh1X + $_TeensyThumbStick_MHWidth}]
        set mh2Y $mh1Y
        install mh2 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh2X}] [expr {$oy + $mh2Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_CoverThick \
              -direction Z \
              -color {255 255 255}
        set mh3X $mh2X
        set mh3Y [expr {$mh2Y + $_TeensyThumbStick_MHHeight}]
        install mh3 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh3X}] [expr {$oy + $mh3Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_CoverThick \
              -direction Z \
              -color {255 255 255}
        set mh4X $mh1X
        set mh4Y $mh3Y
        install mh4 using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mh4X}] [expr {$oy + $mh4Y}] $oz] \
              -radius [expr {$_TeensyThumbStick_MHDia / 2.0}] \
              -height $_TeensyThumbStick_CoverThick \
              -direction Z \
              -color {255 255 255}
        install cutout using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$ox + $_TeensyThumbStick_CoverCutoutX}] \
                                      [expr {$oy + $_TeensyThumbStick_CoverCutoutY}] $oz] \
                        -vec1 [list $_TeensyThumbStick_CoverCutoutWidth 0 0] \
                        -vec2 [list 0 $_TeensyThumbStick_CoverCutoutHeight 0]] \
              -vector [list 0 0 $_TeensyThumbStick_CoverThick] \
              -color {0 0 0}
        install button1hole using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_TeensyThumbStick_CoverButtonHole1X}] \
                       [expr {$oy + $_TeensyThumbStick_CoverButtonHoleY}] $oz] \
              -radius [expr {$_TeensyThumbStick_CoverButtonHoleDia / 2.0}] \
              -height $_TeensyThumbStick_CoverThick \
              -direction Z \
              -color {0 0 0}
        #puts stderr "*** $type create $self: button1hole := "
        #puts stderr "***    -bottom    [$button1hole cget -bottom]"
        #puts stderr "***    -radius    [$button1hole cget -radius]"
        #puts stderr "***    -height    [$button1hole cget -height]"
        #puts stderr "***    -direction [$button1hole cget -direction]"
        #puts stderr "***    -color     [$button1hole cget -color]"
        install button2hole using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_TeensyThumbStick_CoverButtonHole2X}] \
                       [expr {$oy + $_TeensyThumbStick_CoverButtonHoleY}] $oz] \
              -radius [expr {$_TeensyThumbStick_CoverButtonHoleDia / 2.0}] \
              -height $_TeensyThumbStick_CoverThick \
              -direction Z \
              -color {0 0 0}
        install button3hole using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $_TeensyThumbStick_CoverButtonHole3X}] \
                       [expr {$oy + $_TeensyThumbStick_CoverButtonHoleY}] $oz] \
              -radius [expr {$_TeensyThumbStick_CoverButtonHoleDia / 2.0}] \
              -height $_TeensyThumbStick_CoverThick \
              -direction Z \
              -color {0 0 0}
    }
    method print {{fp stdout}} {
        $coverpanel print $fp
        $mh1 print $fp
        $mh2 print $fp
        $mh3 print $fp
        $mh4 print $fp
        $button1hole print $fp
        $button2hole print $fp
        $button3hole print $fp
        $cutout print $fp
    }
}

package provide TeensyThumbStick 1.0
