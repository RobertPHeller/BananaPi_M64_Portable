#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 16 13:36:56 2020
#  Last Modified : <200517.1329>
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
package require ParseXML
package require Common

# Viewport type: exactly four doubles
snit::listtype ViewPort -type snit::double -minlen 4 -maxlen 4

snit::type SVGOutput {
    typevariable emptySVGFormat {<svg version="1.1" 
        xmlns="http://www.w3.org/2000/svg" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        x="0%s" y="0%s" width="%f%s" height="%f%s" 
        viewBox="%f %f %f %f" xml:space="preserve" />}
    # Method to put out the pre-XML header blather
    proc xmlheader {fp} {
        puts $fp {<?xml version="1.0" encoding="utf-8"?>}
        puts $fp "<!-- Generator: [file tail $::argv0] -->"
    }
    component xml
    variable viewport
    proc _compute_viewport {units width height vpunits} {
        if {$units eq $vpunits} {
            return [list 0 0 $width $height]
        }
        switch $units {
            in {
                return [list 0 0 [expr {$width * 25.4}] [expr {$height * 25.4}]]
            }
            mm {
                return [list 0 0 [expr {$width / 25.4}] [expr {$height / 25.4}]]
            }
        }
    }
    option -units -type Units -default in -readonly yes
    option -width -type snit::double -default 24 -readonly yes
    option -height -type snit::double -default 48 -readonly yes
    option -vpunits -type Units -default mm -readonly yes 
    constructor {args} {
        $self configurelist $args
        set viewport [_compute_viewport $options(-units) $options(-width) $options(-height) $options(-vpunits)]
        set emptySVG [format $emptySVGFormat \
                 $options(-units) $options(-units) $options(-width) \
                 $options(-units) $options(-height) $options(-units) \
                 [lindex $viewport 0] [lindex $viewport 1] \
                 [lindex $viewport 2] [lindex $viewport 3]]
        set xml [ParseXML %AUTO% $emptySVG]
    }
    method translateTransform {dx dy} {
        return [format {translate(%g,%g)} $dx $dy]
    }
    method rotateTransform {degrees} {
        return [format {rotate(%g)} $degrees]
    }
    method newgroup {name {transform {}} {parent {}}} {
        if {$parent eq {}} {
            set parent [$xml getElementsByTagName svg]
        }
        set attributes [list id $name]
        if {$transform ne ""} {
            lappend attributes transform $transform
        }
        set newgroup [SimpleDOMElement create %AUTO% -tag g -attributes $attributes]
        $parent addchild $newgroup
        return $newgroup
    }
    method addrect {x y width height parent} {
        set newrect [SimpleDOMElement create %AUTO% -tag rect \
                     -attributes [list x $x y $y width $width height $height fill none stroke black stroke-width 1]]
        $parent addchild $newrect
    }
    method addcircle {cx cy r parent} {
        set newcircle [SimpleDOMElement create %AUTO% -tag circle \
                       -attributes [list cx $cx cy $cy r $r fill black stroke none]]
        $parent addchild $newcircle
    }
    method write {filename} {
        set fp [open $filename w]
        xmlheader $fp
        $xml displayTree $fp
        close $fp
    }
}




package provide SVGOutput 1.0
