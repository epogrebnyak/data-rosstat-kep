import unittest 

from config import get_default_spec_path, get_default_csv_path
from csv_data import CSV_Reader
from datapoints import Datapoints
from parsing_definitions import ParsingDefinition

# data
csv_path = get_default_csv_path()
csv_dicts = list(CSV_Reader(path=csv_path).yield_dicts())

# parsing instruction
specfile = get_default_spec_path()
pi = ParsingDefinition(path=specfile)

#dataset
d = Datapoints(csv_dicts, pi)

output = list(d.emit('a'))

def show_2016():
    for z in output:
        if z['year'] == 2016:
            print(z.__repr__() + ",")

testpoints_valid = [
    {'varname': 'GDP_bln_rub', 'year': 2016, 'value': 85881.0},
    {'varname': 'GDP_rog', 'year': 2016, 'value': 99.8},
    {'varname': 'IND_PROD_yoy', 'year': 2016, 'value': 101.3},
    {'varname': 'AGRO_PRODUCTION_yoy', 'year': 2016, 'value': 104.8},
    {'varname': 'PROD_AGRO_MEAT_th_t', 'year': 2016, 'value': 13939.0},
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 103.4},
    {'varname': 'PROD_AGRO_MILK_th_t', 'year': 2016, 'value': 30724.0},
    {'varname': 'PROD_AGRO_MILK_yoy', 'year': 2016, 'value': 99.8},
]

testpoints_invalid = [
    # ERROR CRITICAL: - same label, header or unit did not switch, must edit "__spec.txt"
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 30724.0},
    # ERROR CRITICAL: - same label, header or unit did not switch, must edit "__spec.txt"
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 99.8},
]

# REQUIREMENT 1: release all values from d.emit('a') and test them against 
#              *testpoints_valid*
#            - 
#            - controlling there are no varnames with same value and year

# REQUIREMENT 2: make sure all labels from ParsingDefinition(specfile_path)
#                have data values, at least at some frequency

# "Screening"

# TODO 1: add test showing there are no duplicates in *output*
#       (now there are many, the test will fail)

# TODO 2: show all variables listed in specs + check if these variables are 
#       are read (at any frequency) 

# TODO 3: write a check every variable from specs has a *testpoints_valid* values 
         

# "Remedies"

# TODO 4: concat several "__specs*", edit specs

# TODO 5: work out mechanism to apply parsing definitions to segments of file

# TODO 6: Adding more elements to testpoints_valid 



 
class TestCaseSingleValue2016a(unittest.TestCase):
    def test_positive(self):
        assert len(d.datapoints) > 51400
        assert d.datapoints[0] == {'freq': 'a', 'value': 4823.0, 
                                   'varname': 'GDP_bln_rub', 'year': 1999}        
        
class TestCaseAnnual2016(unittest.TestCase):
    def test_positive(self):
        for t in testpoints_valid:
            assert t in output

    def test_negative(self):
        for t in testpoints_invalid:
            assert t not in output


if __name__ == '__main__':
    #show_2016()
    unittest.main()
