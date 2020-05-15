#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri May 15 07:49:02 2020
#  Last Modified : <200515.1112>
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
package require LCDScreen

snit::macro BracketAngleDims {} {
    typevariable _AngleHeight [expr {(1.0/2.0)*25.4}]
    typevariable _AngleWidth [expr {(1.0/2.0)*25.4}]
    typevariable _AngleThickness [expr {(1.0/16.0)*25.4}]
    typevariable _AngleLength 222.0
    typevariable _BRACKET_r [expr {3.5 / 2.0}]
    typevariable _BRACKET_z [expr {(1.0/4.0)*25.4}]
}

snit::enum Side -values {L R}

snit::type LCDMountingBracket {
    LCDDims
    BracketAngleDims
    Common
    option -side -type Side -default L -readonly yes
    component angle
    component lcdm1
    component lcdm2
    component lcdm3
    component lcdm4
    component bracketm1
    component bracketm2
    component bracketm3
    component bracketm4
    constructor {args} {
        $self configurelist $args
        switch $options(-side) {
            L {
                install angle using Angle %AUTO% \
                      -origin $options(-origin) \
                      -height -$_AngleHeight \
                      -width  -$_AngleWidth \
                      -length $_AngleLength \
                      -thickness $_AngleThickness \
                      -direction Y -color {100 100 100}
                install lcdm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM1_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM2_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM3_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM4_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install bracketm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM1_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM2_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM3_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM4_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
            }
            R {
                install angle using Angle %AUTO% \
                      -origin $options(-origin) \
                      -height -$_AngleHeight \
                      -width  $_AngleWidth \
                      -length $_AngleLength \
                      -thickness $_AngleThickness \
                      -direction Y -color {100 100 100}
                install lcdm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM1_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM2_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM3_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM4_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install bracketm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM1_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM2_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM3_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM4_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
            }
        }
    }
    method MountingHole {name i zBase height} {
        lassign [[set bracketm$i] cget -bottom] hx hy hz
        return [Cylinder create $name \
                -bottom [list $hx $hy $zBase] \
                -radius $_BRACKET_r \
                -height $height \
                -color {255 255 255} \
                -direction Z]
    }
    method print {{fp stdout}} {
        $angle print $fp
        $lcdm1 print $fp
        $lcdm2 print $fp
        $lcdm3 print $fp
        $lcdm4 print $fp
        $bracketm1 print $fp
        $bracketm2 print $fp
        $bracketm3 print $fp
        $bracketm4 print $fp
        
    }
}

package provide LCDMountingBracket 1.0
