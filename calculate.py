# /usr/bin/env python3
# vim:fileencoding=utf-8
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2013-12-01 11:03:52 +0100
# Modified: $Date$
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to calculate.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Module to do and print calculations. Prints formatted statements.
Note that this module uses exec(). It should therefore not be used with
untrusted input."""

from __future__ import division, print_function

__version__ = '$Revision$'[11:-2]


def variable(name, value, unit, fmt=None, texname=None, plaintext=False):
    """Define a variable and print its value.

    :param name: Name of the global variable to define
    :param value: Value of the variable. Will be converted to float internally.
    :param unit: Unit of the variable or None if dimensionless.
    :param fmt: Format for the result.
    :param texname: TeX formatted version of the variable name.
    :param plaintext: Use plaintext output. Default is False; output LaTeX.
    """
    cmd = ' '.join([name, '=', 'float({})'.format(value)])
    exec(cmd, globals())
    if fmt is None:
        fmt = 'g'
    if plaintext:
        if unit is not None:
            print('{n} = {v:{f}} {u}'.format(n=name, v=value, f=fmt, u=unit))
        else:
            print('{n} = {v:{f}}'.format(n=name, v=value, f=fmt))
    else:
        if texname is not None:
            name = texname
        if unit is not None:
            outs = ''.join(['${}$ = '.format(name), r'\SI{',
                            '{v:{f}}'.format(v=value, f=fmt),
                            r'}{', unit, r'}\\'])
        else:
            outs = ''.join(['${}$ = '.format(name), r'\num{',
                            '{v:{f}}'.format(v=value, f=fmt),
                            r'}\\'])
        print(outs)


def equation(name, expr, unit, fmt=None, texname=None, texexpr=None,
             plaintext=False):
    """Print an equation and its resulting value.

    :param name: Name of the global result variable to define
    :param expr: The expression to evaluate
    :param unit: Unit of the result or None if dimensionless.
    :param fmt: Format for the result.
    :param texname: TeX formatted version of the variable name.
    :param texexpr: TeX formatted version of the expression.
    :param plaintext: Use plaintext output. Default is False; output LaTeX.
    """
    cmd = ' '.join([name, '=', expr])
    exec(cmd, globals())
    if fmt is None:
        fmt = 'g'
    if plaintext:
        if unit is not None:
            print('{n} = {e} = {v:{f}} {u}'.format(n=name, e=expr,
                                                   v=eval(name),
                                                   f=fmt, u=unit))
        else:
            print('{n} = {e} = {v:{f}}'.format(n=name, e=expr, v=eval(name),
                                               f=fmt))
    else:
        if texexpr is None:
            texexpr = expr
        if texname is None:
            texname = name
        if unit is not None:
            outs = ''.join(['${}$ = '.format(texname), texexpr, r' = \SI{',
                            '{v:{f}}'.format(v=eval(name), f=fmt),
                            r'}{', unit, r'}\\'])
        else:
            outs = ''.join(['${}$ = '.format(texname), texexpr, r' = \num{',
                            '{v:{f}}'.format(v=eval(name), f=fmt), r'}\\'])
        print(outs)
