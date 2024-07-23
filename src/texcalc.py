# file: texcalc.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2014-2017 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2014-05-04T11:28:35+0200
# Last modified: 2024-07-23T07:18:40+0200
"""
Module to do and print calculations in LaTeX format.
Prints formatted statements.
Note that this module uses both eval() and exec().
It should therefore not be used with untrusted input.
"""

import ast
import sys
from math import (  # noqa
    acos,
    asin,
    atan,
    ceil,
    cos,
    cosh,
    e,
    log,
    log10,
    pi,
    sin,
    sinh,
    sqrt,
    tan,
    tanh,
    radians,
)

__version__ = "2022.4"
# Default format
_fmt = ".2f"


def header(fmt=None):
    """
    Print the header for the calculation, set the default format.
    Ever calculation should start with this.

    Arguments:
        fmt: Number format for the result.
             If not supplied then the default of ".2f" is used.
    """
    global _fmt
    if fmt:
        _fmt = fmt
    print(r"\begin{align*}")


def footer():
    """
    Print the footer.
    Every calculation should end with invoking this.
    """
    print(r"\end{align*}")


def line(name, expr, unit=None, comment=None, fmt=None):
    """Add an equation to the calculation.

    Arguments:
        name: Name of the variable to assign the result to.
            May be None, in which case the result is not assigned.
        expr: Python expression or number. Can contain functions from
            python's math module.
        unit: Unit of the result in SIunitx format.
        fmt: Number format for the result. Default is given during
            writing of the header.
        comment: Any comment string you want to append.
    """
    module_namespace = sys._getframe(1).f_globals
    module_namespace.update(globals())
    if not fmt:
        fmt = _fmt
    expr = str(expr)
    value = eval(expr, module_namespace)
    if name is not None:
        exec(f"{name} = {value}", module_namespace)
        el = [_texify(name) + " &=&"]
    else:
        el = [" &&"]
    n = ast.parse(expr)
    if type(n.body[0].value).__name__ in ("Constant", "BinOp"):
        el.append("&&=&")
    else:
        v = _LatexVisitor()
        v.visit(n)
        el.append("\\displaystyle {} &&=&".format(v.astex()))
    fn = "".join([r"{:", fmt, r"}"]).format(value)
    if unit:
        val = "".join([r"\text{\quad\SI{", fn, r"}", r"{", unit, r"}}"])
    else:
        val = "".join([r"\text{\quad\num{", fn, r"}}"])
    el.append(val)
    if comment:
        el += ["&&", "\\text{{{}}}".format(str(comment)), r"\displaybreak[0]\\"]
    else:
        el.append(r"\displaybreak[0]\\")
    print(" ".join(el))


_fnames = {
    "acos": "\\arccos",
    "asin": "\\arcsin",
    "atan": "\\arctan",
    "ceil": "\\ceil",
    "cos": "\\cos",
    "cosh": "\\cosh",
    "log": "\\ln",
    "log10": "\\log",
    "pi": "\\pi",
    "sin": "\\sin",
    "sinh": "\\sinh",
    "sqrt": "\\sqrt",
    "tan": "\\tan",
    "tanh": "\\tanh",
    "radians": "radians",
}
_greek = {
    "alpha": "\\alpha",
    "Alpha": "\\Alpha",
    "beta": "\\beta",
    "Beta": "\\Beta",
    "chi": "\\chi",
    "Chi": "\\Chi",
    "delta": "\\delta",
    "Delta": "\\Delta",
    "epsilon": "\\epsilon",
    "Epsilon": "\\Epsilon",
    "eta": "\\eta",
    "Eta": "\\Eta",
    "gamma": "\\gamma",
    "Gamma": "\\Gamma",
    "iota": "\\iota",
    "Iota": "\\Iota",
    "kappa": "\\kappa",
    "Kappa": "\\Kappa",
    "lambda": "\\lambda",
    "Lambda": "\\Lambda",
    "mu": "\\mu",
    "Mu": "\\Mu",
    "nu": "\\nu",
    "Nu": "\\Nu",
    "omega": "\\omega",
    "Omega": "\\Omega",
    "omicron": "\\omicron",
    "Omicron": "\\Omicron",
    "phi": "\\phi",
    "Phi": "\\Phi",
    "pi": "\\pi",
    "Pi": "\\Pi",
    "psi": "\\psi",
    "Psi": "\\Psi",
    "rho": "\\rho",
    "Rho": "\\Rho",
    "sigma": "\\sigma",
    "Sigma": "\\Sigma",
    "tau": "\\tau",
    "Tau": "\\Tau",
    "theta": "\\theta",
    "Theta": "\\Theta",
    "upsilon": "\\upsilon",
    "Upsilon": "\\Upsilon",
    "xi": "\\xi",
    "Xi": "\\Xi",
    "zeta": "\\zeta",
    "Zeta": "\\Zeta",
}


