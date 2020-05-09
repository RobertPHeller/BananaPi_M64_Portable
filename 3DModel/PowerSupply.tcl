#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:33:36 2020
#  Last Modified : <200509.1439>
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

## Power Supply: Mouser #490-PSK-S15C-5
# PCB mount, 28.8mm wide 53.8mm long, 23.5mm high

snit::macro PSDims {} {
    typevariable _pswidth 28.8
    typevariable _pslength 53.8
    typevariable _psheight 23.5
    typevariable _pspindia 1.0
    typevariable _pspinlength 6.0
    typevariable _pspin1Xoff [expr {((53.8-45.72)/2.0)+45.72}]
    typevariable _pspin1Yoff [expr {((28.8-20.32)/2.0)+20.32}]
    typevariable _pspin2Xoff [expr {((53.8-45.72)/2.0)+45.72}]
    typevariable _pspin2Yoff [expr {(28.8-20.32)/2.0}]
    typevariable _pspin3Xoff [expr {(53.8-45.72)/2.0}]
    typevariable _pspin3Yoff [expr {((28.8-20.32)/2.0)+10.16}]
    typevariable _pspin4Xoff [expr {(53.8-45.72)/2.0}]
    typevariable _pspin4Yoff [expr {((28.8-20.32)/2.0)+20.32}]
}

snit::type PSK_S15C {
    # 490-PSK-S15C-5
    PSDims
    Common
    component body
    component pin1
    component pin2
    component pin3
    component pin4
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list 0 $_pslength 0] \
                        -vec2 [list $_pswidth 0 0]] \
              -vector [list 0 0 $_psheight] \
              -color [list 0 0 0]
        install pin1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin1Yoff $_pspin1Xoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 255}
        install pin2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin2Yoff $_pspin2Xoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 255}
        install pin3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin3Yoff $_pspin3Xoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 255}
        install pin4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin4Yoff $_pspin4Xoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 244}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
        $pin3 print $fp
        $pin4 print $fp
    }
}


package provide PowerSupply 1.0
