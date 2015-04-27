the TeXcalc module
##################

:date: 2015-04-27
:author: Roland Smith

As an engineer, I often do diverse calculations that I want to save in my
logbooks which I write in LaTeX.  Up to now I've either formatted those by
hand or used the ``listings`` package to include calculations made in IPython.

These techniques are not optimal.  Formatting by hand makes it time consuming
and error-prone to change the typeset calculations; results have to be changed
by hand.  Using the listings package works, but this can only contain the
calculations without explanations or units, and the results aren't always
nicely formatted

Technical calculations without units are generally meaningless, so it was
important for me to be able to include them in the results.

So I wrote a Python module called ``texcalc`` that allows me to do
calculations and typesets the results for me. It works like this;

. code-block:: python

    from __future__ import print_function
    from texcalc import Calculation

    c = Calculation()
    c.add('rho_f', 2.62, 'g/cm^3', 'fiber density')
    c.add('W_f', 450, 'g/cm^2', 'fiber area weight', fmt='.0f')
    c.add('v_f', 0.3, '-', 'fiber volume fraction')
    c.add('rho_m', 1.15, 'g/cm^3', 'matrix density')
    c.add('t_f', 'W_f*10/(10000*rho_f)', 'mm', 'fiber “thickness”')
    c.add('t', 't_f/v_f', 'mm', 'laminate thickness')
    c.add('t_m', 't-t_f', 'mm', 'resin “thickness”')
    c.add('W_m', 't_m/10*rho_m*10000', 'g/m^2', 'resin area weight', fmt='.0f')
    c.add('w_f', 'W_f/(W_f+W_m)', '-', 'fiber weight fraction')
    print(c)

Using a ``Calculation`` object one can define a sequence of variable
assignments or expressions using variables that have been assigned earlier.
Printing the ``Calculation`` (or rather converting it to a string) will cause
a LaTeX formatted version in the form of an array_ environment to be produced.
When this is written to a file it can be included in a LaTeX document using
``\input``.  The typeset result looks quite nice. (Note that siunitx was set
up to use a decimal comma in this example);

.. _array: http://latex.wikia.com/wiki/Array_%28LaTeX_environment%29

.. image:: images/texcalc-example.png
    :alt: texcalc example
    :width: 100%

It uses the siunitx_ package to typeset the units of the variables and
calculation results.  It uses ``\mbox`` to include plain text in the otherwise
math-mode environment.  This means that the comments should be kept reasonably
short so they fit one one line.  The generated LaTeX code isn't set up to
handle comments that would span multiple lines.

.. _siunitx: http://ctan.org/pkg/siunitx

.. code-block:: latex

    $\begin{array}{lclcrl}
    \rho_f & = & & & \mbox{\SI{2.62}{g/cm^3}} & \mbox{fiber density} \\
    W_f & = & & & \mbox{\SI{450}{g/cm^2}} & \mbox{fiber area weight} \\
    v_f & = & & & \mbox{\SI{0.30}{-}} & \mbox{fiber volume fraction} \\
    \rho_m & = & & & \mbox{\SI{1.15}{g/cm^3}} & \mbox{matrix density} \\
    t_f & = & \displaystyle \frac{W_f\cdot 10}{10000\cdot \rho_f} & = & \mbox{\SI{0.17}{mm}} & \mbox{fiber “thickness”} \\
    t & = & \displaystyle \frac{t_f}{v_f} & = & \mbox{\SI{0.57}{mm}} & \mbox{laminate thickness} \\
    t_m & = & \displaystyle t-t_f & = & \mbox{\SI{0.40}{mm}} & \mbox{resin “thickness”} \\
    W_m & = & \displaystyle \frac{t_m}{10}\cdot \rho_m\cdot 10000 & = & \mbox{\SI{461}{g/m^2}} & \mbox{resin area weight} \\
    w_f & = & \displaystyle \frac{W_f}{W_f+W_m} & = & \mbox{\SI{0.49}{-}} & \mbox{fiber weight fraction} \\
    \end{array}$\hfill


.. Note::

    This module uses ``eval``, which exposes the full capabilities of the
    Python interpreter. This module should therefore _not_ be used with
    untrusted input!
