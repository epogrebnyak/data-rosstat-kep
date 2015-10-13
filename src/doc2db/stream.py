# -*- coding: utf-8 -*-
"""Generate stream of data from csv file with var-labelled rows.

Entry point:

   emit_flat_data(p)
   p - path to csv file with var-labelled rows

"""
try:
    from .common import get_labelled_csv_filename, yield_csv_rows
except ImportError:
    from common import get_labelled_csv_filename, yield_csv_rows
    
import os    
import re

#______________________________________________________________________________
#
#  Generate stream from labelled csv file 
#______________________________________________________________________________

def emit_flat_data(p):
    """Emit all data from file *p*"""
    for row_tuple in yield_labelled_row(p):
        for db_row in yield_stream(row_tuple):
            yield db_row
            
def yield_labelled_row(p):
    """Emit varname-labeled rows as tuple of components."""
    f = get_labelled_csv_filename(p)
    
    for row in yield_csv_rows(f):
        var_label = row[0]
        if var_label != "unknown_var":

            var_name = row[0] + "_" + row[1]            
            mod_row = [filter_value(x) for x in row[2:]]
            reader = get_reader_func_by_row_length(row[2:])
            
            y, annual_value, qtr_values, monthly_values = reader(mod_row)
            y = int(y)
            yield var_name, y, annual_value, qtr_values, monthly_values 
           
def yield_stream(row_tuple):
    """Generate tuples (freq, year, qtr, month, label, val) from row components."""
    vn, y, a, qs, ms = row_tuple
        
    if a is not None:
               yield ("a", vn, y, None, None, a)

    if qs is not None:         
        for i, val in enumerate(qs):
            if val is not None:
               yield ("q", vn, y, i+1, None, val)

    if ms is not None:         
        for i, val in enumerate(ms):
            if val is not None:
               yield ("m", vn, y, None, i+1, val)
           
#______________________________________________________________________________
#
#  Read rows by annual, qtr, month section 
#______________________________________________________________________________

def split_row_by_periods(row):           
    """Year A Q Q Q Q M*12"""
    return row[0], row[1], row[2:2+4], row[2+4:(2+4+12)]

def split_row_by_months(row):         
    """Year M*12"""
    return row[0], None, None, row[1:12+1]
    
def split_row_by_months_and_annual(row):         
    """Year A M*12"""
    return row[0], row[1], None, row[2:12+2]

ROW_LENGTH_TO_FUNC = { 1+1+4+12: split_row_by_periods, 
                           1+12: split_row_by_months,
                         1+1+12: split_row_by_months_and_annual }

def get_reader_func_by_row_length(row):
    return ROW_LENGTH_TO_FUNC[len(row)]       

#______________________________________________________________________________
#
#  Filter data on db import
#______________________________________________________________________________

# Allows to catch a value with with comment) or even double comment
COMMENT_CATCHER = re.compile("([\d.]*)\s*(?=\d\))")

def kill_comment(text):    
    return COMMENT_CATCHER.match(text).groups()[0]

def process_text_with_bracket(text):     
     # if there is mess like '6512.3 6762.31)' in  cell, return first value
     if " " in text:
        return filter_value(text.split(" ")[0])          
     # otherwise just through away comment   
     else:
        return kill_comment(text)          
    
def filter_value(text):  
   """Converts *text* to float number assuming it may contain 'comment)'."""
   text = text.replace(",",".")
   if ')' in text:
       text = process_text_with_bracket(text)
   if text == "":       
       return None
   else:       
       try: 
          return float(text)
       except:
          return "###"       
       
if __name__ == "__main__":
    p = os.path.abspath("../data/1-07/1-07.txt")
    gen = emit_flat_data(p)
    for x in gen:
        print(x)