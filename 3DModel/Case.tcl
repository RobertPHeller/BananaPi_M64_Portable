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
#  Last Modified : <200509.1236>
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

snit::macro PortableM64CaseCommon {} {
    typevariable _Width [expr {14 * 25.4}]
    typevariable _Height [expr {10 * 25.4}]
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
    #PSBoxHolesAndCutouts
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    component m64_m1
    component m64_m2
    component m64_m3
    component m64_m4
    #component psbox_m1
    #component psbox_m2
    #component psbox_m3
    #component psbox_m4
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
        #install psbox_m1 using Cylinder %AUTO% \
        #      -bottom [list [lindex $_psBoxMH1 0] [lindex $_psBoxMH1 1] $cz] \
        #      -radius $_psBoxMHRadius \
        #      -height [$panel PanelThickness] \
        #      -direction [$panel PanelDirection] \
        #      -color {255 255 255}
        #install psbox_m2 using Cylinder %AUTO% \
        #      -bottom [list [lindex $_psBoxMH2 0] [lindex $_psBoxMH2 1] $cz] \
        #      -radius $_psBoxMHRadius \
        #      -height [$panel PanelThickness] \
        #      -direction [$panel PanelDirection] \
        #      -color {255 255 255}
        #install psbox_m3 using Cylinder %AUTO% \
        #      -bottom [list [lindex $_psBoxMH3 0] [lindex $_psBoxMH3 1] $cz] \
        #      -radius $_psBoxMHRadius \
        #      -height [$panel PanelThickness] \
        #      -direction [$panel PanelDirection] \
        #      -color {255 255 255}
        #install psbox_m4 using Cylinder %AUTO% \
        #      -bottom [list [lindex $_psBoxMH4 0] [lindex $_psBoxMH4 1] $cz] \
        #      -radius $_psBoxMHRadius \
        #      -height [$panel PanelThickness] \
        #      -direction [$panel PanelDirection] \
        #      -color {255 255 255}
        
    }
    method print {{fp stdout}} {
        $panel print $fp
        $m64_m1 print $fp
        $m64_m2 print $fp
        $m64_m3 print $fp
        $m64_m4 print $fp
        #$psbox_m1 print $fp
        #$psbox_m2 print $fp
        #$psbox_m3 print $fp
        #$psbox_m4 print $fp
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
        #$psbox_m1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        #$psbox_m2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        #$psbox_m3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        #$psbox_m4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Bottom Panel Drill Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _hole $m64_m1 $cx $cy
        _hole $m64_m2 $cx $cy
        _hole $m64_m3 $cx $cy
        _hole $m64_m4 $cx $cy
        #_hole $psbox_m1 $cx $cy
        #_hole $psbox_m2 $cx $cy
        #_hole $psbox_m3 $cx $cy
        #_hole $psbox_m4 $cx $cy
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
    #PSBoxHolesAndCutouts
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    variable fangrillholes [list]
    typevariable _fangrillholeradius [expr {6.35/2.0}];# 1/4 in
    proc _makeHole {i x y h} {
        lassign [set _fan${i}Center] cx cy cz
        set dia [set _fan${i}Diameter]
        return [Cylinder create %AUTO% \
                -bottom [list $cx \
                         [expr {$cy + ($x*($dia/2.0))}] \
                         [expr {$cz + ($y*($dia/2.0))}]] \
                -radius $_fangrillholeradius \
                -direction X \
                -height $h \
                -color {255 255 255}]
    }
    constructor {args} {
        install panel using PortableM64CaseRightPanel %AUTO% \
              -origin [from args -origin] \
              -depth  [from args -depth]
        set panelThick [$panel PanelThickness]
        #set x .25
        #set y .75
        #lappend fangrillholes [_makeHole 1  $x  $y $panelThick]
        #lappend fangrillholes [_makeHole 1  $y  $x $panelThick]
        #lappend fangrillholes [_makeHole 1  $y -$x $panelThick]
        #lappend fangrillholes [_makeHole 1  $x -$y $panelThick]
        #lappend fangrillholes [_makeHole 1 -$x -$y $panelThick]
        #lappend fangrillholes [_makeHole 1 -$y -$x $panelThick]
        #lappend fangrillholes [_makeHole 1 -$y  $x $panelThick]
        #lappend fangrillholes [_makeHole 1 -$x  $y $panelThick]
        #lappend fangrillholes [_makeHole 1  0   0  $panelThick]
        #lappend fangrillholes [_makeHole 2  $x  $y $panelThick]
        #lappend fangrillholes [_makeHole 2  $y  $x $panelThick]
        #lappend fangrillholes [_makeHole 2  $y -$x $panelThick]
        #lappend fangrillholes [_makeHole 2  $x -$y $panelThick]
        #lappend fangrillholes [_makeHole 2 -$x -$y $panelThick]
        #lappend fangrillholes [_makeHole 2 -$y -$x $panelThick]
        #lappend fangrillholes [_makeHole 2 -$y  $x $panelThick]
        #lappend fangrillholes [_makeHole 2 -$x  $y $panelThick]
        #lappend fangrillholes [_makeHole 2  0   0  $panelThick]
    }
    method print {{fp stdout}} {
        $panel print $fp
        foreach fgh $fangrillholes {
            $fgh print $fp
        }
    }
    method printPS {} {
    }
}

snit::type PortableM64CaseBottomBackPanel {
    #PSBoxHolesAndCutouts
    component panel
    delegate method * to panel except {print}
    delegate option * to panel
    #component inletcutout
    constructor {args} {
        install panel using PortableM64CaseBackPanel %AUTO% \
              -origin [from args -origin] \
              -depth  [from args -depth]
        set panelThick [$panel PanelThickness]
        #install inletcutout using PrismSurfaceVector %AUTO% \
        #      -surface [PolySurface create %AUTO% \
        #                -rectangle yes \
        #                -cornerpoint [GeometryFunctions translate3D_point \
        #                              [$self cget -origin] \
        #                              $_inletCornerPoint] \
        #                -vec1 $_inletVec1 \
        #                -vec2 $_inletVec2] \
        #      -vector [list 0 -$panelThick 0] \
        #      -color {255 255 255}
    }
    method print {{fp stdout}} {
        $panel print $fp
        #$inletcutout print $fp
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
        #PostScriptFile newPage {Back bottom Cutouts}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        #[$inletcutout cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        #PostScriptFile newPage {Back bottom Cutouts Report}
        #lassign [$panel PanelCornerPoint] cx cy cz
        #_cutout [$inletcutout cget -surface] $cx $cz
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
        install right   using PortableM64CaseBottomRightPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
        install front   using PortableM64CaseBottomFrontPanel %AUTO% \
              -origin $options(-origin) \
              -depth $_BottomDepth
        install back   using PortableM64CaseBottomBackPanel %AUTO% \
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
        $front printPS
        $left printPS
        $back printPS
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
    M64Dims
    typemethod M64XOff {} {return [expr {$_m64XOff+$_WallThickness}]}
    typemethod M64YOff {} {return [expr {$_m64YOff+$_WallThickness}]}
    typemethod M64ZOff {} {return [expr {$_m64Standoff+$_WallThickness}]}
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






package provide Case 1.0
