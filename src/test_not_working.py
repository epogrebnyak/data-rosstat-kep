# *****************************************************************************
    
import os

from word import dump_labelled_rows_to_csv, get_reference_csv_filename
from word import yield_csv_rows, check_vars_not_in_labelled_csv
 
def compare_iterables(gen1, gen2):
   for a, b in zip(gen1, gen2):
       assert a == b

def check_make_labelled_csv(f):
    # dump from .doc not tested
    t = dump_labelled_rows_to_csv(f)
    t0 = get_reference_csv_filename(f)    
    compare_iterables(yield_csv_rows(t), 
                      yield_csv_rows(t0))    
    # dump to database not tested
    
def test_make_labelled_csv():    
    src_csv = ["../data/1-07/1-07.csv", "../data/minitab/minitab.csv"]
    for f in src_csv:
       print(f)
       path = os.path.abspath(f)
       check_make_labelled_csv(path)
       assert check_vars_not_in_labelled_csv(f) == []
