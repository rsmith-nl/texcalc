#!/usr/bin/env python
# vim:fileencoding=utf-8
# file: tests1.py
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2014-07-06 22:53:36 +0200
# $Date$
# $Revision$
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to tests1.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

from calculate import expression

expression('rho_f', '1.62', 'g/cm^3')
expression('rho_r', '1.1', 'g/cm^3')
expression('v_f', '0.3')
expression('W_f', '450', 'g/m^2')
expression('t_f', 'W_f/(10000*rho_f)*10', 'mm')
expression('t', 't_f/v_f', 'mm')
expression('t_r', 't-t_f', 'mm')
expression('W_r', 't_f/10*(10000*rho_r)', 'g/m^2')
expression('Q', '(3.24-2)*(12-9)')
expression('W', '(3.24*2)*(12-9)')
