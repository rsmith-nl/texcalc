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

__version__ = '$Revision$'[11:-2]


def expression(name, expr, unit='', fmt=":.2f"):
    """@todo: Docstring for expression

    :param name: @todo
    :param expr: @todo
    :param unit: @todo
    :returns: @todo
    """
    value = eval(expr)
    exec('{} = {}'.format(name, value), globals())
    n = ast.parse(expr)
    if type(n.body[0].value).__name__ == 'Num':
        el = ['${}$'.format(name), '=']
        val = ''.join(['\SI{{{', fmt, '}}}', '{{', unit, '}}'])
        el.append(val.format(value))
    else:
        v = LatexVisitor()
        v.visit(n)
        el = ['${} = {}$'.format(name, v.astex()), '=']
        val = ''.join(['\SI{{{', fmt, '}}}', '{{', unit, '}}'])
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
        if type(node.op).__name__ == 'Div':
            self.txtexpr.append(r'\frac{')
            self.visit(node.left)
            self.txtexpr.append(r'}{')
            self.visit(node.right)
            self.txtexpr.append(r'}')
            return
        self.visit(node.left)
        self.visit(node.op)
        self.visit(node.right)

    def visit_Name(self, node):
        if node.id in LatexVisitor._fnames:
            self.txtexpr.append(LatexVisitor._fnames[node.id])
        else:
            self.txtexpr.append(node.id)

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

# Tests
if __name__ == '__main__':
    from math import sin, pi
    sin(pi)
    expression('rho_f', '1.62', 'g/cm^3')
    expression('rho_r', '1.1', 'g/cm^3')
    expression('v_f', '0.3')
    expression('W_f', '450', 'g/m^2')
    expression('t_f', 'W_f/(10000*rho_f)*10', 'mm')
    expression('t', 't_f/v_f', 'mm')
    expression('t_r', 't-t_f', 'mm')
    expression('W_r', 't_f/10*(10000*rho_r)', 'g/m^2')
    expression('D', '3', 'mm')
    expression('A', 'pi/4*D**2', 'mm^2')
    expression('s', 'sin(0.2*pi)')
