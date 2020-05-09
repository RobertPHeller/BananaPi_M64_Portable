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
#  Last Modified : <200508.2057>
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
    typevariable _stripExtra 7.62
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
                set stripCP1 [GeometryFunctions translate3D_point $options(-origin) \
                              [list $_stripOffset \
                              [expr {$sy - ($_stripWidth / 2.0)}] \
                              0.0]]
                set stripCP2 [GeometryFunctions translate3D_point $options(-origin) \
                              [list [expr {$_stripOffset + $xoff + $_pspin4Xoff - $_stripIncr - $_stripExtra}]\
                               [expr {$sy - ($_stripWidth / 2.0)}] \
                               0.0]]
                set striplen [expr {$xoff + $_pspin1Xoff + $_stripExtra}]
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
                set stripCP [GeometryFunctions translate3D_point $options(-origin) \
                             [list $_stripOffset \
                              [expr {$sy - ($_stripWidth / 2.0)}] \
                              0.0]]
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
    method MountingHoleBottom {i {z 0}} {
        lassign [[set mh$i] cget -bottom] x y dummy
        return [list $x $y $z]
    }
    method MountingHoleRadius {} {
        return [expr {$_mhdia / 2.0}]
    }
    
    method MountingHole {name i baseZ height} {
        lassign [[set mh$i] cget -bottom] x y z
        set bottom [list $x $y $baseZ]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [[set mh$i] cget -radius] \
                -height $height \
                -color {255 255 255}]
    }
    method Standoff {name i baseZ height diameter color} {
        lassign [[set mh$i] cget -bottom] x y z
        set bottom [list $x $y $baseZ]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [expr {$diameter / 2.0}] \
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

snit::type Littlefuse_FuseHolder_02810005H_02810008H {
    Common
    typevariable _dia      [expr {0.25*25.4}]
    typevariable _height   [expr {0.23*25.4}]
    typevariable _standoff [expr {0.032*25.4}]
    typevariable _pinlen   [expr {0.23*25.4}]
    typevariable _pindia   [expr {0.046*25.4}]
    typevariable _pinXoff  2.54
    typevariable _pinYoff  5.08
    component body
    component standoff1
    component standoff2
    component standoff3
    component standoff4
    component pin1
    component pin2
    constructor {args} {
        $self configurelist $args
        set bodyradius [expr {$_dia / 2.0}]
        set pinradius  [expr {$_pindia / 2.0}]
        set standoffdelta [expr {$bodyradius - $pinradius}]
        install body using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 0 $_standoff]] \
              -radius $bodyradius \
              -height $_height \
              -direction Z \
              -color {255 255 255}
        install standoff1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 $standoffdelta 0]] \
              -radius $pinradius \
              -height $_standoff \
              -direction Z \
              -color {255 255 255}
        install standoff2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list -$standoffdelta 0 0]] \
              -radius $pinradius \
              -height $_standoff \
              -direction Z \
              -color {255 255 255}
        install standoff3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 -$standoffdelta 0]] \
              -radius $pinradius \
              -height $_standoff \
              -direction Z \
              -color {255 255 255}
        install standoff4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $standoffdelta 0 0]] \
              -radius $pinradius \
              -height $_standoff \
              -direction Z \
              -color {255 255 255}
        install pin1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list [expr {-($_pinXoff/2.0)}] \
                        [expr {-($_pinYoff/2.0)}] 0]] \
              -radius $pinradius \
              -height -$_pinlen \
              -direction Z \
              -color {200 200 200}
        install pin2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list [expr {($_pinXoff/2.0)}] \
                        [expr {($_pinYoff/2.0)}] 0]] \
              -radius $pinradius \
              -height -$_pinlen \
              -direction Z \
              -color {200 200 200}
    }
    method print {{fp stdout}} {
        $body      print $fp
        $standoff1 print $fp
        $standoff2 print $fp
        $standoff3 print $fp
        $standoff4 print $fp
        $pin1      print $fp
        $pin2      print $fp
    }
}

# 576-30313150421 3.15A fuse

