# vim:fileencoding=utf-8
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2014-05-04 11:28:35 +0200
# Modified: $Date$
#
# To the extent possible under law, R.F. Smith has waived all copyright and
# related or neighboring rights to texcalc.py. This work is published
# from the Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Module to do and print calculations. Prints formatted statements.
Note that this module uses exec(). It should therefore not be used with
untrusted input."""

from __future__ import division, print_function
import ast

# To make expressions more TeX-like, we make all the math functions available.
import math

__version__ = '$Revision$'[11:-2]

_greek = {'tau': '\\tau', 'xi': '\\xi', 'Chi': '\\Chi', 'alpha': '\\alpha',
          'Theta': '\\Theta', 'zeta': '\\zeta', 'Pi': '\\Pi', 'Iota':
          '\\Iota', 'Phi': '\\Phi', 'Psi': '\\Psi', 'Sigma': '\\Sigma', 'chi':
          '\\chi', 'Omicron': '\\Omicron', 'Nu': '\\Nu', 'Beta': '\\Beta',
          'Rho': '\\Rho', 'Delta': '\\Delta', 'theta': '\\theta', 'pi':
          '\\pi', 'Omega': '\\Omega', 'nu': '\\nu', 'phi': '\\phi', 'psi':
          '\\psi', 'Kappa': '\\Kappa', 'Upsilon': '\\Upsilon', 'epsilon':
          '\\epsilon', 'omicron': '\\omicron', 'Mu': '\\Mu', 'Alpha':
          '\\Alpha', 'beta': '\\beta', 'Eta': '\\Eta', 'rho': '\\rho',
          'delta': '\\delta', 'upsilon': '\\upsilon', 'omega': '\\omega',
          'Gamma': '\\Gamma', 'Lambda': '\\Lambda', 'Tau': '\\Tau', 'Xi':
          '\\Xi', 'kappa': '\\kappa', 'iota': '\\iota', 'mu': '\\mu', 'eta':
          '\\eta', 'Epsilon': '\\Epsilon', 'Zeta': '\\Zeta', 'sigma':
          '\\sigma', 'gamma': '\\gamma', 'lambda': '\\lambda'}

# To make eval() less dangerous.
_globals = {"__builtins__": None}
_lnames = ('acos', 'asin', 'atan', 'ceil', 'cos', 'cosh', 'e', 'log', 'log10',
           'pi', 'sin', 'sinh', 'sqrt', 'tan', 'tanh')
_locals = {k: eval('math.'+k) for k in _lnames}


def _texify(name):
    """Convert a name to TeX format. Recognizes greek letters and a subscript.

    :param name: String to be TeXified
    :returns: Converted string.
    """
    name = name.strip()
    items = name.split('_')
    if items[0] in _greek:
        items[0] = _greek[items[0]]
    if len(items) == 2:
        if items[1] in _greek:
            items[1] = '{' + _greek[items[1]] + '}'
        elif len(items[1]) > 1:
            items[1] = '{' + items[1] + '}'
    return '_'.join(items)


class Calculation(object):
    """Class to contain a set of coherent calculations."""

    def __init__(self):
        """Initialize the calculation."""
        self.prefix = [r'$\begin{array}{lclcrl}']
        self.suffix = [r'\end{array}$\hfill']
        self.lines = []

    def add(self, name, expr, unit=None, comment=None, fmt=".2f"):
        """Add an equation to the calculation.

        :param name: Name of the variable to assign the result to.
        :param expr: Python expression or number. Can contain functions from
                     python's math module.
        :param unit: Unit of the result in SIunitx format.
        :param fmt: Number format for the result. Defaults to '.2f'
        :param comment: @todo
        """
        expr = str(expr)
        value = eval(expr, _globals, _locals)
        exec('{} = {}'.format(name, value), _locals)
        n = ast.parse(expr)
        el = ['{} & = &'.format(_texify(name))]
        if type(n.body[0].value).__name__ == 'Num':
            el.append('& &')
        else:
            v = _LatexVisitor()
            v.visit(n)
            el.append('\\displaystyle {} & = &'.format(v.astex()))
        if unit:
            val = ''.join(['\\mbox{{\\SI{{{:', fmt, '}}}', '{{', unit, '}}}}'])
        else:
            val = ''.join(['\\mbox{{\\num{{{:', fmt, '}}}}}'])
        el.append(val.format(value))
        if comment:
            el += ['&', '\\mbox{{{}}}'.format(str(comment)), r'\\']
        else:
            el.append(r'\\')
        self.lines.append(' '.join(el))

    def __str__(self):
        """Create a string representation of the calculation.
        :returns: string
        """
        total = self.prefix + self.lines + self.suffix
        return '\n'.join(total)


class _LatexVisitor(ast.NodeVisitor):
    """ example recursive visitor """

    _fnames = {k: '\\{}'.format(k) for k in _lnames}
    # Exceptions where TeX deviates from Python:
    _fnames['log'] = '\\ln'
    _fnames['log10'] = '\\log'
    del(_fnames['e'])  # Not a special name in TeX.

    def __init__(self):
        self.txtexpr = []
        self.target = None
        ast.NodeVisitor.__init__(self)

    def astex(self):
        """Return a TeX mathematical expression"""
        return ''.join(self.txtexpr)

    def generic_visit(self, node):
        pass

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Usub):
            self.txtexpr.append('-')

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Div):
            self.txtexpr.append(r'\frac{')
            self.visit(node.left)
            self.txtexpr.append(r'}{')
            self.visit(node.right)
            self.txtexpr.append(r'}')
            return
        if (isinstance(node.left, ast.BinOp) and
           (type(node.left.op).__name__ in ['Add', 'Sub'] or
           isinstance(node.op, ast.Pow))):
            self.txtexpr.append(r'{\left(')
            self.visit(node.left)
            self.txtexpr.append(r'\right)}')
        else:
            self.visit(node.left)
        self.visit(node.op)
        if (isinstance(node.right, ast.BinOp) and
           (type(node.right.op).__name__ in ['Add', 'Sub'] or
           isinstance(node.op, ast.Pow))):
            self.txtexpr.append(r'{\left(')
            self.visit(node.right)
            self.txtexpr.append(r'\right)}')
        else:
            self.visit(node.right)

    def visit_Name(self, node):
        if node.id in _LatexVisitor._fnames:
            self.txtexpr.append(_LatexVisitor._fnames[node.id])
        else:
            self.txtexpr.append(_texify(node.id))

    def visit_Attribute(self, node):
        if node.attr in _LatexVisitor._fnames:
            self.txtexpr.append(_LatexVisitor._fnames[node.attr])
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
        '''Handled at the BinOp level, so pass.'''
        pass
