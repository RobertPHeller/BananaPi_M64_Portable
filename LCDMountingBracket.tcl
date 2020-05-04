#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat Apr 18 19:34:28 2020
#  Last Modified : <200418.2036>
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


lappend auto_path [lindex [glob -nocomplain /usr/share/tcl*/tcllib*] 0]
package require snit
package require struct::matrix

## Primitive types:
snit::listtype point -minlen 3 -maxlen 3 -type snit::double
snit::listtype pointlist -minlen 3 -type point
snit::integer cval -min 0 -max 255
snit::listtype color -minlen 3 -maxlen 3 -type cval
snit::enum Direction -values {X Y Z}

## Generic solid cylinders
snit::type Cylinder {
    option -bottom -type point -readonly yes -default {0 0 0}
    option -radius -type snit::double -readonly yes -default 1
    option -height -type snit::double -readonly yes -default 1
    option -color -type color -readonly yes -default {0 0 0}
    option -direction -type Direction -readonly yes -default Z
    variable index
    typevariable _index 20
    constructor {args} {
        $self configurelist $args
        set index $_index
        incr _index
    }
    method print {{fp stdout}} {
        puts $fp [eval [list format {DEFCOL %d %d %d}] $options(-color)]
        puts $fp [format {C%d = P (%f %f %f) VAL (%f) D%s} $index \
                  [lindex $options(-bottom) 0] \
                  [lindex $options(-bottom) 1] \
                  [lindex $options(-bottom) 2] \
                  $options(-radius) $options(-direction)]
        puts $fp [format {b%d = PRISM C%d %f} $index $index $options(-height)]
    }
    method printPS {fp {xi 0} {yi 1} {xorg 0} {yorg 0} {xscale .01968} {yscale .01968}} {
        set b $options(-bottom)
        set xcenter [lindex $b $xi]
        set ycenter [lindex $b $yi]
        set raduis  $options(-radius)
        puts $fp [format {gsave %f %f translate %f %f scale} $xorg $yorg $xscale $yscale]
        puts $fp [format {newpath %f %f %f 0 360 arc fill} $xcenter $ycenter $raduis]
        puts $fp {grestore}
    }
    typemethod validate {obj} {
        if {[catch {$obj info type} thetype]} {
            error "Not a $type: $obj"
        } elseif {$thetype ne $type} {
            error "Not a $type: $obj"
        } else {
            return $obj
        }
    }
}