snit::type Littlefuse_FuseHolder_02810007H_02810010H {
    Common
    typevariable _width     [expr {0.25*25.4}]
    typevariable _length    [expr {0.28*25.4}]
    typevariable _height    [expr {0.26*25.4}]
    typevariable _pinlen    [expr {0.20*25.4}]
    typevariable _pindia    [expr {0.046*25.4}]
    typevariable _pinXspace [expr {0.1*25.4}]
    typevariable _pinYspace [expr {0.20*25.4}]
    component body
    component pin1
    component pin2
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) xc yc zc
        set w2 [expr {$_width / 2.0}]
        set l2 [expr {$_length / 2.0}]
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$xc - $w2}] \
                                      [expr {$yc - $l2}] $zc] \
                        -vec1 [list $_width 0 0] \
                        -vec2 [list 0 $_length 0]] \
              -vector [list 0 0 $_height] \
              -color {255 255 255}
        install pin1 using Cylinder %AUTO% \
              -bottom [list [expr {$xc - ($_pinXspace / 2.0)}] \
                       [expr {$yc - ($_pinYspace / 2.0)}] \
                       $zc] \
              -radius [expr {$_pindia / 2.0}] \
              -direction Z \
              -height -$_pinlen \
              -color {200 200 200}
        install pin2 using Cylinder %AUTO% \
              -bottom [list [expr {$xc + ($_pinXspace / 2.0)}] \
                       [expr {$yc + ($_pinYspace / 2.0)}] \
                       $zc] \
              -radius [expr {$_pindia / 2.0}] \
              -direction Z \
              -height -$_pinlen \
              -color {200 200 200}
    }
    method print {{fp stdout}} {
        $body print $fp
        $pin1 print $fp
        $pin2 print $fp
    }
}

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
              -bottom [list $xc [expr {$yc - $l2}] [expr {$zc - $brad}]] \
              -radius $brad \
              -height $_bodylen \
              -direction Y \
              -color {50 50 50}
        install lead1h using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc - $l2}] [expr {$zc - $brad}]] \
              -radius [expr {$_leaddia/2.0}] \
              -height -$leadhlen \
              -direction Y \
              -color {250 250 250}
        install lead2h using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc + $l2}] [expr {$zc - $brad}]] \
              -radius [expr {$_leaddia/2.0}] \
              -height $leadhlen \
              -direction Y \
              -color {250 250 250}
        install lead1v using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc - ($_leadspacing/2.0)}] [expr {$zc - $brad}]] \
              -radius [expr {$_leaddia/2.0}] \
              -height $leadvlen \
              -direction Z \
              -color {250 250 250}
        install lead2v using Cylinder %AUTO% \
              -bottom [list $xc [expr {$yc + ($_leadspacing/2.0)}] [expr {$zc - $brad}]] \
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

