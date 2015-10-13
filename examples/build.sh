#!/bin/sh
# file: build.sh
# vim:fileencoding=utf-8:ft=sh
# Build file for example graphic
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-09-28 20:53:19 +0200
# Last modified: 2015-10-13 21:16:57 +0200

cp ../texcalc.py .
python3 ex1.py >ex1.tex
pdflatex -interaction batchmode >/dev/null driver.tex
convert -density 600 -units PixelsPerInch driver.pdf \
 -crop 2690x1640+1084+1040 -resize 50% ex1.png
rm -rf texcalc.py driver.log driver.aux driver.pdf __pycache__
