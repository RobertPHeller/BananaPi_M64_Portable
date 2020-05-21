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
#  Last Modified : <200521.1837>
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
package require HDMIConverter
package require SVGOutput
package require csv

snit::type BananaPiM64Model {
    pragma -hastypeinfo no
    pragma -hastypedestroy no
    pragma -hasinstances no
    typevariable _scriptroot
    typevariable _dirname
    typevariable _default_gcadfile
    typevariable _default_svgfile
    typevariable _default_partsfile
    typevariable _default_postscriptfile
    typevariable _default_leftbracketsvgfile
    typevariable _default_rightbracketsvgfile
    typeconstructor {
        set _scriptroot [file rootname [file tail [info script]]]
        set _dirname [file dirname [file dirname [file dirname \
                                                  [file dirname [info script]]]]]
        set _default_gcadfile [file join $_dirname ${_scriptroot}.gcad]
        set _default_svgfile [file join $_dirname ${_scriptroot}.svg]
        set _default_partsfile [file join $_dirname ${_scriptroot}_parts.csv]
        set _default_postscriptfile [file join $_dirname ${_scriptroot}.ps]
        set _default_leftbracketsvgfile [file join $_dirname ${_scriptroot}_leftbracket.svg]
        set _default_rightbracketsvgfile [file join $_dirname ${_scriptroot}_rightbracket.svg]
    }
    typecomponent m64case
    typecomponent svg
    typemethod Main {argv} {
        if {[from argv -generateall no]} {
            set generategcad yes
            set generatesvg yes
            set generateparts yes
            set generatepostscript yes
            set generateleftbracketsvg yes
            set generaterightbracketsvg yes
        } else {
            set generategcad  [from argv -generategcad no]
            set generatesvg   [from argv -generatesvg no]
            set generateparts [from argv -generateparts no]
            set generatepostscript [from argv -generatepostscript no]
            set generateleftbracketsvg [from argv -generateleftbracketsvg no]
            set generaterightbracketsvg [from argv -generaterightbracketsvg no]
        }
        set sections [from argv -sections all]
        if {$generateleftbracketsvg || $generaterightbracketsvg} {
            if {$sections ne "all" ||
                "Middle" ni $sections} {
                lappend sections Middle
            }
        }
        set m64case [PortableM64Case create %AUTO% \
                     -sections $sections]
        if {$generategcad} {
            set modelFP [open [from argv -gcadfile $_default_gcadfile] w]
            $m64case print $modelFP
            close $modelFP
        }
        if {$generatesvg} {
            set svg [SVGOutput create %AUTO%]
            $m64case svgout $svg {}
            $svg write [from argv -svgfile $_default_svgfile]
        }
        if {$generateparts} {
            $m64case addPart parts
            set partsFP [open [from argv -partsfile $_default_partsfile] w]
            puts $partsFP [::csv::join [list "Panel Size" "Panel Count"]]
            foreach p [lsort -dictionary [array names parts]] {
                puts $partsFP [::csv::join [list $p $parts($p)]]
            }
            close $partsFP
        }
        if {$generatepostscript} {
            PostScriptFile open -filename [from argv -postscriptfile $_default_postscriptfile]
            $m64case printPS
            PostScriptFile close
        }
        if {$generateleftbracketsvg} {
            set leftbracketsvg [$m64case leftbracket SVG3View]
            $leftbracketsvg write [from argv -leftbracketsvgfile $_default_leftbracketsvgfile]
        }
        if {$generaterightbracketsvg} {
            set rightbracketsvg [$m64case rightbracket SVG3View]
            $rightbracketsvg write [from argv -rightbracketsvgfile $_default_rightbracketsvgfile]
        }
    }
}        

BananaPiM64Model Main $::argv

