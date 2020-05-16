#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 11:54:16 2020
#  Last Modified : <200515.2240>
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
package require M64
package require PSBox
package require DCDC_5_12
package require LCDScreen
package require LCDMountingBracket
package require HDMIConverter

snit::macro PortableM64CaseCommon {} {
    typevariable _Width [expr {15 * 25.4}]
    typevariable _Height [expr {11 * 25.4}]
    typevariable _BottomDepth [expr {1.75 * 25.4}]
    typevariable _MiddleTotalDepth [expr {1.5 * 25.4}]
    typevariable _MiddleLowerDepth [expr {.5 * 25.4}]
    typevariable _TopDepth [expr {(.5+.125) * 25.4}]
    typevariable _WallThickness [expr {.125 * 25.4}]
}

snit::type PortableM64CasePanel {
    Common
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
    Common
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
    Common
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
    Common
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
    Common
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
    Common
    M64Dims
    HDMIConverterDims
    option -psbox -default {} -readonly yes
    option -dcdc512 -default {} -readonly yes
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component m64_m1
    component m64_m2
    component m64_m3
    component m64_m4
    component psbox_m1
    component psbox_m2
    component psbox_m3
    component psbox_m4
    component dcdc512_m1
    component dcdc512_m2
    component dcdc512_m3
    component dcdc512_m4
    component dcdc512_standoff1
    component dcdc512_standoff2
    component dcdc512_standoff3
    component dcdc512_standoff4
    component hdmiconvertermainboard
    component hdmiconvertermainboard_mh1
    component hdmiconvertermainboard_mh2
    component hdmiconvertermainboard_mh3
    component hdmiconvertermainboard_mh4
    component hdmiconvertermainboard_standoff1
    component hdmiconvertermainboard_standoff2
    component hdmiconvertermainboard_standoff3
    component hdmiconvertermainboard_standoff4
    component widthdim
    component lengthdim
    component m64ydim
    component hdmixdim
    component hdmiydim
    component m64tohtmiydim
    constructor {args} {
        install panel using PortableM64CasePanel %AUTO% \
              -origin [from args -origin]
        $self configurelist $args
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
        if {$options(-psbox) ne {}} {
            set psbox_m1 [$options(-psbox) MountingHole %AUTO% 1 $cz [$panel PanelThickness]]
            set psbox_m2 [$options(-psbox) MountingHole %AUTO% 2 $cz [$panel PanelThickness]]
            set psbox_m3 [$options(-psbox) MountingHole %AUTO% 3 $cz [$panel PanelThickness]]
            set psbox_m4 [$options(-psbox) MountingHole %AUTO% 4 $cz [$panel PanelThickness]]
        }
        if {$options(-dcdc512) ne {}} {
            set dcdc512_m1 [$options(-dcdc512) MountingHole %AUTO% 1 $cz [$panel PanelThickness]]
            set dcdc512_m2 [$options(-dcdc512) MountingHole %AUTO% 2 $cz [$panel PanelThickness]]
            set dcdc512_m3 [$options(-dcdc512) MountingHole %AUTO% 3 $cz [$panel PanelThickness]]
            set dcdc512_m4 [$options(-dcdc512) MountingHole %AUTO% 4 $cz [$panel PanelThickness]]
            set dcdc512_standoff1 [$options(-dcdc512) Standoff %AUTO% 1 [expr {$cz + [$panel PanelThickness]}] 6]
            set dcdc512_standoff2 [$options(-dcdc512) Standoff %AUTO% 2 [expr {$cz + [$panel PanelThickness]}] 6]
            set dcdc512_standoff3 [$options(-dcdc512) Standoff %AUTO% 3 [expr {$cz + [$panel PanelThickness]}] 6]
            set dcdc512_standoff4 [$options(-dcdc512) Standoff %AUTO% 4 [expr {$cz + [$panel PanelThickness]}] 6]
        }
        set panelsurf [$panel cget -surface]
        lassign [$panelsurf cget -vec2] dummy panelheight dummy
        install hdmiconvertermainboard using HDMIConverterMainBoard %AUTO% \
              -origin [list [expr {$cx + 12.7}] \
                       [expr {$cy + $panelheight - (12.7+$_HDMIConv_mainboardHeight)}] \
                       [expr {$cz + 6.35 + [$panel PanelThickness]}]]
        set hdmiconvertermainboard_mh1 [$hdmiconvertermainboard MountingHole %AUTO% 1 $cz [$panel PanelThickness]]
        set hdmiconvertermainboard_mh2 [$hdmiconvertermainboard MountingHole %AUTO% 2 $cz [$panel PanelThickness]]
        set hdmiconvertermainboard_mh3 [$hdmiconvertermainboard MountingHole %AUTO% 3 $cz [$panel PanelThickness]]
        set hdmiconvertermainboard_mh4 [$hdmiconvertermainboard MountingHole %AUTO% 4 $cz [$panel PanelThickness]]
        set hdmiconvertermainboard_standoff1 [$hdmiconvertermainboard Standoff %AUTO% 1 [expr {$cz + [$panel PanelThickness]}] 6.35 6.35 {255 255 0}]
        set hdmiconvertermainboard_standoff2 [$hdmiconvertermainboard Standoff %AUTO% 2 [expr {$cz + [$panel PanelThickness]}] 6.35 6.35 {255 255 0}]
        set hdmiconvertermainboard_standoff3 [$hdmiconvertermainboard Standoff %AUTO% 3 [expr {$cz + [$panel PanelThickness]}] 6.35 6.35 {255 255 0}]
        set hdmiconvertermainboard_standoff4 [$hdmiconvertermainboard Standoff %AUTO% 4 [expr {$cz + [$panel PanelThickness]}] 6.35 6.35 {255 255 0}]
        set psurf [$panel cget -surface]
        set vec1  [$psurf cget -vec1]
        set w [lindex $vec1 0]
        set mid [expr {$w / 2.0}]
        set toff -20
        lassign [$panel PanelCornerPoint] pcx pcy pcz
        install widthdim using Dim3D %AUTO% \
              -point1 [$panel PanelCornerPoint] \
              -point2 [list [expr {$cx + $w}] $cy $cz] \
              -textpoint [list [expr {$cx + $mid}] [expr {$cy + ($toff*2)}] [expr {$pcz+($_m64Standoff*3.5)}]] \
              -plane P \
              -additionaltext " mm"
        set vec2 [$psurf cget -vec2]
        set l [lindex $vec2 1]
        set mid [expr {$l / 2.0}]
        install lengthdim using Dim3D %AUTO% \
              -point1 [$panel PanelCornerPoint] \
              -point2 [list $cx [expr {$cy + $l}] $cz] \
              -textpoint [list [expr {$cx - $toff}] [expr {$cy + $mid}] [expr {$pcz+($_m64Standoff*3.5)}]] \
              -plane P \
              -additionaltext " mm"
        install m64ydim using Dim3D %AUTO% \
              -point1 [$panel PanelCornerPoint] \
              -point2 [GeometryFunctions translate3D_point \
                       [$panel PanelCornerPoint] \
                       [list 0 $_m64YOff 0]] \
              -textpoint [GeometryFunctions translate3D_point \
                          [$panel PanelCornerPoint] \
                          [list [expr {-4*$toff}] [expr {$_m64YOff / 2.0}] [expr {($_m64Standoff*3.5)}]]] \
              -plane P \
              -additionaltext " mm"
        lassign [$hdmiconvertermainboard cget -origin] hcx hcy hcz
        install hdmiydim using Dim3D %AUTO% \
              -point1 [$panel PanelCornerPoint] \
              -point2 [list $pcx $hcy $pcz] \
              -textpoint [list [expr {-2*$toff}] [expr {($pcy+$hcy)/2.0}] [expr {$pcz+($_m64Standoff*3.5)}]] \
              -plane P \
              -additionaltext " mm"
        install m64tohtmiydim using Dim3D %AUTO% \
              -point2 [list $pcx $hcy $pcz] \
              -point1 [list $pcx [expr {$pcy + $_m64YOff + $_m64Width}] $pcz] \
              -textpoint [list [expr {-3*($toff)}] \
                          [expr {($hcy + ($pcy + $_m64YOff + $_m64Width))/2.0}] \
                          [expr {$pcz+($_m64Standoff*1.5)}]] \
              -plane P \
              -additionaltext " mm"
    }
    method print {{fp stdout}} {
        $panel print $fp
        $m64_m1 print $fp
        $m64_m2 print $fp
        $m64_m3 print $fp
        $m64_m4 print $fp
        if {$options(-psbox) ne {}} {
            $psbox_m1 print $fp
            $psbox_m2 print $fp
            $psbox_m3 print $fp
            $psbox_m4 print $fp
        }
        if {$options(-dcdc512) ne {}} {
            $dcdc512_m1 print $fp
            $dcdc512_m2 print $fp
            $dcdc512_m3 print $fp
            $dcdc512_m4 print $fp
            $dcdc512_standoff1 print $fp
            $dcdc512_standoff2 print $fp
            $dcdc512_standoff3 print $fp
            $dcdc512_standoff4 print $fp
        }
        $hdmiconvertermainboard print $fp
        $hdmiconvertermainboard_mh1 print $fp
        $hdmiconvertermainboard_mh2 print $fp
        $hdmiconvertermainboard_mh3 print $fp
        $hdmiconvertermainboard_mh4 print $fp
        $hdmiconvertermainboard_standoff1 print $fp
        $hdmiconvertermainboard_standoff2 print $fp
        $hdmiconvertermainboard_standoff3 print $fp
        $hdmiconvertermainboard_standoff4 print $fp
        $widthdim print $fp
        $lengthdim print $fp
        $m64ydim print $fp
        $hdmiydim print $fp
        $m64tohtmiydim print $fp
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
        if {$options(-psbox) ne {}} {
            $psbox_m1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            $psbox_m2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            $psbox_m3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            $psbox_m4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        }
        PostScriptFile newPage {Bottom Panel Drill Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _hole $m64_m1 $cx $cy
        _hole $m64_m2 $cx $cy
        _hole $m64_m3 $cx $cy
        _hole $m64_m4 $cx $cy
        if {$options(-psbox) ne {}} {
            _hole $psbox_m1 $cx $cy
            _hole $psbox_m2 $cx $cy
            _hole $psbox_m3 $cx $cy
            _hole $psbox_m4 $cx $cy
        }
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
                       [expr {$m64Y - (($_AudioYMinBody+$_AudioYMaxBody)/2.0)}] \
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
        set xorg 0
        set yorg 0
        set xscale .01968
        set yscale .01968
        set surf [$panel cget -surface]
        PostScriptFile newPage {Front bottom Cutouts}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        [$gpiocutout cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Left bottom Cutouts Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _cutout [$gpiocutout cget -surface] $cx $cz
    }
    proc _cutout {cutoutSurf cx cy} {
        lassign [$cutoutSurf cget -cornerpoint] cux dummy cuy
        lassign [$cutoutSurf cget -vec1] w dummy dummy
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        PostScriptFile cutout [expr {$cux - $cx}] [expr {$cuy - $cy}] $w $h
    }
}


snit::type PortableM64CaseBottomRightPanel {
    option -psbox -default {} -readonly yes
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component fancutout1
    component fancutout2
    constructor {args} {
        install panel using PortableM64CaseRightPanel %AUTO% \
              -origin [from args -origin] \
              -depth  [from args -depth]
        set panelThick [$panel PanelThickness]
        $self configurelist $args
        lassign [$panel PanelCornerPoint] cx cy cz
        if {$options(-psbox) ne {}} {
            set fancutout1 [$options(-psbox) SquareFanHole1 %AUTO% $cx $panelThick]
            set fancutout2 [$options(-psbox) SquareFanHole2 %AUTO% $cx $panelThick]
        }
    }
    method print {{fp stdout}} {
        $panel print $fp
        if {$options(-psbox) ne {}} {
            $fancutout1 print $fp
            $fancutout2 print $fp
        }
    }
    method printPS {} {
    }
}

snit::type PortableM64CaseBottomBackPanel {
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component inletcutout
    option -psbox -readonly yes -default {}
    constructor {args} {
        install panel using PortableM64CaseBackPanel %AUTO% \
              -origin [from args -origin] \
              -depth  [from args -depth]
        set panelThick [$panel PanelThickness]
        $self configurelist $args
        if {$options(-psbox) ne {}} {
            set inletcutout [$options(-psbox) InletFlangCutout %AUTO% $panelThick]
        }
    }
    method print {{fp stdout}} {
        $panel print $fp
        if {$options(-psbox) ne {}} {
            $inletcutout print $fp
        }
    }
    method printPS {} {
        set fp [PostScriptFile fp]
        set xi 0
        set yi 2
        set xorg 7
        set yorg 0
        set xscale -.01968
        set yscale .01968
        set surf [$panel cget -surface]
        if {$options(-psbox) ne {}} {
            PostScriptFile newPage {Back bottom Cutouts}
            $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            [$inletcutout cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            PostScriptFile newPage {Back bottom Cutouts Report}
            lassign [$panel PanelCornerPoint] cx cy cz
            _cutout [$inletcutout cget -surface] $cx $cz
        }
    }
    proc _cutout {cutoutSurf cx cy} {
        lassign [$cutoutSurf cget -cornerpoint] cux dummy cuy
        lassign [$cutoutSurf cget -vec1] w dummy dummy
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        PostScriptFile cutout [expr {$cux - $cx}] [expr {$cuy - $cy}] $w $h
    }
}




snit::type PortableM64CaseBottom {
    Common
    PortableM64CaseCommon
    M64Dims
    CU_3002ADims
    Fan02510SS_05P_AT00Dims
    component bottom
    component left
    component right
    component front
    component back
    component m64
    component psbox
    component dcdc512
    typevariable _dcdc512Xoff 100
    typevariable _dcdc512Yoff [expr {1*25.4}]
    typevariable _dcdc512StandoffHeight 6
    constructor {args} {
        $self configurelist $args
        install psbox using PSBox %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list [expr {$_Width - $_fandepth - $_WallThickness - \
                              $_CU_3002A_basewidth}] \
                        [expr {$_Height - $_CU_3002A_baselength - \
                         $_WallThickness}] \
                              $_WallThickness]]
        install m64 using M64Board %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list [expr {$_m64XOff+$_WallThickness}] \
                        [expr {$_m64YOff+$_WallThickness}] \
                        [expr {$_m64Standoff+$_WallThickness}]]]
        install dcdc512 using DCDC_5_12_Horiz12Right %AUTO% \
            -origin [GeometryFunctions translate3D_point $options(-origin) \
                     [list [expr {$_dcdc512Xoff + $_WallThickness}] \
                      [expr {$_dcdc512Yoff + $_WallThickness}] \
                      [expr {$_dcdc512StandoffHeight + $_WallThickness}]]]
        install bottom using PortableM64CaseBottomPanel %AUTO% \
              -origin $options(-origin) -psbox $psbox -dcdc512 $dcdc512
        install left   using PortableM64CaseBottomLeftPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
        install right   using PortableM64CaseBottomRightPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth -psbox $psbox
        install front   using PortableM64CaseBottomFrontPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
        install back   using PortableM64CaseBottomBackPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth -psbox $psbox
    }
    method print {{fp stdout}} {
        $bottom print $fp
        $left   print $fp
        $right  print $fp
        $front  print $fp
        $back   print $fp
        $m64    print $fp
        $psbox  print $fp
        $dcdc512 print $fp
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
        $front printPS
        $left printPS
        $back printPS
    }
}

