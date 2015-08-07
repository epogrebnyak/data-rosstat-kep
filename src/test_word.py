# -*- coding: utf-8 -*-
"""
Test reader functions
"""

# *****************************************************************************

from word import split_row_by_periods, reader12, reader12_with_annual 

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
    
def test_row_split3():   
    row = ["1999", '27,00', '22,60', '22,86', '24,18', '24,23', '24,44', '24,22', 
                   '24,19', '24,75', '25,08', '26,05', '26,42', '27,00']
    y, a, q, m = reader12_with_annual(row)
    assert y == '1999'
    assert q == None
    assert a == '27,00'    
    assert len (m) == 12 
    assert a == m[-1]



    

    
# *****************************************************************************
    
from word import kill_comment, filter_value
def test_filter_comment():
    assert kill_comment("20.5 3)") == "20.5"
    
def test_filter_value():
    assert filter_value("20.5 3)") == 20.5    
    assert filter_value ('6512.3 6762.31)') == 6512.3
    
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
