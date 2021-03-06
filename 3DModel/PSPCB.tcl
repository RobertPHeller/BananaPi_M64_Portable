#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 13:36:01 2020
#  Last Modified : <200511.0943>
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
package require PowerSupply
package require TerminalBlocks
package require Capacitors
package require Diode
package require FuseHolder
package require MOV

snit::macro PCBDims {} {
    typevariable _psPCBwidth 45.72
    typevariable _psPCBlength 76.2
    typevariable _psPCBThickness [expr {(1.0/16.0)*25.4}]
    typevariable _pstermxoff  0.98
    typevariable _psactermyoff  5.08
    typevariable _psdctermyoff  10.16
}

snit::type PCBwithStrips {
    typevariable _stripWidth [expr {2.54*.8}]
    typevariable _stripIncr  2.54
    typevariable _stripOffset 1.27
    typevariable _stripThickness .1
    typevariable _stripExtra 7.62
    typevariable _mhdia 3.5
    PCBDims
    PSDims
    Common
    component board
    variable strips [list]
    component mh1
    component mh2
    component mh3
    component mh4
    constructor {args} {
        $self configurelist $args
        install board using PrismSurfaceVector %AUTO% \
              -surface [PolySurface  create %AUTO% \
                        -rectangle yes \
                        -cornerpoint $options(-origin) \
                        -vec1 [list $_psPCBwidth 0 0] \
                        -vec2 [list 0 $_psPCBlength 0]] \
              -vector [list 0 0 $_psPCBThickness] \
              -color {210 180 140}
        set yoff [expr {($_psPCBlength - $_pslength)/2.0}]
        set xoff [expr {($_psPCBwidth - $_pswidth)/2.0}]
        set pin1X [expr {$_pspin1Yoff+$xoff}]
        set pin2X [expr {$_pspin2Yoff+$xoff}]
        for {set sx $_stripIncr} \
              {($sx + $_stripIncr) <= $_psPCBwidth} \
              {set sx [expr {$sx + $_stripIncr}]} {
            if {$sx <= $pin1X && $sx >= $pin2X} {
                set stripCP1 [GeometryFunctions translate3D_point $options(-origin) \
                              [list [expr {$sx - ($_stripWidth / 2.0)}] \
                               $_stripOffset \
                               0.0]]
                set stripCP2 [GeometryFunctions translate3D_point $options(-origin) \
                              [list [expr {$sx - ($_stripWidth / 2.0)}] \
                               [expr {$_stripOffset + $xoff + $_pspin1Xoff - $_stripExtra}]\
                               0.0]]
                set striplen [expr {$yoff + $_pspin4Xoff + $_stripExtra}]
                lappend strips \
                      [PrismSurfaceVector create %AUTO% \
                       -surface [PolySurface  create %AUTO% \
                                 -rectangle yes \
                                 -cornerpoint $stripCP1 \
                                 -vec1 [list $_stripWidth 0 0] \
                                 -vec2 [list 0 $striplen 0]] \
                       -vector [list 0 0 -$_stripThickness] \
                       -color {255 255 0}]
                lappend strips \
                      [PrismSurfaceVector create %AUTO% \
                       -surface [PolySurface  create %AUTO% \
                                 -rectangle yes \
                                 -cornerpoint $stripCP2 \
                                 -vec1 [list $_stripWidth 0 0] \
                                 -vec2 [list 0 $striplen 0]] \
                       -vector [list 0 0 -$_stripThickness] \
                       -color {255 255 0}]
            } else {    
                set stripCP [GeometryFunctions translate3D_point $options(-origin) \
                             [list [expr {$sx - ($_stripWidth / 2.0)}] \
                              $_stripOffset \
                              0.0]]
                lappend strips \
                      [PrismSurfaceVector create %AUTO% \
                       -surface [PolySurface  create %AUTO% \
                                 -rectangle yes \
                                 -cornerpoint $stripCP \
                                 -vec1 [list $_stripWidth 0 0] \
                                 -vec2 [list 0 [expr {$_psPCBlength - ($_stripOffset*2)}] 0]] \
                       -vector [list 0 0 -$_stripThickness] \
                       -color {255 255 0}]
           }
       }
       install mh1 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list $_stripIncr [expr {$_stripIncr + 5*2.54}]  -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
       install mh2 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list [expr {$_psPCBwidth - $_stripIncr}] \
                       [expr {$_stripIncr + 5*2.54}] \
                       -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
       install mh3 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list $_stripIncr \
                       [expr {$_psPCBlength - ($_stripIncr + 5*2.54)}] \
                       -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
       install mh4 using Cylinder %AUTO% \
             -bottom [GeometryFunctions translate3D_point $options(-origin) \
                      [list [expr {$_psPCBwidth - $_stripIncr}] \
                       [expr {$_psPCBlength - ($_stripIncr + 5*2.54)}] \
                       -$_stripThickness]] \
             -radius [expr {$_mhdia / 2.0}] \
             -height [expr {$_stripThickness + $_psPCBThickness}] \
             -color {255 255 255}
    }
    method print {{fp stdout}} {
        $board print $fp
        foreach s $strips {
            $s print $fp
        }
        $mh1 print $fp
        $mh2 print $fp
        $mh3 print $fp
        $mh4 print $fp
    }
    method MountingHoleBottom {i {z 0}} {
        lassign [[set mh$i] cget -bottom] x y dummy
        return [list $x $y $z]
    }
    method MountingHoleRadius {} {
        return [expr {$_mhdia / 2.0}]
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
    method Standoff {name i baseZ height diameter color} {
        lassign [[set mh$i] cget -bottom] x y z
        set bottom [list $x $y $baseZ]
        return [Cylinder create $name \
                -bottom $bottom \
                -radius [expr {$diameter / 2.0}] \
                -height $height \
                -color $color]
    }
            
}


snit::type PSOnPCB {
    PSDims
    PCBDims
    TB007_508_xxBE
    Common
    component powersupply;# 490-PSK-S15C-5
    component pcboard;# BPS-MAR-ST6U-001
    component acterm;#490-TB007-508-03BE
    component dcterm;#490-TB006-508-02BE
    component fuseholder;# 02810010H
    component mov;# 871-B72220S2301K101
    component bypasscap;# 80-C333C105K5R  1uf 50V  
    component filtercap;# 661-EGXE160ELL221M
    component esd;# 821-P6KE8V2A  ESD/TVS diode.
    variable wires [list]
    typevariable _fuseholderX [expr {76.2-6.35}]
    typevariable _fuseholderY [expr {45.72-25.40}]
    typevariable _bypassX 27.94;#[expr {76.2-27.94}]
    typevariable _bypassY [expr {45.72-15.24}]
    typevariable _filterX 5.08;#[expr {76.2-5.08}]
    typevariable _filterY [expr {45.72-27.94}]
    typevariable _esdX 17.78;#[expr {76.2-17.78}]
    typevariable _esdY [expr {45.72-17.78}]
    typevariable _wiredia 1.5
    delegate method MountingHole to pcboard
    delegate method MountingHoleBottom to pcboard
    delegate method MountingHoleRadius to pcboard
    delegate method Standoff to pcboard
    constructor {args} {
        $self configurelist $args
        set yoff [expr {($_psPCBlength - $_pslength)/2.0}]
        set xoff [expr {($_psPCBwidth - $_pswidth)/2.0}]
        set psoffset [list $xoff $yoff $_psPCBThickness]
        install powersupply using PSK_S15C %AUTO% \
              -origin [GeometryFunctions translate3D_point $options(-origin) \
                       $psoffset]
        install pcboard using PCBwithStrips %AUTO% \
              -origin $options(-origin)
        install acterm using TB007_508_03BE %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                         $options(-origin) \
                       [list [expr {$_psPCBwidth - $_psactermyoff - [TB007_508_03BE Length]}] [expr {$_psPCBlength - $_pstermxoff - $_termwidth}] $_psPCBThickness]]
        install dcterm using TB007_508_02BE %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list [expr {$_psPCBwidth - $_psdctermyoff - [TB007_508_02BE Length]}] $_pstermxoff $_psPCBThickness]]
        install bypasscap using C333 %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_bypassY $_bypassX 0]]
        install filtercap using AL_CAP_Radial_5mm10x12.5 %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_filterY $_filterX $_psPCBThickness]]
        install esd using DO_15_bendedLeads_400_under %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_esdY $_esdX 0]]
        install fuseholder using Littlefuse_FuseHolder_02810007H_02810010H %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list $_fuseholderY $_fuseholderX $_psPCBThickness]]
        install mov using B72220S2301K101 %AUTO% \
              -origin [GeometryFunctions translate3D_point \
                       $options(-origin) \
                       [list [expr {$_psPCBwidth / 2.0}] \
                        [expr {($_psPCBlength - ($yoff+$_pspin3Xoff+3) + 3.81)}] 0]]
        set groundj1X [expr {($_psPCBlength / 2.0)+1.27}]
        set groundj1Y [expr {($_pspin1Yoff)+$yoff}]
        set groundj1L [expr {20.32+5.08}]
        set wireradius [expr {$_wiredia / 2.0}]
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $groundj1Y $groundj1X -$wireradius]] \
                       -radius $wireradius \
                       -direction X \
                       -height -$groundj1L \
                       -color {0 255 0}]
        for {set i 1} {$i <= 3} {incr i} {
            set yy [expr {$i * 2.54}]
            set xx [expr {($i & 1) * 2.54}]
            set y1 [expr {$groundj1Y + $yy}]
            set y2 [expr {$groundj1Y-$groundj1L-$yy}]
            set x  [expr {$groundj1X - $xx}]
            lappend wires [Cylinder create %AUTO% \
                           -bottom [GeometryFunctions translate3D_point \
                                    $options(-origin) \
                                    [list $y1 $x -$wireradius]] \
                           -radius $wireradius \
                           -direction X \
                           -height -2.54 \
                           -color {0 255 0}]
            lappend wires [Cylinder create %AUTO% \
                           -bottom [GeometryFunctions translate3D_point \
                                    $options(-origin) \
                                    [list $y2 $x -$wireradius]] \
                           -radius $wireradius \
                           -direction X \
                           -height  2.54 \
                           -color {0 255 0}]
        }
        set l1Y [expr {$_psactermyoff + (7*2.54)}]
        set l1X [expr {$_psPCBlength-(5.08 + 2.54)}]
        set l1L 5.08
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $l1Y $l1X -$wireradius]] \
                       -radius $wireradius \
                       -direction X \
                       -height $l1L \
                       -color {0 0 0}]
        set l2Y [expr {$l1Y - 5.08 - 5.08}]
        set l2X [expr {$_psPCBlength-5.08}]
        set l2L 5.08
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $l2Y $l2X -$wireradius]] \
                       -radius $wireradius \
                       -direction X \
                       -height $l2L \
                       -color {0 0 0}]
        set M1Y [expr {$_psdctermyoff + (5*2.54)}]
        set M1X [expr {$_pstermxoff + ($_termwidth/2.0) + 2.54}]
        set M1L 5.08
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $M1Y $M1X -$wireradius]] \
                       -radius $wireradius \
                       -direction X \
                       -height $M1L \
                       -color {0 0 0}]
        set M2Y [expr {$M1Y - $M1L - 2.54}]
        set M2X [expr {$M1X + 2.54}]
        set M2L 7.62
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $M2Y $M2X -$wireradius]] \
                       -radius $wireradius \
                       -direction X \
                       -height $M2L \
                       -color {0 0 0}]
        set P1Y [expr {$_psdctermyoff + 5.08 + 5.08}]
        set P1X [expr {$M2X + 2.54}]
        set P1L [expr {2.54*5}]
        lappend wires [Cylinder create %AUTO% \
                       -bottom [GeometryFunctions translate3D_point \
                                $options(-origin) \
                                [list $P1Y $P1X -$wireradius]] \
                       -radius $wireradius \
                       -direction X \
                       -height $P1L \
                       -color {255 0 0}]
        
        
    }
    method print {{fp stdout}} {
        $powersupply print $fp
        $pcboard print $fp
        $acterm print $fp
        $dcterm print $fp
        $bypasscap print $fp
        $filtercap print $fp
        $esd print $fp
        $fuseholder print $fp
        $mov print $fp
        foreach w $wires {
            $w print $fp
        }
    }
}


package provide PSPCB 1.0
