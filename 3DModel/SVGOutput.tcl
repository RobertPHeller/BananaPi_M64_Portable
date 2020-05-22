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
#  Last Modified : <200522.1614>
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
    typevariable _ArrowOutEndAttributes {id "ArrowOutEnd"
        viewBox "0 0 10 10" refX "10" refY "5"
        markerUnits "strokeWidth"
        markerWidth "4" markerHeight "3"
        orient "auto"
    }
    typevariable _ArrowPathEndOut {M 0 0 L 10 5 L 0 10 z}
    typevariable _ArrowInEndAttributes {id "ArrowInEnd"
        viewBox "0 0 10 10" refX "0" refY "5"
        markerUnits "strokeWidth"
        markerWidth "4" markerHeight "3"
        orient "auto"
    }
    typevariable _ArrowPathEndIn {M 0 5 L 10 0 L 10 10 z}
    typevariable _ArrowOutStartAttributes {id "ArrowOutStart"
        viewBox "0 0 10 10" refX "0" refY "5"
        markerUnits "strokeWidth"
        markerWidth "4" markerHeight "3"
        orient "auto"
    }
    typevariable _ArrowPathStartOut {M 0 5 L 10 0 L 10 10 z}
    typevariable _ArrowInStartAttributes {id "ArrowInStart"
        viewBox "0 0 10 10" refX "10" refY "5"
        markerUnits "strokeWidth"
        markerWidth "4" markerHeight "3"
        orient "auto"
    }
    typevariable _ArrowPathStartIn {M 0 0 L 10 5 L 0 10 z}
    method defineArrowMarkers {} {
        set svg [$xml getElementsByTagName svg -depth 1]
        set defs [$svg getElementsByTagName defs -depth 1]
        if {$defs eq {}} {
            set defs [SimpleDOMElement create %AUTO% -tag defs]
            $svg addchild $defs
        }
        set needArrowOutStart yes
        set needArrowInStart  yes
        set needArrowOutEnd yes
        set needArrowInEnd  yes
        foreach m [$defs getElementsByTagName marker] {
            if {[$m attribute id] eq "ArrowOutStart"} {
                set needArrowOutStart no
            }
            if {[$m attribute id] eq "ArrowInStart"} {
                set needArrowInStart no
            }
            if {[$m attribute id] eq "ArrowOutEnd"} {
                set needArrowOutEnd no
            }
            if {[$m attribute id] eq "ArrowInEnd"} {
                set needArrowInEnd no
            }
        }
        if {$needArrowOutStart} {
            set arrowOutStartMarker [SimpleDOMElement create %AUTO% -tag marker \
                                -attributes $_ArrowOutStartAttributes]
            $defs addchild $arrowOutStartMarker
            set path [SimpleDOMElement create %AUTO% -tag path \
                      -attributes [list d $_ArrowPathStartOut]]
            $arrowOutStartMarker addchild $path
        }
        if {$needArrowInStart} {
            set arrowInStartMarker [SimpleDOMElement create %AUTO% -tag marker \
                               -attributes $_ArrowInStartAttributes]
            $defs addchild $arrowInStartMarker
            set path [SimpleDOMElement create %AUTO% -tag path \
                      -attributes [list d $_ArrowPathStartIn]]
            $arrowInStartMarker addchild $path
        }
        if {$needArrowOutEnd} {
            set arrowOutEndMarker [SimpleDOMElement create %AUTO% -tag marker \
                                -attributes $_ArrowOutEndAttributes]
            $defs addchild $arrowOutEndMarker
            set path [SimpleDOMElement create %AUTO% -tag path \
                      -attributes [list d $_ArrowPathEndOut]]
            $arrowOutEndMarker addchild $path
        }
        if {$needArrowInEnd} {
            set arrowInEndMarker [SimpleDOMElement create %AUTO% -tag marker \
                               -attributes $_ArrowInEndAttributes]
            $defs addchild $arrowInEndMarker
            set path [SimpleDOMElement create %AUTO% -tag path \
                      -attributes [list d $_ArrowPathEndIn]]
            $arrowInEndMarker addchild $path
        }
    }
    method translateTransform {dx dy} {
        return [format {translate(%g,%g)} $dx $dy]
    }
    method rotateTransform {degrees} {
        return [format {rotate(%g)} $degrees]
    }
    method newgroup {name args} {
        set parent [from args -parent {}]
        if {$parent eq {}} {
            set parent [$xml getElementsByTagName svg -depth 1]
        }
        set attributes [list id $name]
        set transform [from args -transform ""]
        if {$transform ne ""} {
            lappend attributes transform $transform
        }
        set style [from args -style ""]
        if {$style ne ""} {
            lappend attributes style $style
        }
        set newgroup [SimpleDOMElement create %AUTO% -tag g -attributes $attributes]
        $parent addchild $newgroup
        return $newgroup
    }
    method addrect {x y width height parent} {
        set newrect [SimpleDOMElement create %AUTO% -tag rect \
                     -attributes [list x $x y $y width $width height $height \
                                  fill none stroke black stroke-width 1]]
        $parent addchild $newrect
    }
    method addcircle {cx cy r parent} {
        set newcircle [SimpleDOMElement create %AUTO% -tag circle \
                       -attributes [list cx $cx cy $cy r $r fill black stroke none]]
        $parent addchild $newcircle
    }
    method addpoly {pointlist parent} {
        set attributes [list fill none stroke black stroke-width 1]
        set points ""
        set space ""
        foreach p $pointlist {
            lassign $p x y
            append points [format {%s%g,%g} $space $x $y]
            set space " "
        }
        lappend attributes points $points
        set newpoly [SimpleDOMElement create %AUTO% -tag polygon \
                     -attributes $attributes]
        $parent addchild $newpoly
    }
    method addline {x1 y1 x2 y2 parent args} {
        set attributes [list fill none]
        lappend attributes stroke [from args -stroke black] stroke-width [from args -stroke-width 1]
        set markerStart [from args -marker-start {}]
        set markerEnd   [from args -marker-end   {}]
        set markerMid   [from args -marker-mid   {}]
        set marker      [from args -marker       {}]
        if {$markerStart ne {}} {
            lappend attributes marker-start $markerStart
        }
        if {$markerEnd ne {}} {
            lappend attributes marker-end $markerEnd
        }
        if {$markerMid ne {}} {
            lappend attributes marker-mid $markerMid
        }
        if {$marker ne {}} {
            lappend attributes marker $marker
        }
        lappend attributes x1 [format "%g" $x1]
        lappend attributes y1 [format "%g" $y1]
        lappend attributes x2 [format "%g" $x2]
        lappend attributes y2 [format "%g" $y2]
        set newline [SimpleDOMElement create %AUTO% -tag line \
                     -attributes $attributes]
        $parent addchild $newline
    }
    method addpolyline {pointlist parent args} {
        set attributes [list fill none]
        lappend attributes stroke [from args -stroke black] stroke-width [from args -stroke-width 1]
        set markerStart [from args -marker-start {}]
        set markerEnd   [from args -marker-end   {}]
        set markerMid   [from args -marker-mid   {}]
        set marker      [from args -marker       {}]
        if {$markerStart ne {}} {
            lappend attributes marker-start $markerStart
        }
        if {$markerEnd ne {}} {
            lappend attributes marker-end $markerEnd
        }
        if {$markerMid ne {}} {
            lappend attributes marker-mid $markerMid
        }
        if {$marker ne {}} {
            lappend attributes marker $marker
        }
        set points ""
        set space ""
        foreach p $pointlist {
            lassign $p x y
            append points [format {%s%g,%g} $space $x $y]
            set space " "
        }
        lappend attributes points $points
        set newpoly [SimpleDOMElement create %AUTO% -tag polyline \
                     -attributes $attributes]
        $parent addchild $newpoly
    }
    method addtext {x y text parent args} {
        set rotate [from args -rotate 0]
        set attributes [list fill black]
        lappend attributes x [format "%g" $x]
        lappend attributes y [format "%g" $y]
        lappend attributes rotate [format "%g" $rotate]
        set newtext [SimpleDOMElement create %AUTO% -tag text \
                     -attributes $attributes]
        $parent addchild $newtext
        $newtext setdata $text
    }
    method addXdimension {name x1 x2 y dimy text parent {in false}} {
        set group [$self newgroup $name -parent $parent]
        $self addline $x1 $y $x1 $dimy $group -stroke-width .5
        $self addline $x2 $y $x2 $dimy $group -stroke-width .5
        if {$in} {
            $self addline $x1 $dimy $x2 $dimy $group   -stroke-width .5  -marker-end "url(#ArrowInEnd)" -marker-start "url(#ArrowInStart)"
        } else {
            $self addline $x1 $dimy $x2 $dimy $group -marker-start "url(#ArrowOutStart)" -marker-end "url(#ArrowOutEnd)"  -stroke-width .5
        }
        set midx [expr {($x1+$x2)/2.0}]
        $self addtext $midx $dimy $text $group
    }
    method addYdimension {name y1 y2 x dimx text parent {in false}} {
        set group [$self newgroup $name -parent $parent]
        $self addline $x $y1 $dimx $y1 $group -stroke-width .5
        $self addline $x $y2 $dimx $y2 $group -stroke-width .5
        if {$in} {
            $self addline $dimx $y1 $dimx $y2 $group -stroke-width .5  -marker-end "url(#ArrowInEnd)" -marker-start "url(#ArrowInStart)"
        } else {
            $self addline $dimx $y1 $dimx $y2 $group -stroke-width .5 -marker-start "url(#ArrowOutStart)" -marker-end "url(#ArrowOutEnd)"
        }
        set midy [expr {($y1+$y2)/2.0}]
        $self addtext $dimx $midy $text $group;# -rotate 90
    }
    method addHoledimension {name hx hy dimy dimx1 dimx2 text parent} {
        set group [$self newgroup $name -parent $parent]
        $self addpolyline [list [list $dimx2 $dimy] [list $dimx1 $dimy] \
                            [list $hx $hy]] $group -marker-end "url(#ArrowOutEnd)"  -stroke-width .5 
        $self addtext $dimx2 $dimy $text $group
    }
    method write {filename} {
        set fp [open $filename w]
        xmlheader $fp
        $xml displayTree $fp
        close $fp
    }
}




package provide SVGOutput 1.0