snit::type PortableM64CaseMiddlePanel {
    Common
    LCDDims
    BracketAngleDims
    HDMIConverterDims
    Common
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component leftbracket
    component rightbracket
    component screen
    component leftbracket_m1
    component leftbracket_m2
    component leftbracket_m3
    component leftbracket_m4
    component rightbracket_m1
    component rightbracket_m2
    component rightbracket_m3
    component rightbracket_m4
    component hdmibuttonboard
    component hdmibuttonboard_mh1
    component hdmibuttonboard_mh2
    component hdmibuttonboard_standoff1
    component hdmibuttonboard_standoff2
    component hdmihvpowerboard
    component hdmihvpowerboard_mh1
    component hdmihvpowerboard_mh2
    component hdmihvpowerboard_standoff1
    component hdmihvpowerboard_standoff2
    constructor {args} {
        install panel using PortableM64CasePanel %AUTO% \
              -origin [from args -origin]
        $self configurelist $args
        lassign [$panel PanelCornerPoint] cx cy cz
        set psurf [$panel cget -surface]
        set vec1  [$psurf cget -vec1]
        set panelWidth [lindex $vec1 0]
        set vec2 [$psurf cget -vec2]
        set panelLength [lindex $vec2 1]
        set wOffset [expr {($panelWidth / 2.0)-($_LCDWidth/2.0)}]
        install leftbracket using LCDMountingBracket %AUTO% \
              -origin [list [expr {$cx + $wOffset}] [expr {$cy + 25.4}] $cz] \
              -side L
        install rightbracket using LCDMountingBracket %AUTO% \
              -origin [list [expr {$cx + $wOffset + $_LCDWidth}] [expr {$cy + 25.4}] $cz] \
              -side R
        install screen using LCDScreen %AUTO% \
              -origin [list [expr {$cx + $wOffset}] \
                       [expr {$cy + 25.4}] \
                       [expr {$cz-((6.5/2.0)+(((1.0/2.0)*25.4)/2.0))}]]
        set leftbracket_m1 [$leftbracket MountingHole %AUTO% 1 $cz [$panel PanelThickness]]
        set leftbracket_m2 [$leftbracket MountingHole %AUTO% 2 $cz [$panel PanelThickness]]
        set leftbracket_m3 [$leftbracket MountingHole %AUTO% 3 $cz [$panel PanelThickness]]
        set leftbracket_m4 [$leftbracket MountingHole %AUTO% 4 $cz [$panel PanelThickness]]
        set rightbracket_m1 [$rightbracket MountingHole %AUTO% 1 $cz [$panel PanelThickness]]
        set rightbracket_m2 [$rightbracket MountingHole %AUTO% 2 $cz [$panel PanelThickness]]
        set rightbracket_m3 [$rightbracket MountingHole %AUTO% 3 $cz [$panel PanelThickness]]
        set rightbracket_m4 [$rightbracket MountingHole %AUTO% 4 $cz [$panel PanelThickness]]
        install hdmibuttonboard using HDMIButtonBoard_Upsidedown %AUTO% \
              -origin [list [expr {$cx + 12.7}] \
                       [expr {($cy+$panelLength)-$_HDMIConv_buttonboardHeight}] \
                       [expr {$cz - 6.35 - $_HDMIConv_boardthickness}]]
        set hdmibuttonboard_mh1 [$hdmibuttonboard MountingHole %AUTO% 1 $cz [$panel PanelThickness]]
        set hdmibuttonboard_mh2 [$hdmibuttonboard MountingHole %AUTO% 2 $cz [$panel PanelThickness]]
        set hdmibuttonboard_standoff1 [$hdmibuttonboard Standoff %AUTO% 1 $cz -6.35 6.35 {255 255 0}]
        set hdmibuttonboard_standoff2 [$hdmibuttonboard Standoff %AUTO% 2 $cz -6.35 6.35 {255 255 0}]
        install hdmihvpowerboard using HDMIHVPowerBoard_Upsidedown %AUTO% \
              -origin [list [expr {($cx+$panelWidth)-(12.7+$_HDMIConv_hvpowerboardWidth)}] \
                       [expr {($cy+$panelLength)-$_HDMIConv_hvpowerboardHeight}] \
                       [expr {$cz - 6.35 - $_HDMIConv_boardthickness}]]
        set hdmihvpowerboard_mh1 [$hdmihvpowerboard MountingHole %AUTO% 1 $cz [$panel PanelThickness]]
        set hdmihvpowerboard_mh2 [$hdmihvpowerboard MountingHole %AUTO% 2 $cz [$panel PanelThickness]]
        set hdmihvpowerboard_standoff1 [$hdmihvpowerboard Standoff %AUTO% 1 $cz -6.35 6.35 {255 255 0}]
        set hdmihvpowerboard_standoff2 [$hdmihvpowerboard Standoff %AUTO% 2 $cz -6.35 6.35 {255 255 0}]
    
    }
    method print {{fp stdout}} {
        $panel print $fp
        $leftbracket print $fp
        $rightbracket print $fp
        $screen print $fp
        $leftbracket_m1 print $fp
        $leftbracket_m2 print $fp
        $leftbracket_m3 print $fp
        $leftbracket_m4 print $fp
        $rightbracket_m1 print $fp
        $rightbracket_m2 print $fp
        $rightbracket_m3 print $fp
        $rightbracket_m4 print $fp
        $hdmibuttonboard print $fp
        $hdmibuttonboard_mh1 print $fp
        $hdmibuttonboard_mh2 print $fp
        $hdmibuttonboard_standoff1 print $fp
        $hdmibuttonboard_standoff2 print $fp
        $hdmihvpowerboard print $fp
        $hdmihvpowerboard_mh1 print $fp
        $hdmihvpowerboard_mh2 print $fp
        $hdmihvpowerboard_standoff1 print $fp
        $hdmihvpowerboard_standoff2 print $fp
    }
}


snit::type PortableM64CaseMiddle {
    Common
    PortableM64CaseCommon
    component middle
    component left                                                              
    component right                                                             
    component front                                                             
    component back
    constructor {args} {
        $self configurelist $args
        install middle using PortableM64CaseMiddlePanel %AUTO% \
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
    Common
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
    Common
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
        #$caseMiddle print $fp
        #$caseTop    print $fp
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






package provide Case 1.0
