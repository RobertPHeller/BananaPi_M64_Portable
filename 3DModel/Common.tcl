#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 09:45:23 2020
#  Last Modified : <200529.2140>
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
package require struct::matrix

## Primitive types:
snit::listtype point -minlen 3 -maxlen 3 -type snit::double
snit::listtype pointlist -minlen 3 -type point
snit::integer cval -min 0 -max 255
snit::listtype color -minlen 3 -maxlen 3 -type cval
snit::enum Direction -values {X Y Z}

snit::type Circle {
    option -bottom -type point -readonly yes -default {0 0 0}
    option -radius -type snit::double -readonly yes -default 1
    option -direction -type Direction -readonly yes -default Z
    variable index
    typevariable _index 20
    constructor {args} {
        $self configurelist $args
        set index $_index
        incr _index
    }
    method print {{fp stdout}} {
        puts $fp [format {C%d = P (%f %f %f) VAL (%f) D%s} $index \
                  [lindex $options(-bottom) 0] \
                  [lindex $options(-bottom) 1] \
                  [lindex $options(-bottom) 2] \
                  $options(-radius) $options(-direction)]
    }
    method Index {} {return $index}
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

## Generic solid cylinders
snit::type Cylinder {
    component circle
    delegate option * to circle
    option -height -type snit::double -readonly yes -default 1
    option -color -type color -readonly yes -default {0 0 0}
    variable index
    typevariable _index 20
    constructor {args} {
        install circle using Circle %AUTO% \
              -bottom [from args -bottom {0 0 0}] \
              -radius [from args -radius 1] \
              -direction [from args -direction Z]
        $self configurelist $args
        set index $_index
        incr _index
    }
    method print {{fp stdout}} {
        puts $fp [eval [list format {DEFCOL %d %d %d}] $options(-color)]
        $circle print $fp
        puts $fp [format {B%d = PRISM C%d %f} $index [$circle Index] $options(-height)]
    }
    method printPS {fp {xi 0} {yi 1} {xorg 0} {yorg 0} {xscale .01968} {yscale .01968}} {
        set b [$self cget -bottom]
        set xcenter [lindex $b $xi]
        set ycenter [lindex $b $yi]
        set raduis  [$self cget -radius]
        puts $fp [format {gsave %f %f translate %f %f scale} $xorg $yorg $xscale $yscale]
        puts $fp [format {newpath %f %f %f 0 360 arc fill} $xcenter $ycenter $raduis]
        puts $fp {grestore}
    }
    method TheCircle {} {return $circle}
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
    option -closedpolygon -type snit::boolean -readonly yes -default yes
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
        #puts stderr "*** $self print (-rectangle is $options(-rectangle), -closedpolygon is $options(-closedpolygon)"
        if {$options(-rectangle)} {
            set cpp [eval [list format {P(%f,%f,%f)}] $options(-cornerpoint)]
            set v1  [eval [list format {D(%f,%f,%f)}] $options(-vec1)]
            set v2  [eval [list format {D(%f,%f,%f)}] $options(-vec2)]
            puts $fp [format {S%d = REC %s %s %s} $index $cpp $v1 $v2]
        } elseif {$options(-closedpolygon)} {
            puts -nonewline $fp [format {S%d = POL} $index]
            foreach p $options(-polypoints) {
                puts -nonewline $fp [eval [list format { P(%f,%f,%f)}] $p]
            }
            puts $fp {}
        } else {
            #puts stderr "*** $self print: CCV"
            puts -nonewline $fp [format {S%d = CCV} $index]
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
    typevariable _index 100
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

snit::enum DimPlane -values {X Y Z P}

snit::type NoteIndex {
    variable index
    typevariable _index 10
    constructor {args} {
        set index $_index
        incr _index
    }
    method Index {} {return $index}
}

snit::type Dim3D {
    option -point1 -type point -default {0.0 0.0 0.0} -readonly yes
    option -point2 -type point -default {0.0 0.0 0.0} -readonly yes
    option -textpoint -type point -default {0.0 0.0 0.0} -readonly yes
    option -plane -type DimPlane -default P -readonly yes 
    option -additionaltext -default {} -readonly yes
    component index
    constructor {args} {
        $self configurelist $args
        install index using NoteIndex %AUTO%
    }
    method print {{fp stdout}} {
        puts $fp [format {n%d = DIM3 P(%f %f %f) P(%f %f %f) P(%f %f %f) %s "%s"} \
                  [$index Index] [lindex $options(-point1) 0] \
                  [lindex $options(-point1) 1] [lindex $options(-point1) 2] \
                  [lindex $options(-point2) 0] [lindex $options(-point2) 1] \
                  [lindex $options(-point2) 2] [lindex $options(-textpoint) 0] \
                  [lindex $options(-textpoint) 1] \
                  [lindex $options(-textpoint) 2] $options(-plane) $options(-additionaltext)]
    }
}


snit::type DimDiameter {
    option -textpoint -type point -default {0.0 0.0 0.0} -readonly yes
    option -circle -type Circle -readonly yes -default {}
    option -additionaltext -default {} -readonly yes
    component index
    constructor {args} {
        $self configurelist $args
        install index using NoteIndex %AUTO%
    }
    method print {{fp stdout}} {
        puts $fp [format {n%d = DIMD C%d P(%f %f %f) "%s"} \
                  [$index Index] [$options(-circle) Index] \
                  [lindex $options(-textpoint) 0] \
                  [lindex $options(-textpoint) 1] \
                  [lindex $options(-textpoint) 2] $options(-additionaltext)]
    }
}
    
snit::type Text {
    option -textpoint -type point -default {0.0 0.0 0.0} -readonly yes
    option -size -type snit::double -default 10 -readonly yes
    option -angle -type snit::double -default 0 -readonly yes
    option -text -default {} -readonly yes
    component index
    constructor {args} {
        $self configurelist $arg
        install index using NoteIndex %AUTO%
    }
    method print {{fp stdout}} {
        puts $fp [format {n%d = P(%f %f %f) %f ANG(%f) "%s"} [$index Index] \
                  [lindex $options(-textpoint) 0] \
                  [lindex $options(-textpoint) 1] \
                  [lindex $options(-textpoint) 2] \
                  $options(-size) $options(-angle) $options(-text)]
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
    typemethod open {args} {
        set psName [from args -filename [file rootname [info script]].ps]
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

snit::type Angle {
    component a
    component b
    proc signof {x} {
        if {$x < 0} {
            return -1
        } elseif {$x > 0} {
            return 1
        } else {
            return 0
        }
    }
    option -origin -type point -default {0.0 0.0 0.0} -readonly yes
    option -height -type snit::double -default 0.0 -readonly yes
    option -width -type snit::double -default 0.0 -readonly yes
    option -length -type snit::double -default 0.0 -readonly yes
    option -thickness -type snit::double -default 0.0 -readonly yes
    option -direction -type Direction -readonly yes -default Y
    option -color -type color -default {192 192 192} -readonly yes
    constructor {args} {
        $self configurelist $args
        switch $options(-direction) {
            X {
                install a using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list $options(-length) 0 0] \
                                -vec2 [list 0 $options(-width) 0]] \
                      -vector [list  0 0 [expr {[signof $options(-height)]*$options(-thickness)}]] \
                      -color $options(-color)
                install b using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list $options(-length) 0 0] \
                                -vec2 [list 0 0 $options(-height)]] \
                      -vector [list 0 [expr {[signof $options(-width)]*$options(-thickness)}] 0] \
                      -color $options(-color)
            }
            Y {
                install a using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list $options(-width) 0 0] \
                                -vec2 [list 0 $options(-length) 0]] \
                      -vector [list  0 0 [expr {[signof $options(-height)]*$options(-thickness)}]] \
                      -color $options(-color)
                install b using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list 0 0 $options(-height)] \
                                -vec2 [list 0 $options(-length) 0]] \
                      -vector [list [expr {[signof $options(-width)]*$options(-thickness)}] 0 0] \
                      -color $options(-color)
            }
            Z {
                install a using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list 0 0 $options(-length)] \
                                -vec2 [list 0 $options(-width) 0]] \
                      -vector [list [expr {[signof $options(-height)]*$options(-thickness)}] 0 0] \
                      -color $options(-color)
                install b using PrismSurfaceVector %AUTO% \
                      -surface [PolySurface  create %AUTO% \
                                -rectangle yes \
                                -cornerpoint $options(-origin) \
                                -vec1 [list 0 0 $options(-length)] \
                                -vec2 [list $options(-height) 0 0]] \
                      -vector [list 0 [expr {[signof $options(-width)]*$options(-thickness)}] 0] \
                      -color $options(-color)
            }
        }
    }
    method print {{fp stdout}} {
        $a print $fp
        $b print $fp
    }
}

snit::enum Units -values {in mm}

snit::macro Common {} {
    option -origin -type point -default {0.0 0.0 0.0} -readonly yes
    option -partunits -type Units -default in
    proc _normPartSizeMM {X Y Z} {
        return [format {%.3fx%.3fx%.3f} $X $Y $Z]
    }
    proc _inch {mm} {return [expr {$mm / 25.4}]}
    proc _normPartSizeIN {X Y Z} {
        return [format {%.4fx%.4fx%.4f} [_inch $X] [_inch $Y] [_inch $Z]]
    }
    method _normPartSize {X Y Z} {
        #puts stderr "*** $self _normPartSize $X $Y $Z"
        switch $options(-partunits) {
            in {
                return [_normPartSizeIN $X $Y $Z]
            }
            mm {
                return [_normPartSizeMM $X $Y $Z]
            }
        }
    }
}

proc GCadPrefix {{fp stdout}} {
    ## GCad prefix blather.
    puts $fp "# [clock format [clock seconds] -format {%Y/%m/%d-%M:%M:%S}]"
    puts $fp {DEFCOL 0 0 0}
}

package provide Common 1.0
