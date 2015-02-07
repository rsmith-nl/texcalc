#!/usr/bin/env python3
# vim:fileencoding=utf-8
# file: tests2.py
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2014-07-06 22:55:28 +0200
# $Date$
# $Revision$
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to tests2.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

from __future__ import division, print_function
from texcalc import Calculation

c = Calculation()
c.add('D', 3, 'mm')
c.add('A', 'pi/4*D**2', 'mm^2')
c.add('s', 'sin(0.2*pi)')
c.add('k', 'log10(e)')
c.add('sigma_max', '0.5*(D*A*k)**(1/3)')
c.add('som', '7 + -2')
print(c)
