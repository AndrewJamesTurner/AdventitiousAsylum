#!/bin/bash

for x in *.svg; do 
	inkscape -z -e trout.png -w 1024 trout.svg; 
done