## PolySurface -- a rect or polygon 
snit::type PolySurface {
    typevariable _index 20
    option -rectangle -type snit::boolean -readonly yes -default no
    option -cornerpoint -type point -readonly yes -default {0 0 0}
    option -vec1 -type point -readonly yes -default {0 0 0}
    option -vec2 -type point -readonly yes -default {0 0 0}
    option -polypoints -type pointlist -readonly yes -default {{0 0 0} {0 0 0} {0 0 0}}
    variable index
    
    constructor {args} {
        $self configurelist $args
        set index $_index
        incr _index
    }
    method print {{fp stdout}} {
        if {$options(-rectangle)} {
            set cpp [eval [list format {P(%f,%f,%f)}] $options(-cornerpoint)]
            set v1  [eval [list format {D(%f,%f,%f)}] $options(-vec1)]
            set v2  [eval [list format {D(%f,%f,%f)}] $options(-vec2)]
            puts $fp [format {S%d = REC %s %s %s} $index $cpp $v1 $v2]
        } else {
            puts -nonewline $fp [format {S%d = POL} $index]
            foreach p $options(-polypoints) {
                puts -nonewline $fp [eval [list format { P(%f,%f,%f)}] $p]
            }
            puts $fp {}
        }
        return [format {S%d} $index]
    }
    method printPS {fp {xi 0} {yi 1} {xorg 0} {yorg 0} {xscale .01968} {yscale .01968}} {
        if {$options(-rectangle)} {
            set p $options(-cornerpoint)
            set x0 [lindex $p $xi]
            set y0 [lindex $p $yi]
            set v1 $options(-vec1)
            set v2 $options(-vec2)
            set dx1 [lindex $v1 $xi]
            set dx2 [lindex $v2 $xi]
            set dy1 [lindex $v1 $yi]
            set dy2 [lindex $v2 $yi]
            set dx [expr {$dx1 + $dx2}]
            set dy [expr {$dy1 + $dy2}]
            puts $fp [format {gsave %f %f translate %f %f scale} $xorg $yorg $xscale $yscale]
            puts $fp [format {newpath %f %f moveto} $x0 $y0]
            puts $fp [format {%f %f rlineto} 0 $dy]
            puts $fp [format {%f %f rlineto} $dx 0]
            puts $fp [format {%f %f rlineto} 0 [expr {0-$dy}]]
            puts $fp [format {%f %f rlineto} [expr {0-$dx}] 0]
            puts $fp {stroke grestore}
        } else {
            puts $fp [format {gsave %f %f translate %f %f scale newpath} $xorg $yorg $xscale $yscale]
            set cmd moveto
            foreach p $options(-polypoints) {
                puts $fp [format {%f %f %s} [lindex $p $xi] [lindex $p $yi] $cmd]
                set cmd lineto
            }
            puts $fp {stroke grestore}
        }
    }
    typemethod validate {obj} {
        if {[catch {$obj info type} thetype]} {
            error "Not a $type: $obj"
        } elseif {$thetype ne $type} {
            error "Not a $type: $obj"
        } else {
            return $obj
        }
    }
}

## PrismSurfaceVector -- a rect or polygon with depth/thickness
## (PolySurface + depth/thickness vector)
snit::type PrismSurfaceVector {
    typevariable _index 80
    option -surface -type ::PolySurface -readonly yes -default {}
    component surface
    option -vector  -type point -readonly yes -default {0 0 0}
    option -color -type color -readonly yes -default {147 147 173}
    variable index
    constructor {args} {
        $self configurelist $args
        set index $_index
        incr _index
        set surface $options(-surface)
    }
    method print {{fp stdout}} {
        puts $fp [eval [list format {DEFCOL %d %d %d}] $options(-color)]
        set s [$surface print $fp]
        set pr [format {B%d} $index]
        puts $fp [eval [list format {B%d = PRISM %s D(%f,%f,%f)} $index $s] $options(-vector)]
        return $pr
    }
    typemethod validate {obj} {
        if {[catch {$obj info type} thetype]} {
            error "Not a $type: $obj"
        } elseif {$thetype ne $type} {
            error "Not a $type: $obj"
        } else {
            return $obj
        }
    }
}

