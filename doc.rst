

Use of the Variable class

v = Variable('sgk', 1.75, 'g/cm³')

Properties:
v.name
v.texname
v.unit
v.texunit
v.getvalue()
v.settex(r'\rho_k', 'g/cm^3')
>>>str(v)
sg = 1.75 g/cm³
>>>v.gettex()
$\rho_k$ = \SI{1.75}{g/cm^3}

e = Equation('v', 'sgk*L*B*h', 'g')
e.name
e.texname
e.unit
e.texunit
e.getvalue()
e.formula
