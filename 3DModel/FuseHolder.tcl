#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:43:33 2020
#  Last Modified : <200509.1344>
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

# 576-30313150421 3.15A fuse

snit::type Littlefuse_FuseHolder_02810007H_02810010H {
    Common
    typevariable _width     [expr {0.25*25.4}]
    typevariable _length    [expr {0.28*25.4}]
    typevariable _height    [expr {0.26*25.4}]
    typevariable _pinlen    [expr {0.20*25.4}]
    typevariable _pindia    [expr {0.046*25.4}]
    typevariable _pinXspace [expr {0.1*25.4}]
    typevariable _pinYspace [expr {0.20*25.4}]
    component body
    component pin1
    component pin2
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) xc yc zc
        set w2 [expr {$_width / 2.0}]
        set l2 [expr {$_length / 2.0}]
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$xc - $w2}] \
                                      [expr {$yc - $l2}] $zc] \
                        -vec1 [list $_width 0 0] \
                        -vec2 [list 0 $_length 0]] \
              -vector [list 0 0 $_height] \
              -color {255 255 255}
        install pin1 using Cylinder %AUTO% \
              -bottom [list [expr {$xc - ($_pinXspace / 2.0)}] \
                       [expr {$yc - ($_pinYspace / 2.0)}] \
                       $zc] \
              -radius [expr {$_pindia / 2.0}] \
              -direction Z \
              -height -$_pinlen \
              -color {200 200 200}
        install pin2 using Cylinder %AUTO% \
              -bottom [list [expr {$xc + ($_pinXspace / 2.0)}] \
                       [expr {$yc + ($_pinYspace / 2.0)}] \
                       $zc] \
              -radius [expr {$_pindia / 2.0}] \
              -direction Z \
              -height -$_pinlen \
              -color {200 200 200}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
    }
}

package provide FuseHolder 1.0
