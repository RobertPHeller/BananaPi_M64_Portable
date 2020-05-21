#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri May 15 07:49:02 2020
#  Last Modified : <200521.1912>
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
package require LCDScreen
package require SVGOutput

snit::macro BracketAngleDims {} {
    typevariable _AngleHeight [expr {(1.0/2.0)*25.4}]
    typevariable _AngleWidth [expr {(1.0/2.0)*25.4}]
    typevariable _AngleThickness [expr {(1.0/16.0)*25.4}]
    typevariable _AngleLength 222.0
    typevariable _BRACKET_r [expr {3.5 / 2.0}]
    typevariable _BRACKET_z [expr {(1.0/4.0)*25.4}]
}

snit::enum Side -values {L R}

snit::type LCDMountingBracket {
    LCDDims
    BracketAngleDims
    typevariable _AngleNotchDX 4
    typevariable _AngleNotchDY1 
    typevariable _AngleNotchDY2
    typeconstructor {
        set _AngleNotchDY1 [expr {$_LCDM3_y+1.0}]
        set _AngleNotchDY2 [expr {$_LCDM2_y-2.0}]
    }
    Common
    option -side -type Side -default L -readonly yes
    component angle_a
    component angle_b
    component lcdm1
    component lcdm2
    component lcdm3
    component lcdm4
    component bracketm1
    component bracketm2
    component bracketm3
    component bracketm4
    proc signof {x} {
        if {$x < 0} {
            return -1
        } elseif {$x > 0} {
            return 1
        } else {
            return 0
        }
    }
    proc _printPoly {fp polylist} {
        foreach point $polylist {
            puts $fp [eval [list format {%10.3f %10.3f %10.3f}] $point]
        }
    }
    constructor {args} {
        $self configurelist $args
        switch $options(-side) {
            L {
                set bracketPoly [list $options(-origin)]
                lassign $options(-origin) ox oy oz
                set x $ox
                set y [expr {$oy + $_AngleLength}]
                lappend bracketPoly [list $x $y $oz]
                set x [expr {$x - $_AngleWidth}]
                lappend bracketPoly [list $x $y $oz]
                set y [expr {$y - $_AngleNotchDY2}]
                lappend bracketPoly [list $x $y $oz]
                set x [expr {$x + $_AngleNotchDX}]
                lappend bracketPoly [list $x $y $oz]
                set y [expr {$y - ($_AngleNotchDY1-$_AngleNotchDY2)}]
                lappend bracketPoly [list $x $y $oz]
                set x [expr {$x - $_AngleNotchDX}]
                lappend bracketPoly [list $x $y $oz]
                set y [expr {$y - ($_AngleLength - $_AngleNotchDY1)}]
                lappend bracketPoly [list $x $y $oz]
                #set x $ox
                #lappend bracketPoly [list $x $y $oz]
                #puts stderr "*** $type create $self: bracketPoly is:"
                #_printPoly stderr $bracketPoly
                install angle_a using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle no \
                                -polypoints $bracketPoly] \
                      -vector [list  0 0 -$_AngleThickness] \
                      -color  {100 100 100}
                install angle_b using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list 0 0 -$_AngleHeight] \
                                -vec2 [list 0 $_AngleLength  0]] \
                      -vector [list  -$_AngleThickness 0 0] \
                      -color  {100 100 100}
                install lcdm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM1_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM2_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM3_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM4_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install bracketm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM1_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM2_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM3_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list -$_BRACKET_z $_LCDM4_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
            }
            R {
                set bracketPoly [list $options(-origin)]
                lassign $options(-origin) ox oy oz
                set x $ox
                set y [expr {$oy + $_AngleLength}]
                lappend bracketPoly [list $x $y $oz]
                set x [expr {$x + $_AngleWidth}]
                lappend bracketPoly [list $x $y $oz]
                set y [expr {$y - $_AngleNotchDY2}]
                lappend bracketPoly [list $x $y $oz]
                set x [expr {$x - $_AngleNotchDX}]
                lappend bracketPoly [list $x $y $oz]
                set y [expr {$y - ($_AngleNotchDY1-$_AngleNotchDY2)}]
                lappend bracketPoly [list $x $y $oz]
                set x [expr {$x + $_AngleNotchDX}]
                lappend bracketPoly [list $x $y $oz]
                set y [expr {$y - ($_AngleLength - $_AngleNotchDY1)}]
                lappend bracketPoly [list $x $y $oz]
                #set x $ox
                #lappend bracketPoly [list $x $y $oz]
                install angle_a using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle no \
                                -polypoints $bracketPoly] \
                      -vector [list  0 0 -$_AngleThickness] \
                      -color  {100 100 100}
                install angle_b using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list 0 0 -$_AngleHeight] \
                                -vec2 [list 0 $_AngleLength  0]] \
                      -vector [list  $_AngleThickness 0 0] \
                      -color  {100 100 100}
                install lcdm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM1_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM2_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM3_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install lcdm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list 0 $_LCDM4_y -$_LCDM_x]] \
                      -radius $_LCDM_r \
                      -height $_AngleThickness \
                      -color {255 255 255} \
                      -direction X
                install bracketm1 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM1_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm2 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM2_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm3 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM3_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
                install bracketm4 using Cylinder %AUTO% \
                      -bottom [GeometryFunctions translate3D_point \
                               $options(-origin) \
                               [list $_BRACKET_z $_LCDM4_y 0]] \
                      -radius $_BRACKET_r \
                      -height -$_AngleThickness \
                      -color {255 255 255} \
                      -direction Z
            }
        }
    }
    method MountingHole {name i zBase height} {
        lassign [[set bracketm$i] cget -bottom] hx hy hz
        return [Cylinder create $name \
                -bottom [list $hx $hy $zBase] \
                -radius $_BRACKET_r \
                -height $height \
                -color {255 255 255} \
                -direction Z]
    }
    method print {{fp stdout}} {
        $angle_a print $fp
        $angle_b print $fp
        $lcdm1 print $fp
        $lcdm2 print $fp
        $lcdm3 print $fp
        $lcdm4 print $fp
        $bracketm1 print $fp
        $bracketm2 print $fp
        $bracketm3 print $fp
        $bracketm4 print $fp
        
    }
    method SVG3View {} {
        lassign $options(-origin) ox oy oz
        set svgpage [SVGOutput create %AUTO% -width 8.5 -height 11]
        set topview [$svgpage newgroup topview "[$svgpage translateTransform 12.7 12.7]"]
        $svgpage addrect 0 0 $_AngleHeight $_AngleThickness $topview
        $svgpage addrect 0 0 $_AngleThickness $_AngleWidth $topview
        set frontview [$svgpage newgroup frontview "[$svgpage translateTransform 12.7 [expr {12.7+25.4}]]"]
        $svgpage addrect 0 0 $_AngleHeight $_AngleLength $frontview
        for {set i 1} {$i <= 4} {incr i} {
            lassign [[set lcdm$i] cget -bottom] dummy by bx
            set r [[set lcdm$i] cget -radius]
            set x [expr {$oz-$bx}]
            set y [expr {$by-$oy}]
            $svgpage addcircle $x $y $r $frontview
        }
        set sideview [$svgpage newgroup sideview "[$svgpage translateTransform [expr {12.7+50.8}] [expr {12.7+25.4}]]"]
        set points2d [list]
        foreach p [[$angle_a cget -surface] cget -polypoints] {
            lassign $p x y z
            if {$options(-side) eq "L"} {
                lappend points2d [list [expr {$ox-$x}] [expr {$y-$oy}]]
            } else {
                lappend points2d [list [expr {$x-$ox}] [expr {$y-$oy}]]
            }
        }
        $svgpage addpoly $points2d $sideview
        for {set i 1} {$i <= 4} {incr i} {
            lassign [[set bracketm$i] cget -bottom] bx by dummy
            set r [[set bracketm$i] cget -radius]
            if {$options(-side) eq "L"} {
                set x [expr {$ox-$bx}]
            } else {
                set x [expr {$bx-$ox}]
            }
            set y [expr {$by-$oy}]
            $svgpage addcircle $x $y $r $sideview
        }
        return $svgpage
    }
}

package provide LCDMountingBracket 1.0
