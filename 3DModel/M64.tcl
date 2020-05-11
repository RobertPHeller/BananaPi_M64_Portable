#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 10:07:22 2020
#  Last Modified : <200510.0938>
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

snit::macro M64Dims {} {
    typevariable _m64_m1_relpos [list [expr {96.4-93.64472}] [expr {59.9-57.15}]]
    typevariable _m64_m2_relpos [list [expr {96.4-7.79526}] [expr {59.9-57.15}]]
    typevariable _m64_m3_relpos [list [expr {96.4-93.64472}] [expr {59.9-2.794}]]
    typevariable _m64_m4_relpos [list [expr {96.4-7.79526}] [expr {59.9-8.0772}]]
    typevariable _m64_mh_dia 2.750
    typevariable _m64XOff 0
    typevariable _m64YOff [expr {1*25.4}]
    typevariable _m64YMin 0
    typevariable _m64YMax 59.90082
    typevariable _m64XMin 5.00126
    typevariable _m64XMax 96.40062
    typevariable _m64Width 59.90082
    typevariable _m64Length [expr {96.40062-5.00126}]
    typevariable _m64Thickness [expr {.06125*25.4}]
    typevariable _m64Standoff [expr {.25*25.4}]
    typevariable _m64StandoffDia 6
    typevariable _PlateHeight 16
    typevariable _DualUSBcutoutYMin 30.83814
    typevariable _DualUSBcutoutYMax 45.23994
    typevariable _DualUSBHeight 15.60
    typevariable _DualUSBWidth 14.40
    typevariable _DualUSBLength [expr {100.93452-79.34452}]
    typevariable _DualUSBXMin 79.34452
    typevariable _DualUSBXMax 100.93452
    typevariable _DualUSBYMin 10.96518
    typevariable _DualUSBYMax 26.45918
    typevariable _RJ45YMin 30.83814
    typevariable _RJ45YMax 45.23994
    typevariable _RJ45XMin 83.55584
    typevariable _RJ45XMax 100.90404
    typevariable _RJ45Height 13.35
    typevariable _RJ45Width 16
    typevariable _RJ45Length [expr {100.90404 - 83.55584}] 
    typevariable _AudioYMinBody 47.55642
    typevariable _AudioYMaxBody 53.15458
    typevariable _AudioDiameter 5.6
    typevariable _AudioXMinBody 84.29244
    typevariable _AudioXMaxBody 96.393
    typevariable _AudioBodyLength [expr {14.0 - 2.0}]
    typevariable _AudioBodyWidth  6.0
    typevariable _AudioBodyHeight 5.0
    typevariable _AudioXMinBarrel 96.393
    typevariable _AudioXMaxBarrel 98.39198
    typevariable _gpioHeaderXOffset [expr {26.16962-3.57}]
    typevariable _gpioHeaderLength 55.4
    typevariable _gpioHeaderHeight 16.1
}

snit::type M64Board {
    Common
    M64Dims
    component board
    component dualusb
    component rj45
    component audiobody
    component audiobarrel
    component mh1
    component mh2
    component mh3
    component mh4
    component standoff1
    component standoff2
    component standoff3
    component standoff4
    constructor {args} {
        $self configurelist $args
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_m64Length 0 0] \
                        -vec2 [list 0 $_m64Width 0]] \
              -vector [list 0 0 $_m64Thickness] \
              -color  {0 255 0}
        install dualusb using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) [list [expr {$_m64XMax - $_DualUSBXMax}] [expr {$_m64YMax - $_DualUSBYMax}] $_m64Thickness]] \
                        -vec1 [list $_DualUSBLength 0 0] \
                        -vec2 [list 0 $_DualUSBWidth 0]] \
              -vector [list 0 0 $_DualUSBHeight] \
              -color  {250 250 250}
        install rj45 using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) [list [expr {$_m64XMax - $_RJ45XMax}] [expr {$_m64YMax - $_RJ45YMax}] $_m64Thickness]] \
                        -vec1 [list $_RJ45Length 0 0] \
                        -vec2 [list 0 $_RJ45Width 0]] \
              -vector [list 0 0 $_RJ45Height] \
              -color  {250 250 250}
        install audiobody using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) [list [expr {$_m64XMax - $_AudioXMaxBody}] [expr {$_m64YMax - $_AudioYMaxBody}] $_m64Thickness]] \
                        -vec1 [list $_AudioBodyLength 0 0] \
                        -vec2 [list 0 $_AudioBodyWidth 0]] \
              -vector [list 0 0 $_AudioBodyHeight] \
              -color {0 0 0}
        install audiobarrel using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list 0 [expr {$_m64YMax - $_AudioYMaxBody + ($_AudioBodyWidth/2.0)}] [expr {$_m64Thickness + ($_AudioBodyHeight / 2.0)}]]] \
              -radius [expr {$_AudioDiameter / 2.0}] \
              -direction X \
              -height [expr {$_AudioXMinBarrel - $_AudioXMaxBarrel}] \
              -color {0 0 0}
        install mh1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m1_relpos 0] [lindex $_m64_m1_relpos 1] 0]] \
              -radius [expr {$_m64_mh_dia / 2.0}] \
              -direction Z \
              -height $_m64Thickness \
              -color {255 255 255}
        install mh2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m2_relpos 0] [lindex $_m64_m2_relpos 1] 0]] \
              -radius [expr {$_m64_mh_dia / 2.0}] \
              -direction Z \
              -height $_m64Thickness \
              -color {255 255 255}
        install mh3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m3_relpos 0] [lindex $_m64_m3_relpos 1] 0]] \
              -radius [expr {$_m64_mh_dia / 2.0}] \
              -direction Z \
              -height $_m64Thickness \
              -color {255 255 255}
        install mh4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m4_relpos 0] [lindex $_m64_m4_relpos 1] 0]] \
              -radius [expr {$_m64_mh_dia / 2.0}] \
              -direction Z \
              -height $_m64Thickness \
              -color {255 255 255}
        install standoff1 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m1_relpos 0] [lindex $_m64_m1_relpos 1] 0]] \
              -radius [expr {$_m64StandoffDia / 2.0}] \
              -direction Z \
              -height -$_m64Standoff \
              -color {255 255 255}
        install standoff2 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m2_relpos 0] [lindex $_m64_m2_relpos 1] 0]] \
              -radius [expr {$_m64StandoffDia / 2.0}] \
              -direction Z \
              -height -$_m64Standoff \
              -color {255 255 255}
        install standoff3 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m3_relpos 0] [lindex $_m64_m3_relpos 1] 0]] \
              -radius [expr {$_m64StandoffDia / 2.0}] \
              -direction Z \
              -height -$_m64Standoff \
              -color {255 255 255}
        install standoff4 using Cylinder %AUTO% \
              -bottom [GeometryFunctions translate3D_point $options(-origin) [list [lindex $_m64_m4_relpos 0] [lindex $_m64_m4_relpos 1] 0]] \
              -radius [expr {$_m64StandoffDia / 2.0}] \
              -direction Z \
              -height -$_m64Standoff \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $board print $fp
        $dualusb print $fp
        $rj45 print $fp
        $audiobody print $fp
        $audiobarrel print $fp
        $mh1 print $fp
        $mh2 print $fp
        $mh3 print $fp
        $mh4 print $fp
        $standoff1 print $fp
        $standoff2 print $fp
        $standoff3 print $fp
        $standoff4 print $fp
    }
}


package provide M64 1.0
