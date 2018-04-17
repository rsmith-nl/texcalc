#!/usr/bin/env python3
# file: ex1.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2014-2015 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2014-07-06T22:53:36+0200
# Last modified: 2018-04-17T21:31:26+0200

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
