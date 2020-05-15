#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 08:43:51 2020
#  Last Modified : <200515.0917>
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


package require snit
package require Common
package require M64
package require PSBox
package require Case
package require DCDC_5_12
package require LCDMountingBracket
package require LCDScreen

set scriptroot [file rootname [file tail [info script]]]
set dirname [file dirname [file dirname [file dirname \
                                         [file dirname [info script]]]]]


set gcadfile [file join $dirname ${scriptroot}.gcad]

set modelFP [open $gcadfile w]

GCadPrefix $modelFP

PortableM64Case create m64case
#m64case print $modelFP

#PSOnPCB create pcb -origin [list 0 0 -100]
#pcb print $modelFP

#DCDC_5_12_Horiz12Right create dcdcvert
#dcdcvert print $modelFP

LCDMountingBracket create left -side L -origin {0 0 0}
LCDMountingBracket create right -side R -origin [list 344 0 0]
LCDScreen create screen -origin [list 0 0 [expr {-((6.5/2.0)+(((1.0/2.0)*25.4)/2.0))}]]

left print $modelFP
right print $modelFP
screen print $modelFP

close $modelFP

m64case addPart parts

PostScriptFile open -filename [file join $dirname ${scriptroot}.ps]
m64case printPS
PostScriptFile close

package require csv

set partsFP [open [file join $dirname ${scriptroot}_parts.csv] w]

puts $partsFP [::csv::join [list "Panel Size" "Panel Count"]]

foreach p [lsort -dictionary [array names parts]] {
    puts $partsFP [::csv::join [list $p $parts($p)]]
}
close $partsFP