snit::type B72220S2301K101 {
    Common
    typevariable _W 21.5
    typevariable _th 6.1
    typevariable _h 25.5
    typevariable _d 1.0
    typevariable _e 10
    typevariable _a 2.1
    typevariable _l 25.0
    typevariable _seatoffset 3
    typevariable _leadspacing [expr {8 * 2.54}]
    component body
    component seat1
    component seat2
    component lead1h
    component lead2h
    component lead1v
    component lead2v
    constructor {args} {
        $self configurelist $args
        lassign $options(-origin) xc yc zc
        set bodyradius [expr {$_W / 2.0}]
        install body using Cylinder %AUTO% \
              -bottom [list [expr {$xc +  $bodyradius}] $yc $zc] \
              -radius $bodyradius \
              -direction Z \
              -height -$_th \
              -color {0 0 0}
        install seat1 using Cylinder %AUTO% \
              -bottom [list [expr {$xc + ($_seatoffset*.5)}] [expr {$yc - ($_e/2.0)}] [expr {($zc - ($_th/2.0)) - ($_a/2.0)}]] \
              -radius $_d \
              -direction X \
              -height [expr {$_seatoffset*(-1.5)}] \
              -color {0 0 0}
        install seat2 using Cylinder %AUTO% \
              -bottom [list [expr {$xc + ($_seatoffset*.5)}] [expr {$yc + ($_e/2.0)}] [expr {($zc - ($_th/2.0)) + ($_a/2.0)}]] \
              -radius $_d \
              -direction X \
              -height [expr {$_seatoffset*(-1.5)}] \
              -color {0 0 0}
        set leadhlen [expr {($_leadspacing/2.0)-($_e/2.0)}]
        install lead1h using Cylinder %AUTO% \
              -bottom [list [expr {$xc -$_seatoffset}] \
                       [expr {$yc - ($_e/2.0)}] \
                       [expr {($zc - ($_th/2.0)) - ($_a/2.0)}]] \
              -radius [expr {$_d / 2.0}] \
              -direction Y \
              -height -$leadhlen \
              -color {250 250 250}
        lassign [$lead1h cget -bottom] l1x l1y l1z
        set l1vheight [expr {abs($zc-(((1/16.0)*2.54)) + $l1z)}]
        #puts stderr "*** $type create $self: zc = $zc, l1z = $l1z, l1vheight = $l1vheight"
        set l1vy      [expr {$l1y - $leadhlen}]
        install lead1v using Cylinder %AUTO% \
              -bottom [list $l1x $l1vy $l1z] \
              -radius [expr {$_d / 2.0}] \
              -direction Z \
              -height $l1vheight \
              -color {250 250 250}
        install lead2h using Cylinder %AUTO% \
              -bottom [list [expr {$xc -$_seatoffset}] \
                       [expr {$yc + ($_e/2.0)}] \
                       [expr {($zc - ($_th/2.0)) + ($_a/2.0)}]] \
              -radius [expr {$_d / 2.0}] \
              -direction Y \
              -height $leadhlen \
              -color {250 250 250}
        lassign [$lead2h cget -bottom] l2x l2y l2z
        set l2vheight [expr {abs($zc-(((1/16.0)*2.54)) + $l2z)}]
        set l2vy      [expr {$l2y + $leadhlen}]
        install lead2v using Cylinder %AUTO% \
              -bottom [list $l2x $l2vy $l2z] \
              -radius [expr {$_d / 2.0}] \
              -direction Z \
              -height $l2vheight \
              -color {250 250 250}
    }
    method print {{fp stdout}} {
        $body print $fp
        $seat1 print $fp
        $seat2 print $fp
        $lead1h print $fp
        $lead1v print $fp
        $lead2h print $fp
        $lead2v print $fp

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
    component fuseholder;# 02810010H
    component mov;# 871-B72220S2301K101
    component bypasscap;# 80-C333C105K5R  1uf 50V  
    component filtercap;# 661-EGXE160ELL221M
    component esd;# 821-P6KE8V2A  ESD/TVS diode.
    variable wires [list]
    typevariable _fuseholderX 6.35
    typevariable _fuseholderY 25.40
    typevariable _bypassX [expr {76.2-27.94}]
    typevariable _bypassY 15.24
    typevariable _filterX [expr {76.2-5.08}]
    typevariable _filterY 27.94
    typevariable _esdX [expr {76.2-17.78}]
    typevariable _esdY 17.78
    typevariable _wiredia 1.5
    delegate method MountingHole to pcboard
    delegate method MountingHoleBottom to pcboard
    delegate method MountingHoleRadius to pcboard
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
        install bypasscap using C333 %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_bypassX $_bypassY 0]]
        install filtercap using AL_CAP_Radial_5mm10x12.5 %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_filterX $_filterY $_psPCBThickness]]
        install esd using DO_15_bendedLeads_400_under %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_esdX $_esdY 0]]
        install fuseholder using Littlefuse_FuseHolder_02810007H_02810010H %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_fuseholderX $_fuseholderY $_psPCBThickness]]
        install mov using B72220S2301K101 %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list [expr {$xoff + $_pspin1Xoff}] \
                        [expr {$_psPCBwidth / 2.0}] 0]]
        set groundj1X [expr {$_psPCBlength / 2.0}]
        set groundj1Y [expr {($_pspin1Yoff - 2.54)+$yoff}]
        set groundj1L [expr {20.32+5.08}]
        set wireradius [expr {$_wiredia / 2.0}]
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $groundj1X $groundj1Y -$wireradius]] \
                       -radius $wireradius \
                       -direction Y \
                       -height $groundj1L \
                       -color {0 255 0}]
        for {set i 1} {$i <= 3} {incr i} {
            set yy [expr {$i * 2.54}]
            set xx [expr {($i & 1) * 2.54}]
            set y1 [expr {$groundj1Y - $yy}]
            set y2 [expr {$groundj1Y+$groundj1L+$yy}]
            set x  [expr {$groundj1X + $xx}]
            lappend wires [Cylinder create %AUTO% \
                           -bottom [GeometryFunctions translate3D_point \
                                    $options(-origin) \
                                    [list $x $y1 -$wireradius]] \
                           -radius $wireradius \
                           -direction Y \
                           -height 2.54 \
                           -color {0 255 0}]
            lappend wires [Cylinder create %AUTO% \
                           -bottom [GeometryFunctions translate3D_point \
                                    $options(-origin) \
                                    [list $x $y2 -$wireradius]] \
                           -radius $wireradius \
                           -direction Y \
                           -height -2.54 \
                           -color {0 255 0}]
        }
        set l1Y [expr {$_psactermyoff + (5*2.54)}]
        set l1X [expr {5.08 + 2.54}]
        set l1L 5.08
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $l1X $l1Y -$wireradius]] \
                       -radius $wireradius \
                       -direction Y \
                       -height $l1L \
                       -color {0 0 0}]
        set l2Y [expr {$l1Y + 5.08 +5.08}]
        set l2X 5.08
        set l2L 5.08
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $l2X $l2Y -$wireradius]] \
                       -radius $wireradius \
                       -direction Y \
                       -height $l2L \
                       -color {0 0 0}]
        set P1Y [expr {$_psdctermyoff + (3*2.54)}]
        set P1X [expr {$_psPCBlength - $_pstermxoff - ($_termwidth/2.0) - 2.54}]
        set P1L 5.08
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $P1X $P1Y -$wireradius]] \
                       -radius $wireradius \
                       -direction Y \
                       -height $P1L \
                       -color {255 0 0}]
        set P2Y [expr {$P1Y + $P1L}]
        set P2X [expr {$P1X - 2.54}]
        set P2L 7.62
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $P2X $P2Y -$wireradius]] \
                       -radius $wireradius \
                       -direction Y \
                       -height $P2L \
                       -color {255 0 0}]
        set M1Y [expr {$_psdctermyoff + 2.54}]
        set M1X [expr {$P2X - 2.54}]
        set M1L [expr {2.54*5}]
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $M1X $M1Y -$wireradius]] \
                       -radius $wireradius \
                       -direction Y \
                       -height $M1L \
                       -color {0 0 0}]
        
        
    }
    method print {{fp stdout}} {
        $powersupply print $fp
        $pcboard print $fp
        $acterm print $fp
        $dcterm print $fp
        $bypasscap print $fp
        $filtercap print $fp
        $esd print $fp
        $fuseholder print $fp
        $mov print $fp
        foreach w $wires {
            $w print $fp
        }
    }
}


