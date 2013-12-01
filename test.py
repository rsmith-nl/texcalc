# /usr/bin/env python
# vim:fileencoding=utf-8
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2013-12-01 20:35:45 +0100
# Modified: $Date$
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to sandwich3.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Berekeningen van een sandwich"""

from __future__ import division, print_function
import calculate as ca

print(r'Gegevens van de koolstofvezel:\\')
ca.variable('sgv', 1.76, 'g/cm^3')
ca.variable('Ev', 240000, 'MPa')
print(r'Gegevens van de hars:\\')
ca.variable('sgh', 1.15, 'g/cm^3')
ca.variable('Eh', 3000, 'MPa')
print(r'Gegevens van de Divinycell H80 kern:\\')
ca.variable('Ek', 92, 'MPa')
ca.variable('Gk', 29, 'MPa')
ca.variable('h', 30, 'mm')
print(r'Gegevens van het laminaat:\\')
ca.variable('vf', 0.5, None)
ca.equation('vm', '1-vf', None, texexpr=None)
ca.equation('Elam', 'Ev*vf+Eh*(1-vf)', 'MPa',
            texexpr='$Ev\cdot f+Eh\cdot(1-vf)$')
ca.variable('lagen', 5, None)
ca.variable('opp_gew', 300, 'g/m^2')
ca.equation('opp_gew', 'lagen*opp_gew/10000', 'g/cm^2',
            r'$lagen\cdot\frac{opp_gew}{10000}$')
ca.equation('tv', 'opp_gew/sgv*10', 'mm', r'$\frac{opp_gew}{sgv}\cdot 10$')
ca.equation('t', 'tv*(1+vm/vf)', 'mm', r'$tv\cdot(1+\frac{vm}{vf})$')
print(r'Gegevens van de sandwich:\\')
ca.equation('H', 'h+2*t', 'mm', r'$h+2\cdot t$')
ca.equation('e', 'H/2', 'mm', r'$\frac{H}{2}$')
ca.variable('L', 1200, 'mm')
ca.variable('B', 400, 'mm')
print(r'Gegevens van de belasting:\\')
ca.variable('F', 6700, 'N')
print(r'Eigenschappen van de sandwich:\\')
ca.equation('M', 'F*L', 'N.mm', r'$F\cdot L$')
ca.equation('I', 'B*(H**3-h**3)/12', 'mm^4', r'$\frac{B\cdot(H^3-h^3)}{12}$')
ca.equation('EI', 'Elam*I', 'N.mm^2', r'$Elam\cdot I$')
ca.equation('GA', 'Gk*B*h', 'N', r'$G\cdot B\cdot h$')
ca.equation('fb', 'F*L**3/(3*EI)', 'mm', r'$\frac{F\cdot L^3}{3\cdot EI}$')
ca.equation('fa', '1.5*F*L/GA', 'mm', r'$\frac{1.5\cdot F\cdot L}{GA}$')
ca.equation('f', 'fb + fa', 'mm', texexpr=None)
ca.equation('s', 'M*e/I', 'MPa', r'$\frac{M\cdot e}{I}$')
ca.equation('smax', '0.5*(Elam*Ek*Gk)**(1/3)', 'MPa',
            r'$0.5\cdot(Elam\cdot Ek\cdot Gk)^{\frac{1}{3}}$')
