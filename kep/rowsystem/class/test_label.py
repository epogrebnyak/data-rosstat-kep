# some testing      
from label import Label

z = Label()
r = z
z.label = "THIS_VAR_some_unit"
r.head = "THIS_VAR"
r.unit = "some_unit"
w = Label("THIS_VAR_some_unit")
q = Label("THIS_VAR", "some_unit")  
assert z == w
assert w == q
assert z == r
assert Label()._get_head('PROD_E_TWh') == 'PROD_E' 
assert Label()._get_unit('PROD_E_TWh') == 'TWh'
