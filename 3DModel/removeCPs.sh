#!/bin/bash
out=`echo $1|sed 's/\.svg/-nocps.svg/g'`
grep -v 'M0,42 L0,-42 M42,0 L-42,0' $1 >$out
