#!/usr/bin/env python3
# file: ex2.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2015-05-06T10:41:50+0200
# Last modified: 2020-07-28T16:05:54+0200
"""Texcalc example."""

import texcalc as tc

print("texcalc version:", tc.__version__)
print()

tb = r"""Properties of \SI{0.75}{in} thick sandwich panels:"""
print(tb)
print("")

tc.header()
tc.line("H", "3/4*25.4", "mm", "total thickness", fmt=".1f")
tc.line("t", 0.351, "mm", "total skin thickness", fmt=".2f")
tc.line("h", "H-t", "mm", "core thickness", fmt=".1f")
tc.line("B", 1000, "mm", "width", fmt=".0f")
tc.line("A", "h*B", "mm^2", "core cross section area", fmt=".0f")
tc.line("E", 65820, "N/mm^2", "Young's modulus laminate", fmt=".0f")
tc.line("G", 8.5, "N/mm^2", "shear modulus core", fmt=".1f")
tc.line("I", "(B*(H**3-h**3))/12", "mm^4", "second area moment", fmt=".0f")
tc.line("EI", "E*I", "N.mm^2", "bending stiffness per m width", fmt=".0f")
tc.line("GA", "G*A", "N", "shear stiffness per m width", fmt=".0f")
tc.footer()

print("")

tb = r"""Properties of \SI{0.5}{in} thick sandwich panels:"""
print(tb)
print("")

tc.header()
tc.line("H", "1/2*25.4", "mm", "total thickness", fmt=".1f")
tc.line("t", 0.527, "mm", "total skin thickness", fmt=".2f")
tc.line("h", "H-t", "mm", "core thickness", fmt=".1f")
tc.line("B", 1000, "mm", "width", fmt=".0f")
tc.line("A", "h*B", "mm^2", "core cross section area", fmt=".0f")
tc.line("E", 65680, "N/mm^2", "Young's modulus laminate", fmt=".0f")
tc.line("G", 8.5, "N/mm^2", "shear modulus core", fmt=".1f")
tc.line("I", "(B*(H**3-h**3))/12", "mm^4", "second area moment", fmt=".0f")
tc.line("EI", "E*I", "N.mm^2", "bending stiffness per m width", fmt=".0f")
tc.line("GA", "G*A", "N", "shear stiffness per m width", fmt=".0f")
tc.footer()
