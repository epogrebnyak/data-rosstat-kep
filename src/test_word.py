# -*- coding: utf-8 -*-
"""
Test reader functions
"""

# *****************************************************************************

from word import split_row_by_periods, reader12 

def test_row_split1():   
    row = [2007, 6716.2, 897.6, 1414.4, 1744.1, 2660.1, 255.3, 298.0, 344.3, 364.5, 
       472.2, 577.7, 543.1, 584.2, 616.8, 684.7, 740.4, 1235.0]
    y, a, q, m = split_row_by_periods(row)
    assert y == 2007
    assert len (q) == 4
    assert len (m) == 12    
    assert sum (q) == a
    assert sum (m) == a

def test_row_split2():   
    row = ['1999', '196.9', '203.3', '207.6', '213.1', '216.7', '220.7', '226.5',
                   '221.0', '162.0', '157.1', '150.5', '136.5']
    y, a, q, m = reader12(row)
    assert y == '1999'
    assert q == None
    assert a == None    
    assert len (m) == 12  
    
# *****************************************************************************
    
from word import kill_comment, filter_value
def test_filter_comment():
    assert kill_comment("20.5 3)") == "20.5"
    
def test_filter_value():
    assert filter_value("20.5 3)") == 20.5    
    assert filter_value ('6512.3 6762.31)') == 6512.3
    
# *****************************************************************************
    
from word import yield_csv_rows, load_spec, get_basename  
from word import make_labelled_csv
import os

def compare_iterables(gen1, gen2):
   for a, b in zip(gen1, gen2):
       assert a == b

def check_make_labelled_csv(f):
    # dump from .doc not tested
    c = os.path.abspath(f)
    label_dict, sec_label_dict, reader_dict = load_spec(f)
    t = make_labelled_csv(c, label_dict, sec_label_dict)
    t0 = get_basename(t) + "_reference_dataset.txt"
    compare_iterables(yield_csv_rows(t), 
                      yield_csv_rows(t0))    
    # dump to database not tested
    
def test_make_labelled_csv():
    # dump from .doc not tested
    src_csv = ["../data/1-07/1-07.csv", "../data/minitab/minitab.csv"]
    for f in src_csv:
       path = os.path.abspath(f)
       check_make_labelled_csv(path)
    