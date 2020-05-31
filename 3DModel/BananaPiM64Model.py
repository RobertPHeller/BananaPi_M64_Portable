#!/usr/bin/FreeCAD
#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 30 10:49:38 2020
#  Last Modified : <200531.1137>
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

import FreeCAD as App

import Part
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))
from traceback import *

#from M64 import *
from PSPCB import *
#from  PSBox import *
#from  Case import *
#from  DCDC_5_12 import *
#from  LCDMountingBracket import *
#from  LCDScreen import *
#from  HDMIConverter import *
#from  USB_SATA_Adapter import *
#from  SVGOutput import *

if __name__ == '__main__':
    doc = App.newDocument("BananaPiM64Model")
    App.setActiveDocument ( "BananaPiM64Model" )
    board = PSOnPCB("pspcb",Base.Vector(0,0,0)) 
    Gui.SendMsgToActiveView("ViewFit")
    doc.FileName="BananaPiM64Model.fcstd"
    doc.Label="BananaPiM64Model"
    doc.save()
