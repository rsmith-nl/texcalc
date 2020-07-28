the TeXcalc module
##################

Introduction
------------

As an engineer, I often do diverse calculations that I want to save in my
logbooks which I write in LaTeX.  Up to now I've either formatted those by
hand or used the ``listings`` package to include calculations made in IPython.

These techniques are not optimal.  Formatting by hand makes it time consuming
and error-prone to change the typeset calculations; results have to be changed
by hand.  Using the listings package works, but this can only contain the
calculations without explanations or units, and the results aren't always
nicely formatted. Technical calculations without units are generally
meaningless, so it was important for me to be able to include them in the
results.


How it works
------------

So I wrote a Python module called ``texcalc`` that allows me to do
calculations and typesets the results for me. It works like this;

.. code-block:: python

    import texcalc as tc

    tc.header()
    tc.line('rho_f', '1.62', 'g/cm^3', 'Fiber density')
    tc.line('rho_r', '1.2', 'g/cm^3', "Resin density")
    tc.line('v_f', '0.3', '-', 'Fiber volume fraction')
    tc.line('W_f', '450', 'g/m^2', "Area weight fibers", fmt=".0f")
    tc.line('t_f', 'W_f/(10000*rho_f)*10', 'mm')
    tc.line('t', 't_f/v_f', 'mm', "Laminate thickness")
    tc.line('t_r', 't-t_f', 'mm')
    tc.line('W_r', 't_f/10*(10000*rho_r)', 'g/m^2', "Area weight resin", fmt=".0f")
    tc.footer()


The ``texcalc.line`` function evaluates the given assignments and expressions
and prints LaTeX code to typeset them.

The ``texcalc.header`` and ``texcalc.footer`` functions do the obvious and
print the header and footer for the ``align*`` environment that contains the
calculations.

The defined variables are also injected into the scope of the module where
``texcalc.line`` is called using ``sys._getframe(1).f_globals``, which I saw
in a StackOverflow comment on `this answer`_.
This is done so you can use them in e.g. further generated text.

.. _this answer: https://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function/27642440#27642440

This module requires the ``align*`` environment from the amsmath_ package to typeset the
whole set of equations. The units and values of the variables and results are
set using the siunitx_ package.  It uses ``\text`` to include plain text in
the otherwise math-mode ``align*`` environment.  This means that the comments
should be kept reasonably short so they fit one one line.  The generated LaTeX
code isn't set up to handle comments that would span multiple lines.

.. _amsmath: http://www.ams.org/arc/resources/amslatex-about.html
.. _siunitx: http://ctan.org/pkg/siunitx

To typeset the calculations you need a LaTeX document.
A simple version using the ``standalone`` document class is shown below.

.. code-block:: latex

    \documentclass[preview]{standalone}
    \usepackage[utf8]{inputenc}
    \usepackage{tgpagella}
    \usepackage{siunitx}
    \usepackage{amsmath}
    \sisetup{detect-all=true, mode=text, group-digits=true,
        input-decimal-markers={.,}, exponent-product=\times,
        separate-uncertainty=true, load-configurations=abbreviations}
    \begin{document}
    \input{ex1}
    \end{document}

The ``siunitx`` and ``amsmath`` packages are *required* to typeset the
calculations properly.

A formatted version of the calculation shown at the beginning and the
aforementioned template is shown below.

.. image:: examples/ex1.png
    :alt: texcalc example
    :width: 100%

As shown in this example, transliterated greek letters are converted to their
proper typeset greek letters. (Also for upper case, so ``delta`` produces
δ and ``Delta`` produces Δ.) In a similar way, underscores are used as
a prefix for subscripts.

.. Note::

    This module uses ``eval`` and ``exec``, which exposes the full
    capabilities of the Python interpreter. This module should therefore _not_
    be used with untrusted input!


Tests
-----

The file ``tests.py`` contains the tests for this code. You can run the tests
with ``py.test -v tests.py``.

