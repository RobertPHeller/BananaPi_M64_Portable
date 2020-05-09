#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:39:13 2020
#  Last Modified : <200509.1341>
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

snit::macro TB007_508_xxBE {} {
    typevariable _termwidth 8.2
    typevariable _termheight 10.0
    typevariable _termpitch  5.08
    typevariable _3belength 15.24
    typevariable _2belength 10.16
    typevariable _termhyoff 2.54
    typevariable _termhxoff 4.10
    typevariable _termpindia 1.3
    typevariable _termpinlen 3.8
}


snit::type TB007_508_03BE {
    TB007_508_xxBE
    Common
    component body
    component pin1
    component pin2
    component pin3
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_termwidth 0 0] \
                        -vec2 [list 0 $_3belength 0]] \
              -vector [list 0 0 $_termheight] \
              -color  [list 0 0 255]
        install pin1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff $_termhyoff 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
        install pin2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff [expr {$_termhyoff + $_termpitch}] 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
        install pin3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff [expr {$_termhyoff + (2*$_termpitch)}] 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
        $pin3 print $fp
    }
}

snit::type TB007_508_02BE {
    TB007_508_xxBE
    Common
    component body
    component pin1
    component pin2
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_termwidth 0 0] \
                        -vec2 [list 0 $_2belength 0]] \
              -vector [list 0 0 $_termheight] \
              -color  [list 0 0 255]
        install pin1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff $_termhyoff 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
        install pin2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff [expr {$_termhyoff + $_termpitch}] 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
    }
}

package provide TerminalBlocks 1.0
