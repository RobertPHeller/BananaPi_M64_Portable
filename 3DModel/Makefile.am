##-*- makefile -*-############################################################
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sat May 9 08:36:05 2020
#  Last Modified : <200515.0846>
#
#  Description	
#
#  Notes
#
#  History
#	
#  $Log$
#
##############################################################################
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
##############################################################################


ACLOCAL_AMFLAGS = -I m4
SUBDIRS = BuildScripts
EXTRA_DIST = bootstrap BananaPiM64Model.tcl

bin_SCRIPTS = BananaPiM64Model.kit

AddKitDir = $(top_srcdir)/BuildScripts/AddKitDir.kit
AddKitFile = $(top_srcdir)/BuildScripts/AddKitFile.kit
MakePkgIndex = $(top_srcdir)/BuildScripts/MakePkgIndex.kit

BananaPiM64ModelLibScripts = Common.tcl M64.tcl PSBox.tcl Case.tcl \
	PowerSupply.tcl Diode.tcl MOV.tcl TerminalBlocks.tcl \
	FuseHolder.tcl PSPCB.tcl Electromech.tcl Capacitors.tcl \
	DCDC-5-12.tcl LCDMountingBracket.tcl LCDScreen.tcl

EXTRA_DIST += $(BananaPiM64ModelLibScripts)

BananaPiM64Model.kit : BananaPiM64Model.tcl $(BananaPiM64ModelLibScripts) \
			COPYING
	-rm -rf BananaPiM64Model.vfs BananaPiM64Model.kit
	$(TCLKIT) $(SDX) qwrap $(srcdir)/BananaPiM64Model.tcl
	$(TCLKIT) $(SDX) unwrap BananaPiM64Model.kit
	-rm -rf BananaPiM64Model.kit
	$(TCLKIT) $(AddKitDir) BananaPiM64Model lib $(SNITLIB)
	$(TCLKIT) $(AddKitDir) BananaPiM64Model lib $(CSVLIB)
	$(TCLKIT) $(AddKitDir) BananaPiM64Model lib $(CMDLINELIB)
	$(TCLKIT) $(AddKitDir) BananaPiM64Model lib $(STRUCTLIB)
	$(TCLKIT) $(AddKitFile) -srcdir $(srcdir) BananaPiM64Model  \
		lib/Scripts $(BananaPiM64ModelLibScripts)
	$(TCLKIT) $(MakePkgIndex) BananaPiM64Model Scripts
	$(TCLKIT) $(AddKitFile) BananaPiM64Model Copyright COPYING
	$(TCLKIT) $(SDX) wrap BananaPiM64Model.kit
	-rm -rf BananaPiM64Model.vfs
	

clean-local:
	-rm -rf BananaPiM64Model.vfs
	        
