#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue May 19 09:04:37 2020
#  Last Modified : <200519.0952>
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

snit::macro SpeakerDims {} {
    typevariable _Speaker_Width 18.86
    typevariable _Speaker_Length 93.71
    typevariable _Speaker_Thickness 7.14
    typevariable _Speaker_MHoleDia 2.5
    typevariable _Speaker_LTopHoleX [expr {6.43 + (2.5/2.0)}]
    typevariable _Speaker_RTopHoleX [expr {10.29 + (2.5/2.0)}]
    typevariable _Speaker_TopHoleY [expr {84.5 + (2.5/2.0)}]
    typevariable _Speaker_LBottomHoleX [expr {8.2 + (2.5/2.0)}]
    typevariable _Speaker_RBottomHoleX [expr {8.41 + (2.5/2.0)}]
    typevariable _Speaker_BottomHoleY [expr {4.66 + (2.5/2.0)}]
    typevariable _Speaker_StandoffRecessDia 6.16
    typevariable _Speaker_StandoffRecessDepth 3.15
}

snit::type SpeakerLeft_UpsideDown {
    Common
    SpeakerDims
    component body
    component mhtop
    component mhbottom
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_Speaker_Width 0 0] \
                        -vec2 [list 0 $_Speaker_Length 0]] \
              -vector [list 0 0 -$_Speaker_Thickness] \
              -color  {0 0 0}
        lassign $options(-origin) ox oy oz
        set mhTopX $_Speaker_LTopHoleX
        set mhTopY [expr {$_Speaker_Length - $_Speaker_TopHoleY}]
        install mhtop using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mhTopX}] [expr {$oy + $mhTopY}] $oz] \
              -radius [expr {$_Speaker_MHoleDia / 2.0}] \
              -height -$_Speaker_Thickness \
              -direction Z -color {255 255 255}
        set mhBottomX $_Speaker_LBottomHoleX
        set mhBottomY [expr {$_Speaker_Length - $_Speaker_BottomHoleY}]
        install mhbottom using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mhBottomX}] [expr {$oy + $mhBottomY}] $oz] \
              -radius [expr {$_Speaker_MHoleDia / 2.0}] \
              -height -$_Speaker_Thickness \
              -direction Z -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $mhtop print $fp
        $mhbottom print $fp
    }
    method MountingHole {name which zBase height} {
        lassign [[set mh$which] cget -bottom] bx by dummy
        return [Cylinder create %AUTO% \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$_Speaker_MHoleDia / 2.0}] \
                -height $height -direction Z -color {255 255 255}]
    }
    method Standoff {name which zBase height diameter color} {
        lassign [[set mh$which] cget -bottom] bx by dummy
        return [Cylinder create %AUTO% \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$diameter / 2.0}] \
                -height $height -direction Z -color $color]
    }
}
    
snit::type SpeakerRight_UpsideDown {
    Common
    SpeakerDims
    component body
    component mhtop
    component mhbottom
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_Speaker_Width 0 0] \
                        -vec2 [list 0 $_Speaker_Length 0]] \
              -vector [list 0 0 -$_Speaker_Thickness] \
              -color  {0 0 0}
        lassign $options(-origin) ox oy oz
        set mhTopX $_Speaker_RTopHoleX
        set mhTopY [expr {$_Speaker_Length - $_Speaker_TopHoleY}]
        install mhtop using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mhTopX}] [expr {$oy + $mhTopY}] $oz] \
              -radius [expr {$_Speaker_MHoleDia / 2.0}] \
              -height -$_Speaker_Thickness \
              -direction Z -color {255 255 255}
        set mhBottomX $_Speaker_RBottomHoleX
        set mhBottomY [expr {$_Speaker_Length - $_Speaker_BottomHoleY}]
        install mhbottom using Cylinder %AUTO% \
              -bottom [list [expr {$ox + $mhBottomX}] [expr {$oy + $mhBottomY}] $oz] \
              -radius [expr {$_Speaker_MHoleDia / 2.0}] \
              -height -$_Speaker_Thickness \
              -direction Z -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $mhtop print $fp
        $mhbottom print $fp
    }
    method MountingHole {name which zBase height} {
        lassign [[set mh$which] cget -bottom] bx by dummy
        return [Cylinder create %AUTO% \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$_Speaker_MHoleDia / 2.0}] \
                -height $height -direction Z -color {255 255 255}]
    }
    method Standoff {name which zBase height diameter color} {
        lassign [[set mh$which] cget -bottom] bx by dummy
        return [Cylinder create %AUTO% \
                -bottom [list $bx $by $zBase] \
                -radius [expr {$diameter / 2.0}] \
                -height $height -direction Z -color $color]
    }
}
    
    
package provide Speaker 1.0
