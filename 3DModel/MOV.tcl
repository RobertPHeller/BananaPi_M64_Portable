#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:47:52 2020
#  Last Modified : <200509.1911>
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

snit::type B72220S2301K101 {
    Common
    typevariable _W 21.5
    typevariable _th 6.1
    typevariable _h 25.5
    typevariable _d 1.0
    typevariable _e 10
    typevariable _a 2.1
    typevariable _l 25.0
    typevariable _seatoffset 3
    typevariable _leadspacing [expr {8 * 2.54}]
    component body
    component seat1
    component seat2
    component lead1h
    component lead2h
    component lead1v
    component lead2v
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) xc yc zc
        set bodyradius [expr {$_W / 2.0}]
        install body using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc -  $bodyradius}] $zc] \
              -radius $bodyradius \
              -direction Z \
              -height -$_th \
              -color {0 0 0}
        install seat1 using Cylinder %AUTO% \
              -bottom [list [expr {$xc - ($_e/2.0)}] [expr {$yc + ($_seatoffset*.5)}] [expr {($zc - ($_th/2.0)) - ($_a/2.0)}]] \
              -radius $_d \
              -direction Y \
              -height [expr {$_seatoffset*(-1.5)}] \
              -color {0 0 0}
        install seat2 using Cylinder %AUTO% \
              -bottom [list [expr {$xc + ($_e/2.0)}] [expr {$yc + ($_seatoffset*.5)}] [expr {($zc - ($_th/2.0)) + ($_a/2.0)}]] \
              -radius $_d \
              -direction Y \
              -height [expr {$_seatoffset*(-1.5)}] \
              -color {0 0 0}
        set leadhlen [expr {($_leadspacing/2.0)-($_e/2.0)}]
        install lead1h using Cylinder %AUTO% \
              -bottom [list [expr {$xc - ($_e/2.0)}] \
                             [expr {$yc + ($_seatoffset*.5)}] \
                       [expr {($zc - ($_th/2.0)) - ($_a/2.0)}]] \
              -radius [expr {$_d / 2.0}] \
              -direction X \
              -height -$leadhlen \
              -color {250 250 250}
        lassign [$lead1h cget -bottom] l1x l1y l1z
        set l1vheight [expr {abs($zc-(((1/16.0)*2.54)) + $l1z)}]
        #puts stderr "*** $type create $self: zc = $zc, l1z = $l1z, l1vheight = $l1vheight"
        set l1vx      [expr {$l1x - $leadhlen}]
        install lead1v using Cylinder %AUTO% \
              -bottom [list $l1vx $l1y $l1z] \
              -radius [expr {$_d / 2.0}] \
              -direction Z \
              -height $l1vheight \
              -color {250 250 250}
        install lead2h using Cylinder %AUTO% \
              -bottom [list [expr {$xc + ($_e/2.0)}] \
                       [expr {$yc + ($_seatoffset*.5)}] \
                       [expr {($zc - ($_th/2.0)) + ($_a/2.0)}]] \
              -radius [expr {$_d / 2.0}] \
              -direction X \
              -height $leadhlen \
              -color {250 250 250}
        lassign [$lead2h cget -bottom] l2x l2y l2z
        set l2vheight [expr {abs($zc-(((1/16.0)*2.54)) + $l2z)}]
        set l2vx      [expr {$l2x + $leadhlen}]
        install lead2v using Cylinder %AUTO% \
              -bottom [list $l2vx $l2y $l2z] \
              -radius [expr {$_d / 2.0}] \
              -direction Z \
              -height $l2vheight \
              -color {250 250 250}
    }
    method print {{fp stdout}} {
        $body print $fp
        $seat1 print $fp
        $seat2 print $fp
        $lead1h print $fp
        $lead1v print $fp
        $lead2h print $fp
        $lead2v print $fp

    }
}

package provide MOV 1.0
