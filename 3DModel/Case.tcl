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
#  Last Modified : <200526.1016>
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
package require SVGOutput
package require TeensyThumbStick
package require Speaker
package require Battery
package require USBHub
package require OTGAdaptor
package require USB_SATA_Adapter
package require harddisk

snit::macro PortableM64CaseCommon {} {
    typevariable _Width [expr {15.5 * 25.4}]
    typevariable _Height [expr {11 * 25.4}]
    typevariable _BottomDepth [expr {1.75 * 25.4}]
    typevariable _MiddleTotalDepth [expr {1.5 * 25.4}]
    typevariable _MiddleLowerDepth [expr {.5 * 25.4}]
    typevariable _TopDepth [expr {(.5+.125) * 25.4}]
    typevariable _WallThickness [expr {.125 * 25.4}]
    typevariable _ShelfHeight [expr {1.25 * 25.4}]
    typevariable _ShelfLength [expr {6 * 25.4}]
    typevariable _BlockThick [expr {.375*25.4}]
    typevariable _BlockWidth [expr {.5*25.4}]
    typevariable _TeensyThumbStickDrop [expr {.25*25.4}]
}

snit::type BlockX {
    Common
    option -length -readonly yes -type snit::double -default 0
    PortableM64CaseCommon
    component block
    delegate method * to block
    delegate option * to block
    constructor {args} {
        $self configurelist $args
        install block using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list 0 0 $_BlockThick] \
                        -vec2 [list 0 $_BlockWidth 0]] \
              -vector [list $options(-length) 0 0] \
              -color  {0 255 0}
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set bsurf [$block cget -surface]
        set thick [lindex [$bsurf cget -vec1] 2]
        set width [lindex [$bsurf cget -vec2] 1]
        set length [expr {abs([lindex [$block cget -vector] 0])}]
        incr partListArray([$self _normPartSize $width $thick $length])
    }
}

snit::type BlockY {
    Common
    option -length -readonly yes -type snit::double -default 0
    PortableM64CaseCommon
    component block
    delegate method * to block
    delegate option * to block
    constructor {args} {
        $self configurelist $args
        install block using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_BlockWidth 0 0] \
                        -vec2 [list 0 0 $_BlockThick]] \
              -vector [list 0 $options(-length) 0] \
              -color  {0 255 0}
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set bsurf [$block cget -surface]
        set thick [lindex [$bsurf cget -vec2] 2]
        set width [lindex [$bsurf cget -vec1] 0]
        set length [expr {abs([lindex [$block cget -vector] 1])}]
        incr partListArray([$self _normPartSize $width $thick $length])
    }
}

snit::type BlockZa {
    Common
    option -length -readonly yes -type snit::double -default 0
    PortableM64CaseCommon
    component block
    delegate method * to block
    delegate option * to block
    constructor {args} {
        $self configurelist $args
        install block using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_BlockThick 0 0] \
                        -vec2 [list 0 $_BlockWidth 0]] \
              -vector [list 0 0 $options(-length)] \
              -color  {0 255 0}
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set bsurf [$block cget -surface]
        set thick [lindex [$bsurf cget -vec1] 0]
        set width [lindex [$bsurf cget -vec2] 1]
        set length [expr {abs([lindex [$block cget -vector] 2])}]
        incr partListArray([$self _normPartSize $width $thick $length])
    }
}

