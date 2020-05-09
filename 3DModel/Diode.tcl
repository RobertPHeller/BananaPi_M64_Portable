#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:46:43 2020
#  Last Modified : <200509.1642>
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

snit::type DO_15_bendedLeads_400_under {
    Common
    typevariable _bodydia 3.6
    typevariable _bodylen 7.6
    typevariable _leadspacing [expr {.400*25.4}]
    typevariable _leaddia 0.9
    typevariable _totalleadLength 25.4
    component body
    component lead1h
    component lead2h
    component lead1v
    component lead2v
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) xc yc zc
        set l2 [expr {$_bodylen / 2.0}]
        set brad [expr {$_bodydia / 2.0}]
        set leadhlen [expr {($_leadspacing-$_bodylen)/2.0}]
        set availleadvlen [expr {$_totalleadLength - $leadhlen}]
        set leadvlen [expr {$brad+((1.0/16.0)*25.4)}]
        if {$leadvlen > $availleadvlen} {set leadvlen $availleadvlen}
        install body using Cylinder %AUTO% \
              -bottom [list [expr {$xc - $l2}] $yc [expr {$zc - $brad}]] \
              -radius $brad \
              -height $_bodylen \
              -direction X \
              -color {50 50 50}
        install lead1h using Cylinder %AUTO% \
              -bottom [list [expr {$xc - $l2}] $yc [expr {$zc - $brad}]] \
              -radius [expr {$_leaddia/2.0}] \
              -height -$leadhlen \
              -direction X \
              -color {250 250 250}
        install lead2h using Cylinder %AUTO% \
              -bottom [list [expr {$xc + $l2}] $yc [expr {$zc - $brad}]] \
              -radius [expr {$_leaddia/2.0}] \
              -height $leadhlen \
              -direction X \
              -color {250 250 250}
        install lead1v using Cylinder %AUTO% \
              -bottom [list [expr {$xc - ($_leadspacing/2.0)}] $yc [expr {$zc - $brad}]] \
              -radius [expr {$_leaddia/2.0}] \
              -height $leadvlen \
              -direction Z \
              -color {250 250 250}
        install lead2v using Cylinder %AUTO% \
              -bottom [list [expr {$xc + ($_leadspacing/2.0)}] $yc [expr {$zc - $brad}]] \
              -radius [expr {$_leaddia/2.0}] \
              -height $leadvlen \
              -direction Z \
              -color {250 250 250}
        
    }
    method print {{fp stdout}} {
        $body print $fp
        $lead1h print $fp
        $lead2h print $fp
        $lead1v print $fp
        $lead2v print $fp
    }
}

package provide Diode 1.0