## Al. box:      Mouser #563-CU-3002A
# Base: 2.125in wide, 4.000in long, 1.625in high
# Cover 2.031in wide, 3.906in long, 1.562in high

snit::macro CU_3002ADims {} {
    typevariable _CU_3002A_basewidth [expr {2.125*25.4}]
    typevariable _CU_3002A_baselength [expr {4.000*25.4}]
    typevariable _CU_3002A_baseheight [expr {1.625*25.4}]
    typevariable _CU_3002A_baseflangewidth  [expr {0.375*25.4}]
    typevariable _CU_3002A_baseholeoffset [expr {0.172*25.4}]
    typevariable _CU_3002A_baseholeheightoffset [expr {0.594*25.4}]
    typevariable _CU_3002A_baseholediameter [expr {(5.0/32.0)*25.4}]
    typevariable _CU_3002A_coverwidth [expr {2.031*25.4}]
    typevariable _CU_3002A_coverlength [expr {3.906*25.4}]
    typevariable _CU_3002A_coverheight [expr {1.562*25.4}]
    typevariable _CU_3002A_coverholeoffset [expr {0.156*25.4}]
    typevariable _CU_3002A_coverholeheightoffset [expr {0.968*25.4}]
    typevariable _CU_3002A_coverholediameter [expr {(3.0/32.0)*25.4}]
    typevariable _CU_3002A_thickness [expr {0.04*25.4}]
}

