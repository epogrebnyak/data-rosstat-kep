import unittest 
from itertools import groupby

from config import get_default_csv_path
from csv_data import CSV_Reader
import parsing_definitions
from emitter import Datapoints



# data
csv_dicts = CSV_Reader(path=get_default_csv_path()).yield_dicts()
# main parsing instruction
pdef = parsing_definitions.get_definitions()['default']
# more parsing instructions for segment
more_pdefs = parsing_definitions.get_definitions()['additional']

# dataset
d = Datapoints(csv_dicts, pdef)
output = list(x for x in d.emit('a') if x['year']==2016)

def show_2016():
    for z in output:
        print(z.__repr__() + ",")

if __name__ == '__main__':  
    #show_2016()
    unittest.main()