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
ca.variable('sgv', 1.76, 'g/cm^3', texname=r'\rho_v')
ca.variable('Ev', 240000, 'MPa', texname=r'E_v')
print(r'Gegevens van de hars:\\')
ca.variable('sgh', 1.15, 'g/cm^3', texname=r'\rho_h')
ca.variable('Eh', 3000, 'MPa', texname=r'E_h')
print(r'Gegevens van de Divinycell H80 kern:\\')
ca.variable('Ek', 92, 'MPa', texname=r'E_k')
ca.variable('Gk', 29, 'MPa', texname=r'G_h')
ca.variable('h', 30, 'mm')
print(r'Gegevens van het laminaat:\\')
ca.variable('vf', 0.5, None, texname=r'v_f')
ca.equation('vm', '1-vf', None, texname=r'v_m', texexpr=None)
ca.equation('Elam', 'Ev*vf+Eh*(1-vf)', 'MPa',
            texname=r'E_{lam}', texexpr='E_v\cdot f+E_h\cdot(1-v_f)')
ca.variable('n', 5, None)
ca.variable('opp_gew', 300, 'g/m^2', texname='g_o')
ca.equation('opp_gew', 'n*opp_gew/10000', 'g/cm^2', fmt='.2f',
            texname='g_o', texexpr=r'n\cdot\frac{g_o}{10000}')
ca.equation('tv', 'opp_gew/sgv*10', 'mm', fmt='.2f', texname=r't_v',
            texexpr=r'\frac{g_o}{\rho_v}\cdot 10')
ca.equation('t', 'tv*(1+vm/vf)', 'mm', fmt='.2f',
            texexpr=r't_v\cdot(1+\frac{v_m}{v_f})')
print(r'Gegevens van de sandwich:\\')
ca.equation('H', 'h+2*t', 'mm', fmt='.1f', texexpr=r'h+2\cdot t')
ca.equation('e', 'H/2', 'mm', fmt='.1f', texexpr=r'\frac{H}{2}')
ca.variable('L', 1200, 'mm')
ca.variable('B', 400, 'mm')
print(r'Gegevens van de belasting:\\')
ca.variable('F', 6500, 'N')
print(r'Eigenschappen van de sandwich:\\')
ca.equation('M', 'F*L', 'N.mm', fmt='.3g', texexpr=r'F\cdot L')
ca.equation('I', 'B*(H**3-h**3)/12', 'mm^4', fmt='.4g',
            texexpr=r'\frac{B\cdot(H^3-h^3)}{12}')
ca.equation('EI', 'Elam*I', 'N.mm^2', fmt='.4g', texexpr=r'Elam\cdot I')
ca.equation('GA', 'Gk*B*h', 'N', fmt='.4g', texexpr=r'G\cdot B\cdot h')
ca.equation('fb', 'F*L**3/(3*EI)', 'mm', fmt='.1f', texname=r'f_b',
            texexpr=r'\frac{F\cdot L^3}{3\cdot EI}')
ca.equation('fa', '1.5*F*L/GA', 'mm', fmt='.1f', texname=r'f_a',
            texexpr=r'\frac{1.5\cdot F\cdot L}{GA}')
ca.equation('f', 'fb + fa', 'mm', fmt='.1f')
ca.equation('s', 'M*e/I', 'MPa', fmt='.0f', texname=r'\sigma',
            texexpr=r'\frac{M\cdot e}{I}')
ca.equation('smax', '0.5*(Elam*Ek*Gk)**(1/3)', 'MPa', fmt='.0f',
            texname=r'\overline\sigma',
            texexpr=r'0.5\cdot(Elam\cdot Ek\cdot Gk)^{\frac{1}{3}}')
