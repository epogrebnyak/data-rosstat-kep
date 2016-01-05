# -*- coding: utf-8 -*-
"""Generate stream of database-ready tuples from var-labelled rows with mixed frequencies.

   Features:
   - defines data frequency based on number of columns in table (row)
   - attempts to filter data (e.g. eliminate comments in cells)

   Entry point: 
      stream_flat_data(lab_rows)
"""

import re

#------------------------------------------------------------------------------
#  Read rows by annual, qtr, month section 
#------------------------------------------------------------------------------

def stream_flat_data(lab_rows):
    """Emit varname-labeled rows as flat database-ready rows."""
    for row_tuple in yield_labelled_rows_by_component(lab_rows):
        for db_row in yield_flat_tuples(row_tuple):
            yield db_row
    
def yield_labelled_rows_by_component(lab_rows):
    """Emit components of var-labelled rows."""
    for row in lab_rows:
        var_label = row[0]
        if var_label != "unknown_var":
            var_name = row[0] + "_" + row[1]            
            values = row[2:]
            # cleaning data             
            mod_row = [filter_value(x) for x in values]
            # breaking to annual/quarter/monthly
            reader = get_reader_func_by_row_length(values)            
            year, annual_value, qtr_values, monthly_values = reader(mod_row)
            yield var_name, year, annual_value, qtr_values, monthly_values 
 
SAFE_NONE = -1
  
def yield_flat_tuples(row_tuple):
    """Generate flat tuples (freq, year, qtr, month, label, val) from row components."""
    vn, y, a, qs, ms = row_tuple
        
    if a is not None:
               yield ("a", vn, y, SAFE_NONE, SAFE_NONE, a)

    if qs is not None:         
        for i, val in enumerate(qs):
            if val is not None:
               yield ("q", vn, y, i+1, SAFE_NONE, val)

    if ms is not None:         
        for j, val in enumerate(ms):
            if val is not None:
               yield ("m", vn, y, SAFE_NONE, j+1, val)
           
#------------------------------------------------------------------------------
#  Read rows by annual, qtr, month section 
#------------------------------------------------------------------------------

# split* functions return (year, annual value, quarterly values list, monthly values list) 

def split_row_by_periods(row):           
    """Year A Q Q Q Q M*12"""
    return int(row[0]), row[1], row[2:2+4], row[2+4:2+4+12]

def split_row_by_months(row):         
    """Year M*12"""
    return int(row[0]), None, None, row[1:12+1]
    
def split_row_by_months_and_annual(row):         
    """Year A M*12"""
    return int(row[0]), row[1], None, row[2:12+2]

def split_row_by_accum_qtrs(row):         
    """Year Annual AccumQ1 AccumH1 Accum9mo"""
	# Год Year	I квартал Q 1	I полугодие 1st half-year	Январь-сентябрь January-September
    # WARNING: may interfere with other qtr readers  
    return int(row[0]), row[1], row[2:2+3] + [row[1]], None    

def split_row_by_year_and_qtr(row):         
    """Year A Q Q Q Q"""
    return int(row[0]), row[1], row[2:2+4], None    
	
    
ROW_LENGTH_TO_FUNC = { 1+1+4+12: split_row_by_periods, 
                           1+12: split_row_by_months,
                         1+1+12: split_row_by_months_and_annual,
                            1+4: split_row_by_accum_qtrs,
                          1+1+4: split_row_by_year_and_qtr
							}

def get_reader_func_by_row_length(row):
    return ROW_LENGTH_TO_FUNC[len(row)]       

#------------------------------------------------------------------------------
#  Filter data on db import
#------------------------------------------------------------------------------

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
   """Converts *text* to float number assuming it may contain 'comment)'  or other unexpected contents"""
   text = text.replace(",",".")
   if ')' in text:
       text = process_text_with_bracket(text)
   if text == "" or text == "…":       
       return None   
   else:       
       try: 
          return float(text)
	   # WARNING: bad error handling, needs testing.  	  
       except ValueError:
          return "### This value encountered error on import - refer to stream.filter_value() for code ###"       