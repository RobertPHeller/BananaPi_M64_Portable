#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 11:53:56 2020
#  Last Modified : <200510.1950>
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
package require PSPCB
package require Electromech

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
                        -vec1 [list 0 $_CU_3002A_baselength 0] \
                        -vec2 [list $_CU_3002A_basewidth 0 0]] \
              -vector [list 0 0 $_CU_3002A_thickness] \
              -color {192 192 192}
        install front using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_CU_3002A_basewidth 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list 0 $_CU_3002A_thickness 0] \
              -color {192 192 192}
        install back using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 $_CU_3002A_baselength 0]] \
                        -vec1 [list $_CU_3002A_basewidth 0 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color {192 192 192}
        install leftfrontflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_basewidth 0 0]] \
                        -vec1 [list 0 $_CU_3002A_baseflangewidth 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}
        lassign [[$leftfrontflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install leftfrontflangehole using Cylinder %AUTO% \
              -bottom [list $lffx \
                       [expr {($lffy + $_CU_3002A_baseflangewidth) - $_CU_3002A_baseholeoffset}]  \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
              -color {255 255 255}
        install leftbottomflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_basewidth 0 0]] \
                        -vec1 [list 0 $_CU_3002A_baselength 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseflangewidth]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}
        install leftbackflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_basewidth $_CU_3002A_baselength 0]] \
                        -vec1 [list 0 -$_CU_3002A_baseflangewidth 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}                        
        lassign [[$leftbackflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install leftbackflangehole using Cylinder %AUTO% \
              -bottom [list $lffx  \
                       [expr {($lffy - $_CU_3002A_baseflangewidth) + $_CU_3002A_baseholeoffset}] \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
              -color {255 255 255}
        install leftfrontflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_basewidth 0 0]] \
                        -vec1 [list 0 $_CU_3002A_baseflangewidth 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}
        install rightfrontflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 0 0]] \
                        -vec1 [list 0 $_CU_3002A_baseflangewidth 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}
        lassign [[$rightfrontflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install rightfrontflangehole using Cylinder %AUTO% \
              -bottom [list $lffx  \
                       [expr {($lffy + $_CU_3002A_baseflangewidth) - $_CU_3002A_baseholeoffset}] \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
              -color {255 255 255}
        install rightbottomflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 0 0]] \
                        -vec1 [list 0 $_CU_3002A_baselength 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseflangewidth]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}
        install rightbackflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list 0 $_CU_3002A_baselength 0]] \
                        -vec1 [list 0 -$_CU_3002A_baseflangewidth 0] \
                        -vec2 [list 0 0 $_CU_3002A_baseheight]] \
              -vector [list -$_CU_3002A_thickness 0 0] \
              -color {192 192 192}                        
        lassign [[$rightbackflange cget -surface] cget -cornerpoint] lffx lffy lffz
        install rightbackflangehole using Cylinder %AUTO% \
              -bottom [list $lffx  \
                       [expr {($lffy - $_CU_3002A_baseflangewidth) + $_CU_3002A_baseholeoffset}] \
                       [expr {($lffz + $_CU_3002A_baseheight) - $_CU_3002A_baseholeheightoffset}]] \
              -radius [expr {$_CU_3002A_baseholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
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
                        -vec1 [list 0 $_CU_3002A_coverlength 0] \
                        -vec2 [list $_CU_3002A_coverwidth 0 0]] \
              -vector [list 0 0 -$_CU_3002A_thickness] \
              -color  {192 192 192}
        install left using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_CU_3002A_thickness $_CU_3002A_thickness $_CU_3002A_thickness]]\
                        -vec1 [list 0 $_CU_3002A_coverlength 0] \
                        -vec2 [list 0 0 $_CU_3002A_coverheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color  {192 192 192}
        lassign [[$left cget -surface] cget -cornerpoint] lx ly lz
        install leftfronthole using Cylinder %AUTO% \
              -bottom [list $lx [expr {$ly + $_CU_3002A_coverholeoffset}] \
                       [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
              -color {255 255 255}
        install leftbackhole  using Cylinder %AUTO% \
              -bottom [list $lx [expr {$ly + $_CU_3002A_coverlength - $_CU_3002A_coverholeoffset}] \
                       [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
              -color {255 255 255}
        install right using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list [expr {$_CU_3002A_thickness + $_CU_3002A_coverwidth}] \
                                       $_CU_3002A_thickness \
                                       $_CU_3002A_thickness]]\
                        -vec1 [list 0 $_CU_3002A_coverlength 0] \
                        -vec2 [list 0 0 $_CU_3002A_coverheight]] \
              -vector [list 0 -$_CU_3002A_thickness 0] \
              -color  {192 192 192}
        lassign [[$right cget -surface] cget -cornerpoint] rx ry rz
        install rightfronthole using Cylinder %AUTO% \
              -bottom [list $rx [expr {$ry + $_CU_3002A_coverholeoffset}] \
                       [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
              -color {255 255 255}
        install rightbackhole  using Cylinder %AUTO% \
              -bottom [list $rx [expr {$ry + $_CU_3002A_coverlength - $_CU_3002A_coverholeoffset}] \
                       [expr {$_CU_3002A_thickness+$_CU_3002A_coverholeheightoffset}]] \
              -radius [expr {$_CU_3002A_coverholediameter / 2.0}] \
              -height -$_CU_3002A_thickness \
              -direction X \
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


snit::type PSBox {
    Common
    CU_3002ADims
    Fan02510SS_05P_AT00Dims
    PSDims
    PCBDims
    701w202_890462Dims
    typevariable _standoff_height 9.0
    typevariable _standoff_dia 5.0
    typevariable _inletXoff  4
    typevariable _inletZoff  19
    typevariable _dcstrainXoff 26.9875
    typevariable _dcstrainZoff 20.6375
    proc _fanXoff {} {
        return [expr {$_CU_3002A_thickness + $_CU_3002A_coverwidth}]
    }
    proc _fanZoff {} {
        return [expr {$_CU_3002A_baseflangewidth+$_CU_3002A_thickness}]
    }
    proc _fan1Yoff {} {
        return [expr {($_CU_3002A_coverlength-(2*$_fanwidth_height))/2.0}]
    }
    proc _fan2Yoff {} {
        return [expr {[_fan1Yoff]+$_fanwidth_height}]
    }
    component box
    component pcb
    delegate method MountingHole to pcb
    delegate method Standoff to pcb
    component standoff1
    component standoff2
    component standoff3
    component standoff4
    component mh1
    component mh2
    component mh3
    component mh4
    component inlet
    method InletFlangCutout {name panelDepth} {
        return [PrismSurfaceVector create $name \
                -surface [$inlet FlangeSurface] \
                -vector [list 0 $panelDepth 0] -color {255 255 255}]
    }
    component dcstrainrelief
    component fan1
    component fan1mh1
    component fan1mh2
    component fan1mh3
    component fan1mh4
    component fan2
    component fan2mh1
    component fan2mh2
    component fan2mh3
    component fan2mh4
    constructor {args} {
        $self configurelist $args
        install box using CU_3002A %AUTO% \
              -origin $options(-origin)
        install pcb using PSOnPCB %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list [expr {($_CU_3002A_basewidth-$_psPCBwidth)/2.0}] \
                        [expr {($_CU_3002A_baselength-$_psPCBlength)/2.0}] \
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
                       [list $_inletXoff $_CU_3002A_baselength $_inletZoff]]
        install dcstrainrelief using DCStrainRelief %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list $_dcstrainXoff 0 $_dcstrainZoff]]
        install fan1 using Fan02510SS_05P_AT00 %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list [_fanXoff] [_fan1Yoff] [_fanZoff]]]
        install fan2 using Fan02510SS_05P_AT00 %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       [list [_fanXoff] [_fan2Yoff] [_fanZoff]]]
        lassign [$fan1 cget -origin] fx fy fz
        set fan1mh1 [$fan1 MountingHole %AUTO% 1 $fx -$_CU_3002A_thickness]
        set fan1mh2 [$fan1 MountingHole %AUTO% 2 $fx -$_CU_3002A_thickness]
        set fan1mh3 [$fan1 MountingHole %AUTO% 3 $fx -$_CU_3002A_thickness]
        set fan1mh4 [$fan1 MountingHole %AUTO% 4 $fx -$_CU_3002A_thickness]
        set fan2mh1 [$fan2 MountingHole %AUTO% 1 $fx -$_CU_3002A_thickness]
        set fan2mh2 [$fan2 MountingHole %AUTO% 2 $fx -$_CU_3002A_thickness]
        set fan2mh3 [$fan2 MountingHole %AUTO% 3 $fx -$_CU_3002A_thickness]
        set fan2mh4 [$fan2 MountingHole %AUTO% 4 $fx -$_CU_3002A_thickness]
    }
    delegate method SquareFanHole1 to fan1 as SquareFanHole
    delegate method SquareFanHole2 to fan2 as SquareFanHole
    delegate method RoundFanHole1 to fan1 as RoundFanHole
    delegate method RoundFanHole2 to fan2 as RoundFanHole
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
        $fan1mh1   print $fp
        $fan1mh2   print $fp
        $fan1mh3   print $fp
        $fan1mh4   print $fp
        $fan2mh1   print $fp
        $fan2mh2   print $fp
        $fan2mh3   print $fp
        $fan2mh4   print $fp
    }
}



package provide PSBox 1.0

