#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue May 5 10:07:03 2020
#  Last Modified : <200505.1534>
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

## Power Supply: Mouser #490-PSK-S15C-5
# PCB mount, 28.8mm wide 53.8mm long, 23.5mm high

snit::macro PSDims {} {
    typevariable _pswidth 28.8
    typevariable _pslength 53.8
    typevariable _psheight 23.5
    typevariable _pspindia 1.0
    typevariable _pspinlength 6.0
    typevariable _pspin1Xoff [expr {(53.8-45.72)/2.0}]
    typevariable _pspin1Yoff [expr {(28.8-20.32)/2.0}]
    typevariable _pspin2Xoff [expr {(53.8-45.72)/2.0}]
    typevariable _pspin2Yoff [expr {((28.8-20.32)/2.0)+20.32}]
    typevariable _pspin3Xoff [expr {((53.8-45.72)/2.0)+45.72}]
    typevariable _pspin3Yoff [expr {((28.8-20.32)/2.0)+10.16}]
    typevariable _pspin4Xoff [expr {((53.8-45.72)/2.0)+45.72}]
    typevariable _pspin4Yoff [expr {(28.8-20.32)/2.0}]
    typevariable _psPCBwidth 45.72
    typevariable _psPCBlength 76.2
    typevariable _psPCBThickness [expr {(1.0/16.0)*25.4}]
    typevariable _pstermxoff  0.98
    typevariable _psactermyoff  5.08
    typevariable _psdctermyoff  10.16
}

snit::macro TB007_508_xxBE {} {
    typevariable _termwidth 8.2
    typevariable _termheight 10.0
    typevariable _termpitch  5.08
    typevariable _3belength 15.24
    typevariable _2belength 10.16
    typevariable _termhyoff 2.54
    typevariable _termhxoff 4.10
    typevariable _termpindia 1.3
    typevariable _termpinlen 3.8
}

snit::type PSK_S15C {
    # 490-PSK-S15C-5
    PSDims
    Common
    component body
    component pin1
    component pin2
    component pin3
    component pin4
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_pslength 0 0] \
                        -vec2 [list 0 $_pswidth 0]] \
              -vector [list 0 0 $_psheight] \
              -color [list 0 0 0]
        install pin1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin1Xoff $_pspin1Yoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 255}
        install pin2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin2Xoff $_pspin2Yoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 255}
        install pin3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin3Xoff $_pspin3Yoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 255}
        install pin4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_pspin4Xoff $_pspin4Yoff 0]] \
              -radius [expr {$_pspindia / 2.0}] \
              -height [expr {-$_pspinlength}] \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
        $pin3 print $fp
        $pin4 print $fp
    }
}

snit::type PCBwithStrips {
    typevariable _stripWidth [expr {2.54*.8}]
    typevariable _stripIncr  2.54
    typevariable _stripOffset 1.27
    typevariable _stripThickness .1
    typevariable _mhdia 3.5
    PSDims
    Common
    component board
    variable strips [list]
    component mh1
    component mh2
    component mh3
    component mh4
    constructor {args} {
        $self configurelist $args
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_psPCBlength 0 0] \
                        -vec2 [list 0 $_psPCBwidth 0]] \
              -vector [list 0 0 $_psPCBThickness] \
              -color {210 180 140}
        set xoff [expr {($_psPCBlength - $_pslength)/2.0}]
        set yoff [expr {($_psPCBwidth - $_pswidth)/2.0}]
        set pin1Y [expr {$_pspin1Yoff+$yoff}]
        set pin2Y [expr {$_pspin2Yoff+$yoff}]
        for {set sy $_stripIncr} \
              {($sy + $_stripIncr) <= $_psPCBwidth} \
              {set sy [expr {$sy + $_stripIncr}]} {
            if {$sy >= $pin1Y && $sy <= $pin2Y} {
                set stripCP1 [list $_stripOffset \
                              [expr {$sy - ($_stripWidth / 2.0)}] \
                              0.0]
                set stripCP2 [list [expr {$_stripOffset + $xoff + $_pspin4Xoff - $_stripIncr}]\
                              [expr {$sy - ($_stripWidth / 2.0)}] \
                              0.0]
                set striplen [expr {$xoff + $_pspin1Xoff}]
                lappend strips \
                      [PrismSurfaceVector create %AUTO% \
                       -surface [PolySurface  create %AUTO% \
                                 -rectangle yes \
                                 -cornerpoint $stripCP1 \
                                 -vec1 [list $striplen 0 0] \
                                 -vec2 [list 0 $_stripWidth 0]] \
                       -vector [list 0 0 -$_stripThickness] \
                       -color {255 255 0}]
                lappend strips \
                      [PrismSurfaceVector create %AUTO% \
                       -surface [PolySurface  create %AUTO% \
                                 -rectangle yes \
                                 -cornerpoint $stripCP2 \
                                 -vec1 [list $striplen 0 0] \
                                 -vec2 [list 0 $_stripWidth 0]] \
                       -vector [list 0 0 -$_stripThickness] \
                       -color {255 255 0}]
            } else {    
                set stripCP [list $_stripOffset \
                             [expr {$sy - ($_stripWidth / 2.0)}] \
                             0.0]
                lappend strips \
                      [PrismSurfaceVector create %AUTO% \
                       -surface [PolySurface  create %AUTO% \
                                 -rectangle yes \
                                 -cornerpoint $stripCP \
                                 -vec1 [list [expr {$_psPCBlength - ($_stripOffset*2)}] 0 0] \
                                 -vec2 [list 0 $_stripWidth 0]] \
                       -vector [list 0 0 -$_stripThickness] \
                       -color {255 255 0}]
           }
       }
       install mh1 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list [expr {$_stripIncr + 5*2.54}] $_stripIncr -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
       install mh2 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list [expr {$_stripIncr + 5*2.54}] \
                       [expr {$_psPCBwidth - $_stripIncr}] \
                       -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
       install mh3 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list [expr {$_psPCBlength - ($_stripIncr + 5*2.54)}] \
                       $_stripIncr -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
       install mh4 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list [expr {$_psPCBlength - ($_stripIncr + 5*2.54)}] \
                       [expr {$_psPCBwidth - $_stripIncr}] \
                       -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
    }
    method print {{fp stdout}} {
        $board print $fp
        foreach s $strips {
            $s print $fp
        }
        $mh1 print $fp
        $mh2 print $fp
        $mh3 print $fp
        $mh4 print $fp
    }
    method MountingHole {name i baseZ height} {
        lassign [[set mh$i] cget -bottom] x y z
        set bottom [list $x $y $baseZ]]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [[set mh$i] cget -radius] \
                -height $height \
                -color {255 255 255}]
    }
    method Standoff {name i baseZ height diameter color} {
        lassign [[set mh$i] cget -bottom] x y z
        set bottom [list $x $y $baseZ]]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [expr {$diameter / 2.0}]
                -height $height \
                -color $color]
    }
            
}



