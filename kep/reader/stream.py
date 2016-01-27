"""dicts_as_stream() applies to RowSystem instance to obtain a stream on flat dicts from it."""

import re

# -----------------------------------------------------------------------------------------------
#       
# 1. SPLIT BY COLUMN AND FILTER ROWS
#    Read rows by annual, qtr, month section 
#    split* functions return (year, annual value, quarterly values list, monthly values list) 
#
# -----------------------------------------------------------------------------------------------

SAFE_NONE = -1

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

def special_case_testing(row):         
    return int(row[0]), row[1], None, None

    
ROW_LENGTH_TO_FUNC = { 1+1+4+12: split_row_by_periods, 
                           1+12: split_row_by_months,
                         1+1+12: split_row_by_months_and_annual,
                            1+4: split_row_by_accum_qtrs,
                          1+1+4: split_row_by_year_and_qtr,
                            1+1: special_case_testing
}
    
# fiscal row sample
'''
	Год Year	Янв. Jan.	Янв-фев. Jan-Feb	I квартал Q1	Янв-апр. Jan-Apr	Янв-май Jan-May	I полугод. 1st half year	Янв-июль Jan-Jul	Янв-авг. Jan-Aug	Янв-cент. Jan-Sent	Янв-окт. Jan-Oct	Янв-нояб. Jan-Nov
Консолидированные бюджеты субъектов Российской Федерации, млрд.рублей / Consolidated budgets of constituent entities of the Russian Federation, bln rubles												
1999	653,8	22,7	49,2	91,5	138,7	185,0	240,0	288,5	345,5	400,6	454,0	528,0
   0	    1	   2       3 	   4	    5	    6	    7	    8	    9	   10	   11	   12
'''

def split_row_fiscal(row):         
    return int(row[0]), row[1], [row[x] for x in [3,6,9,1]], row[2:2+11] + [row[1]]

SPECIAL_FUNC_NAMES_TO_FUNC = {'fiscal': split_row_fiscal}
   
def get_reader_func_by_row_length_and_special_dict(row, reader):

   if reader is None:
        return ROW_LENGTH_TO_FUNC[len(row)]

   elif reader in SPECIAL_FUNC_NAMES_TO_FUNC.keys():
        return SPECIAL_FUNC_NAMES_TO_FUNC[reader]

   else:
        raise ValueError("Special reader function not recognised: " + rdr + ".\nTry checking spec file.")    
   

# -----------------------------------------------------------------------------------------------
#       
# 2. FILTER ROWS
#    Read rows by annual, qtr, month section 
#    split* functions return (year, annual value, quarterly values list, monthly values list) 
#
# -----------------------------------------------------------------------------------------------

# Allows to catch a value with with comment) or even double comment
_COMMENT_CATCHER = re.compile("([\d.]*)\s*(?=\d\))")

def kill_comment(text):    
    return _COMMENT_CATCHER.match(text).groups()[0]

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

# -----------------------------------------------------------------------------------------------
#       
# 3. STREAM DATA AS DICTS
#
# -----------------------------------------------------------------------------------------------

def get_labelled_rows_by_component(rs):
   for i, row, label, reader in rs.labelled_data_rows:
        var_name = label.labeltext
        filtered_list = [filter_value(x) for x in row]             
        reader_func = get_reader_func_by_row_length_and_special_dict(row, reader)            
        year, annual_value, qtr_values, monthly_values = reader_func(filtered_list)
        yield var_name, year, annual_value, qtr_values, monthly_values

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
 
def stream_flat_data(rs):
     """Emit varname-labeled rows as flat database-ready rows."""
     for row_tuple in get_labelled_rows_by_component(rs):
         for db_row in yield_flat_tuples(row_tuple):
             yield db_row 

def db_tuple_to_dict(db_tuple):
    return {'freq'    :db_tuple[0],
            'varname' :db_tuple[1],
            'year'    :db_tuple[2],
            'qtr'     :db_tuple[3],
            'month'   :db_tuple[4],
            'value'   :db_tuple[5]}
             
def dicts_as_stream(rs):
    for db_row in stream_flat_data(rs):
        out = db_tuple_to_dict(db_row)
        yield out