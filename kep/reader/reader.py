from config import get_default_spec_path, get_default_csv_path
from parsing_definitions import ParsingDefinition
from csv_data import CSV_Reader
from datapoints import Datapoints

# data
csv_path = get_default_csv_path()
csv_dicts = list(CSV_Reader(csv_path).yield_dicts())

# parsing instruction
specfile_path = get_default_spec_path()
pi = ParsingDefinition(specfile_path)

#dataset
d = Datapoints(csv_dicts, pi)
assert len(d.datapoints) > 51400
assert d.datapoints[0] == {'freq': 'a', 'value': 4823.0, 'varname': 'GDP_bln_rub', 'year': 1999}

# truncate csv_dicts, too many errors in whole file
output = list(d.emit('a'))[:140]

for z in output:
    if z['year'] == 2016:
        print(z.__repr__() + ",")

testpoints = [
    {'varname': 'GDP_bln_rub', 'year': 2016, 'value': 85881.0},
    {'varname': 'GDP_rog', 'year': 2016, 'value': 99.8},
    {'varname': 'IND_PROD_yoy', 'year': 2016, 'value': 101.3},
    # ERROR CRITICAL: - same label, header or unti did not switch
    {'varname': 'IND_PROD_yoy', 'year': 2016, 'value': 104.8},
    {'varname': 'PROD_AGRO_MEAT_th_t', 'year': 2016, 'value': 13939.0},
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 103.4},
    # ERROR CRITICAL: - same label, header or unti did not switch
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 30724.0},
    # ERROR CRITICAL: - same label, header or unti did not switch
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 99.8},
]

for t in testpoints:
    assert t in output