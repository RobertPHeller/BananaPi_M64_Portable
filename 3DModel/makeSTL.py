#!/usr/bin/FreeCADCmd
#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun Jun 21 09:46:08 2020
#  Last Modified : <200621.1016>
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
import sys

if __name__ == '__main__':
    App.open("BananaPiM64Model.fcstd")
    doc = App.getDocument('BananaPiM64Model')
    App.ActiveDocument=doc
    cradle = doc.M64Case_bottom_cradle
    cradle.Shape.exportStl("BananaPiM64Model_cradle.stl")
    buttonplunger = doc.M64Case_keyboardshelf_teensythumbstick_left
    buttonplunger.Shape.exportStl("BananaPiM64Model_buttonplunger.stl")
    sys.exit(0)
