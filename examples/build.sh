#!/bin/sh
# file: build.sh
# vim:fileencoding=utf-8:ft=sh
# Build file for example graphic
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-09-28 20:53:19 +0200
# Last modified: 2020-07-28T16:01:50+0200

env PYTHONPATH=.. python3 ex1.py >ex1.tex
env PYTHONPATH=.. python3 ex2.py >ex2.tex
pdflatex -interaction batchmode >/dev/null driver1.tex
pdflatex -interaction batchmode >/dev/null driver2.tex
convert -density 600 -units PixelsPerInch driver1.pdf -resize 50% ex1.png
convert -density 600 -units PixelsPerInch driver2.pdf -resize 50% ex2.png
rm -rf driver?.log driver?.aux driver?.pdf __pycache__ ex?.tex
