#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri May 29 14:04:14 2020
#  Last Modified : <200529.2145>
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

snit::macro PianoHingeDims {} {
    typevariable _PianoHinge_Length [expr {12*25.4}]
    typevariable _PianoHinge_Thick  1.00
    typevariable _PianoHinge_FlangeWidth 10.54
    typevariable _PianoHinge_PinDia 4.4
    typevariable _PianoHinge_PinOff 1.2
    typevariable _PianoHinge_HoleDia 4.75
    typevariable _PianoHinge_1stHoleOff [expr {22.25+(4.75/2.0)}]
    typevariable _PianoHinge_Holespace  [expr {46.24+4.75}]
    typevariable _PianoHinge_HoleCount 6
    typevariable _PianoHinge_HoleSideOff [expr {10.54/2.0}]
}

snit::type PianoHingeFlatOutsideBack {
    Common
    PianoHingeDims
    component flange1
    component flange2
    component pin
    variable holes -array {}
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) ox oy oz
        install flange1 using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_PianoHinge_Length 0 0] \
                        -vec2 [list 0 0 $_PianoHinge_FlangeWidth]] \
              -vector [list 0 $_PianoHinge_Thick 0] \
              -color  {190 190 190}
        install pin using Cylinder %AUTO% \
              -bottom [list $ox [expr {$oy + ($_PianoHinge_PinDia / 2)}] \
                       [expr {$oz + $_PianoHinge_FlangeWidth + $_PianoHinge_PinOff + ($_PianoHinge_PinDia / 2)}]] \
              -radius [expr {$_PianoHinge_PinDia / 2}] \
              -height $_PianoHinge_Length \
              -direction X \
              -color {190 190 190}
        install flange2 using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list $ox $oy \
                                      [expr {$oz + $_PianoHinge_FlangeWidth + $_PianoHinge_PinOff + $_PianoHinge_PinDia + $_PianoHinge_PinOff}]] \
                        -vec1 [list $_PianoHinge_Length 0 0] \
                        -vec2 [list 0 0 $_PianoHinge_FlangeWidth]] \
              -vector [list 0 $_PianoHinge_Thick 0] \
              -color  {190 190 190}
        for {set f 1} {$f <= 2} {incr f} {
            set hoff $_PianoHinge_1stHoleOff
            set surf [[set flange$f] cget -surface]
            lassign [$surf cget -cornerpoint] fx fy fz
            for {set h 1} {$h <= 6} {incr h} {
                set holes($f,$h) [Cylinder create %AUTO% \
                                  -bottom [list [expr {$fx +$hoff}] $fy [expr {$fz + $_PianoHinge_HoleSideOff}]] \
                                  -radius [expr {$_PianoHinge_HoleDia / 2.0}] \
                                  -height $_PianoHinge_Thick \
                                  -direction Y \
                                  -color {255 255 255}]
                set hoff [expr {$hoff + $_PianoHinge_Holespace}]
            }
        }
    }
    method print {{fp stdout}} {
        $flange1 print $fp
        $flange2 print $fp
        $pin     print $fp
        foreach n [array names holes] {
            $holes($n) print $fp
        }
    }
    method MountingHole {name f h baseZ height} {
        lassign [$holes($f,$h) cget -bottom] x y z
        set bottom [list $x $y $baseZ]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [$holes($f,$h) cget -radius] \
                -height $height \
                -color {255 255 255}]
    }
}

snit::type PianoHingeFlatInsideClosedFront {
    Common
    PianoHingeDims
    component flange1
    component flange2
    component pin
    variable holes -array {}
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) ox oy oz
        install flange1 using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_PianoHinge_Length 0 0] \
                        -vec2 [list 0 0 $_PianoHinge_FlangeWidth]] \
              -vector [list 0 $_PianoHinge_Thick 0] \
              -color  {190 190 190}
        install pin using Cylinder %AUTO% \
              -bottom [list $ox [expr {$oy + ($_PianoHinge_PinDia / 2)}] \
                       [expr {$oz + $_PianoHinge_FlangeWidth + $_PianoHinge_PinOff + ($_PianoHinge_PinDia / 2)}]] \
              -radius [expr {$_PianoHinge_PinDia / 2}] \
              -height $_PianoHinge_Length \
              -direction X \
              -color {190 190 190}
        install flange2 using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list $ox [expr {$oy + $_PianoHinge_PinDia - $_PianoHinge_Thick}] $oz] \
                        -vec1 [list $_PianoHinge_Length 0 0] \
                        -vec2 [list 0 0 $_PianoHinge_FlangeWidth]] \
              -vector [list 0 $_PianoHinge_Thick 0] \
              -color  {190 190 190}
        for {set f 1} {$f <= 2} {incr f} {
            set hoff $_PianoHinge_1stHoleOff
            set surf [[set flange$f] cget -surface]
            lassign [$surf cget -cornerpoint] fx fy fz
            for {set h 1} {$h <= 6} {incr h} {
                set holes($f,$h) [Cylinder create %AUTO% \
                                  -bottom [list [expr {$fx + $hoff}] $fy [expr {$fz + $_PianoHinge_HoleSideOff}]] \
                                  -radius [expr {$_PianoHinge_HoleDia / 2.0}] \
                                  -height $_PianoHinge_Thick \
                                  -direction Y \
                                  -color {255 255 255}]
                set hoff [expr {$hoff + $_PianoHinge_Holespace}]
            }
        }
    }
    method print {{fp stdout}} {
        $flange1 print $fp
        $flange2 print $fp
        $pin     print $fp
        foreach n [array names holes] {
            $holes($n) print $fp
        }
    }
    method MountingHole {name f h baseZ height} {
        lassign [$holes($f,$h) cget -bottom] x y z
        set bottom [list $x $y $baseZ]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [$holes($f,$h) cget -radius] \
                -height $height \
                -color {255 255 255}]
    }
}


package provide PianoHinge 1.0

