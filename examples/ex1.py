#!/usr/bin/env python3
# vim:fileencoding=utf-8
# file: ex1.py
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2014-07-06 22:53:36 +0200
# Last modified: 2015-09-28 21:46:00 +0200
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to tests1.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

from texcalc import Calculation

c = Calculation()
c.add('rho_f', '1.62', 'g/cm^3', 'Fiber density')
c.add('rho_r', '1.2', 'g/cm^3', "Resin density")
c.add('v_f', '0.3', '-', 'Fiber volume fraction')
c.add('W_f', '450', 'g/m^2', "Area weight fibers", fmt=".0f")
c.add('t_f', 'W_f/(10000*rho_f)*10', 'mm')
c.add('t', 't_f/v_f', 'mm', "Laminate thickness")
c.add('t_r', 't-t_f', 'mm')
c.add('W_r', 't_f/10*(10000*rho_r)', 'g/m^2', "Area weight resin", fmt=".0f")
print(c)