snit::type CU_3002A_Base {
    Common
    CU_3002ADims
    component bottom
    component front
    component back
    component leftfrontflange
    component leftfrontflangehole
    component leftbottomflange
    component leftbackflange
    component leftbackflangehole
    component rightfrontflange
    component rightfrontflangehole
    component rightbottomflange
    component rightbackflange
    component rightbackflangehole
    constructor {args} {
        $self configurelist $args
        install bottom using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_CU_3002A_baselength 0 0] \
                        -vec2 [list 0 $_CU_3002A_basewidth 0]] \
              -vector [list 0 0 $_CU_3002A_thickness] \
              -color {192 192 192}
        install front using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list 0 $_CU_3002A_basewidth 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list $_CU_3002A_thickness 0 0] \
              -color {192 192 192}
        install back using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_baselength 0 0]] \
                        -vec1 [list 0 $_CU_3002A_basewidth 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}
        install leftfrontflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 $_CU_3002A_basewidth 0]] \
                        -vec1 [list $_CU_3002A_baseflangewidth 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}
        lassign [[$leftfrontflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install leftfrontflangehole using Cylinder %AUTO% \
              -bottom [list [expr {($lffx + $_CU_3002A_baseflangewidth) - $_CU_3002A_baseholeoffset}] \
                       $lffy  \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
        install leftbottomflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 $_CU_3002A_basewidth 0]] \
                        -vec1 [list $_CU_3002A_baselength 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseflangewidth]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}
        install leftbackflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_baselength $_CU_3002A_basewidth 0]] \
                        -vec1 [list -$_CU_3002A_baseflangewidth 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}                        
        lassign [[$leftbackflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install leftbackflangehole using Cylinder %AUTO% \
              -bottom [list [expr {($lffx - $_CU_3002A_baseflangewidth) + $_CU_3002A_baseholeoffset}] \
                       $lffy  \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
                install leftfrontflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 $_CU_3002A_basewidth 0]] \
                        -vec1 [list $_CU_3002A_baseflangewidth 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}
        install rightfrontflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 0 0]] \
                        -vec1 [list $_CU_3002A_baseflangewidth 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}
        lassign [[$rightfrontflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install rightfrontflangehole using Cylinder %AUTO% \
              -bottom [list [expr {($lffx + $_CU_3002A_baseflangewidth) - $_CU_3002A_baseholeoffset}] \
                       $lffy  \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
        install rightbottomflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 0 0]] \
                        -vec1 [list $_CU_3002A_baselength 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseflangewidth]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}
        install rightbackflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_baselength 0 0]] \
                        -vec1 [list -$_CU_3002A_baseflangewidth 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}                        
        lassign [[$rightbackflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install rightbackflangehole using Cylinder %AUTO% \
              -bottom [list [expr {($lffx - $_CU_3002A_baseflangewidth) + $_CU_3002A_baseholeoffset}] \
                       $lffy  \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $bottom print $fp
        $front  print $fp
        $back   print $fp
        $leftfrontflange print $fp
        $leftfrontflangehole print $fp
        $leftbottomflange print $fp
        $leftbackflange print $fp
        $leftbackflangehole print $fp
        $rightfrontflange print $fp
        $rightfrontflangehole print $fp
        $rightbottomflange print $fp
        $rightbackflange print $fp
        $rightbackflangehole print $fp
        
    }
}

snit::type CU_3002A_Cover {
    Common
    CU_3002ADims
    component top
    component left
    component leftfronthole
    component leftbackhole
    component right
    component rightfronthole
    component rightbackhole
    constructor {args} {
        $self configurelist $args
        install top using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_thickness $_CU_3002A_thickness [expr {$_CU_3002A_thickness + $_CU_3002A_coverheight}]]]\
                        -vec1 [list $_CU_3002A_coverlength 0 0] \
                        -vec2 [list 0 $_CU_3002A_coverwidth 0]] \
              -vector [list 0 0 -$_CU_3002A_thickness] \
              -color  {192 192 192}
        install left using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_thickness $_CU_3002A_thickness $_CU_3002A_thickness]]\
                        -vec1 [list $_CU_3002A_coverlength 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_coverheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color  {192 192 192}
        lassign [[$left cget -surface] cget -cornerpoint] lx ly lz
        install leftfronthole using Cylinder %AUTO% \
              -bottom [list [expr {$lx + $_CU_3002A_coverholeoffset}] \
                       $ly [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
        install leftbackhole  using Cylinder %AUTO% \
              -bottom [list [expr {$lx + $_CU_3002A_coverlength - $_CU_3002A_coverholeoffset}] \
                       $ly [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
        install right using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list $_CU_3002A_thickness \
                                       [expr {$_CU_3002A_thickness + $_CU_3002A_coverwidth}] \
                                       $_CU_3002A_thickness]]\
                        -vec1 [list $_CU_3002A_coverlength 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_coverheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color  {192 192 192}
        lassign [[$right cget -surface] cget -cornerpoint] rx ry rz
        install rightfronthole using Cylinder %AUTO% \
              -bottom [list [expr {$rx + $_CU_3002A_coverholeoffset}] \
                       $ry [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
        install rightbackhole  using Cylinder %AUTO% \
              -bottom [list [expr {$rx + $_CU_3002A_coverlength - $_CU_3002A_coverholeoffset}] \
                       $ry [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction Y \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $top print $fp
        $left print $fp
        $leftfronthole print $fp
        $leftbackhole print $fp
        $right print $fp
        $rightfronthole print $fp
        $rightbackhole print $fp
    }
}


snit::type CU_3002A {
    Common
    CU_3002ADims
    component base
    component cover
    constructor {args} {
        $self configurelist $args
        install base using CU_3002A_Base %AUTO% \
              -origin $options(-origin)
        install cover using CU_3002A_Cover %AUTO% \
              -origin $options(-origin)
    }
    method print {{fp stdout}} {
        $base print $fp
        $cover print $fp
    }
}

snit::macro 701w202_890462Dims {} {
    typevariable _flangewidth 30.7
    typevariable _flangeheight 23.7
    typevariable _flangedepth 3.2
    typevariable _bodywidth 27
    typevariable _bodyheight 20
    typevariable _bodydepth 16
    typevariable _lugwidth 24
    typevariable _lugheight 16
    typevariable _lugdepth 7
}

snit::type 701w202_890462 {
    Common
    701w202_890462Dims
    component flange
    component body
    component solderlugs
    constructor {args} {
        $self configurelist $args
        set flangexoff [expr {($_flangewidth - $_bodywidth)/2.0}]
        set flageeyoff [expr {($_flangeheight - $_bodyheight)/2.0}]
        install flange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list 0 -$flangexoff -$flageeyoff]] \
                        -vec1 [list 0 $_flangewidth 0] \
                        -vec2 [list 0 0 $_flangeheight]] \
              -vector [list -$_flangedepth 0 0] \
              -color {0 0 0}
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list 0 $_bodywidth 0] \
                        -vec2 [list 0 0 $_bodyheight]] \
              -vector [list $_bodydepth 0 0] \
              -color {0 0 0}
        set lugxoff [expr {($_bodywidth - $_lugwidth) / 2.0}]
        set lugyoff [expr {($_bodyheight - $_lugheight) / 2.0}]
        install solderlugs using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list $_bodydepth $lugxoff $lugyoff]] \
                        -vec1 [list 0 $_lugwidth 0] \
                        -vec2 [list 0 0 $_lugheight]] \
              -vector [list $_lugdepth 0 0] \
              -color {192 192 192}
    }
    method FlangeSurface {} {
        return [$flange cget -surface]
    }
    method print {{fp stdout}} {
        $flange print $fp
        $body   print $fp
        $solderlugs print $fp
    }
}

