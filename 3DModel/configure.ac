AC_INIT(BananaPiM64Model,0.0.0,[support@deepsoft.com])
AC_CANONICAL_BUILD
AC_CANONICAL_HOST
AC_SUBST(build)
AC_CANONICAL_TARGET
AC_SUBST(target)
AC_CONFIG_SRCDIR(BananaPiM64Model.tcl)
AM_INIT_AUTOMAKE([-Wno-portability])
AC_CONFIG_MACRO_DIR([m4])
if test "x${prefix}" = "xNONE"; then
    prefix=/usr/local
        fi
            if test "x${exec_prefix}" = "xNONE"; then
                    exec_prefix="${prefix}"
                            fi
                                            
BUILD_DIR=`pwd`
TOP_DIR=${BUILD_DIR}

AC_SUBST(TOP_DIR)
AC_SUBST(BUILD_DIR)

srcdir=`dirname $0`
cd $srcdir
SRC_DIR=`pwd`
cd $BUILD_DIR

AC_SUBST(SRC_DIR)
AC_SUBST(target)

m4_pattern_allow(PKG_)
TEA_INIT([3.5])
TEA_PATH_TCLCONFIG
TEA_LOAD_TCLCONFIG
TEA_PREFIX
TEA_PROG_TCLSH
dnl Check for external Tcl/Tk libraries
AX_SNIT
AX_CMDLINE
AX_CSV
AX_STRUCT
AC_PATH_PROGS(UNZIP,unzip)
AC_PATH_PROGS(SDX,[sdx sdx.kit])
AC_PATH_PROGS(TCLKIT,[tclkit])
AC_CONFIG_FILES([BuildScripts/Makefile Makefile])
AC_OUTPUT