snit::type BlockZb {
    Common
    option -length -readonly yes -type snit::double -default 0
    PortableM64CaseCommon
    component block
    delegate method * to block
    delegate option * to block
    constructor {args} {
        $self configurelist $args
        install block using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list 0 $_BlockThick 0] \
                        -vec2 [list $_BlockWidth 0 0]] \
              -vector [list 0 0 $options(-length)] \
              -color  {0 255 0}
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set bsurf [$block cget -surface]
        set thick [lindex [$bsurf cget -vec1] 1]
        set width [lindex [$bsurf cget -vec2] 0]
        set length [expr {abs([lindex [$block cget -vector] 2])}]
        incr partListArray([$self _normPartSize $width $thick $length])
    }
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
    method svgout {svgout parent} {
        set panelsurf [$panel cget -surface]
        set width [lindex [$panelsurf cget -vec1] 0]
        set height [lindex [$panelsurf cget -vec2] 1]
        $svgout addrect 0 -$height $width $height $parent
        #$svgout addcircle 0 -$height 5 $parent
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
    method svgout {svgout parent} {
        set panelsurf [$panel cget -surface]
        set height [lindex [$panelsurf cget -vec2] 2]
        set width [lindex [$panelsurf cget -vec1] 1]
        $svgout addrect 0 -$height $width $height $parent
        #$svgout addcircle 0 -$height 5 $parent
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
    method svgout {svgout parent} {
        set panelsurf [$panel cget -surface]
        set height [lindex [$panelsurf cget -vec2] 2]
        set width [lindex [$panelsurf cget -vec1] 1]
        $svgout addrect 0 -$height $width $height $parent
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
    method svgout {svgout parent} {
        set panelsurf [$panel cget -surface]
        set height [lindex [$panelsurf cget -vec2] 2]
        set width [lindex [$panelsurf cget -vec1] 0]
        $svgout addrect 0 -$height $width $height $parent
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
    method svgout {svgout parent} {
        set panelsurf [$panel cget -surface]
        set height [lindex [$panelsurf cget -vec2] 2]
        set width [lindex [$panelsurf cget -vec1] 0]
        $svgout addrect 0 -$height $width $height $parent
    }
}

snit::type PortableM64CaseBottomPanel {
    Common
    PortableM64CaseCommon
    M64Dims
    HDMIConverterDims
    BatteryDims
    USBHubDims
    OTGAdaptorDims
    USB_SATA_AdapterDims
    Disk25_2HDims
    option -psbox -default {} -readonly yes
    option -dcdc512 -default {} -readonly yes
    option -otg -default {} -readonly yes
    component panel
    #delegate method * to panel except {print addPart}
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
    component battery
    component usbhub
    component otgadaptor
    component usbsataadaptor
    component harddisk
    component frontblock
    component backblock
    component leftblock
    component rightblock
    component leftfrontcorner
    component rightfrontcorner
    component leftbackcorner
    component rightbackcorner
    component widthdim
    component lengthdim
    component m64ydim
    component psboxxdim
    component psboxydim
    component hdmixdim
    component hdmiydim
    component m64tohtmiydim
    constructor {args} {
        install panel using PortableM64CasePanel %AUTO% \
              -origin [from args -origin]
        $self configurelist $args
        lassign [$panel PanelCornerPoint] cx cy cz
        set dimz [expr {$cz + 12.7}]
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
            lassign [$options(-psbox) cget -origin] psx psy psz
            install psboxydim using Dim3D %AUTO% \
                  -point1 [list $psx $psy $dimz] \
                  -point2 [list $psx $cy $dimz] \
                  -textpoint [list [expr {$psx - 25}] [expr {($cy + $psy)/2}] $dimz] \
                  -plane P -additionaltext " mm"
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
        if {$options(-otg) ne {}} {
            lassign [[$options(-otg) cget -surface] cget -cornerpoint] otg_x otg_y otg_z
            set otgadaptor_x [expr {$otg_x + (($_OTG_Width - $_OTGAdaptor_MicroB_Width)/2.0) - $_OTGAdaptor_MicroB_XOff}]
            set otgadaptor_y [expr {$otg_y + $_OTGAdaptor_MicroB_Length}]
            set otgadaptor_z [expr {$otg_z + (($_OTG_Thick - $_OTGAdaptor_MicroB_Thick)/2.0) - $_OTGAdaptor_MicroB_ZOff}]
            install otgadaptor using OTGAdaptor %AUTO% \
                  -origin [list $otgadaptor_x $otgadaptor_y $otgadaptor_z]
        }
        set panelsurf [$panel cget -surface]
        lassign [$panelsurf cget -vec2] dummy panelheight dummy
        install harddisk using Disk25_2H %AUTO% \
              -origin [list [expr {$cx + 12.7 + $_HDMIConv_mainboardWidth + 6.35}] \
                       [expr {$cy + $panelheight - (12.7+$_Disk25_2H_Length)}] \
                       [expr {$cz + [$panel PanelThickness]}]]
        set usbsataadaptor_x [expr {$cx + 12.7 + $_HDMIConv_mainboardWidth + 6.35}]
        set usbsataadaptor_y [expr {$cy + $panelheight - (12.7+$_Disk25_2H_Length + 50.8 + $_USB_SATA_Adapter_OverallLength)}]
        set usbsataadaptor_z [expr {$cz + [$panel PanelThickness] + 6.35}]
        install usbsataadaptor using USB_SATA_Adapter %AUTO% \
              -origin [list $usbsataadaptor_x $usbsataadaptor_y \
                       $usbsataadaptor_z]
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
        install battery using Battery %AUTO% \
              -origin [list [expr {$cx + ($w - $_Battery_Length)}] $cy [expr {$cz + [$panel PanelThickness]}]]
        install usbhub usinf USBHub %AUTO% \
              -origin [list [expr {$cx + (5*25.4)}] $cy \
                       [expr {$cz + [$panel PanelThickness]}]]
        install frontblock using BlockX %AUTO% \
              -origin [list $cx $cy [expr {$cz + [$panel PanelThickness]}]] \
              -length [expr {5*25.4}]
        set vec2  [$psurf cget -vec2]
        install backblock using BlockX %AUTO% \
              -origin [list $cx \
                       [expr {$cy + [lindex $vec2 1] - $_BlockWidth}] \
                       [expr {$cz + [$panel PanelThickness]}]] \
              -length [expr {12*25.4}]
        install leftblock using BlockY %AUTO% \
              -origin [list $cx \
                       [expr {$cy + $_m64YOff + $_m64YMax}] \
                       [expr {$cz + [$panel PanelThickness]}]] \
              -length [expr {[lindex $vec2 1] - ($_m64YOff + $_m64YMax + $_BlockWidth)}]
        install rightblock using BlockY %AUTO% \
              -origin [list [expr {$cx + $w - $_BlockWidth}] \
                       [expr {$cy + $_Battery_Width}] \
                       [expr {$cz + [$panel PanelThickness]}]] \
              -length [expr {170 - $_Battery_Width}]
        install leftfrontcorner using BlockZa %AUTO% \
              -origin [list $cx $cy [expr {$cz + [$panel PanelThickness] + $_BlockThick}]] \
              -length [expr {$_ShelfHeight - ([$panel PanelThickness]+$_BlockThick)}]
        install rightfrontcorner using BlockZa %AUTO% \
              -origin [list [expr {$cx + $w - $_BlockThick}] \
                       $cy [expr {$cz + [$panel PanelThickness] + $_Battery_Height}]] \
              -length [expr {$_ShelfHeight - ([$panel PanelThickness]+$_Battery_Height)}]
        install leftbackcorner using BlockZa %AUTO% \
              -origin [list $cx \
                       [expr {$cy + [lindex $vec2 1] - $_BlockWidth}] \
                       [expr {$cz + [$panel PanelThickness] + $_BlockThick}]] \
              -length [expr {$_BottomDepth - ([$panel PanelThickness]+$_BlockThick)}]
        install rightbackcorner using BlockZa %AUTO% \
              -origin [list [expr {$cx + $w - $_BlockThick}] \
                       [expr {$cy + [lindex $vec2 1] - $_BlockWidth}] \
                       [expr {$cz + [$panel PanelThickness]}]] \
              -length [expr {$_BottomDepth - [$panel PanelThickness]}]
        set mid [expr {$w / 2.0}]
        set toff -20
        install widthdim using Dim3D %AUTO% \
              -point2 [list $cx $cy $dimz] \
              -point1 [list [expr {$cx + $w}] $cy $dimz] \
              -textpoint [list [expr {$cx + $mid}] [expr {$cy + ($toff*(-16))}] $dimz] \
              -plane P \
              -additionaltext " mm"
        set vec2 [$psurf cget -vec2]
        set l [lindex $vec2 1]
        set mid [expr {$l / 2.0}]
        install lengthdim using Dim3D %AUTO% \
              -point1 [list $cx $cy $dimz] \
              -point2 [list $cx [expr {$cy + $l}] $dimz] \
              -textpoint [list [expr {$cx - $toff}] [expr {$cy + $mid}] $dimz] \
              -plane P \
              -additionaltext " mm"
        install m64ydim using Dim3D %AUTO% \
              -point1 [list $cx $cy $dimz] \
              -point2 [list $cx [expr {$cy + $_m64YOff}] $dimz] \
              -textpoint [list [expr {$cx + (2*$toff)}] [expr {$cy + ($_m64YOff/2.0)}] $dimz] \
              -plane P \
              -additionaltext " mm"
        lassign [$hdmiconvertermainboard cget -origin] hcx hcy hcz
        install hdmiydim using Dim3D %AUTO% \
              -point1 [list $cx $cy $dimz] \
              -point2 [list $cx $hcy $dimz] \
              -textpoint [list [expr {-2*$toff}] [expr {($cy+$hcy)/2.0}] $dimz] \
              -plane P \
              -additionaltext " mm"
        install m64tohtmiydim using Dim3D %AUTO% \
              -point2 [list $hcx $hcy $dimz] \
              -point1 [list $hcx [expr {$cy + $_m64YOff + $_m64Width}] $dimz] \
              -textpoint [list [expr {-3*($toff)}] \
                          [expr {($hcy + ($cy + $_m64YOff + $_m64Width))/2.0}] \
                          $dimz] \
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
            $psboxydim print $fp
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
        if {$options(-otg) ne {}} {
            $otgadaptor print $fp
        }
        $harddisk print $fp
        $usbsataadaptor print $fp
        $hdmiconvertermainboard print $fp
        $hdmiconvertermainboard_mh1 print $fp
        $hdmiconvertermainboard_mh2 print $fp
        $hdmiconvertermainboard_mh3 print $fp
        $hdmiconvertermainboard_mh4 print $fp
        $hdmiconvertermainboard_standoff1 print $fp
        $hdmiconvertermainboard_standoff2 print $fp
        $hdmiconvertermainboard_standoff3 print $fp
        $hdmiconvertermainboard_standoff4 print $fp
        $battery print $fp
        $usbhub print $fp
        $frontblock print $fp
        $backblock print $fp
        $leftblock print $fp
        $rightblock print $fp
        $leftfrontcorner print $fp
        $rightfrontcorner print $fp
        $leftbackcorner print $fp
        $rightbackcorner print $fp
        $widthdim print $fp
        $lengthdim print $fp
        $m64ydim print $fp
        $hdmiydim print $fp
        $m64tohtmiydim print $fp
    }
    method addPart {partListArrayName} {
        #puts stderr "*** $self addPart $partListArrayName"
        upvar $partListArrayName partListArray
        $panel addPart partListArray
        $frontblock addPart partListArray
        $backblock addPart partListArray
        $leftblock addPart partListArray
        $rightblock addPart partListArray
        $leftfrontcorner addPart partListArray
        $rightfrontcorner addPart partListArray
        $leftbackcorner addPart partListArray
        $rightbackcorner addPart partListArray
        
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
        if {$options(-dcdc512) ne {}} {
            $dcdc512_m1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            $dcdc512_m2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            $dcdc512_m3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
            $dcdc512_m4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        }
        $hdmiconvertermainboard_mh1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $hdmiconvertermainboard_mh2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $hdmiconvertermainboard_mh3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $hdmiconvertermainboard_mh4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
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
        if {$options(-dcdc512) ne {}} {
            _hole $dcdc512_m1 $cx $cy
            _hole $dcdc512_m2 $cx $cy
            _hole $dcdc512_m3 $cx $cy
            _hole $dcdc512_m4 $cx $cy
        }
        _hole $hdmiconvertermainboard_mh1 $cx $cy
        _hole $hdmiconvertermainboard_mh2 $cx $cy
        _hole $hdmiconvertermainboard_mh3 $cx $cy
        _hole $hdmiconvertermainboard_mh4 $cx $cy
    }
    proc _hole {holecyl cx cy} {
        lassign [$holecyl cget -bottom] hx hy hz
        PostScriptFile hole [expr {$hx - $cx}] [expr {$hy - $cy}] \
              [expr {[$holecyl cget -radius] * 2.0}]
    }
    proc _svghole {svgout holecyl cx cy parent} {
        lassign [$holecyl cget -bottom] hx hy hz
        $svgout addcircle [expr {$hx - $cx}] [expr {-($hy - $cy)}] [$holecyl cget -radius] $parent
    }
    method svgout {svgout parent} {
        $panel svgout $svgout $parent
        lassign [$panel PanelCornerPoint] cx cy cz
        _svghole $svgout $m64_m1 $cx $cy $parent
        _svghole $svgout $m64_m2 $cx $cy $parent
        _svghole $svgout $m64_m3 $cx $cy $parent
        _svghole $svgout $m64_m4 $cx $cy $parent
        if {$options(-psbox) ne {}} {
            _svghole $svgout $psbox_m1 $cx $cy $parent
            _svghole $svgout $psbox_m2 $cx $cy $parent
            _svghole $svgout $psbox_m3 $cx $cy $parent
            _svghole $svgout $psbox_m4 $cx $cy $parent
        }
        if {$options(-dcdc512) ne {}} {
            _svghole $svgout $dcdc512_m1 $cx $cy $parent
            _svghole $svgout $dcdc512_m2 $cx $cy $parent
            _svghole $svgout $dcdc512_m3 $cx $cy $parent
            _svghole $svgout $dcdc512_m4 $cx $cy $parent
        }
        _svghole $svgout $hdmiconvertermainboard_mh1 $cx $cy $parent
        _svghole $svgout $hdmiconvertermainboard_mh2 $cx $cy $parent
        _svghole $svgout $hdmiconvertermainboard_mh3 $cx $cy $parent
        _svghole $svgout $hdmiconvertermainboard_mh4 $cx $cy $parent
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
                        -cornerpoint [list $cx [expr {$m64Y - $_DualUSBYMin}] $zbase] \
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
    proc _svghole {svgout holecyl cx cy parent} {
        lassign [$holecyl cget -bottom] dum hx hy
        $svgout addcircle [expr {$hx - $cx}] [expr {-($hy - $cy)}] [$holecyl cget -radius] $parent
    }
    proc _svgcutout {svgout cutoutSurf cx cy parent} {
        lassign [$cutoutSurf cget -cornerpoint] dummy cux cuy
        lassign [$cutoutSurf cget -vec1] dummy w dummy
        set w [expr {-($w)}]
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        $svgout addrect [expr {($cux - $cx)-$w}] [expr {-($cuy - $cy)-$h}] $w $h $parent
    }
    method svgout {svgout parent} {
        $panel svgout $svgout $parent
        lassign [$panel PanelCornerPoint] cx cy cz
        _svghole $svgout $audiojackcutout $cy $cz $parent
        _svgcutout $svgout [$rj45cutout cget -surface] $cy $cz $parent
        _svgcutout $svgout [$dualUSBcutout cget -surface] $cy $cz $parent
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
    proc _svgcutout {svgout cutoutSurf cx cy parent} {
        lassign [$cutoutSurf cget -cornerpoint] cux dummy cuy
        lassign [$cutoutSurf cget -vec1] w dummy dummy
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        $svgout addrect [expr {$cux - $cx}] [expr {-($cuy - $cy)-$h}] $w $h $parent
    }
    method svgout {svgout parent} {
        $panel svgout $svgout $parent 
        lassign [$panel PanelCornerPoint] cx cy cz
        _svgcutout $svgout [$gpiocutout cget -surface] $cx $cz $parent
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
        set fp [PostScriptFile fp]
        set xi 1
        set yi 2
        set xorg 0
        set yorg 0
        set xscale .01968
        set yscale .01968
        set surf [$panel cget -surface]
        PostScriptFile newPage {Front bottom Cutouts}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        [$fancutout1 cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        [$fancutout2 cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Left bottom Cutouts Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _cutout [$fancutout1 cget -surface] $cy $cz
        _cutout [$fancutout2 cget -surface] $cy $cz
    }
    proc _cutout {cutoutSurf cx cy} {
        lassign [$cutoutSurf cget -cornerpoint] dummy cux cuy
        lassign [$cutoutSurf cget -vec1] dummy w dummy
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        PostScriptFile cutout [expr {$cux - $cx}] [expr {$cuy - $cy}] $w $h
    }
    proc _svgcutout {svgout cutoutSurf cx cy parent} {
        lassign [$cutoutSurf cget -cornerpoint] dummy cux cuy
        lassign [$cutoutSurf cget -vec1] dummy w dummy
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        $svgout addrect [expr {$cux - $cx}] [expr {-($cuy - $cy)-$h}] $w $h $parent
    }
    method svgout {svgout parent} {
        $panel svgout $svgout $parent
        lassign [$panel PanelCornerPoint] cx cy cz
        _svgcutout  $svgout [$fancutout1 cget -surface] $cy $cz $parent
        _svgcutout  $svgout [$fancutout2 cget -surface] $cy $cz $parent
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
    proc _svgcutout {svgout cutoutSurf cx cy parent} {
        lassign [$cutoutSurf cget -cornerpoint] cux dummy cuy
        lassign [$cutoutSurf cget -vec1] w dummy dummy
        lassign [$cutoutSurf cget -vec2] dummy dummy h
        $svgout addrect [expr {($cux - $cx)-$w}] [expr {-($cuy - $cy)-$h}] $w $h $parent
    }
    method svgout {svgout parent} {
        $panel svgout $svgout $parent
        lassign [$panel PanelCornerPoint] cx cy cz
        _svgcutout  $svgout [$inletcutout cget -surface] $cx $cz $parent
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
    typevariable _dcdc512Yoff [expr {2*25.4}]
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
            -origin $options(-origin) -psbox $psbox -dcdc512 $dcdc512 \
            -otg [$m64 OTG]
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
    method svgout {svgout parent} {
        set bottomgroup [$svgout newgroup bottom -parent $parent]
        set xoff 6.35
        set yoff [expr {6.35 + (2*($_Width + 6.35))}]
        set panelgroup [$svgout newgroup panel -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $bottomgroup]
        $bottom svgout $svgout $panelgroup
        set xoff [expr {$xoff + $_Height + 6.35}]
        set leftgroup [$svgout newgroup left -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $bottomgroup]
        $left svgout $svgout $leftgroup
        set xoff [expr {$xoff + $_BottomDepth + 6.35}]
        set rightgroup [$svgout newgroup right -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $bottomgroup]
        $right svgout $svgout $rightgroup
        set xoff [expr {$xoff + $_BottomDepth + 6.35}]
        set frontgroup [$svgout newgroup front -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $bottomgroup]
        $front svgout $svgout $frontgroup
        set xoff [expr {$xoff + $_BottomDepth + 6.35}]
        set backgroup [$svgout newgroup back -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $bottomgroup]
        $back svgout $svgout $backgroup
    }
}

snit::type PortableM64CaseMiddlePanel {
    Common
    PortableM64CaseCommon
    LCDDims
    BracketAngleDims
    HDMIConverterDims
    SpeakerDims
    Common
    component panel
    delegate method * to panel except {print addPart}
    delegate option * to panel
    component leftbracket
    delegate method {leftbracket SVG3View} to leftbracket as SVG3View
    component rightbracket
    delegate method {rightbracket SVG3View} to rightbracket as SVG3View
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
    component hdmibuttonboard_blockhole1
    component hdmibuttonboard_blockhole2
    component hdmihvpowerboard
    component hdmihvpowerboard_mh1
    component hdmihvpowerboard_mh2
    component hdmihvpowerboard_standoff1
    component hdmihvpowerboard_standoff2
    component hdmihvpowerboard_blockhole1
    component hdmihvpowerboard_blockhole2
    component leftspeaker
    component leftspeaker_mhtop
    component leftspeaker_mhbottom
    component leftspeaker_standofftop
    component leftspeaker_standoffbottom
    component leftspeaker_blockholetop
    component leftspeaker_blockholebottom
    component rightspeaker
    component rightspeaker_mhtop
    component rightspeaker_mhbottom
    component rightspeaker_standofftop
    component rightspeaker_standoffbottom
    component rightspeaker_blockholetop
    component rightspeaker_blockholebottom
    component frontblock
    component backblock
    component leftblock
    component rightblock
    component leftfrontcorner
    component rightfrontcorner
    component leftbackcorner
    component rightbackcorner
    component rightspeaker_mhtop_to_rightbracket_m2_dim
    component rightspeaker_mhbottom_to_rightbracket_m3_dim
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
        install leftspeaker using SpeakerLeft_UpsideDown %AUTO% \
              -origin [list $cx \
                       [expr {$cy + (($panelLength-$_Speaker_Length)/2.0)}] \
                       [expr {$cz - (6.35-$_Speaker_StandoffRecessDepth)}]]
        set leftspeaker_mhtop [$leftspeaker MountingHole %AUTO% top $cz [$panel PanelThickness]]
        set leftspeaker_mhbottom [$leftspeaker MountingHole %AUTO% bottom $cz [$panel PanelThickness]]
        set leftspeaker_standofftop [$leftspeaker Standoff %AUTO% top $cz -6.35 6 {255 255 0}]
        set leftspeaker_standoffbottom [$leftspeaker Standoff %AUTO% bottom $cz -6.35 6 {255 255 0}]
        install rightspeaker using SpeakerRight_UpsideDown %AUTO% \
              -origin [list [expr {($cx + $panelWidth)-$_Speaker_Width}] \
                       [expr {$cy + (($panelLength-$_Speaker_Length)/2.0)}] \
                       [expr {$cz - (6.35-$_Speaker_StandoffRecessDepth)}]]
        set rightspeaker_mhtop [$rightspeaker MountingHole %AUTO% top $cz [$panel PanelThickness]]
        set rightspeaker_mhbottom [$rightspeaker MountingHole %AUTO% bottom $cz [$panel PanelThickness]]
        set rightspeaker_standofftop [$rightspeaker Standoff %AUTO% top $cz -6.35 6 {255 255 0}]
        set rightspeaker_standoffbottom [$rightspeaker Standoff %AUTO% bottom $cz -6.35 6 {255 255 0}]
        set psurf [$panel cget -surface]
        set vec1  [$psurf cget -vec1]
        set w [lindex $vec1 0]
        set vec2  [$psurf cget -vec2]
        set h [lindex $vec2 1]
        install frontblock using BlockX %AUTO% \
              -origin [list $cx $cy [expr {$cz + [$panel PanelThickness]}]] \
              -length $w
        install backblock  using BlockX %AUTO% \
              -origin [list $cx \
                       [expr {$cy + $h - $_BlockWidth}] \
                       [expr {$cz + [$panel PanelThickness]}]] \
              -length $w
        install leftblock using BlockY %AUTO% \
              -origin [list $cx [expr {$cy + $_BlockWidth}] \
                       [expr {$cz + [$panel PanelThickness]}]] \
              -length [expr {$h - (2*$_BlockWidth)}]
        install rightblock using BlockY %AUTO% \
              -origin [list [expr {$cx + $w - $_BlockWidth}] \
                       [expr {$cy + $_BlockWidth}] [expr {$cz + [$panel PanelThickness]}]] \
              -length [expr {$h - (2*$_BlockWidth)}]
        install leftfrontcorner using BlockZa %AUTO% \
              -origin [list $cx $cy [expr {$cz + [$panel PanelThickness] + $_BlockThick}]] \
              -length [expr {$_MiddleTotalDepth - ($_MiddleLowerDepth + [$panel PanelThickness] + $_BlockThick)}]
        install rightfrontcorner using BlockZa %AUTO% \
              -origin [list [expr {$cx + $w - $_BlockThick}] \
                       $cy [expr {$cz + [$panel PanelThickness] + $_BlockThick}]] \
              -length [expr {$_MiddleTotalDepth - ($_MiddleLowerDepth + [$panel PanelThickness] + $_BlockThick)}]
        install leftbackcorner using BlockZa %AUTO% \
              -origin [list $cx \
                       [expr {$cy + $h - $_BlockWidth}] \
                       [expr {$cz + [$panel PanelThickness] + $_BlockThick}]] \
              -length [expr {$_MiddleTotalDepth - ($_MiddleLowerDepth + [$panel PanelThickness] + $_BlockThick)}]
        install rightbackcorner using BlockZa %AUTO% \
              -origin [list [expr {$cx + $w - $_BlockThick}] \
                       [expr {$cy + $h - $_BlockWidth}] \
                       [expr {$cz + [$panel PanelThickness] + $_BlockThick}]] \
              -length [expr {$_MiddleTotalDepth - ($_MiddleLowerDepth + [$panel PanelThickness] + $_BlockThick)}]
        set hdmibuttonboard_blockhole1 [$hdmibuttonboard Standoff %AUTO% 1 [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6.35 {255 255 0}]
        set hdmibuttonboard_blockhole2 [$hdmibuttonboard Standoff %AUTO% 2 [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6.35 {255 255 0}]
        set hdmihvpowerboard_blockhole1 [$hdmihvpowerboard Standoff %AUTO% 1 [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6.35 {255 255 0}]
        set hdmihvpowerboard_blockhole2 [$hdmihvpowerboard Standoff %AUTO% 2 [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6.35 {255 255 0}]
        set leftspeaker_blockholetop [$leftspeaker Standoff %AUTO% top [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6 {255 255 0}]
        set leftspeaker_blockholebottom [$leftspeaker Standoff %AUTO% bottom [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6 {255 255 0}]
        set rightspeaker_blockholetop [$rightspeaker Standoff %AUTO% top [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6 {255 255 0}]
        set rightspeaker_blockholebottom [$rightspeaker Standoff %AUTO% bottom [expr {$cz + [$panel PanelThickness]}] $_BlockThick 6 {255 255 0}]
        set dimz [expr {$cz - 12.7}]
        set dimx [expr {$cx + $w + 25.4}]
        lassign [$rightspeaker_mhtop cget -bottom] x1 y1 dummy
        lassign [$rightbracket_m2 cget -bottom] x2 y2 dummy
        install rightspeaker_mhtop_to_rightbracket_m2_dim using Dim3D %AUTO% \
              -point1 [list [expr {($x1 + $x2)/2.0}] $y2 $dimz] \
              -point2 [list [expr {($x1 + $x2)/2.0}] $y1 $dimz] \
              -textpoint [list $dimx [expr {($y1 + $y2)/2.0}] $dimz] \
              -plane P \
              -additionaltext " mm"
        puts stderr [format {*** $type create $self: rightspeaker_mhtop_to_rightbracket_m2_dim is %g} [expr {abs($y2-$y1)}]]
        lassign [$rightspeaker_mhbottom cget -bottom] x1 y1 dummy
        lassign [$rightbracket_m3 cget -bottom] x2 y2 dummy
        install rightspeaker_mhbottom_to_rightbracket_m3_dim using Dim3D %AUTO% \
              -point1 [list [expr {($x1 + $x2)/2.0}] $y1 $dimz] \
              -point2 [list [expr {($x1 + $x2)/2.0}] $y2 $dimz] \
              -textpoint [list $dimx [expr {($y1 + $y2)/2.0}] $dimz] \
              -plane P \
              -additionaltext " mm"
        puts stderr [format {*** $type create $self: rightspeaker_mhbottom_to_rightbracket_m3_dim is %g} [expr {abs($y2-$y1)}]]
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
        $leftspeaker print $fp
        $leftspeaker_mhtop print $fp
        $leftspeaker_mhbottom print $fp
        $leftspeaker_standofftop print $fp
        $leftspeaker_standoffbottom print $fp
        $rightspeaker print $fp
        $rightspeaker_mhtop print $fp        
        $rightspeaker_mhbottom print $fp
        $rightspeaker_standofftop print $fp
        $rightspeaker_standoffbottom print $fp
        $frontblock print $fp
        $backblock  print $fp
        $leftblock print $fp
        $rightblock print $fp
        $leftfrontcorner print $fp
        $rightfrontcorner print $fp
        $leftbackcorner print $fp
        $rightbackcorner print $fp
        $hdmibuttonboard_blockhole1 print $fp
        $hdmibuttonboard_blockhole2 print $fp
        $hdmihvpowerboard_blockhole1 print $fp
        $hdmihvpowerboard_blockhole2 print $fp
        $leftspeaker_blockholetop print $fp
        $leftspeaker_blockholebottom print $fp
        $rightspeaker_blockholetop print $fp
        $rightspeaker_blockholebottom print $fp
        #$rightspeaker_mhtop_to_rightbracket_m2_dim print $fp
        #$rightspeaker_mhbottom_to_rightbracket_m3_dim print $fp
    }
    method addPart {partListArrayName} {
        #puts stderr "*** $self addPart $partListArrayName"
        upvar $partListArrayName partListArray
        $panel addPart partListArray
        $frontblock addPart partListArray
        $backblock addPart partListArray
        $leftblock addPart partListArray
        $rightblock addPart partListArray
        $leftfrontcorner addPart partListArray
        $rightfrontcorner addPart partListArray
        $leftbackcorner addPart partListArray
        $rightbackcorner addPart partListArray
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
        PostScriptFile newPage {Middle Panel Drill Pattern}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $leftbracket_m1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $leftbracket_m2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $leftbracket_m3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $leftbracket_m4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $rightbracket_m1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $rightbracket_m2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $rightbracket_m3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $rightbracket_m4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $hdmibuttonboard_mh1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $hdmibuttonboard_mh2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $hdmihvpowerboard_mh1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $hdmihvpowerboard_mh2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $leftspeaker_mhtop printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $leftspeaker_mhbottom printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $rightspeaker_mhtop printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $rightspeaker_mhbottom printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Middle Panel Drill Report}
        lassign [$panel PanelCornerPoint] cx cy cz
        _hole $leftbracket_m1 $cx $cy
        _hole $leftbracket_m2 $cx $cy
        _hole $leftbracket_m3 $cx $cy
        _hole $leftbracket_m4 $cx $cy
        _hole $rightbracket_m1 $cx $cy
        _hole $rightbracket_m2 $cx $cy
        _hole $rightbracket_m3 $cx $cy
        _hole $rightbracket_m4 $cx $cy
        _hole $hdmibuttonboard_mh1 $cx $cy
        _hole $hdmibuttonboard_mh2 $cx $cy
        _hole $hdmihvpowerboard_mh1 $cx $cy
        _hole $hdmihvpowerboard_mh2 $cx $cy
        _hole $leftspeaker_mhtop $cx $cy
        _hole $leftspeaker_mhbottom $cx $cy
        _hole $rightspeaker_mhtop $cx $cy
        _hole $rightspeaker_mhbottom $cx $cy
    }
    proc _hole {holecyl cx cy} {
        lassign [$holecyl cget -bottom] hx hy hz
        PostScriptFile hole [expr {$hx - $cx}] [expr {$hy - $cy}] \
              [expr {[$holecyl cget -radius] * 2.0}]
    }
    proc _svghole {svgout holecyl cx cy parent} {
        lassign [$holecyl cget -bottom] hx hy hz
        $svgout addcircle [expr {$hx - $cx}] [expr {-($hy - $cy)}] [$holecyl cget -radius] $parent
    }
    method svgout {svgout parent} {
        $panel svgout $svgout $parent
        lassign [$panel PanelCornerPoint] cx cy cz
        _svghole $svgout $leftbracket_m1 $cx $cy $parent
        _svghole $svgout $leftbracket_m2 $cx $cy $parent
        _svghole $svgout $leftbracket_m3 $cx $cy $parent
        _svghole $svgout $leftbracket_m4 $cx $cy $parent
        _svghole $svgout $rightbracket_m1 $cx $cy $parent
        _svghole $svgout $rightbracket_m2 $cx $cy $parent
        _svghole $svgout $rightbracket_m3 $cx $cy $parent
        _svghole $svgout $rightbracket_m4 $cx $cy $parent
        _svghole $svgout $hdmibuttonboard_mh1 $cx $cy $parent
        _svghole $svgout $hdmibuttonboard_mh2 $cx $cy $parent
        _svghole $svgout $hdmihvpowerboard_mh1 $cx $cy $parent
        _svghole $svgout $hdmihvpowerboard_mh2 $cx $cy $parent
        _svghole $svgout $leftspeaker_mhtop $cx $cy $parent
        _svghole $svgout $leftspeaker_mhbottom $cx $cy $parent
        _svghole $svgout $rightspeaker_mhtop $cx $cy $parent
        _svghole $svgout $rightspeaker_mhbottom $cx $cy $parent
    }
    method {backblock drillsheet} {} {
        lassign [[$backblock cget -surface] cget -cornerpoint] bcx bcy dummy
        lassign [[$backblock cget -surface] cget -vec2] dummy width dummy
        lassign [$backblock cget -vector] length dummy dummy
        set svgpage [SVGOutput create %AUTO% -width 8.5 -height 11]
        set drillgroup [$svgpage newgroup drillgroup -transform "[$svgpage scaleTransform .5] [$svgpage translateTransform 76.2 25.4]" -style {font-family:Monospace;font-size:4pt;}]
        $svgpage addrect 0 0 $width $length $drillgroup
        set r [$hdmibuttonboard_blockhole1 cget -radius]
        set dims(HoleDia) [expr {$r * 2.0}]
        set yPrev 0
        lassign [$hdmibuttonboard_blockhole1 cget -bottom] bx by dummy
        set y [expr {$bx-$bcx}]
        set x [expr {$by-$bcy}]
        $svgpage addHoledimension HoleDia $x $y [expr {$y - 25}] [expr {$x + 7}] [expr {$x + 15}] "HoleDia (4x)" $drillgroup
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension hdmibuttonboardMY1 $yPrev $y $x [expr {$width + 7.5}] M1 $drillgroup
        set dims(M1) [expr {$y - $yPrev}]
        set yPrev $y
        $svgpage addXdimension hdmibuttonboardMX1 0 $x $y [expr {$y + 10}] N1 $drillgroup true
        set dims(N1) $x
        lassign [$hdmibuttonboard_blockhole2 cget -bottom] bx by dummy
        set y [expr {$bx-$bcx}]
        set x [expr {$by-$bcy}]
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension hdmibuttonboardMY2 $yPrev $y $x [expr {$width + 7.5}] M2 $drillgroup
        set dims(M2) [expr {$y - $yPrev}]
        set yPrev $y
        $svgpage addXdimension hdmibuttonboardMX2 0 $x $y [expr {$y - 10}] N2 $drillgroup true
        set dims(N2) $x
        lassign [$hdmihvpowerboard_blockhole1 cget -bottom] bx by dummy
        set y [expr {$bx-$bcx}]
        set x [expr {$by-$bcy}]
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension hdmihvpowerboardMY1 $yPrev $y $x [expr {$width + 7.5}] M3 $drillgroup
        set dims(M3) [expr {$y - $yPrev}]
        set yPrev $y
        $svgpage addXdimension hdmihvpowerboardMX1 0 $x $y [expr {$y + 10}] N3 $drillgroup true
        set dims(N3) $x
        lassign [$hdmihvpowerboard_blockhole2 cget -bottom] bx by dummy
        set y [expr {$bx-$bcx}]
        set x [expr {$by-$bcy}]
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension hdmihvpowerboardMY2 $yPrev $y $x [expr {$width + 7.5}] M4 $drillgroup
        set dims(M4) [expr {$y - $yPrev}]
        $svgpage addXdimension hdmihvpowerboardMX2 0 $x $y [expr {$y - 10}] N4 $drillgroup true
        set dims(N4) $x
        set dimensiongroup [$svgpage newgroup dimensions -transform "[$svgpage translateTransform [expr {12.7+92}] [expr {12.7+25.4}]]" -style {font-family:Monospace;font-size:5px;}]
        set dimnames [lsort -dictionary [array names dims]]
        set tline [string repeat "-" [string length $_dimtableHeading]]
        $svgpage addtext 0 20 "$tline" $dimensiongroup
        $svgpage addtext 0 25 $_dimtableHeading $dimensiongroup
        $svgpage addtext 0 30 "$tline" $dimensiongroup
        set y 35
        foreach d $dimnames {
            set dline [format $_dimtableFormat $d [expr {$dims($d) / 25.4}] $dims($d)]
            $svgpage addtext 0 $y $dline $dimensiongroup
            incr y 5
        }
        $svgpage addtext 0 $y $tline $dimensiongroup
        return $svgpage
    }
    typevariable _dimtableFormat {|%-11.11s|%10.6f|%10.6f|}
    typevariable _dimtableHeading [format {|%-11.11s|%10.10s|%10.10s|} \
                                   Dim inch mm]
    method {leftblock drillsheet} {} {
        lassign [[$leftblock cget -surface] cget -cornerpoint] bcx bcy dummy
        lassign [[$leftblock cget -surface] cget -vec1] width dummy dummy
        lassign [$leftblock cget -vector] dummy length dummy
        set svgpage [SVGOutput create %AUTO% -width 8.5 -height 11]
        set drillgroup [$svgpage newgroup drillgroup -transform "[$svgpage scaleTransform .5] [$svgpage translateTransform 76.2 25.4]" -style {font-family:Monospace;font-size:4pt;}]
        $svgpage addrect 0 0 $width $length $drillgroup
        set r [$leftspeaker_blockholetop cget -radius]
        set dims(HoleDia) [expr {$r * 2.0}]
        set yPrev 0
        lassign [$leftspeaker_blockholetop cget -bottom] bx by dummy
        set x [expr {$bx-$bcx}]
        set y [expr {$by-$bcy}]
        $svgpage addHoledimension HoleDia $x $y [expr {$y - 25}] [expr {$x + 10}] [expr {$x + 20}] "HoleDia (2x)" $drillgroup
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension leftspeaker_topMY $yPrev $y $x [expr {$width + 7.5}] M1 $drillgroup
        set dims(M1) [expr {$y - $yPrev}]
        set yPrev $y
        $svgpage addXdimension leftspeaker_topMX 0 $x $y [expr {$y + 10}] N1 $drillgroup true
        set dims(N1) $x
        lassign [$leftspeaker_blockholebottom cget -bottom] bx by dummy
        set x [expr {$bx-$bcx}]
        set y [expr {$by-$bcy}]
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension leftspeaker_bottomMY $yPrev $y $x [expr {$width + 7.5}] M2 $drillgroup
        set dims(M2) [expr {$y - $yPrev}]
        set yPrev $y
        $svgpage addXdimension leftspeaker_bottomMX 0 $x $y [expr {$y - 10}] N2 $drillgroup true
        set dims(N2) $x
        set dimensiongroup [$svgpage newgroup dimensions -transform "[$svgpage translateTransform [expr {12.7+92}] [expr {12.7+25.4}]]" -style {font-family:Monospace;font-size:5px;}]
        set dimnames [lsort -dictionary [array names dims]]
        set tline [string repeat "-" [string length $_dimtableHeading]]
        $svgpage addtext 0 20 "$tline" $dimensiongroup
        $svgpage addtext 0 25 $_dimtableHeading $dimensiongroup
        $svgpage addtext 0 30 "$tline" $dimensiongroup
        set y 35
        foreach d $dimnames {
            set dline [format $_dimtableFormat $d [expr {$dims($d) / 25.4}] $dims($d)]
            $svgpage addtext 0 $y $dline $dimensiongroup
            incr y 5
        }
        $svgpage addtext 0 $y $tline $dimensiongroup
        return $svgpage
    }
    method {rightblock drillsheet} {} {
        lassign [[$rightblock cget -surface] cget -cornerpoint] bcx bcy dummy
        lassign [[$rightblock cget -surface] cget -vec1] width dummy dummy
        lassign [$rightblock cget -vector] dummy length dummy
        set svgpage [SVGOutput create %AUTO% -width 8.5 -height 11]
        set drillgroup [$svgpage newgroup drillgroup -transform "[$svgpage scaleTransform .5] [$svgpage translateTransform 76.2 25.4]" -style {font-family:Monospace;font-size:4pt;}]
        $svgpage addrect 0 0 $width $length $drillgroup
        set r [$rightspeaker_blockholetop cget -radius]
        set dims(HoleDia) [expr {$r * 2.0}]
        set yPrev 0
        lassign [$rightspeaker_blockholetop cget -bottom] bx by dummy
        set x [expr {$bx-$bcx}]
        set y [expr {$by-$bcy}]
        $svgpage addHoledimension HoleDia $x $y [expr {$y - 25}] [expr {$x + 10}] [expr {$x + 20}] "HoleDia (2x)" $drillgroup
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension rightspeaker_topMY $yPrev $y $x [expr {$width + 7.5}] M1 $drillgroup
        set dims(M1) [expr {$y - $yPrev}]
        set yPrev $y
        $svgpage addXdimension rightspeaker_topMX 0 $x $y [expr {$y + 10}] N1 $drillgroup true
        set dims(N1) $x
        lassign [$rightspeaker_blockholebottom cget -bottom] bx by dummy
        set x [expr {$bx-$bcx}]
        set y [expr {$by-$bcy}]
        $svgpage addcircle $x $y $r $drillgroup
        $svgpage addYdimension rightspeaker_bottomMY $yPrev $y $x [expr {$width + 7.5}] M2 $drillgroup
        set dims(M2) [expr {$y - $yPrev}]
        set yPrev $y
        $svgpage addXdimension rightspeaker_bottomMX 0 $x $y [expr {$y - 10}] N2 $drillgroup true
        set dims(N2) $x
        set dimensiongroup [$svgpage newgroup dimensions -transform "[$svgpage translateTransform [expr {12.7+92}] [expr {12.7+25.4}]]" -style {font-family:Monospace;font-size:5px;}]
        set dimnames [lsort -dictionary [array names dims]]
        set tline [string repeat "-" [string length $_dimtableHeading]]
        $svgpage addtext 0 20 "$tline" $dimensiongroup
        $svgpage addtext 0 25 $_dimtableHeading $dimensiongroup
        $svgpage addtext 0 30 "$tline" $dimensiongroup
        set y 35
        foreach d $dimnames {
            set dline [format $_dimtableFormat $d [expr {$dims($d) / 25.4}] $dims($d)]
            $svgpage addtext 0 $y $dline $dimensiongroup
            incr y 5
        }
        $svgpage addtext 0 $y $tline $dimensiongroup
        return $svgpage
    }
}


snit::type PortableM64CaseMiddle {
    Common
    PortableM64CaseCommon
    component middle
    delegate method * to middle
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
    method printPS {} {
        $middle printPS
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        $middle addPart partListArray
        $left addPart partListArray
        $right addPart partListArray
        $front addPart partListArray
        $back addPart partListArray
    }
    method svgout {svgout parent} {
        set middlegroup [$svgout newgroup middle -parent $parent]
        set xoff 6.35
        set yoff [expr {6.35 + $_Width + 6.35}]
        set panelgroup [$svgout newgroup panel -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $middlegroup]
        $middle svgout $svgout $panelgroup
        set xoff [expr {$xoff + $_Height + 6.35}]
        set leftgroup [$svgout newgroup left -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $middlegroup]
        $left svgout $svgout $leftgroup
        set xoff [expr {$xoff + $_MiddleTotalDepth + 6.35}]
        set rightgroup [$svgout newgroup right -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $middlegroup]
        $right svgout $svgout $rightgroup
        set xoff [expr {$xoff + $_MiddleTotalDepth + 6.35}]
        set frontgroup [$svgout newgroup front -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $middlegroup]
        $front svgout $svgout $frontgroup
        set xoff [expr {$xoff + $_MiddleTotalDepth + 6.35}]
        set backgroup [$svgout newgroup back -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $middlegroup]
        $back svgout $svgout $backgroup
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
    component frontblock
    component backblock
    component leftblock
    component rightblock
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
        lassign [$top PanelCornerPoint] cx cy cz
        set psurf [$top  cget -surface]
        set vec1  [$psurf cget -vec1]
        set panelWidth [lindex $vec1 0]
        set vec2 [$psurf cget -vec2]
        set panelLength [lindex $vec2 1]
        set panelThick [$top PanelThickness]
        install frontblock using BlockX %AUTO% \
              -origin [list $cx $cy [expr {$cz - $_BlockThick}]] \
              -length $panelWidth
        install backblock  using BlockX %AUTO% \
              -origin [list $cx \
                       [expr {$cy + $panelLength - $_BlockWidth}] \
                       [expr {$cz - $_BlockThick}]] \
              -length $panelWidth
        install leftblock using BlockY %AUTO% \
              -origin [list $cx [expr {$cy + $_BlockWidth}] \
                       [expr {$cz - $_BlockThick}]] \
              -length [expr {$panelLength - (2*$_BlockWidth)}]
        install rightblock using BlockY %AUTO% \
              -origin [list [expr {$cx + $panelWidth - $_BlockWidth}] \
                       [expr {$cy + $_BlockWidth}] [expr {$cz - $_BlockThick}]] \
              -length [expr {$panelLength - (2*$_BlockWidth)}]
                       
    }
    method print {{fp stdout}} {
        $top print $fp
        $left   print $fp
        $right   print $fp
        $front   print $fp
        $back   print $fp
        $frontblock print $fp
        $backblock print $fp
        $leftblock print $fp
        $rightblock print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        $top addPart partListArray
        $left addPart partListArray
        $right addPart partListArray
        $front addPart partListArray
        $back addPart partListArray
        $frontblock addPart partListArray
        $backblock addPart partListArray
        $leftblock addPart partListArray
        $rightblock addPart partListArray
    }
    method svgout {svgout parent} {
        set topgroup [$svgout newgroup top -parent $parent]
        set xoff 6.35
        set yoff 6.35
        set panelgroup [$svgout newgroup panel -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $topgroup]
        $top svgout $svgout $panelgroup
        set xoff [expr {$xoff + $_Height + 6.35}]
        set leftgroup [$svgout newgroup left -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $topgroup]
        $left svgout $svgout $leftgroup
        set xoff [expr {$xoff + $_TopDepth + 6.35}]
        set rightgroup [$svgout newgroup right -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $topgroup]
        $right svgout $svgout $rightgroup
        set xoff [expr {$xoff + $_TopDepth + 6.35}]
        set frontgroup [$svgout newgroup front -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $topgroup]
        $front svgout $svgout $frontgroup
        set xoff [expr {$xoff + $_TopDepth + 6.35}]
        set backgroup [$svgout newgroup back -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $topgroup]
        $back svgout $svgout $backgroup
    }
    
}

snit::enum Section -values {Top Middle Bottom KeyboardShelf}
snit::listtype _SectionList -type Section

snit::type SectionList {
    pragma -hastypeinfo no
    pragma -hastypedestroy no
    pragma -hasinstances no
    typemethod validate {value} {
        if {$value eq "all"} {
            return $value
        } elseif {[catch {_SectionList validate $value}]} {
            return -errorcode INVALID
        } else {
            return $value
        }
    }
}

snit::type PortableM64CaseKeyboardShelf {
    Common
    PortableM64CaseCommon
    TeensyThumbStickDims
    component shelf
    component hingeblock
    component teensythumbstickcutout
    component teensythumbstick
    component teensythumbstick_mh1
    component teensythumbstick_mh2
    component teensythumbstick_mh3
    component teensythumbstick_mh4
    component teensythumbstick_standoff1
    component teensythumbstick_standoff2
    component teensythumbstick_standoff3
    component teensythumbstick_standoff4
    component teensythumbstickcover
    constructor {args} {
        $self configurelist $args
        install shelf using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point $options(-origin) \
                                      [list $_WallThickness $_WallThickness $_ShelfHeight]] \
                        -vec1 [list [expr {$_Width - (2*$_WallThickness)}] 0 0] \
                        -vec2 [list 0 $_ShelfLength 0]] \
              -vector [list 0 0 $_WallThickness] \
              -color  {255 0 0}
        lassign [[$shelf cget -surface] cget -cornerpoint] sx sy sz
        lassign [[$shelf cget -surface] cget -vec1] shelfwidth dummy dummy
        install hingeblock using BlockX %AUTO% \
              -origin [list $sx $sy [expr {$sz + $_WallThickness}]] \
              -length $shelfwidth
        set teensythumbstickX [expr {$sx + ($shelfwidth - ($_TeensyThumbStick_Width + 12.7))}]
        set teensythumbstickY [expr {$sy + ($_ShelfLength - ($_TeensyThumbStick_Height + 12.7))}]
        install teensythumbstickcutout using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list $teensythumbstickX [expr {$teensythumbstickY + 6.35}] $sz] \
                        -vec1 [list $_TeensyThumbStick_Width 0 0] \
                        -vec2 [list 0 [expr {$_TeensyThumbStick_Height - 12.7}] 0]] \
              -vector [list 0 0 $_WallThickness] \
              -color  {255 255 255}
        install teensythumbstick using TeensyThumbStick %AUTO% \
              -origin [list $teensythumbstickX $teensythumbstickY \
                       [expr {$sz - $_TeensyThumbStickDrop - $_TeensyThumbStick_BoardThick}]]
        set teensythumbstick_mh1 [$teensythumbstick MountingHole %AUTO% 1 $sz $_WallThickness]
        set teensythumbstick_mh2 [$teensythumbstick MountingHole %AUTO% 2 $sz $_WallThickness]
        set teensythumbstick_mh3 [$teensythumbstick MountingHole %AUTO% 3 $sz $_WallThickness]
        set teensythumbstick_mh4 [$teensythumbstick MountingHole %AUTO% 4 $sz $_WallThickness]
        set teensythumbstick_standoff1 [$teensythumbstick Standoff %AUTO% 1 $sz -$_TeensyThumbStickDrop [expr {.25*25.4}] {255 255 0}]
        set teensythumbstick_standoff2 [$teensythumbstick Standoff %AUTO% 2 $sz -$_TeensyThumbStickDrop [expr {.25*25.4}] {255 255 0}]
        set teensythumbstick_standoff3 [$teensythumbstick Standoff %AUTO% 3 $sz -$_TeensyThumbStickDrop [expr {.25*25.4}] {255 255 0}]
        set teensythumbstick_standoff4 [$teensythumbstick Standoff %AUTO% 4 $sz -$_TeensyThumbStickDrop [expr {.25*25.4}] {255 255 0}]
        install teensythumbstickcover using TeensyThumbStickCover %AUTO% \
              -origin [list $teensythumbstickX $teensythumbstickY [expr {$sz + $_WallThickness}]]
    }
    method print {{fp stdout}} {
        $shelf print $fp
        $hingeblock print $fp
        $teensythumbstickcutout print $fp
        $teensythumbstick print $fp
        $teensythumbstick_mh1 print $fp
        $teensythumbstick_mh2 print $fp
        $teensythumbstick_mh3 print $fp
        $teensythumbstick_mh4 print $fp
        $teensythumbstick_standoff1 print $fp
        $teensythumbstick_standoff2 print $fp
        $teensythumbstick_standoff3 print $fp
        $teensythumbstick_standoff4 print $fp
        $teensythumbstickcover print $fp
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        set shelfsurf [$shelf cget -surface]
        set width [lindex [$shelfsurf cget -vec1] 0]
        set height [lindex [$shelfsurf cget -vec2] 1]
        set thick [lindex [$shelf cget -vector] 2]
        incr partListArray([$self _normPartSize $width $height $thick])
        $hingeblock addPart partListArray
    }
    method printPS {} {
        set fp  [PostScriptFile fp]
        set xi 0
        set yi 1
        set xorg 0
        set yorg 0
        set xscale .01968
        set yscale .01968
        set surf [$shelf cget -surface]
        PostScriptFile newPage {Keyboard Shelf Drill and Cutout Pattern}
        $surf printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $teensythumbstick_mh1 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $teensythumbstick_mh2 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $teensythumbstick_mh3 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        $teensythumbstick_mh4 printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        [$teensythumbstickcutout cget -surface] printPS $fp $xi $yi $xorg $yorg $xscale $yscale
        PostScriptFile newPage {Keyboard Shelf Drill and Cutouts Report}
        lassign [[$shelf cget -surface] cget -cornerpoint] cx cy cz
        _hole $teensythumbstick_mh1 $cx $cy
        _hole $teensythumbstick_mh2 $cx $cy
        _hole $teensythumbstick_mh3 $cx $cy
        _hole $teensythumbstick_mh4 $cx $cy
        _cutout [$teensythumbstickcutout cget -surface] $cx $cx
    }
    proc _cutout {cutoutSurf cx cy} {
        lassign [$cutoutSurf cget -cornerpoint] cux cuy dummy
        lassign [$cutoutSurf cget -vec1] w dummy dummy
        lassign [$cutoutSurf cget -vec2] dummy h dummy
        PostScriptFile cutout [expr {$cux - $cx}] [expr {$cuy - $cy}] $w $h
    }
    proc _hole {holecyl cx cy} {
        lassign [$holecyl cget -bottom] hx hy hz
        PostScriptFile hole [expr {$hx - $cx}] [expr {$hy - $cy}] \
              [expr {[$holecyl cget -radius] * 2.0}]
    }
    proc _svghole {svgout holecyl cx cy parent} {
        lassign [$holecyl cget -bottom] hx hy hz
        $svgout addcircle [expr {$hx - $cx}] [expr {-($hy - $cy)}] [$holecyl cget -radius] $parent
    }
    proc _svgcutout {svgout cutoutSurf cx cy parent} {
        lassign [$cutoutSurf cget -cornerpoint] cux cuy dummy
        lassign [$cutoutSurf cget -vec1] w dummy dummy
        #set w [expr {-($w)}]
        lassign [$cutoutSurf cget -vec2] dummy h dummy
        $svgout addrect [expr {($cux - $cx)}] [expr {-($cuy - $cy)-$h}] $w $h $parent
    }
    
    method svgout {svgout parent} {
        set xoff [expr {6.35 + $_Height + 6.35 + 4*($_TopDepth + 6.35)}]
        set yoff 6.35
        set shelfsurf [$shelf cget -surface]
        set width [lindex [$shelfsurf cget -vec1] 0]
        set height [lindex [$shelfsurf cget -vec2] 1]
        set keyboardshelfgroup [$svgout newgroup keyboardshelf -transform "[$svgout translateTransform $xoff $yoff] [$svgout rotateTransform 90]" -parent $parent]
        $svgout addrect 0 -$height $width $height $keyboardshelfgroup
        lassign [[$shelf cget -surface] cget -cornerpoint] cx cy cz
        _svghole $svgout $teensythumbstick_mh1 $cx $cy $keyboardshelfgroup
        _svghole $svgout $teensythumbstick_mh2 $cx $cy $keyboardshelfgroup
        _svghole $svgout $teensythumbstick_mh3 $cx $cy $keyboardshelfgroup
        _svghole $svgout $teensythumbstick_mh4 $cx $cy $keyboardshelfgroup
        _svgcutout $svgout [$teensythumbstickcutout cget -surface] $cx $cx $keyboardshelfgroup
    }
}


snit::type PortableM64Case {
    Common
    PortableM64CaseCommon
    component caseBottom
    component caseMiddle
    delegate method * to caseMiddle
    component caseTop
    component keyboardShelf
    option -sections -type SectionList -default all
    constructor {args} {
        $self configurelist $args
        install caseBottom using PortableM64CaseBottom %AUTO% -origin $options(-origin)
        install caseMiddle using PortableM64CaseMiddle %AUTO% -origin $options(-origin)
        install caseTop    using PortableM64CaseTop %AUTO%    -origin $options(-origin)
        install keyboardShelf using PortableM64CaseKeyboardShelf %AUTO%    -origin $options(-origin)
    }
    method print {{fp stdout}} {
        if {$options(-sections) eq "all" || "Bottom" in $options(-sections)} {
            $caseBottom print $fp
        }
        if {$options(-sections) eq "all" || "Middle" in $options(-sections)} {
            $caseMiddle print $fp
        }
        if {$options(-sections) eq "all" || "Top" in $options(-sections)} {
            $caseTop    print $fp
        }
        if {$options(-sections) eq "all" || "KeyboardShelf" in $options(-sections)} {
            $keyboardShelf print $fp
        }
    }
    method addPart {partListArrayName} {
        upvar $partListArrayName partListArray
        if {$options(-sections) eq "all" || "Bottom" in $options(-sections)} {
            $caseBottom addPart partListArray
        }
        if {$options(-sections) eq "all" || "Middle" in $options(-sections)} {
            $caseMiddle addPart partListArray
        }
        if {$options(-sections) eq "all" || "Top" in $options(-sections)} {
            $caseTop    addPart partListArray
        }
        if {$options(-sections) eq "all" || "KeyboardShelf" in $options(-sections)} {
            $keyboardShelf addPart partListArray
        }
    }
    method printPS {} {
        if {$options(-sections) eq "all" || "Bottom" in $options(-sections)} {
            $caseBottom printPS
        }
        if {$options(-sections) eq "all" || "Middle" in $options(-sections)} {
            $caseMiddle printPS
        }
        if {$options(-sections) eq "all" || "KeyboardShelf" in $options(-sections)} {
            $keyboardShelf printPS
        }
    }
    method svgout {svgout parent} {
        set casegroup [$svgout newgroup case]
        if {$options(-sections) eq "all" || "Bottom" in $options(-sections)} {
            $caseBottom svgout $svgout $casegroup
        }
        if {$options(-sections) eq "all" || "Middle" in $options(-sections)} {
            $caseMiddle svgout $svgout $casegroup
        }
        if {$options(-sections) eq "all" || "Top" in $options(-sections)} {
            $caseTop    svgout $svgout $casegroup
        }
        if {$options(-sections) eq "all" || "KeyboardShelf" in $options(-sections)} {
            $keyboardShelf svgout $svgout $casegroup
        }
    }
}






package provide Case 1.0
