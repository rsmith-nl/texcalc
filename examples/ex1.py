#!/usr/bin/env python3
# file: ex1.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2014-2015 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2014-07-06T22:53:36+0200
# Last modified: 2020-07-28T16:04:27+0200

import texcalc as tc


print("texcalc version:", tc.__version__)

tc.header()
tc.line("rho_f", "1.62", "g/cm^3", "Fiber density")
tc.line("rho_r", "1.2", "g/cm^3", "Resin density")
tc.line("v_f", "0.3", "-", "Fiber volume fraction")
tc.line("W_f", "450", "g/m^2", "Area weight fibers", fmt=".0f")
tc.line("t_f", "W_f/(10000*rho_f)*10", "mm")
tc.line("t", "t_f/v_f", "mm", "Laminate thickness")
tc.line("t_r", "t-t_f", "mm")
tc.line("W_r", "t_f/10*(10000*rho_r)", "g/m^2", "Area weight resin", fmt=".0f")
tc.line(None, "W_f+W_r", "g/m^2", "Total area weight", fmt=".0f")
tc.footer()
