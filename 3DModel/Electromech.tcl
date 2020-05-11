#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:50:48 2020
#  Last Modified : <200510.1939>
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
        set flangeyoff [expr {($_flangewidth - $_bodywidth)/2.0}]
        set flangexoff [expr {($_flangeheight - $_bodyheight)/2.0}]
        install flange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list -$flangexoff 0 -$flangeyoff]] \
                        -vec1 [list $_flangewidth 0 0] \
                        -vec2 [list 0 0 $_flangeheight]] \
              -vector [list 0 $_flangedepth 0] \
              -color {0 0 0}
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_bodywidth 0 0] \
                        -vec2 [list 0 0 $_bodyheight]] \
              -vector [list 0 -$_bodydepth 0] \
              -color {0 0 0}
        set lugyoff [expr {($_bodywidth - $_lugwidth) / 2.0}]
        set lugxoff [expr {($_bodyheight - $_lugheight) / 2.0}]
        install solderlugs using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list $lugxoff -$_bodydepth $lugyoff]] \
                        -vec1 [list $_lugwidth 0 0] \
                        -vec2 [list 0 0 $_lugheight]] \
              -vector [list 0 -$_lugdepth 0] \
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
              -height -$_flangedepth \
              -direction Y \
              -color {0 0 0}
        install body using Cylinder %AUTO% \
              -bottom $options(-origin) \
              -radius [expr {$_bodydia / 2.0}] \
              -height $_bodydepth \
              -direction Y \
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
                        -vec1 [list 0 $_fanwidth_height 0] \
                        -vec2 [list 0 0 $_fanwidth_height]] \
              -vector [list $_fandepth 0 0] \
              -color {0 0 0}
        set mhXYoff [expr {($_fanwidth_height-$_fanmholespacing)/2.0}]
        install mh1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 $mhXYoff $mhXYoff]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction X \
              -height $_fandepth \
              -color {255 255 255}
        install mh2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 [expr {$mhXYoff+$_fanmholespacing}] $mhXYoff]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction X \
              -height $_fandepth \
              -color {255 255 255}
        install mh3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 $mhXYoff  [expr {$mhXYoff+$_fanmholespacing}]]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction X \
              -height $_fandepth \
              -color {255 255 255}
        install mh4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) \
                       [list 0 [expr {$mhXYoff+$_fanmholespacing}] [expr {$mhXYoff+$_fanmholespacing}]]] \
              -radius [expr {$_fanmholedia/2.0}] \
              -direction X \
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
    method MountingHole {name i xBase height} {
        lassign [[set mh$i] cget -bottom] mhx mhy mhz
        return [Cylinder create $name \
                -bottom [list $xBase $mhy $mhz] \
                -radius [expr {$_fanmholedia/2.0}] \
                -direction X \
                -height $height \
                -color {255 255 255}]
    }
    method RoundFanHole {name xBase height} {
        lassign $options(-origin) ox oy oz
        set x $xBase
        set y [expr {$oy + ($_fanwidth_height/2.0)}]
        set z [expr {$oz + ($_fanwidth_height/2.0)}]
        return [Cylinder create $name \
                -bottom [list $x $y $z] \
                -radius [expr {$_fanholedia/2.0}] \
                -direction X \
                -height $height \
                -color {255 255 255}]
    }
    method SquareFanHole {name xBase height} {
        lassign $options(-origin) ox oy oz
        return [PrismSurfaceVector %AUTO% \
                -surface [PolySurface  create %AUTO% \
                          -rectangle yes \
                          -cornerpoint [list $xBase $oy $oz] \
                          -vec1 [list 0 $_fanwidth_height 0] \
                          -vec2 [list 0 0 $_fanwidth_height]] \
                -vector [list $height 0 0] \
                -color {255 255 255}]
    }
}


package provide Electromech 1.0
