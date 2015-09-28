#!/bin/sh
# file: build.sh
# vim:fileencoding=utf-8:ft=sh
# Build file for example graphic
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-09-28 20:53:19 +0200
# Last modified: 2015-09-28 21:22:32 +0200

cp ../texcalc.py .
python3 ex1.py >ex1.tex
pdflatex -interaction batchmode >/dev/null driver.tex
convert -density 600 -units PixelsPerInch driver.pdf \
 -crop 2666x1460+1084+1040 -resize 50% example.png
rm ex1.tex texcalc.py driver.log driver.aux driver.pdf
