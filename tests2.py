#!/usr/bin/env python
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

from calculate import expression

expression('D', '3', 'mm')
expression('A', 'pi/4*D**2', 'mm^2')
expression('s', 'sin(0.2*pi)')
