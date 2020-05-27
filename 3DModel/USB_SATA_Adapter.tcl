#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon May 25 16:59:46 2020
#  Last Modified : <200527.0949>
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

snit::macro USB_SATA_AdapterDims {} {
    typevariable _USB_SATA_Adapter_OverallLength 62.68
    typevariable _USB_SATA_Adapter_BoardPolyH { 
        {9.44 15.94 0 1} {28.15 15.94 0 1} {28.15 62.85 0 1} {0 62.85 0 1} 
        {0 50.21 0 1} {9.44 28.12 0 1} {9.44 15.94 0 1}} 
    typevariable _USB_SATA_Adapter_RotateOffset [expr {-(28.15+10)}]
    typevariable _USB_SATA_Adapter_BoardThick 1.73
    typevariable _USB_SATA_Adapter_USBPlug_XOff 14.85
    typevariable _USB_SATA_Adapter_USBPlug_YOff 0
    typevariable _USB_SATA_Adapter_USBPlug_Width 12.03
    typevariable _USB_SATA_Adapter_USBPlug_Length 18.84
    typevariable _USB_SATA_Adapter_USBPlug_Height 4.57
}

snit::type USB_SATA_Adapter {
    Common
    USB_SATA_AdapterDims
    component board
    component usbplug
    constructor {args} {
        $self configurelist $args
        set boardpoly [GeometryFunctions StripHomogenous \
                       [GeometryFunctions translate3D \
                        $_USB_SATA_Adapter_BoardPolyH \
                        $options(-origin)]]
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -closedpolygon yes \
                        -polypoints $boardpoly] \
              -vector [list 0 0 $_USB_SATA_Adapter_BoardThick] \
              -color {128 0 0}

        lassign $options(-origin) ox oy oz
        install usbplug using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$ox + $_USB_SATA_Adapter_USBPlug_XOff}] \
                                      [expr {$oy + $_USB_SATA_Adapter_USBPlug_YOff}] \
                                      $oz] \
                        -vec1 [list $_USB_SATA_Adapter_USBPlug_Width 0 0] \
                        -vec2 [list 0 $_USB_SATA_Adapter_USBPlug_Length 0]] \
              -vector [list 0 0 $_USB_SATA_Adapter_USBPlug_Height] \
              -color  {250 250 250}

    }
    method print {{fp stdout}} {
        $board print $fp
        $usbplug print $fp
    }
}

snit::type USB_SATA_Adapter_Horiz {
    Common
    USB_SATA_AdapterDims
    component board
    component usbplug
    constructor {args} {
        $self configurelist $args
        set boardpoly [GeometryFunctions StripHomogenous \
                       [GeometryFunctions translate3D \
                        [GeometryFunctions rotateZAxis \
                         [GeometryFunctions translate3D \
                          $_USB_SATA_Adapter_BoardPolyH \
                          [list $_USB_SATA_Adapter_RotateOffset 0 0]] \
                         [GeometryFunctions radians -90]] \
                        $options(-origin)]]
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -closedpolygon yes \
                        -polypoints $boardpoly] \
              -vector [list 0 0 $_USB_SATA_Adapter_BoardThick] \
              -color {128 0 0}

        lassign $options(-origin) ox oy oz
        install usbplug using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$ox + $_USB_SATA_Adapter_USBPlug_YOff}] \
                                      [expr {$oy + $_USB_SATA_Adapter_USBPlug_XOff}] \
                                      $oz] \
                        -vec1 [list $_USB_SATA_Adapter_USBPlug_Length 0 0] \
                        -vec2 [list 0 $_USB_SATA_Adapter_USBPlug_Width 0]] \
              -vector [list 0 0 $_USB_SATA_Adapter_USBPlug_Height] \
              -color  {250 250 250}

    }
    method print {{fp stdout}} {
        $board print $fp
        $usbplug print $fp
    }
}

