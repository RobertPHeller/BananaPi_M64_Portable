#* 
#* ------------------------------------------------------------------
#* ax_tcl_libraries.m4 - Checks for Tcl Libraries
#* Created by Robert Heller on Sat Mar  2 15:25:28 2013
#* ------------------------------------------------------------------
#* Modification History: $Log: headerfile.text,v $
#* Modification History: Revision 1.1  2002/07/28 14:03:50  heller
#* Modification History: Add it copyright notice headers
#* Modification History:
#* ------------------------------------------------------------------
#* Contents:
#* ------------------------------------------------------------------
#*  
#*     Generic Project
#*     Copyright (C) 2010  Robert Heller D/B/A Deepwoods Software
#* 			51 Locke Hill Road
#* 			Wendell, MA 01379-9728
#* 
#*     This program is free software; you can redistribute it and/or modify
#*     it under the terms of the GNU General Public License as published by
#*     the Free Software Foundation; either version 2 of the License, or
#*     (at your option) any later version.
#* 
#*     This program is distributed in the hope that it will be useful,
#*     but WITHOUT ANY WARRANTY; without even the implied warranty of
#*     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#*     GNU General Public License for more details.
#* 
#*     You should have received a copy of the GNU General Public License
#*     along with this program; if not, write to the Free Software
#*     Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#* 
#*  
#* 

AC_DEFUN([AX_SNIT],[
AC_MSG_CHECKING(snit dir)
searchdirs=`echo 'puts $auto_path'|${TCLSH_PROG}`
for dir in $searchdirs ; do
  dirs="${dir}/snit* ${dir}/tcllib*/snit*"
  for i in $dirs ; do
    if test -d "$i" -a -f "$i/pkgIndex.tcl"; then
      SNITLIB=`cd $i; pwd`
    fi
  done
done
AC_ARG_WITH(snitlib, [  --with-snitlib=DIR          use snit from DIR], SNITLIB=$withval,)
if test x$SNITLIB != x -a -d $SNITLIB; then
   AC_MSG_RESULT([using snit library in $SNITLIB])
else
   AC_MSG_ERROR(Snit library directory not found)
fi
AC_SUBST(SNITLIB)
])

AC_DEFUN([AX_CMDLINE],[
AC_MSG_CHECKING(cmdline dir)
searchdirs=`echo 'puts $auto_path'|${TCLSH_PROG}`
for dir in $searchdirs ; do
  dirs="${dir}/cmdline* ${dir}/tcllib*/cmdline*"
  for i in $dirs ; do
    if test -d "$i" -a -f "$i/pkgIndex.tcl"; then
      CMDLINELIB=`cd $i; pwd`
    fi
  done
done
AC_ARG_WITH(cmdlinelib, [  --with-cmdlinelib=DIR          use cmdline from DIR], CMDLINELIB=$withval,)
if test x$CMDLINELIB != x -a -d $CMDLINELIB; then
   AC_MSG_RESULT([using cmdline library in $CMDLINELIB])
else
   AC_MSG_ERROR(Cmdline library directory not found)
fi
AC_SUBST(CMDLINELIB)
])

AC_DEFUN([AX_CSV],[
AC_MSG_CHECKING(csv dir)
searchdirs=`echo 'puts $auto_path'|${TCLSH_PROG}`
for dir in $searchdirs ; do
  dirs="${dir}/csv* ${dir}/tcllib*/csv*"
  for i in $dirs ; do
    if test -d "$i" -a -f "$i/pkgIndex.tcl"; then
      CSVLIB=`cd $i; pwd`
    fi
  done
done
AC_ARG_WITH(csvlib, [  --with-csvlib=DIR          use csv from DIR], CSVLIB=$withval,)
if test x$CSVLIB != x -a -d $CSVLIB; then
   AC_MSG_RESULT([using csv library in $CSVLIB])
else
   AC_MSG_ERROR(Csv library directory not found)
fi
AC_SUBST(CSVLIB)
])

AC_DEFUN([AX_HTMLPARSE],[
AC_MSG_CHECKING(htmlparse dir)
searchdirs=`echo 'puts $auto_path'|${TCLSH_PROG}`
for dir in $searchdirs ; do
  dirs="${dir}/htmlparse ${dir}/tcllib*/htmlparse"
  for i in $dirs ; do
    if test -d "$i" -a -f "$i/pkgIndex.tcl"; then
      HTMLPARSELIB=`cd $i; pwd`
    fi
  done
done
AC_ARG_WITH(htmlparselib, [  --with-htmlparselib=DIR          use htmlparse from DIR], HTMLPARSELIB=$withval,)
if test x$HTMLPARSELIB != x -a -d $HTMLPARSELIB; then
   AC_MSG_RESULT([using htmlparse library in $HTMLPARSELIB])
else
   AC_MSG_ERROR(Htmlparse library directory not found)
fi
AC_SUBST(HTMLPARSELIB)
])

AC_DEFUN([AX_STRUCT],[
AC_MSG_CHECKING(struct dir)
searchdirs=`echo 'puts $auto_path'|${TCLSH_PROG}`
for dir in $searchdirs ; do
  dirs="${dir}/struct* ${dir}/tcllib*/struct*"
  for i in $dirs ; do
    if test -d "$i" -a -f "$i/pkgIndex.tcl"; then
      STRUCTLIB=`cd $i; pwd`
    fi
  done
done
AC_ARG_WITH(structlib, [  --with-structlib=DIR          use struct from DIR], STRUCTLIB=$withval,)
if test x$STRUCTLIB != x -a -d $STRUCTLIB; then
   AC_MSG_RESULT([using struct library in $STRUCTLIB])
else
   AC_MSG_ERROR(Struct library directory not found)
fi
AC_SUBST(STRUCTLIB)
])
AC_DEFUN([AX_URI],[
AC_MSG_CHECKING(uri dir)
searchdirs=`echo 'puts $auto_path'|${TCLSH_PROG}`
for dir in $searchdirs ; do
  dirs="${dir}/uri* ${dir}/tcllib*/uri*"
  for i in $dirs ; do
    if test -d "$i" -a -f "$i/pkgIndex.tcl"; then
      URILIB=`cd $i; pwd`
    fi
  done
done
AC_ARG_WITH(urilib, [  --with-urilib=DIR          use uri from DIR], URILIB=$withval,)
if test x$URILIB != x -a -d $URILIB; then
   AC_MSG_RESULT([using uri library in $URILIB])
else
   AC_MSG_ERROR(Uri library directory not found)
fi
AC_SUBST(URILIB)
])

                          