snit::type DCStrainRelief {
    Common
    typevariable _holedia 11.40
    typevariable _flangedia 13.40
    typevariable _flangedepth 4.0
    typevariable _bodydia 13.31
    typevariable _bodydepth 6.0
    component flange
    component body
    constructor {args} {
        $self configurelist $args
        install flange using Cylinder %AUTO% \
              -bottom $options(-origin) \
              -radius [expr {$_flangedia / 2.0}] \
              -height $_flangedepth \
              -direction X \
              -color {0 0 0}
        install body using Cylinder %AUTO% \
              -bottom $options(-origin) \
              -radius [expr {$_bodydia / 2.0}] \
              -height -$_bodydepth \
              -direction X \
              -color {0 0 0}
    }
    method print {{fp stdout}} {
        $flange print $fp
        $body   print $fp
    }
}

# 472-02510SS-05P-AT00 DC Fans DC Axial Fan, 25x10mm, 5VDC, 2.5CFM, Rib, Sleeve Bearing, Tachometer, 3 Lead Wires

snit::macro Fan02510SS_05P_AT00Dims {} {
    typevariable _fanwidth_height 25
    typevariable _fandepth 10
    typevariable _fanmholespacing 20
    typevariable _fanmholedia 2.8
    typevariable _fanholedia 24.3
}

snit::type Fan02510SS_05P_AT00 {
    Common
    Fan02510SS_05P_AT00Dims
    component body
    component mh1
    component mh2
    component mh3
    component mh4
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_fanwidth_height 0 0] \
                        -vec2 [list 0 0 $_fanwidth_height]] \
              -vector [list 0 $_fandepth 0] \
              -color {0 0 0}
        set mhXYoff [expr {($_fanwidth_height-$_fanmholespacing)/2.0}]
        install mh1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $mhXYoff 0 $mhXYoff]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction Y \
              -height $_fandepth \
              -color {255 255 255}
        install mh2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list [expr {$mhXYoff+$_fanmholespacing}] 0 $mhXYoff]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction Y \
              -height $_fandepth \
              -color {255 255 255}
        install mh3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list $mhXYoff 0  [expr {$mhXYoff+$_fanmholespacing}]]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction Y \
              -height $_fandepth \
              -color {255 255 255}
        install mh4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list [expr {$mhXYoff+$_fanmholespacing}] 0 [expr {$mhXYoff+$_fanmholespacing}]]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction Y \
              -height $_fandepth \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $body print $fp
        $mh1  print $fp
        $mh2  print $fp
        $mh3  print $fp
        $mh4  print $fp
    }
    method MountingHole {name i yBase height} {
        lassign [[set mh$i] cget -bottom] mhx mhy mhz
        return [Cyninder create $name \
                -bottom [list $mhx $yBase $mhz] \
                -radius [expr {$_fanmholedia/2.0}] \
                -direction Y \
                -height $height \
                -color {255 255 255}]
    }
    method FanHole {name yBase height} {
        lassign $options(-origin) ox oy oz
        set x [expr {$ox + ($_fanwidth_height/2.0)}]
        set y $yBase
        set z [expr {$oz + ($_fanwidth_height/2.0)}]
        return [Cylinder create $name \
                -bottom [list $x $y $z] \
                -radius [expr {$_fanholedia/2.0}] \
                -direction Y \
                -height $height \
                -color {255 255 255}]
    }
    method FanHoleDims {args} {
        set i [from args -fanno 1]
        set reportfp [from args -reportfp stdout]
        set macrofp  [from args -macrofp  {}]
        set origin [from args -origin [list 0.0 0.0 0.0]]
        set rotation [from args -rotation 0.0]
        set fansurf [$body cget -surface]
        set corner  [$fansurf cget -cornerpoint]
        lassign $corner ox oy oz
        #puts stderr "*** $self FanHoleDims: corner = ($ox $oy $oz)"
        set x [expr {$ox + $_fandepth}]
        set y [expr {$oy + ($_fanwidth_height/2.0)}]
        set z [expr {$oz + ($_fanwidth_height/2.0)}]
        set points [list [list $x $y $z 1]]
        #puts stderr "*** $self FanHoleDims: points (center) is $points"
        set rotated [GeometryFunctions rotateZAxis $points [GeometryFunctions radians $rotation]]
        #puts stderr "*** $self FanHoleDims: rotated (center) is $rotated"
        set translated [GeometryFunctions translate3D $rotated $origin]
        #puts stderr "*** $self FanHoleDims: translated (center) is $translated"
        lassign [lindex $translated 0] ox oy oz H
        #puts stderr "*** $self FanHoleDims: ox oy oz (center): ($ox $oy $oz)"
        puts $reportfp [format {Fan%d: Center {%g %g %g}, Diameter %g} $i $ox $oy $oz $_fanholedia]
        if {$macrofp ne {}} {
            puts $macrofp [format {    typevariable _fan%dCenter {%g %g %g}} $i $ox $oy $oz]
            puts $macrofp [format {    typevariable _fan%dDiameter %g} $i $_fanholedia]
        }
    }
}