def _texify(name):
    """
    Convert a name to TeX format. Recognizes greek letters and a subscript.

    Arguments:
        name: A string to be TeXified.

    Returns:
        The converted string.
    """
    name = name.strip()
    items = name.split("_")
    if items[0] in _greek:
        items[0] = _greek[items[0]]
    if len(items) == 2:
        if items[1] in _greek:
            items[1] = "{" + _greek[items[1]] + "}"
        elif len(items[1]) > 1:
            items[1] = "{" + items[1] + "}"
    return "_".join(items)


class _LatexVisitor(ast.NodeVisitor):
    """Recursive visitor for LaTeX."""

    __slots__ = ("txtexpr", "target")

    def __init__(self):
        self.txtexpr = []
        self.target = None
        ast.NodeVisitor.__init__(self)

    def astex(self):
        """Return a TeX mathematical expression"""
        return "".join(self.txtexpr)

    def generic_visit(self, node):
        pass

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            self.txtexpr.append("-")
            self.visit(node.operand)

    def visit_BinOp(self, node):
        def wrap(nd):
            self.txtexpr.append(r"{\left(")
            self.visit(nd)
            self.txtexpr.append(r"\right)}")

        if isinstance(node.op, ast.Div):
            self.txtexpr.append(r"\frac{")
            self.visit(node.left)
            self.txtexpr.append(r"}{")
            self.visit(node.right)
            self.txtexpr.append(r"}")
            return
        if isinstance(node.op, ast.Pow):
            if isinstance(node.left, ast.BinOp):
                wrap(node.left)
            else:
                self.visit(node.left)
            self.visit(node.op)
            if isinstance(node.right, ast.BinOp):
                self.txtexpr.append(r"{")
                self.visit(node.right)
                self.txtexpr.append(r"}")
            else:
                self.visit(node.right)
            return
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.BinOp) and isinstance(
                node.left.op, (ast.Add, ast.Sub)
            ):
                wrap(node.left)
            else:
                self.visit(node.left)
            self.visit(node.op)
            if isinstance(node.right, ast.BinOp) and isinstance(
                node.right.op, (ast.Add, ast.Sub)
            ):
                wrap(node.right)
            else:
                self.visit(node.right)
        else:
            self.visit(node.left)
            self.visit(node.op)
            self.visit(node.right)

    def visit_Name(self, node):
        if node.id in _fnames:
            self.txtexpr.append(_fnames[node.id])
        else:
            self.txtexpr.append(_texify(node.id))

    def visit_Attribute(self, node):
        if node.attr in _fnames:
            self.txtexpr.append(_fnames[node.attr])
        else:
            self.txtexpr.append(node.attr)

    def visit_Constant(self, node):
        self.txtexpr.append(str(node.value))

    def visit_Add(self, node):
        self.txtexpr.append("+")

    def visit_Sub(self, node):
        self.txtexpr.append("-")

    def visit_Mult(self, node):
        self.txtexpr.append(r"\cdot ")

    def visit_Pow(self, node):
        self.txtexpr.append("^")

    def visit_Call(self, node):
        self.visit(node.func)
        self.txtexpr.append("(")
        for a in node.args:
            self.visit(a)
        self.txtexpr.append(")")

    def visit_Div(self, node):
        """Handled at the BinOp level."""
        pass
