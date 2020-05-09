#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:45:19 2020
#  Last Modified : <200509.1346>
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

snit::type C333 {
    Common
    typevariable _C333_L 7.11
    typevariable _C333_H 10.16
    typevariable _C333_T 4.07
    typevariable _C333_LeadSpacing 5.08
    typevariable _C333_LeadDia 0.51
    typevariable _C333_LL 7.00
    component body
    component lead1
    component lead2
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) xc yc zc
        set w2 [expr {$_C333_L / 2.0}]
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list $xc [expr {$yc - $w2}] $zc] \
                        -vec1 [list -$_C333_H 0 0] \
                        -vec2 [list 0 $_C333_L 0]] \
              -vector [list 0 0 -$_C333_T] \
              -color  {255 255 0}
        set ls2 [expr {$_C333_LeadSpacing / 2.0}]
        set t2  [expr {$_C333_T / 2.0}]
        install lead1 using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc - $ls2}] [expr {$zc - $t2}]] \
              -radius [expr {$_C333_LeadDia / 2.0}] \
              -direction X \
              -height $_C333_LL \
              -color {192 192 192}
        install lead2 using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc + $ls2}] [expr {$zc - $t2}]] \
              -radius [expr {$_C333_LeadDia / 2.0}] \
              -direction X \
              -height $_C333_LL \
              -color {192 192 192}
    }
    method print {{fp stdout}} {
        $body  print $fp
        $lead1 print $fp
        $lead2 print $fp
    }
}


snit::type AL_CAP_Radial_5mm10x12.5 {
    Common
    typevariable _diameter 10
    typevariable _length  12.5
    typevariable _leaddia .6
    typevariable _leadspacing 5
    typevariable _leadlength [expr {(1.25/16.0)*25.4}]
    component body
    component lead1
    component lead2
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) xc yc zc
        set bodyradius [expr {$_diameter / 2.0}]
        install body using Cylinder %AUTO% \
              -bottom $options(-origin) \
              -radius $bodyradius \
              -height $_length \
              -direction Z \
              -color {240 240 240}
        install lead1 using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc - ($_leadspacing / 2.0)}] $zc] \
              -radius [expr {$_leaddia / 2.0}] \
              -direction Z \
              -height -$_leadlength \
              -color {192 192 192}
        install lead2 using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc + ($_leadspacing / 2.0)}] $zc] \
              -radius [expr {$_leaddia / 2.0}] \
              -direction Z \
              -height -$_leadlength \
              -color {192 192 192}
    }
    method print {{fp stdout}} {
        $body print $fp
        $lead1 print $fp
        $lead2 print $fp
    }
}

package provide Capacitors 1.0