snit::macro BoardCradleDims {} {
    typevariable _BoardCradle_Upper_PolyH {
        {0 25.06 2.54 1} {12.180000 25.06 2.54 1} {34.270000 34.5 2.54 1} 
        {46.91 34.5 2.54 1} {46.91 40.85 2.54 1} 
        {0 40.85 2.54 1} {0 25.06 2.54 1}}        
    typevariable _BoardCradle_LowerRect_Width 6.35
    typevariable _BoardCradle_Length 46.91
    typevariable _BoardCradle_Width 40.85
    typevariable _BoardCradle_UnderThick 2.54
    typevariable _BoardCradle_CradleThick 1.7
    typevariable _BoardCradle_mh1X 23.455
    typevariable _BoardCradle_mh1Y 33
    typevariable _BoardCradle_mh2X 11.7275
    typevariable _BoardCradle_mh2Y  3.175
    typevariable _BoardCradle_mh3X 35.18250
    typevariable _BoardCradle_mh3Y  3.175
    typevariable _BoardCradle_mhdia 3.5
}


snit::type USB_SATA_Adapter_BoardCradleHoriz {
    Common
    BoardCradleDims
    component underbody
    component upperflange
    component lowerflange
    component mh1
    component mh2
    component mh3
    constructor {args} {
        $self configurelist $args
        install underbody using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_BoardCradle_Length 0 0] \
                        -vec2 [list 0 $_BoardCradle_Width 0]] \
              -vector [list 0 0 $_BoardCradle_UnderThick] \
              -color {0 0 0}
        install upperflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -closedpolygon yes \
                        -polypoints [GeometryFunctions StripHomogenous \
                                     [GeometryFunctions translate3D \
                                      $_BoardCradle_Upper_PolyH \
                                      $options(-origin)]]] \
              -vector [list 0 0 $_BoardCradle_CradleThick] \
              -color {0 0 0}
        install lowerflange using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [GeometryFunctions translate3D_point \
                                      $options(-origin) \
                                      [list 0 0 $_BoardCradle_UnderThick]] \
                        -vec1 [list $_BoardCradle_Length 0 0] \
                        -vec2 [list 0 $_BoardCradle_LowerRect_Width 0]] \
              -vector [list 0 0 $_BoardCradle_CradleThick] \
              -color {0 0 0}
        lassign $options(-origin) ox oy oz
        set mhHeight [expr {$_BoardCradle_UnderThick+$_BoardCradle_CradleThick}]
        set mh1X [expr {$ox + $_BoardCradle_mh1X}]
        set mh1Y [expr {$oy + $_BoardCradle_mh1Y}]
        install mh1 using Cylinder %AUTO% \
              -bottom [list $mh1X $mh1Y $oz] \
              -radius [expr {$_BoardCradle_mhdia / 2.0}] \
              -height $mhHeight \
              -direction Z \
              -color {255 255 255}
        set mh2X [expr {$ox + $_BoardCradle_mh2X}]
        set mh2Y [expr {$oy + $_BoardCradle_mh2Y}]
        install mh2 using Cylinder %AUTO% \
              -bottom [list $mh2X $mh2Y $oz] \
              -radius [expr {$_BoardCradle_mhdia / 2.0}] \
              -height $mhHeight \
              -direction Z \
              -color {255 255 255}
        set mh3X [expr {$ox + $_BoardCradle_mh3X}]
        set mh3Y [expr {$oy + $_BoardCradle_mh3Y}]
        install mh3 using Cylinder %AUTO% \
              -bottom [list $mh3X $mh3Y $oz] \
              -radius [expr {$_BoardCradle_mhdia / 2.0}] \
              -height $mhHeight \
              -direction Z \
              -color {255 255 255}
    }
    method print {{fp stdout}} {
        $underbody print $fp
        $upperflange print $fp
        $lowerflange print $fp
        $mh1 print $fp
        $mh2 print $fp
        $mh3 print $fp
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
}
   
package provide USB_SATA_Adapter 1.0