snit::type TB007_508_03BE {
    TB007_508_xxBE
    Common
    component body
    component pin1
    component pin2
    component pin3
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_termwidth 0 0] \
                        -vec2 [list 0 $_3belength 0]] \
              -vector [list 0 0 $_termheight] \
              -color  [list 0 0 255]
        install pin1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff $_termhyoff 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
        install pin2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff [expr {$_termhyoff + $_termpitch}] 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
        install pin3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff [expr {$_termhyoff + (2*$_termpitch)}] 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
        $pin3 print $fp
    }
}

snit::type TB007_508_02BE {
    TB007_508_xxBE
    Common
    component body
    component pin1
    component pin2
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_termwidth 0 0] \
                        -vec2 [list 0 $_2belength 0]] \
              -vector [list 0 0 $_termheight] \
              -color  [list 0 0 255]
        install pin1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff $_termhyoff 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
        install pin2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_termhxoff [expr {$_termhyoff + $_termpitch}] 0]] \
              -radius [expr {$_termpindia / 2.0}] \
              -height -$_termpinlen \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
    }
}


snit::type PSOnPCB {
    PSDims
    TB007_508_xxBE
    Common
    component powersupply;# 490-PSK-S15C-5
    component pcboard;# BPS-MAR-ST6U-001
    component acterm;#490-TB007-508-03BE
    component dcterm;#490-TB006-508-02BE
    delegate method MountingHole to pcboard
    delegate method Standoff to pcboard
    constructor {args} {
        $self configurelist $args
        set xoff [expr {($_psPCBlength - $_pslength)/2.0}]
        set yoff [expr {($_psPCBwidth - $_pswidth)/2.0}]
        set psoffset [list $xoff $yoff $_psPCBThickness]
        install powersupply using PSK_S15C %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       $psoffset]
        install pcboard using PCBwithStrips %AUTO% \
              -origin $options(-origin)
        install acterm using TB007_508_03BE %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                         $options(-origin) \
                       [list $_pstermxoff $_psactermyoff $_psPCBThickness]]
        install dcterm using TB007_508_02BE %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list [expr {$_psPCBlength - $_pstermxoff - $_termwidth}] $_psdctermyoff $_psPCBThickness]]
    }
    method print {{fp stdout}} {
        $powersupply print $fp
        $pcboard print $fp
        $acterm print $fp
        $dcterm print $fp
    }
}


## Al. box:      Mouser #563-CU-3001A
# Base: 2.125in wide, 3.250in long, 1.625in high
# Cover 2.031in wide, 3.156in long, 1.562in high

snit::macro PSBOX {} {
    typevariable _psboxbasewidth [expr {2.125*25.4}]
    typevariable _psboxbaselength [expr {3.250*25.4}]
    typevariable _psboxbaseheight [expr {1.625*25.4}]
    typevariable _psboxbaseflangewidth  [expr {0.375*25.4}]
    typevariable _psboxbaseholeoffset [expr {0.172*25.4}]
    typevariable _psboxbaseholeheightoffset [expr {0.594*25.4}]
    typevariable _psboxcoverwidth [expr {2.031*25.4}]
    typevariable _psboxcoverlength [expr {3.156*25.4}]
    typevariable _psboxcoverheight [expr {1.562*25.4}]
    typevariable _psboxcoverholeoffset [expr {0.156*25.4}]
    typevariable _psboxcoverholeheightoffset [expr {0.968*25.4}]
}

set modelFP [open [file rootname [info script]].gcad w]

## GCad prefix blather.
puts $modelFP "# [clock format [clock seconds] -format {%Y/%m/%d-%M:%M:%S}]"
puts $modelFP {DEFCOL 0 0 0}

PSOnPCB create psonpcb
psonpcb print $modelFP
close $modelFP
