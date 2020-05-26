#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon May 25 21:06:47 2020
#  Last Modified : <200525.2316>
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

snit::macro OTGAdaptorDims {} {
    typevariable _OTGAdaptor_ADepth 9.28
    typevariable _OTGAdaptor_ZDisp -2.91
    typevariable _OTGAdaptor_XOffA -2.94
    typevariable _OTGAdaptor_GrossWidth 17.58
    typevariable _OTGAdaptor_GrossThick 9.82
    typevariable _OTGAdaptor_BodyLength 32.74
    typevariable _OTGAdaptor_BodyPolyH {
        {0 32.74 0 1} {17.58 32.74 0 1} {17.58 15.12 0 1} {12.36 0 0 1} 
        {3.48 0 0 1} {0 15.12 0 1} {0 32.74 0 1}}
    typevariable _OTGAdaptor_MicroB_Length 5.92
    typevariable _OTGAdaptor_MicroB_Width 6.85
    typevariable _OTGAdaptor_MicroB_Thick 1.8
    typevariable _OTGAdaptor_MicroB_XOff 4.35
    typevariable _OTGAdaptor_MicroB_ZOff 3.49
}


snit::type OTGAdaptor {
    Common
    OTGAdaptorDims
    component body
    component microb
    constructor {args} {
        $self configurelist $args
        set bodypoly [GeometryFunctions StripHomogenous \
                      [GeometryFunctions translate3D \
                       $_OTGAdaptor_BodyPolyH $options(-origin)]]
        install body using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -closedpolygon yes \
                        -polypoints $bodypoly] \
              -vector [list 0 0 $_OTGAdaptor_GrossThick] \
              -color {0 0 0}
        lassign $options(-origin) ox oy oz
        install microb using PrismSurfaceVector %AUTO% \
              -surface [PolySurface create %AUTO% \
                        -rectangle yes \
                        -cornerpoint [list [expr {$ox + $_OTGAdaptor_MicroB_XOff}] \
                                      $oy [expr {$oz + $_OTGAdaptor_MicroB_ZOff}]] \
                        -vec1 [list $_OTGAdaptor_MicroB_Width 0 0] \
                        -vec2 [list 0 -$_OTGAdaptor_MicroB_Length 0]] \
              -vector [list 0 0 $_OTGAdaptor_MicroB_Thick] \
              -color {250 250 250}
    }
    method print {{fp stdout}} {
        $body print $fp
        $microb print $fp
    }
}

package provide OTGAdaptor 1.0

