#!/usr/bin/env python3
# file: ex2.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2015-05-06T10:41:50+0200
# Last modified: 2018-04-17T21:31:56+0200
"""Texcalc example."""

from texcalc import Calculation


tb = r"""Properties of \SI{0.75}{in} thick sandwich panels:"""
print(tb)
print('')

c = Calculation()
c.add('H', '3/4*25.4', 'mm', 'total thickness', fmt='.1f')
c.add('t', 0.351, 'mm', 'total skin thickness', fmt='.2f')
c.add('h', 'H-t', 'mm', 'core thickness', fmt='.1f')
c.add('B', 1000, 'mm', 'width', fmt='.0f')
c.add('A', 'h*B', 'mm^2', 'core cross section area', fmt='.0f')
c.add('E', 65820, 'N/mm^2', "Young's modulus laminate", fmt='.0f')
c.add('G', 8.5, 'N/mm^2', "shear modulus core", fmt='.1f')
c.add('I', '(B*(H**3-h**3))/12', 'mm^4', "second area moment", fmt='.0f')
c.add('EI', 'E*I', 'N.mm^2', "bending stiffness per m width", fmt='.0f')
c.add('GA', 'G*A', 'N', "shear stiffness per m width", fmt='.0f')

print(c)
print('')

tb = r"""Properties of \SI{0.5}{in} thick sandwich panels:"""
print(tb)
print('')

d = Calculation()
d.add('H', '1/2*25.4', 'mm', 'total thickness', fmt='.1f')
d.add('t', 0.527, 'mm', 'total skin thickness', fmt='.2f')
d.add('h', 'H-t', 'mm', 'core thickness', fmt='.1f')
d.add('B', 1000, 'mm', 'width', fmt='.0f')
d.add('A', 'h*B', 'mm^2', 'core cross section area', fmt='.0f')
d.add('E', 65680, 'N/mm^2', "Young's modulus laminate", fmt='.0f')
d.add('G', 8.5, 'N/mm^2', "shear modulus core", fmt='.1f')
d.add('I', '(B*(H**3-h**3))/12', 'mm^4', "second area moment", fmt='.0f')
d.add('EI', 'E*I', 'N.mm^2', "bending stiffness per m width", fmt='.0f')
d.add('GA', 'G*A', 'N', "shear stiffness per m width", fmt='.0f')
print(d)
print('')