snit::type PSBox {
    Common
    CU_3002ADims
    Fan02510SS_05P_AT00Dims
    PSDims
    typevariable _standoff_height 9.0
    typevariable _standoff_dia 5.0
    typevariable _inletYoff  24
    typevariable _inletZoff  19
    typevariable _dcstrainYoff 26.9875
    typevariable _dcstrainZoff 20.6375
    proc _fanYoff {} {
        return [expr {$_CU_3002A_thickness + $_CU_3002A_coverwidth}]
    }
    proc _fanZoff {} {
        return [expr {$_CU_3002A_baseflangewidth+$_CU_3002A_thickness}]
    }
    proc _fan1Xoff {} {
        return [expr {($_CU_3002A_coverlength-(2*$_fanwidth_height))/2.0}]
    }
    proc _fan2Xoff {} {
        return [expr {[_fan1Xoff]+$_fanwidth_height}]
    }
    component box
    component pcb
    component standoff1
    component standoff2
    component standoff3
    component standoff4
    component mh1
    component mh2
    component mh3
    component mh4
    component inlet
    component dcstrainrelief
    component fan1
    component fan2
    constructor {args} {
        $self configurelist $args
        install box using CU_3002A %AUTO% \
              -origin $options(-origin)
        install pcb using PSOnPCB %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list [expr {($_CU_3002A_baselength-$_psPCBlength)/2.0}] \
                        [expr {($_CU_3002A_basewidth-$_psPCBwidth)/2.0}] \
                        [expr {$_CU_3002A_thickness+$_standoff_height}]]]
        lassign $options(-origin) x y z
        set standoff1 [$pcb Standoff %AUTO% 1 [expr {$z + $_CU_3002A_thickness}] $_standoff_height $_standoff_dia {255 255 0}]
        set standoff2 [$pcb Standoff %AUTO% 2 [expr {$z + $_CU_3002A_thickness}] $_standoff_height $_standoff_dia {255 255 0}]
        set standoff3 [$pcb Standoff %AUTO% 3 [expr {$z + $_CU_3002A_thickness}] $_standoff_height $_standoff_dia {255 255 0}]
        set standoff4 [$pcb Standoff %AUTO% 4 [expr {$z + $_CU_3002A_thickness}] $_standoff_height $_standoff_dia {255 255 0}]
        set mh1       [$pcb MountingHole %AUTO% 1 $z $_CU_3002A_thickness]
        set mh2       [$pcb MountingHole %AUTO% 2 $z $_CU_3002A_thickness]
        set mh3       [$pcb MountingHole %AUTO% 3 $z $_CU_3002A_thickness]
        set mh4       [$pcb MountingHole %AUTO% 4 $z $_CU_3002A_thickness]
        install inlet using 701w202_890462 %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 $_inletYoff $_inletZoff]]
        install dcstrainrelief using DCStrainRelief %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_CU_3002A_baselength $_dcstrainYoff $_dcstrainZoff]]
        install fan1 using Fan02510SS_05P_AT00 %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list [_fan1Xoff] [_fanYoff] [_fanZoff]]]
        install fan2 using Fan02510SS_05P_AT00 %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list [_fan2Xoff] [_fanYoff] [_fanZoff]]]
    }
    method print {{fp stdout}} {
        $box print $fp
        $pcb print $fp
        $standoff1 print $fp
        $standoff2 print $fp
        $standoff3 print $fp
        $standoff4 print $fp
        $mh1       print $fp
        $mh2       print $fp
        $mh3       print $fp
        $mh4       print $fp
        $inlet     print $fp
        $dcstrainrelief print $fp
        $fan1      print $fp
        $fan2      print $fp
    }
    method CaseHolesAndCutouts {args} {
        set reportfp [from args -reportfp stdout]
        set macrofp  [from args -macrofp  {}]
        if {$macrofp ne {}} {
            puts -nonewline $macrofp "snit::macro PSBoxHolesAndCutouts {} "
            puts $macrofp [format {%c} 123]
        }
        set origin [from args -origin [list 0.0 0.0 0.0]]
        set rotation [from args -rotation 0.0]
        set points [list]
        for {set i 1} {$i <= 4} {incr i} {
            lassign [$pcb MountingHoleBottom $i] mx my mz
            lappend points [list $mx $my $mz 1]
        }
        set rotated [GeometryFunctions rotateZAxis $points [GeometryFunctions radians $rotation]]
        set translated [GeometryFunctions translate3D $rotated $origin]
        puts $reportfp "Mounting holes:"
        set i 1
        foreach p $translated {
            lassign $p x y z h
            puts $reportfp [format {%d %g %g %g} $i $x $y $z]
            if {$macrofp ne {}} {
                puts $macrofp [format {    typevariable _psBoxMH%d [list %g %g 0]} $i $x $y]
            }
            incr i
        }
        puts $reportfp [format {Radius: %g} [$pcb MountingHoleRadius]]
        if {$macrofp ne {}} {
            puts $macrofp [format {    typevariable _psBoxMHRadius %g} [$pcb MountingHoleRadius]]
        }
        set inletSlangeSurf [$inlet FlangeSurface]
        set flangecorner [$inletSlangeSurf cget -cornerpoint]
        set flangevec1   [$inletSlangeSurf cget -vec1]
        set flangevec2   [$inletSlangeSurf cget -vec2]
        set points [GeometryFunctions MakeHomogenous [list $flangecorner $flangevec1 $flangevec2]]
        set rotated [GeometryFunctions rotateZAxis $points [GeometryFunctions radians $rotation]]
        set translated [GeometryFunctions translate3D $rotated $origin]
        puts $reportfp "Inlet opening:"
        lassign [lindex $translated 0] x y z h
        puts $reportfp [format {-cornerpoint %g %g %g} $x $y $z]
        if {$macrofp ne {}} {
            puts $macrofp [format {    typevariable _inletCornerPoint [list %g %g %g]} $x $y $z]
        }
        lassign [lindex $rotated 1] x y z h
        puts $reportfp [format {-vec1 %g %g %g} $x $y $z]
        if {$macrofp ne {}} {
            puts $macrofp [format {    typevariable _inletVec1 [list %g %g %g]} $x $y $z]
        }
        lassign [lindex $rotated 2] x y z h
        puts $reportfp [format {-vec2 %g %g %g} $x $y $z]
        if {$macrofp ne {}} {
            puts $macrofp [format {    typevariable _inletVec2 [list %g %g %g]} $x $y $z]
        }
        $fan1 FanHoleDims -fanno 1 -reportfp $reportfp -macrofp $macrofp \
              -origin $origin -rotation $rotation
        $fan2 FanHoleDims -fanno 2 -reportfp $reportfp -macrofp $macrofp \
              -origin $origin -rotation $rotation
        if {$macrofp ne {}} {
            puts $macrofp [format {%c} 125]
        }
    }
}

set modelFP [open [file rootname [info script]].gcad w]

## GCad prefix blather.
puts $modelFP "# [clock format [clock seconds] -format {%Y/%m/%d-%M:%M:%S}]"
puts $modelFP {DEFCOL 0 0 0}

PSBox create psbox
psbox print $modelFP

#PSOnPCB create pcb
#pcb print $modelFP


close $modelFP

set mountingCutoutReport [open [file rootname [info script]]_mountReport.txt w]
set mountingCutoutMacro  [open [file rootname [info script]]_mountMacro.tcl w]
psbox CaseHolesAndCutouts -reportfp $mountingCutoutReport \
      -macrofp $mountingCutoutMacro -rotation -90 \
      -origin [list [expr {(14 * 25.4)-13.175-(2.125*25.4)}] \
               [expr {(10 * 25.4)-(0.000*25.4)}] \
               [expr {(1.0/8.0)*25.4}]]
close $mountingCutoutReport
close $mountingCutoutMacro