## Assorted geometic functions
snit::type GeometryFunctions {
    pragma -hastypeinfo    no -hastypedestroy no -hasinstances   no
    
    
    typevariable _PI [expr {acos(0)*2}]
    typemethod PI {} {return $_PI}
    
    ## Degrees to Radians

    typemethod radians {degrees} {
        return [expr {($degrees/180.0)*$_PI}]
    }


    ## Compute the 3D point on a circle of a specified radius, at a specificed 
    ## height at a specificed angle.
    typemethod pointXdeltaatang {angle {dx 25} {z 0.0}} {
        set theta [$type radians $angle]
        return [list [expr {sin($theta) * $dx}] [expr {cos($theta) * $dx}] $z]
    }
    proc _homogenous {p} {
        lappend p 1
        return $p
    }
    typemethod MakeHomogenous {points} {
        set result [list]
        foreach p $points {
            lappend result [_homogenous $p]
        }
        return $result
    }
    
    typemethod translate3D {pointsH point3d} {
        set result [list]
        foreach {dx dy dz} $point3d {break}
        foreach p $pointsH {
            foreach {x y z w} $p {break}
            lappend result [list [expr {$x + $dx}] \
                            [expr {$y + $dy}] [expr {$z + $dz}] $w]
        }
        return $result
    }
    typemethod translate3D_point {originPoint DeltaPoint} {
        #puts stderr [list *** $type translate3D_point $originPoint $DeltaPoint]
        foreach {dx dy dz} $DeltaPoint {break}
        foreach {x  y  z}  $originPoint {break}
        set result [list [expr {$x + $dx}] [expr {$y + $dy}] [expr {$z + $dz}]]
        #puts stderr [list *** $type translate3D_point result is $result]
        return $result
    }
    typemethod rotateZAxis {pointsH theta_rads} {
        #puts stderr [list *** $type rotateZAxis $pointsH $theta_rads]
        set p 4
        set n [llength $pointsH]
        set m 4
        #puts stderr "*** $type rotateZAxis: p = $p, n = $n, m = $m"
        set rmat [::struct::matrix]
        $rmat deserialize  [list $m $p [list \
                               [list \
                                [expr {cos($theta_rads)}] \
                                [expr {-sin($theta_rads)}] \
                                0 0] \
                               [list \
                                [expr {sin($theta_rads)}] \
                                [expr {cos($theta_rads)}] \
                                0 0] \
                               {0 0 1 0} {0 0 0 1}]]
        #puts stderr [list *** $type rotateZAxis: rmat = [$rmat serialize]]
        set pointsMat [::struct::matrix]
        $pointsMat deserialize [list $n $m $pointsH]
        #puts stderr [list *** $type rotateZAxis: pointsMat = [$pointsMat serialize]]
        set resultMat [::struct::matrix]
        $resultMat deserialize [list  $n $p {}]
        #puts stderr [list *** $type rotateZAxis: resultMat  = [$resultMat serialize]]

        for {set i 0} {$i < $n} {incr i} {
            for {set j 0} {$j < $p} {incr j} {
                $resultMat set cell $j $i 0.0
                #puts stderr [list *** $type rotateZAxis: resultMat  = [$resultMat serialize]]
                for {set k 0} {$k < $m} {incr k} {
                    #puts stderr "*** $type rotateZAxis: \[\$resultMat get cell $j $i\] = [$resultMat get cell $j $i]"
                    #puts stderr "*** $type rotateZAxis: \[\$pointsMat get cell $k $i\] = [$pointsMat get cell $k $i]"
                    #puts stderr "*** $type rotateZAxis: \[\$rmat get cell $k $j\] = [$rmat get cell $k $j]"
                    set p1 [expr {[$pointsMat get cell $k $i] * \
                                  [$rmat get cell $k $j]}]
                    #puts stderr "*** $type rotateZAxis: p1 = $p1"
                    #snit::double validate $p1
                    set p2 [$resultMat get cell $j $i]    
                    #snit::double validate $p2
                    $resultMat set cell $j $i [expr {$p2 + $p1}]
                }
            }
        }
        set result [lindex [$resultMat serialize] 2]
        #puts stderr [list *** $type rotateZAxis: result is $result]
        $rmat destroy
        $pointsMat destroy
        $resultMat destroy
        return $result
    }
    typemethod rotateZAxis_point {originPoint theta_rads} {
        #puts stderr [list *** $type rotateZAxis_point $originPoint $theta_rads]
        return [lindex [$type StripHomogenous [$type rotateZAxis \
                                               [list [list \
                                                      [lindex $originPoint 0] \
                                                      [lindex $originPoint 1] \
                                                      [lindex $originPoint 2] 1.0]] \
                                               $theta_rads]] 0]
    }
    typemethod StripHomogenous {pointsH} {
        set result [list]
        foreach pH $pointsH {
            lappend result [lrange $pH 0 end-1]
        }
        return $result
    }
}

