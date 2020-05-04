#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Thu Apr 9 14:09:26 2020
#  Last Modified : <200503.1536>
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

snit::macro PortableM64CaseCommon {} {
    typevariable _Width [expr {14 * 25.4}]
    typevariable _Height [expr {10 * 25.4}]
    typevariable _BottomDepth [expr {1.5 * 25.4}]
    typevariable _MiddleTotalDepth [expr {1.5 * 25.4}]
    typevariable _MiddleLowerDepth [expr {.5 * 25.4}]
    typevariable _TopDepth [expr {(.5+.125) * 25.4}]
    typevariable _WallThickness [expr {.125 * 25.4}]
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

snit::macro M64Dims {} {
    typevariable _m64_m1_relpos [list [expr {96.4-93.64472}] [expr {59.9-57.15}]]
    typevariable _m64_m2_relpos [list [expr {96.4-7.79526}] [expr {59.9-57.15}]]
    typevariable _m64_m3_relpos [list [expr {96.4-93.64472}] [expr {59.9-2.794}]]
    typevariable _m64_m4_relpos [list [expr {96.4-7.79526}] [expr {59.9-8.0772}]]
    typevariable _m64XOff 0
    typevariable _m64YOff [expr {1*25.4}]
    typevariable _m64YMin 0
    typevariable _m64YMax 59.90082
    typevariable _m64XMin 5.00126
    typevariable _m64XMax 96.4
    typevariable _m64Thickness [expr {.06125*25.4}]
    typevariable _m64Standoff [expr {.25*25.4}]
    typevariable _PlateHeight 16
    typevariable _DualUSBcutoutYMin 30.83814
    typevariable _DualUSBcutoutYMax 45.23994
    typevariable _DualUSBHeight 15.60
    typevariable _DualUSBWidth 14.40
    typevariable _RJ45YMin 10.96518
    typevariable _RJ45YMax 26.45918
    typevariable _RJ45Height 13.35
    typevariable _RJ45Width 16
    typevariable _AudioYMin 47.55642
    typevariable _AudioYMax 53.15458
    typevariable _AudioDiameter 5.6
    typevariable _gpioHeaderXOffset [expr {26.16962-3.57}]
    typevariable _gpioHeaderLength 55.4
    typevariable _gpioHeaderHeight 16.1
}
snit::type PortableM64CasePanel {
    PortableM64CaseCommon
    component panel
    delegate option * to panel
    constructor {args} {
        $self configurelist $args
        install panel using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) [list $_WallThickness $_WallThickness 0]] \
                        -vec1 [list [expr {$_Width - ($_WallThickness * 2.0)}] 0.0 0.0] \
                        -vec2 [list 0 [expr {$_Height - ($_WallThickness * 2.0)}] 0.0]] \
              -vector [list 0 0 $_WallThickness] \
              -color {255 0 0}
    }
    method PanelCornerPoint {} {
        set panelsurf [$panel cget -surface]
        return [$panelsurf cget -cornerpoint]
    }
    method PanelThickness {} {
        return [lindex [$panel cget -vector] 2]
    }
    method PanelDirection {} {return Z}
    method print {{fp stdout}} {
        $panel print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set panelsurf [$panel cget -surface]
        set width [lindex [$panelsurf cget -vec1] 0]
        set height [lindex [$panelsurf cget -vec2] 1]
        set thick [lindex [$panel cget -vector] 2]
        incr partListArray([$self _normPartSize $width $height $thick])
    }
}

