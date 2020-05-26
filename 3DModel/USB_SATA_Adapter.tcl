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
#  Last Modified : <200525.2319>
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


package provide USB_SATA_Adapter 1.0

