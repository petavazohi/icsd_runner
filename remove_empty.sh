#!/bin/bash
"">empty.txt
for idir in mp-*
do
    if ls ${idir} | grep mp
    then
	echo ""
    else
	echo "${idir}" >> empty.txt
    fi
done