snit::type PortableM64CaseLeftPanel {
    PortableM64CaseCommon
    component panel
    delegate option * to panel
    option -depth -type snit::double -default 0.0 -readonly yes
    constructor {args} {
        $self configurelist $args
        install panel using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) [list 0 $_WallThickness 0]] \
                        -vec1 [list 0 [expr {$_Height - ($_WallThickness * 2.0)}] 0] \
                        -vec2 [list 0 0 $options(-depth)]] \
              -vector [list $_WallThickness 0 0] \
              -color {0 255 0}
    }
    method PanelCornerPoint {} {
        set panelsurf [$panel cget -surface]
        return [$panelsurf cget -cornerpoint]
    }
    method PanelThickness {} {
        return [lindex [$panel cget -vector] 0]
    }
    method PanelDirection {} {return X}
    method print {{fp stdout}} {
        $panel print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set panelsurf [$panel cget -surface]
        set width [lindex [$panelsurf cget -vec2] 2]
        set height [lindex [$panelsurf cget -vec1] 1]
        set thick [lindex [$panel cget -vector] 0]
        incr partListArray([$self _normPartSize $width $height $thick])
    }
}

snit::type PortableM64CaseRightPanel {
    PortableM64CaseCommon
    component panel
    delegate option * to panel
    option -depth -type snit::double -default 0.0 -readonly yes
    constructor {args} {
        $self configurelist $args
        install panel using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list [expr {$_Width - $_WallThickness}] $_WallThickness 0]] \
                        -vec1 [list 0 [expr {$_Height - ($_WallThickness * 2.0)}] 0] \
                        -vec2 [list 0 0 $options(-depth)]] \
              -vector [list $_WallThickness 0 0] \
              -color {0 255 0}
    }
    method PanelCornerPoint {} {
        set panelsurf [$panel cget -surface]
        return [$panelsurf cget -cornerpoint]
    }
    method PanelThickness {} {
        return [lindex [$panel cget -vector] 0]
    }
    method PanelDirection {} {return X}
    method print {{fp stdout}} {
        $panel print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set panelsurf [$panel cget -surface]
        set width [lindex [$panelsurf cget -vec2] 2]
        set height [lindex [$panelsurf cget -vec1] 1]
        set thick [lindex [$panel cget -vector] 0]
        incr partListArray([$self _normPartSize $width $height $thick])
    }
}

snit::type PortableM64CaseFrontPanel {
    PortableM64CaseCommon
    component panel
    delegate option * to panel
    option -depth -type snit::double -default 0.0 -readonly yes
    constructor {args} {
        $self configurelist $args
        install panel using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_Width 0 0] \
                        -vec2 [list 0 0 $options(-depth)]] \
              -vector [list 0 $_WallThickness 0] \
              -color {0 255 0}
    }
    method PanelCornerPoint {} {
        set panelsurf [$panel cget -surface]
        return [$panelsurf cget -cornerpoint]
    }
    method PanelThickness {} {
        return [lindex [$panel cget -vector] 1]
    }
    method PanelDirection {} {return Y}
    method print {{fp stdout}} {
        $panel print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set panelsurf [$panel cget -surface]
        set width [lindex [$panelsurf cget -vec2] 2]
        set height [lindex [$panelsurf cget -vec1] 0]
        set thick [lindex [$panel cget -vector] 1]
        incr partListArray([$self _normPartSize $width $height $thick])
    }
}

snit::type PortableM64CaseBackPanel {
    PortableM64CaseCommon
    component panel
    delegate option * to panel
    option -depth -type snit::double -default 0.0 -readonly yes
    constructor {args} {
        $self configurelist $args
        install panel using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list 0 [expr {$_Height - $_WallThickness}] 0]] \
                        -vec1 [list $_Width 0 0] \
                        -vec2 [list 0 0 $options(-depth)]] \
              -vector [list 0 $_WallThickness 0] \
              -color {0 255 0}
    }
    method PanelCornerPoint {} {
        set panelsurf [$panel cget -surface]
        return [$panelsurf cget -cornerpoint]
    }
    method PanelThickness {} {
        return [lindex [$panel cget -vector] 1]
    }
    method PanelDirection {} {return Y}
    method print {{fp stdout}} {
        $panel print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set panelsurf [$panel cget -surface]
        set width [lindex [$panelsurf cget -vec2] 2]
        set height [lindex [$panelsurf cget -vec1] 0]
        set thick [lindex [$panel cget -vector] 1]
        incr partListArray([$self _normPartSize $width $height $thick])
    }
}

