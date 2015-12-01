# -*- coding: utf-8 -*-
"""Generate stream of database-ready rows from var-labelled rows with mixed frequencies.

   Entry point: stream_flat_data(lab_rows)
   
   """

import re

#------------------------------------------------------------------------------
#  Read rows by annual, qtr, month section 
#------------------------------------------------------------------------------

def stream_flat_data(lab_rows):
    """Emit varname-labeled rows as flat database-ready rows."""
    for row_tuple in yeild_labelled_rows_by_component(lab_rows):
        for db_row in yield_flat_tuples(row_tuple):
            yield db_row
    
def yeild_labelled_rows_by_component(lab_rows):
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

def split_row_by_periods(row):           
    """Year A Q Q Q Q M*12"""
    return int(row[0]), row[1], row[2:2+4], row[2+4:2+4+12]

def split_row_by_months(row):         
    """Year M*12"""
    return int(row[0]), None, None, row[1:12+1]
    
def split_row_by_months_and_annual(row):         
    """Year A M*12"""
    return int(row[0]), row[1], None, row[2:12+2]

ROW_LENGTH_TO_FUNC = { 1+1+4+12: split_row_by_periods, 
                           1+12: split_row_by_months,
                         1+1+12: split_row_by_months_and_annual }

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
   """Converts *text* to float number assuming it may contain 'comment)'."""
   text = text.replace(",",".")
   if ')' in text:
       text = process_text_with_bracket(text)
   if text == "":       
       return None
   else:       
       try: 
          return float(text)
       except ValueError:
          return "###"       

def test_flat_emitter():
    lab_rows = [['I', 'bln_rub', '2014', '13527,7', '1863,8', '2942,0', '3447,6', '5274,3', '492,2', '643,2', '728,4', '770,4', '991,1', '1180,5', '1075,1', '1168,5', '1204,0', '1468,5', '1372,5', '2433,3']   
              , ['PROD_TRANS', 'rog', '2015', '31,1', '126,3', '139,8', '83,8', '94,6', '115,8', '', '', '', '', '', '']]
    
    flat_db_rows = [('a', 'I_bln_rub', 2014, SAFE_NONE, SAFE_NONE, 13527.7),
                    ('q', 'I_bln_rub', 2014, 1, SAFE_NONE, 1863.8),
                    ('q', 'I_bln_rub', 2014, 2, SAFE_NONE, 2942.0),
                    ('q', 'I_bln_rub', 2014, 3, SAFE_NONE, 3447.6),
                    ('q', 'I_bln_rub', 2014, 4, SAFE_NONE, 5274.3),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 1, 492.2),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 2, 643.2),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 3, 728.4),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 4, 770.4),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 5, 991.1),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 6, 1180.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 7, 1075.1),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 8, 1168.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 9, 1204.0),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 10, 1468.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 11, 1372.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 12, 2433.3),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 1, 31.1),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 2, 126.3),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 3, 139.8),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 4, 83.8),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 5, 94.6),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 6, 115.8)]    
    
    assert [x for x in stream_flat_data(lab_rows)] == flat_db_rows 
   
def get_test_flat_db_rows():
    from label_csv import get_test_labelled_rows
    lab_rows = get_test_labelled_rows()
    return stream_flat_data(lab_rows)
    
if __name__ == "__main__":
    test_flat_emitter()
    for i, x in enumerate(get_test_flat_db_rows()):
        print(i, x)