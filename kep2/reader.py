import os
import csv

from parsing_definitions import get_default_definition
from csv_data import get_default_csv_content
#from datapoints import Datapoints

rd = get_default_csv_content()[:100]

# FIXME - must coerce type of parsing instructions 
pi = get_default_definition()['instruction']
pi_list = [pi['headers'], pi['units'], pi['splitter_func']]
     
#d1 = Datapoints(raw_data = rd, 
#                parsing_instructions = pi_list)

#print(next(d1.emit("a")))


#
#  File "D:\__data-kep\data-rosstat-kep-master\kep2\datapoints.py", line 29, in concat_label
#    raise ValueError(label)
#
#ValueError: ['GDP', 'bln_rub', 1.1]