snit::type PortableM64CaseBottomPanel {
    M64Dims
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component m64_m1
    component m64_m2
    component m64_m3
    component m64_m4
    constructor {args} {
        install panel using PortableM64CasePanel %AUTO% \
              -origin [from args -origin]
        lassign [$panel PanelCornerPoint] cx cy cz
        set radius [expr {2.5 / 2.0}]
        set m64X [expr {$cx + $_m64XOff}]
        set m64Y [expr {$cy  + $_m64YOff}]
        install m64_m1 using Cylinder %AUTO% \
              -bottom [list [expr {$m64X + [lindex $_m64_m1_relpos 0]}] \
                       [expr {$m64Y + [lindex $_m64_m1_relpos 1]}] \
                       $cz] \
              -radius $radius \
              -height [$panel PanelThickness] \
              -direction [$panel PanelDirection] \
              -color {255 255 255}
        install m64_m2 using Cylinder %AUTO% \
              -bottom [list [expr {$m64X + [lindex $_m64_m2_relpos 0]}] \
                       [expr {$m64Y + [lindex $_m64_m2_relpos 1]}] \
                       $cz] \
              -radius $radius \
              -height [$panel PanelThickness] \
              -direction [$panel PanelDirection] \
              -color {255 255 255}
        install m64_m3 using Cylinder %AUTO% \
              -bottom [list [expr {$m64X + [lindex $_m64_m3_relpos 0]}] \
                       [expr {$m64Y + [lindex $_m64_m3_relpos 1]}] \
                       $cz] \
              -radius $radius \
              -height [$panel PanelThickness] \
              -direction [$panel PanelDirection] \
              -color {255 255 255}
        install m64_m4 using Cylinder %AUTO% \
              -bottom [list [expr {$m64X + [lindex $_m64_m4_relpos 0]}] \
                       [expr {$m64Y + [lindex $_m64_m4_relpos 1]}] \
                       $cz] \
              -radius $radius \
              -height [$panel PanelThickness] \
              -direction [$panel PanelDirection] \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $panel print $fp
        $m64_m1 print $fp
        $m64_m2 print $fp
        $m64_m3 print $fp
        $m64_m4 print $fp
    }
    method printPS {} {
        set fp  [PostScriptFile fp]
        set xi 0
        set yi 1
        set xorg 0
        set yorg 0
        set xscale .01968
        set yscale .01968
        set surf [$panel cget -surface]
        PostScriptFile newPage {Bottom Panel Drill Pattern}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $m64_m1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $m64_m2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $m64_m3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $m64_m4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Bottom Panel Drill Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _hole $m64_m1 $cx $cy
        _hole $m64_m2 $cx $cy
        _hole $m64_m3 $cx $cy
        _hole $m64_m4 $cx $cy
    }
    proc _hole {holecyl cx cy} {
        lassign [$holecyl cget -bottom] hx hy hz
        PostScriptFile hole [expr {$hx - $cx}] [expr {$hy - $cy}] \
              [expr {[$holecyl cget -radius] * 2.0}]
    }
}


