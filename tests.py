# file: tests.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2015-2016 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2015-09-27T15:48:12+0200
# Last modified: 2018-04-17T21:30:28+0200
"""Nose tests for texcalc."""

from texcalc import _LatexVisitor
import ast


def runvisitor(exptxt, result):
    """Parse the expression, convert to LaTeX and compare.

    Arguments:
        exptxt: The expression as a string.
        result: The expected LaTeX formatted string.
    """
    exp = ast.parse(exptxt)
    v = _LatexVisitor()
    v.visit(exp)
    print("DEBUG: v.astex() = ", v.astex())
    assert result == v.astex()


def test_simple():
    """Test simple expressions."""
    runvisitor('1 + 2', '1+2')
    runvisitor('1 - 2', '1-2')
    runvisitor('1*2', '1\cdot 2')
    runvisitor('1/2', r'\frac{1}{2}')


def test_prec():
    """Tests involving operator precedence."""
    runvisitor('1/2+3', r'\frac{1}{2}+3')
    runvisitor('1/(2+3)', r'\frac{1}{2+3}')
    runvisitor('(2+3)/21', r'\frac{2+3}{21}')
    runvisitor('2**(3+2)', r'2^{3+2}')
    runvisitor('2**(3+2/7)', r'2^{3+\frac{2}{7}}')
    runvisitor('(2+7)*5', r'{\left(2+7\right)}\cdot 5')
    runvisitor('54**((2+7)*5)', r'54^{{\left(2+7\right)}\cdot 5}')


def test_builtins():
    """Text the handling of built-in functions."""
    runvisitor('sin(45)/2', r'\frac{\sin(45)}{2}')
    runvisitor('atan(7)', r'\arctan(7)')
    runvisitor('log10(74)**2', r'\log(74)^2')


def test_greek():
    """Text the handling of Greek letters."""
    runvisitor('tau/2', r'\frac{\tau}{2}')
    runvisitor('alpha**2/7+3', r'\frac{\alpha^2}{7}+3')
