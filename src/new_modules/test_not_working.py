# *****************************************************************************
    
import os

from ..label_csv import dump_labelled_rows_to_csv, check_vars_not_in_labelled_csv 
from ..common import get_reference_csv_filename
from ..common import yield_csv_rows
 
def compare_iterables(gen1, gen2):
   for a, b in zip(gen1, gen2):
       assert a == b

def check_make_labelled_csv(f):        
    t = dump_labelled_rows_to_csv(f)
    t0 = get_reference_csv_filename(f)    
    print ("Actual file:", t)
    print ("Reference file:", t0)
    compare_iterables(yield_csv_rows(t), 
                      yield_csv_rows(t0))    
    
def test_make_labelled_csv():  
    # note: can still keep it as ../data/ because tests startr from doc2db
    src_csv = ["../data/1-07/1-07.csv", "../data/minitab/minitab.csv"]
    for f in src_csv:      
       path = os.path.abspath(f)
       print(f, path)
       check_make_labelled_csv(path)
       assert check_vars_not_in_labelled_csv(f) == []