snit::type PostScriptFile {
    pragma -hastypeinfo    no
    pragma -hastypedestroy no
    pragma -hasinstances   no
    typevariable pageno 0
    typevariable psName {}
    typevariable psFP   {}
    typevariable psTitle {}
    typevariable psCreator {}
    typevariable psPages 0
    typevariable currentPageTitle {}
    typevariable lineCount 0
    typevariable _TopOfPage 8.0
    typevariable _Fontsize [expr {12.0 / 72.0}]
    typevariable _LineIncr [expr {-1.2 * (12.0 / 72.0)}]
    typevariable _MaxLines [expr {int(8 / ((12.0/72)*1.2))}]
    typevariable ypos 8.0
    typemethod open {} {
        set psName  [file rootname [info script]].ps
        set psFP    [open $psName w]
        set psTitle [file rootname [file tail [info script]]]
        set psCreator [file tail [info script]]
        set pageno 0
        set psPages 0
        puts $psFP "%!PS-Adobe-3.0"
        puts $psFP [format {%%Title: %s} $psTitle]
        puts $psFP [format {%%Creator: %s} $psCreator]
        puts $psFP {%%BoundingBox: 0 0 612 792}
        puts $psFP {%%Pages: (atend)}
        puts $psFP {%%EndComments}
        puts $psFP {%%BeginProlog}
        puts $psFP {/inch {72 mul} def}
        puts $psFP {/ReportNP {ReportFont} def}
        puts $psFP "/ReportFontSize \{$_Fontsize\} def"
        puts $psFP {/ReportFont {/Courier findfont ReportFontSize scalefont setfont} def}
        puts $psFP {/DrillReportLine {
                moveto (Hole   at ) show show (mm) show (,) show show (mm) show
                ( diameter: ) show show (mm) show 
            } def
        }
        puts $psFP {/CutoutReportLine {
                moveto (Cutout at ) show show (mm) show (,) show show (mm) show 
                ( size:     ) show show (mm) show ( x ) show  show (mm) show
            } def}
        puts $psFP {%%EndProlog}
        puts $psFP {}
   }
    
    typemethod hole {hx hy dia} {
        if {$lineCount >= $_MaxLines} {
            $type newPage "$currentPageTitle (continued)"
        }
        puts $psFP [format {(%7.3f) (%7.3f) (%7.3f) 0 %f DrillReportLine} $dia $hy $hx $ypos]
        incr lineCount
        set ypos [expr {$ypos + $_LineIncr}]
    }
    typemethod cutout {cx cy w h} {
        if {$lineCount >= $_MaxLines} {
            $type newPage "$currentPageTitle (continued)"
        }
        puts $psFP [format {(%7.3f) (%7.3f) (%7.3f) (%7.3f) 0 %f CutoutReportLine} \
                    $h $w $cy $cx $ypos]
        incr lineCount
        set ypos [expr {$ypos + $_LineIncr}]
    }
    typemethod newPage {{pageTitle {}}} {
        if {$pageno > 0} {
            puts $psFP {showpage}
        }
        incr pageno
        puts $psFP [format {%%%%Page: %d %d} $pageno $pageno]
        puts $psFP {.75 inch 1.5 inch translate 1 inch 1 inch scale}
        puts $psFP {}
        puts $psFP [format {gsave 0 -.75 moveto /NewCenturySchlbk-Bold findfont .25 scalefont setfont 0 0 0 setrgbcolor (%-55.55s Page: %3d) show grestore} $pageTitle $pageno]
        puts $psFP ReportNP
        set lineCount 0
        set xpos $_TopOfPage
        if {[regexp { (continued)$} $currentPageTitle] < 1} {
            set currentPageTitle $pageTitle
        }
    }
    typemethod fp {} {return $psFP}
    typemethod close {} {
        if {$pageno > 0} {
            puts $psFP {showpage}
        }
        puts $psFP {%%Trailer}
        puts $psFP [format {%%%%Pages: %d} $pageno]
        puts $psFP {%%EOF}
        close $psFP
        set psFP {}
    }
}


snit::enum Units -values {in mm}

