#!/bin/sh
# file: build.sh
# vim:fileencoding=utf-8:ft=sh
# Build file for example graphic
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-09-28 20:53:19 +0200
# Last modified: 2024-07-23T01:09:32+0200

env PYTHONPATH=../src python3 ex1.py >ex1.tex
env PYTHONPATH=../src python3 ex2.py >ex2.tex
pdflatex -interaction batchmode >/dev/null example1.tex
pdflatex -interaction batchmode >/dev/null example2.tex
convert -density 600 -units PixelsPerInch example1.pdf -background white -alpha remove -resize 50% ex1.png
convert -density 600 -units PixelsPerInch example2.pdf -background white -alpha remove -resize 50% ex2.png
rm -rf example?.log example?.aux example?.pdf __pycache__ ex?.tex
