#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 23 20:10:58 2020
#  Last Modified : <200528.1450>
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

snit::macro USBHubDims {} {
    typevariable _USBHUB_Length 104.66
    typevariable _USBHUB_Height 36
    typevariable _USBHUB_Width  22.24
    typevariable _USBHUB_EndPolyH {{0 0 0 1} {0 22.24 0 1} {0 22.24 27.55 1} 
        {0 15.38 36 1} {0 0 36 1} {0 0 0 1}} 
    typevariable _USBHUB_EndPoly90H {{0 0 0 1} {0 0 27.55 1} {15.38 0 36 1} 
        {22.24 0 36 1} {22.24 0 0 1} {0 0 0 1}} 
    typevariable _USBHUB_EndPoly270H {{0 0 0 1} {0 0 36 1} {15.38 0 36 1}
        {22.24 0 27.55 1} {22.24 0 0 1} {0 0 0 1}}
}

snit::type USBHub {
    Common
    USBHubDims
    component body
    delegate option * to body
    delegate method * to body
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -closedpolygon yes \
                        -polypoints [GeometryFunctions StripHomogenous \
                                     [GeometryFunctions translate3D \
                                      $_USBHUB_EndPolyH \
                                      $options(-origin)]]] \
              -vector [list $_USBHUB_Length 0 0] \
              -color {0 0 0}
    }
}

snit::type USBHub90 {
    Common
    USBHubDims
    component body
    delegate option * to body
    delegate method * to body
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -closedpolygon yes \
                        -polypoints [GeometryFunctions StripHomogenous \
                                     [GeometryFunctions translate3D \
                                      $_USBHUB_EndPoly90H \
                                      $options(-origin)]]] \
              -vector [list 0 $_USBHUB_Length 0] \
              -color {0 0 0}
    }
}

snit::type USBHub270 {
    Common
    USBHubDims
    component body
    delegate option * to body
    delegate method * to body
    constructor {args} {
        $self configurelist $args
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -closedpolygon yes \
                        -polypoints [GeometryFunctions StripHomogenous \
                                     [GeometryFunctions translate3D \
                                      $_USBHUB_EndPoly270H \
                                      $options(-origin)]]] \
              -vector [list 0 $_USBHUB_Length 0] \
              -color {0 0 0}
    }
}


package provide USBHub 1.0
              