snit::type Angle {
    component a
    component b
    option -origin -type point -default {0.0 0.0 0.0} -readonly yes
    option -height -type snit::double -default 0.0 -readonly yes
    option -width -type snit::double -default 0.0 -readonly yes
    option -length -type snit::double -default 0.0 -readonly yes
    option -thickness -type snit::double -default 0.0 -readonly yes
    constructor {args} {
        $self configurelist $args
        install a using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $options(-height) 0 0] \
                        -vec2 [list 0 $options(-length) 0]] \
              -vector [list  0 0 $options(-thickness)] \
              -color {0 255 0}
        install b using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list 0 0 $options(-width)] \
                        -vec2 [list 0 $options(-length) 0]] \
              -vector [list $options(-thickness) 0 0] \
              -color {0 255 0}
    }
    method print {{fp stdout}} {
        $a print $fp
        $b print $fp
    }
}

snit::type LCDMountingBracket {
    typevariable _AngleHeight [expr {(1.0/2.0)*25.4}]
    typevariable _AngleWidth [expr {(1.0/2.0)*25.4}]
    typevariable _AngleThickness [expr {(1.0/16.0)*25.4}]
    typevariable _AngleLength 220.0
    typevariable _LCDM1_y 11.85
    typevariable _LCDM2_y [expr {11.85 + 54.0}]
    typevariable _LCDM3_y [expr {11.85 + 144.3}]
    typevariable _LCDM4_y [expr {11.85 + 198.0}]
    typevariable _LCDM_x  [expr {3.7 + (6.5 / 2.0)}]
    typevariable _LCDM_r  [expr {2.5 / 2.0}]
    typevariable _BRACKET_r [expr {3.5 / 2.0}]
    typevariable _BRACKET_z [expr {(1.0/4.0)*25.4}]
    option -origin -type point -default {0.0 0.0 0.0} -readonly yes    
    component angle
    component lcdm1
    component lcdm2
    component lcdm3
    component lcdm4
    component bracketm1
    component bracketm2
    component bracketm3
    component bracketm4
    constructor {args} {
        $self configurelist $args
        install angle using Angle %AUTO% \
              -origin $options(-origin) \
              -height $_AngleHeight \
              -width  $_AngleWidth \
              -length $_AngleLength \
              -thickness $_AngleThickness
        install lcdm1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_LCDM_x $_LCDM1_y 0]] \
              -radius $_LCDM_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction Z
        install lcdm2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_LCDM_x $_LCDM2_y 0]] \
              -radius $_LCDM_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction Z
        install lcdm3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_LCDM_x $_LCDM3_y 0]] \
              -radius $_LCDM_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction Z
        install lcdm4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_LCDM_x $_LCDM4_y 0]] \
              -radius $_LCDM_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction Z
        install bracketm1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0.0 $_LCDM1_y $_BRACKET_z]] \
              -radius $_BRACKET_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction X
        install bracketm2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0.0 $_LCDM2_y $_BRACKET_z]] \
              -radius $_BRACKET_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction X
        install bracketm3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0.0 $_LCDM3_y $_BRACKET_z]] \
              -radius $_BRACKET_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction X
        install bracketm4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0.0 $_LCDM4_y $_BRACKET_z]] \
              -radius $_BRACKET_r \
              -height $_AngleThickness \
              -color {255 255 255} \
              -direction X
    }
    method print {{fp stdout}} {
        $angle print $fp
        $lcdm1 print $fp
        $lcdm2 print $fp
        $lcdm3 print $fp
        $lcdm4 print $fp
        $bracketm1 print $fp
        $bracketm2 print $fp
        $bracketm3 print $fp
        $bracketm4 print $fp
        
    }
}

set modelFP [open [file rootname [info script]].gcad w]

## GCad prefix blather.
puts $modelFP "# [clock format [clock seconds] -format {%Y/%m/%d-%M:%M:%S}]"
puts $modelFP {DEFCOL 0 0 0}


LCDMountingBracket create lcdmountingbracket

lcdmountingbracket print $modelFP
close $modelFP
