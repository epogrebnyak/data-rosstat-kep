from collections import OrderedDict, namedtuple
Label = namedtuple("Label", "varname unit")
 
a = OrderedDict([('Консолидированный бюджет', 
                  Label(varname='GOV_CONSOLIDATED_EXPENSE_ACCUM', unit='bln_rub'))])
                  
b = OrderedDict([('Федеральный бюджет', 
     Label(varname='GOV_FEDERAL_EXPENSE_ACCUM', unit='bln_rub'))])
