# file: texcalc.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2014-2017 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2014-05-04T11:28:35+0200
# Last modified: 2018-07-08T12:48:16+0200
"""Module to do and print calculations. Prints formatted statements.
Note that this module uses both eval() and exec().
It should therefore not be used with untrusted input."""

import ast
import math  # noqa

__version__ = "2018.07.08"

_greek = {
    'tau': '\\tau',
    'xi': '\\xi',
    'Chi': '\\Chi',
    'alpha': '\\alpha',
    'Theta': '\\Theta',
    'zeta': '\\zeta',
    'Pi': '\\Pi',
    'Iota': '\\Iota',
    'Phi': '\\Phi',
    'Psi': '\\Psi',
    'Sigma': '\\Sigma',
    'chi': '\\chi',
    'Omicron': '\\Omicron',
    'Nu': '\\Nu',
    'Beta': '\\Beta',
    'Rho': '\\Rho',
    'Delta': '\\Delta',
    'theta': '\\theta',
    'pi': '\\pi',
    'Omega': '\\Omega',
    'nu': '\\nu',
    'phi': '\\phi',
    'psi': '\\psi',
    'Kappa': '\\Kappa',
    'Upsilon': '\\Upsilon',
    'epsilon': '\\epsilon',
    'omicron': '\\omicron',
    'Mu': '\\Mu',
    'Alpha': '\\Alpha',
    'beta': '\\beta',
    'Eta': '\\Eta',
    'rho': '\\rho',
    'delta': '\\delta',
    'upsilon': '\\upsilon',
    'omega': '\\omega',
    'Gamma': '\\Gamma',
    'Lambda': '\\Lambda',
    'Tau': '\\Tau',
    'Xi': '\\Xi',
    'kappa': '\\kappa',
    'iota': '\\iota',
    'mu': '\\mu',
    'eta': '\\eta',
    'Epsilon': '\\Epsilon',
    'Zeta': '\\Zeta',
    'sigma': '\\sigma',
    'gamma': '\\gamma',
    'lambda': '\\lambda'
}

# To make eval() less dangerous.
_globals = {"__builtins__": None}
_lnames = (
    'acos', 'asin', 'atan', 'ceil', 'cos', 'cosh', 'e', 'log', 'log10', 'pi', 'sin', 'sinh',
    'sqrt', 'tan', 'tanh', 'radians'
)
_locals = {k: eval('math.' + k) for k in _lnames}


def _texify(name):
    """
    Convert a name to TeX format. Recognizes greek letters and a subscript.

    Arguments:
        name: A string to be TeXified.

    Returns:
        The converted string.
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

    __slots__ = ('fmt', 'prefix', 'suffix', 'lines')

    def __init__(self, fmt=".2f"):
        """Initialize a Calculation.

        Arguments:
            fmt: standard format to use for numbers. Defaults to “.2f”.
        """
        self.fmt = fmt
        self.prefix = [r'\begin{align*}']
        self.suffix = [r'\end{align*}']
        self.lines = []

    def add(self, name, expr, unit=None, comment=None, fmt=None):
        """Add an equation to the calculation.

        Arguments:
            name: Name of the variable to assign the result to.
            expr: Python expression or number. Can contain functions from
                python's math module.
            unit: Unit of the result in SIunitx format.
            fmt: Number format for the result. Default is given during
                creation of the Calculation object.
            comment: Any comment string you want to append.
        """
        if not fmt:
            fmt = self.fmt
        expr = str(expr)
        value = eval(expr, _globals, _locals)
        exec(f'{name} = {value}', _locals)
        n = ast.parse(expr)
        el = [_texify(name) + ' &=']
        if type(n.body[0].value).__name__ == 'Num':
            el.append('&&=')
        else:
            v = _LatexVisitor()
            v.visit(n)
            el.append('\\displaystyle {} &&='.format(v.astex()))
        fn = ''.join([r'{:', fmt, r'}']).format(value)
        if unit:
            val = ''.join([r'\text{\SI{', fn, r'}', r'{', unit, r'}}'])
        else:
            val = ''.join([r'\text{\num{', fn, r'}}'])
        el.append(val)
        if comment:
            el += ['&&', '\\text{{{}}}'.format(str(comment)), r'\displaybreak[0]\\']
        else:
            el.append(r'\displaybreak[0]\\')
        self.lines.append(' '.join(el))

    def __str__(self):
        """
        Create a string representation of the calculation.

        Returns:
            The calculation in the form of a string.
        """
        if self.lines and self.lines[-1].endswith(r'\\'):
            self.lines[-1] = self.lines[-1][:-2]
        total = self.prefix + self.lines + self.suffix
        return '\n'.join(total)


class _LatexVisitor(ast.NodeVisitor):
    """Recursive visitor for LaTeX."""

    __slots__ = ('txtexpr', 'target')
    _fnames = {k: f'\\{k}' for k in _lnames}
    # Exceptions where TeX deviates from Python:
    _fnames['log'] = '\\ln'
    _fnames['log10'] = '\\log'
    _fnames['asin'] = '\\arcsin'
    _fnames['acos'] = '\\arccos'
    _fnames['atan'] = '\\arctan'
    _fnames['radians'] = 'radians'
    del (_fnames['e'])  # Not a special name in TeX.

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
        if isinstance(node.op, ast.USub):
            self.txtexpr.append('-')
            self.visit(node.operand)

    def visit_BinOp(self, node):

        def wrap(nd):
            self.txtexpr.append(r'{\left(')
            self.visit(nd)
            self.txtexpr.append(r'\right)}')

        if isinstance(node.op, ast.Div):
            self.txtexpr.append(r'\frac{')
            self.visit(node.left)
            self.txtexpr.append(r'}{')
            self.visit(node.right)
            self.txtexpr.append(r'}')
            return
        if isinstance(node.op, ast.Pow):
            if isinstance(node.left, ast.BinOp):
                wrap(node.left)
            else:
                self.visit(node.left)
            self.visit(node.op)
            if isinstance(node.right, ast.BinOp):
                self.txtexpr.append(r'{')
                self.visit(node.right)
                self.txtexpr.append(r'}')
            else:
                self.visit(node.right)
            return
        if isinstance(node.op, ast.Mult):
            if (isinstance(node.left, ast.BinOp) and isinstance(node.left.op, (ast.Add, ast.Sub))):
                wrap(node.left)
            else:
                self.visit(node.left)
            self.visit(node.op)
            if (
                isinstance(node.right, ast.BinOp) and
                isinstance(node.right.op, (ast.Add, ast.Sub))
            ):
                wrap(node.right)
            else:
                self.visit(node.right)
        else:
            self.visit(node.left)
            self.visit(node.op)
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
        '''Handled at the BinOp level.'''
        pass
