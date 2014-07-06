# vim:fileencoding=utf-8
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2014-05-04 11:28:35 +0200
# Modified: $Date$
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to calculate.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Module to do and print calculations. Prints formatted statements.
Note that this module uses exec(). It should therefore not be used with
untrusted input."""

from __future__ import division, print_function
import ast

# To make expressions more TeX-like, we make all the math functions available.
from math import *

__version__ = '$Revision$'[11:-2]


def expression(name, expr, unit=None, fmt=":.2f"):
    """@todo: Docstring for expression

    :param name: Name of the variable to be assigned.
    :param expr: Expression whose value is assigned to the variable
    :param unit: Unit of the variable. Defaults to empty.
    :param fmt:  Format of the result. Defaults to ":.2f".
    :returns: @todo
    """
    value = eval(expr)
    exec('{} = {}'.format(name, value), globals())
    n = ast.parse(expr)
    if type(n.body[0].value).__name__ == 'Num':
        el = ['${}$'.format(name), '=']
    else:
        v = LatexVisitor()
        v.visit(n)
        el = ['${} = {}$'.format(name, v.astex()), '=']
    if unit:
        val = ''.join(['\\SI{{{', fmt, '}}}', '{{', unit, '}}'])
    else:
        val = ''.join(['\\num{{{', fmt, '}}}'])
    el.append(val.format(value))
    print(' '.join(el))


class LatexVisitor(ast.NodeVisitor):
    """ example recursive visitor """

    _fnames = {'sin': '\\sin', 'cos': '\\cos', 'tan': '\\tan',
               'asin': '\\arcsin', 'acos': '\\arccos', 'atan': '\\arctan',
               'sqrt': '\\sqrt', 'log': '\\ln', 'log10': '\\log',
               'pi': '\\pi'}

    def __init__(self):
        """@todo: to be defined """
        self.txtexpr = []
        self.target = None
        ast.NodeVisitor.__init__(self)

    def astex(self):
        """Return a TeX mathematical expression
        """
        return ''.join(self.txtexpr)

    def generic_visit(self, node):
        pass

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Div):
            self.txtexpr.append(r'\frac{')
            self.visit(node.left)
            self.txtexpr.append(r'}{')
            self.visit(node.right)
            self.txtexpr.append(r'}')
            return
        if (isinstance(node.left, ast.BinOp) and
           type(node.left.op).__name__ in ['Add', 'Sub']):
            self.txtexpr.append(r'\left(')
            self.visit(node.left)
            self.txtexpr.append(r'\right)')
        else:
            self.visit(node.left)
        self.visit(node.op)
        if (isinstance(node.right, ast.BinOp) and
           type(node.right.op).__name__ in ['Add', 'Sub']):
            self.txtexpr.append(r'\left(')
            self.visit(node.right)
            self.txtexpr.append(r'\right)')
        else:
            self.visit(node.right)

    def visit_Name(self, node):
        if node.id in LatexVisitor._fnames:
            self.txtexpr.append(LatexVisitor._fnames[node.id])
        else:
            self.txtexpr.append(node.id)

    def visit_Attribute(self, node):
        if node.attr in LatexVisitor._fnames:
            self.txtexpr.append(LatexVisitor._fnames[node.attr])
        else:
            self.txtexpr.append(node.attr)

    def visit_Num(self, node):
        self.txtexpr.append(str(node.n))

    def visit_Add(self, node):
        self.txtexpr.append('+')

    def visit_Sub(self, node):
        self.txtexpr.append('-')

    def visit_Mult(self, node):
        self.txtexpr.append(r'\cdot ')

    def visit_Pow(self, node):
        self.txtexpr.append('^')

    def visit_Call(self, node):
        self.visit(node.func)
        self.txtexpr.append('(')
        for a in node.args:
            self.visit(a)
        self.txtexpr.append(')')

    def visit_Div(self, node):
        pass