snit::type PortableM64CaseBottomLeftPanel {
    M64Dims
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component dualUSBcutout
    component rj45cutout
    component audiojackcutout
    constructor {args} {
        install panel using PortableM64CaseLeftPanel %AUTO% \
              -origin [from args -origin] \
              -depth  [from args -depth]
        lassign [$panel PanelCornerPoint] cx cy cz
        set panelThick [$panel PanelThickness]
        set m64Y [expr {$cy + $_m64YOff + ($_m64YMax-$_m64YMin)}]
        set zbase [expr {$cz + $_m64Thickness + $_m64Standoff + $panelThick}]
        install rj45cutout using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list $cx [expr {$m64Y - $_RJ45YMin}] $zbase] \
                        -vec1 [list 0 -$_RJ45Width 0] \
                        -vec2 [list 0 0 $_RJ45Height]] \
              -vector [list $panelThick 0 0] \
              -color {255 255 255}
        install dualUSBcutout using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list $cx [expr {$m64Y - $_DualUSBcutoutYMin}] $zbase] \
                        -vec1 [list 0 -$_DualUSBWidth 0] \
                        -vec2 [list 0 0 $_DualUSBHeight]] \
              -vector [list $panelThick 0 0] \
              -color {255 255 255}
        install audiojackcutout using Cylinder %AUTO% \
              -bottom [list $cx \
                       [expr {$m64Y - (($_AudioYMin+$_AudioYMax)/2.0)}] \
                       [expr {$zbase + 2.5}]] \
              -radius [expr {$_AudioDiameter / 2.0}] \
              -height $panelThick \
              -direction [$panel PanelDirection] \
              -color {255 255 255}
                                      
    }
    method print {{fp stdout}} {
        $panel print $fp
        $rj45cutout print $fp
        $dualUSBcutout print $fp
        $audiojackcutout print $fp 
    }
    method printPS {} {
        set fp [PostScriptFile fp]
        set xi 1
        set yi 2
        set xorg 5
        set yorg 0
        set xscale -.01968
        set yscale .01968
        set surf [$panel cget -surface]
        PostScriptFile newPage {Left bottom Cutouts}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        [$rj45cutout cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        [$dualUSBcutout cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $audiojackcutout printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Left bottom Cutouts Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _hole $audiojackcutout $cy $cz
        _cutout [$rj45cutout cget -surface] $cy $cz
        _cutout [$dualUSBcutout cget -surface] $cy $cz
    }
    proc _hole {holecyl cx cy} {
        lassign [$holecyl cget -bottom] dum hx hy
        PostScriptFile hole [expr {$hx - $cx}] [expr {$hy - $cy}] \
              [expr {[$holecyl cget -radius] * 2.0}]
    }
    proc _cutout {cutoutSurf cx cy} {
        lassign [$cutoutSurf cget -cornerpoint] dummy cux cuy
        lassign [$cutoutSurf cget -vec1] dummy w dummy
        set w [expr {-($w)}]
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        PostScriptFile cutout [expr {$cux - $cx}] [expr {$cuy - $cy}] $w $h
    }
}

snit::type PortableM64CaseBottomFrontPanel {
    M64Dims
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component gpiocutout
    constructor {args} {
        install panel using PortableM64CaseFrontPanel %AUTO% \
              -origin [from args -origin] \
              -depth  [from args -depth]
        lassign [$panel PanelCornerPoint] cx cy cz
        set panelThick [$panel PanelThickness]
        set zbase [expr {$cz + $_m64Thickness + $_m64Standoff + $panelThick}]
        install gpiocutout using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$cx + $_gpioHeaderXOffset}] $cy $zbase] \
                        -vec1 [list $_gpioHeaderLength 0 0] \
                        -vec2 [list 0 0 $_gpioHeaderHeight]] \
              -vector [list 0 $panelThick 0] \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $panel print $fp
        $gpiocutout print $fp
    }
    method printPS {} {
        set fp [PostScriptFile fp]
        set xi 0
        set yi 2
        set xorg 5
        set yorg 0
        set xscale -.01968
        set yscale .01968
        set surf [$panel cget -surface]
        PostScriptFile newPage {Front bottom Cutouts}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        [$gpiocutout cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Left bottom Cutouts Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _cutout [$gpiocutout cget -surface] $cx $cz
    }
}


snit::type PortableM64CaseBottom {
    PortableM64CaseCommon
    component bottom
    component left
    component right
    component front
    component back
    constructor {args} {
        $self configurelist $args
        install bottom using PortableM64CaseBottomPanel %AUTO% \
              -origin $options(-origin)
        install left   using PortableM64CaseBottomLeftPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
        install right   using PortableM64CaseRightPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
        install front   using PortableM64CaseBottomFrontPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
        install back   using PortableM64CaseBackPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
    }
    method print {{fp stdout}} {
        $bottom print $fp
        $left   print $fp
        $right   print $fp
        $front   print $fp
        $back   print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        $bottom addPart partListArray
        $left addPart partListArray
        $right addPart partListArray
        $front addPart partListArray
        $back addPart partListArray
    }
    method printPS {} {
        $bottom printPS
        $left printPS
    }
}

