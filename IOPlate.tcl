#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Apr 7 13:09:22 2020
#  Last Modified : <200407.1816>
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

snit::type IOPlate {
    option -origin -type point -readonly yes -default {0 0 0}
    component plate
    component dualUSBcutout
    component rj45cutout
    component audiojackcutout
    component m1
    component m2
    component m3
    component m4
    typevariable BYMin 0
    typevariable BYMax 59.90082
    typevariable BXMin 5.00126
    typevariable BXMax 96.4
    typevariable PlateHeight 16
    typevariable CornerRadius 3.17500
    typevariable DualUSBcutoutYMin 10.96518
    typevariable DualUSBcutoutYMax 26.45918
    typevariable DualUSBHeight 15.60
    typevariable DualUSBWidth 14.40
    typevariable RJ45YMin 30.83814
    typevariable RJ45YMax 45.23994
    typevariable RJ45Height 13.35
    typevariable RJ45Width 16
    typevariable AudioYMin 47.55642
    typevariable AudioYMax 53.15458
    typevariable AudioDiameter 5.6
    proc _addpoints {x y Q AA BB {Z 0.0} {Y 0.0}} {
        #puts stderr "_addpoints $x $y $Q $AA $BB $Z $Y"
        upvar $AA A
        upvar $BB B
        #puts stderr "_addpoints: A is $A"
        #puts stderr "_addpoints: B is $B"
        switch $Q {
            1 {
                lappend A [list 0.0 [expr {$x + $Y}] [expr {$y + $Z}]]
                lappend B [list 0.0 [expr {$y + $Y}] [expr {$x + $Z}]]
            }
            2 {
                lappend A [list 0.0 [expr {$y + $Y}] [expr {-($x) + $Z}]]
                lappend B [list 0.0 [expr {$x + $Y}] [expr {-($y) + $Z}]]
            }
            3 {
                lappend A [list 0.0 [expr {-($x) + $Y}] [expr {-($y) + $Z}]]
                lappend B [list 0.0 [expr {-($y) + $Y}] [expr {-($x) + $Z}]]
            }
            4 {
                lappend A [list 0.0 [expr {-($y) + $Y}] [expr {$x + $Z}]]
                lappend B [list 0.0 [expr {-($x) + $Y}] [expr {$y + $Z}]]
            }
        }
        #puts stderr "_addpoints: A is now $A"
        #puts stderr "_addpoints: B is now $B"
    }        
    proc _quarterCircle {R Q {Z 0.0} {Y 0.0} {steps 5}} {
        set resultA [list]
        set resultB [list]
        set x 0.0
        set y $R
        set inc [expr {$R / double($steps+1)}]
        set d [expr {5.0 / 4.0 - $R}]
        _addpoints $x $y $Q resultA resultB $Z $Y
        #puts stderr "_quarterCircle (start): resultA = $resultA"
        #puts stderr "_quarterCircle (start): resultB = $resultB" 
        while {$y > $x} {
            if {$d < 0.0} {
                set d [expr {$d + $x * 2.0 + 3}]
                set x [expr {$x + $inc}]
            } else {
                set d [expr {$d + ($x - $y) * 2.0 + 5}]
                set x [expr {$x + $inc}]
                set y [expr {$y - $inc}]
            }
            _addpoints $x $y $Q resultA resultB $Z $Y
            #puts stderr "_quarterCircle (loop): resultA = $resultA"
            #puts stderr "_quarterCircle (loop): resultB = $resultB"
        }
        #puts stderr "_quarterCircle: resultA = $resultA"
        #puts stderr "_quarterCircle: resultB = $resultB"
        set lenB [llength $resultB]
        for {set ib [expr {$lenB - 1}]} {$ib >= 0} {incr ib -1} {
            lappend resultA [lindex $resultB $ib]
        }
        #puts stderr "_quarterCircle: returning $resultA"
        return $resultA
    }
    proc _lappendRev {l1name l2} {
        upvar $l1name l1
        for {set i [expr {[llength $l2]-1}]} {$i >= 0} {incr i -1} {
            lappend l1 [lindex $l2 $i]
        }
    }
    proc _reverse {l} {
        set result [list]
        for {set i [expr {[llength $l] - 1}]} {$i >= 0} {incr i -1} {
            lappend result [lindex $l $i]
        }
        return $result
    }
    constructor {args} {
        $self configurelist $args
        set Plate0 [_reverse [_quarterCircle $CornerRadius 3 0 0]]
        lappend Plate0 [list 0 $BYMax -$CornerRadius]
        _lappendRev Plate0 [_quarterCircle $CornerRadius 2 0 $BYMax] 
        lappend Plate0 [list 0 [expr {$BYMax + $CornerRadius}] $PlateHeight]
        _lappendRev Plate0 [_quarterCircle $CornerRadius 1 $PlateHeight $BYMax]
        lappend Plate0 [list 0 0 [expr {$PlateHeight + $CornerRadius}]]
        _lappendRev Plate0 [_quarterCircle $CornerRadius 4 $PlateHeight 0]
        lappend Plate0 [list 0 -$CornerRadius 0]
        set pointsH [GeometryFunctions MakeHomogenous $Plate0]
        set points [GeometryFunctions StripHomogenous [GeometryFunctions translate3D $pointsH $options(-origin)]]
        install plate using PrismSurfaceVector ${self}_Plate \
              -surface [PolySurface create ${self}_PlateSurf -rectangle no \
                        -polypoints $points] \
              -vector [list 1.9 0 0] \
              -color {255 0 0}
        install dualUSBcutout using PrismSurfaceVector ${self}_dualUSBcutout \
              -surface [PolySurface create ${self}_dualUSBcutoutSurf \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list 0 $DualUSBcutoutYMin 0]] \
                        -vec1 [list 0 $DualUSBWidth 0] \
                        -vec2 [list 0 0 $DualUSBHeight]] \
              -vector [list 1.9 0 0] \
              -color {255 255 255}
        install rj45cutout  using PrismSurfaceVector ${self}_rj45cutout \
              -surface [PolySurface create ${self}_rj45cutoutSurf \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list 0 $RJ45YMin 0]] \
                        -vec1 [list 0 $RJ45Width 0] \
                        -vec2 [list 0 0 $RJ45Height]] \
              -vector [list 1.9 0 0] \
              -color {255 255 255}
        install audiojackcutout using Cylinder ${self}_audiojackcutout \
              -bottom [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list 0 [expr {($AudioYMin+$AudioYMax)/2.0}] 2.5]] \
              -radius [expr {$AudioDiameter / 2.0}] \
              -height 1.9 \
              -color {255 255 255} \
              -direction X
    }
    method print {{fp stdout}} {
        $plate print $fp
        $dualUSBcutout print $fp
        $rj45cutout print $fp
        $audiojackcutout print $fp
    }
                                     
}

## GCad prefix blather.
puts "# [clock format [clock seconds] -format {%Y/%m/%d-%M:%M:%S}]"
puts {DEFCOL 0 0 0}

set ioplate [IOPlate create IO_Plate -origin {0 0 0}]
$ioplate print

