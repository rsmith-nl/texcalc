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


def expression(name, expr, unit=''):
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
        print('${}$ = \SI{{{}}}{{{}}}'.format(name, value, unit))
    else:
        v = LatexVisitor()
        v.visit(n)
        print('${} = {}$ = \SI{{{}}}{{{}}}'.format(name, v.astex(),
                                                   value, unit))


class LatexVisitor(ast.NodeVisitor):
    """ example recursive visitor """

    def __init__(self):
        """@todo: to be defined """
        self.texexpr = []
        self.target = None
        ast.NodeVisitor.__init__(self)

    def astex(self):
        """Return a TeX mathematical expression
        """
        return ''.join(self.texexpr)

    def visit_Module(self, node):
        """ visit a Module node recursively"""
        self.visit(node.body[0])

    def visit_Expr(self, node):
        """ visit a Module node recursively"""
        self.visit(node.value)

    def visit_BinOp(self, node):
        """ visit a BinOp node"""
        if type(node.op).__name__ == 'Div':
            self.texexpr.append(r'\frac{')
            self.visit(node.left)
            self.texexpr.append(r'}{')
            self.visit(node.right)
            self.texexpr.append(r'}')
            return
        self.visit(node.left)
        self.visit(node.op)
        self.visit(node.right)

    def generic_visit(self, node):
        pass

    def visit_Name(self, node):
        """@todo: Docstring for visit_

        :param node: @todo
        :returns: @todo
        """
        self.texexpr.append(node.id)

    def visit_Num(self, node):
        """@todo: Docstring for visit_Num

        :param node: @todo
        :returns: @todo
        """
        self.texexpr.append(str(node.n))

    def visit_Add(self, node):
        self.texexpr.append('+')

    def visit_Sub(self, node):
        self.texexpr.append('-')

    def visit_Mult(self, node):
        self.texexpr.append(r'\cdot ')

    def visit_Pow(self, node):
        self.texexpr.append('^')

    def visit_Div(self, node):
        pass

# Tests
if __name__ == '__main__':
    expression('rho_f', '1.62', 'g/cm^3')
    expression('rho_r', '1.1', 'g/cm^3')
    expression('v_f', '0.3')
    expression('W_f', '450', 'g/m^2')
    expression('t_f', 'W_f/(10000*rho_f)*10', 'mm')
    expression('t', 't_f/v_f', 'mm')
    expression('t_r', 't-t_f', 'mm')
    expression('W_r', 't_f/10*(10000*rho_r)', 'g/m^2')