snit::type PortableM64CaseMiddle {
    PortableM64CaseCommon
    component middle
    component left                                                              
    component right                                                             
    component front                                                             
    component back
    constructor {args} {
        $self configurelist $args
        install middle using PortableM64CasePanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 [expr {$_MiddleLowerDepth+$_BottomDepth}]]]
        install left   using PortableM64CaseLeftPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 $_BottomDepth]] \
              -depth $_MiddleTotalDepth
        install right   using PortableM64CaseRightPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 $_BottomDepth]] \
              -depth $_MiddleTotalDepth
        install front   using PortableM64CaseFrontPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 $_BottomDepth]] \
              -depth $_MiddleTotalDepth
        install back   using PortableM64CaseBackPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 $_BottomDepth]] \
              -depth $_MiddleTotalDepth
    }
    method print {{fp stdout}} {
        $middle print $fp
        $left   print $fp
        $right   print $fp
        $front   print $fp
        $back   print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        $middle addPart partListArray
        $left addPart partListArray
        $right addPart partListArray
        $front addPart partListArray
        $back addPart partListArray
    }
}

snit::type PortableM64CaseTop {
    PortableM64CaseCommon
    component top
    component left
    component right
    component front
    component back
    constructor {args} {
        $self configurelist $args
        install top using PortableM64CasePanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 [expr {$_MiddleTotalDepth+$_BottomDepth+$_TopDepth-$_WallThickness}]]]
        install left   using PortableM64CaseLeftPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 [expr {$_MiddleTotalDepth+$_BottomDepth}]]] \
              -depth $_TopDepth
        install right   using PortableM64CaseRightPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 [expr {$_MiddleTotalDepth+$_BottomDepth}]]] \
              -depth $_TopDepth
        install front   using PortableM64CaseFrontPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 [expr {$_MiddleTotalDepth+$_BottomDepth}]]] \
              -depth $_TopDepth
        install back   using PortableM64CaseBackPanel %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 0 [expr {$_MiddleTotalDepth+$_BottomDepth}]]] \
              -depth $_TopDepth
    }
    method print {{fp stdout}} {
        $top print $fp
        $left   print $fp
        $right   print $fp
        $front   print $fp
        $back   print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        $top addPart partListArray
        $left addPart partListArray
        $right addPart partListArray
        $front addPart partListArray
        $back addPart partListArray
    }
}

snit::type PortableM64Case {
    PortableM64CaseCommon
    component caseBottom
    component caseMiddle
    component caseTop
    constructor {args} {
        $self configurelist $args
        install caseBottom using PortableM64CaseBottom %AUTO% -origin $options(-origin)
        install caseMiddle using PortableM64CaseMiddle %AUTO% -origin $options(-origin)
        install caseTop    using PortableM64CaseTop %AUTO%    -origin $options(-origin)
    }
    method print {{fp stdout}} {
        $caseBottom print $fp
        $caseMiddle print $fp
        $caseTop    print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        $caseBottom addPart partListArray
        $caseMiddle addPart partListArray
        $caseTop    addPart partListArray
    }
    method printPS {} {
        $caseBottom printPS
    }
}

set modelFP [open [file rootname [info script]].gcad w]

## GCad prefix blather.
puts $modelFP "# [clock format [clock seconds] -format {%Y/%m/%d-%M:%M:%S}]"
puts $modelFP {DEFCOL 0 0 0}

PortableM64Case create m64case

m64case print $modelFP
close $modelFP
m64case addPart parts
PostScriptFile open
m64case printPS
PostScriptFile close

package require csv

set partsFP [open [file rootname [info script]]_parts.csv w]

puts $partsFP [::csv::join [list "Panel Size" "Panel Count"]]

foreach p [lsort -dictionary [array names parts]] {
    puts $partsFP [::csv::join [list $p $parts($p)]]
}
close $partsFP

             
             
