#!/bin/bash

for x in *.svg; do 
	inkscape -z -e $(echo $x | sed s/svg/png/g) -h 50 $x; 
done
