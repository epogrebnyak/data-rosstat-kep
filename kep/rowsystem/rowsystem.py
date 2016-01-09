# -*- coding: utf-8 -*-
'''

csv_input, spec_filename, cfg_filename = get_filenames(data_folder)  

default_spec = load_spec(spec_filename)
segments = load_segments(cfg_filename)

Must support call like:
rs = doc_to_rowsystem(csv_input)
rs = label_rowsystem(rs1, default_spec, segments)
dfa = get_annual_df(rs)

'''
import re
import os
from pprint import pprint

import pandas as pd
from pandas.util.testing import assert_frame_equal

from datetime import date, datetime
from calendar import monthrange
from spec_io import load_spec, load_cfg

import spec_io

UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]
SAFE_NONE = -1

def init_rowsystem_from_folder(folder):
    csv, spec, cfg = spec_io.get_filenames(folder)
    if not os.path.exists(csv):
        raise FileNotFoundError(csv)
    rs = doc_to_rowsystem(csv)    
    default_spec = load_spec(spec)
    segments = load_cfg(cfg)
    return label_rowsystem(rs, default_spec, segments)
    
       
# =============================================================================
# READING ROWSYSTEM

def is_year(s):    
    # case for "20141)"    
    s = s.replace(")", "")
    try:
       int(s)
       return True        
    except ValueError:
       return False

def is_textinfo_row(row):
    head = row['list'][0]
    if is_year(head):
       return False
    elif head == '':
       return False
    else:
       return True

def is_data_row(row):
    if is_year(row['list'][0]):
       return True
    else:
       return False

def doc_to_rowsystem(csv_input):
    """Import CSV file contents from *doc* and return corresponding rowsystem,
       where each line(row) from *doc* is presented as a dictionary containing 
       raw data and supplementary information."""
       
    if os.path.exists(csv_input): 
       rows = ''.join(spec_io.readfile(csv_input)).split('\n')
    else:
       rows = csv_input.split('\n')
       
    rowsystem = []
    for row in rows:
       rs_item = {   'string': row,  # raw string
                       'list': row.split('\t'),  # string separated coverted to list  
                 'head_label': None, # placeholder for parsing result
                 'unit_label': None, # placeholder for parsing result
                       'spec': None} # placeholder parsing specification
       rowsystem.append(rs_item)
    return rowsystem

# END READING ROWSYSTEM
# =============================================================================


# =============================================================================
# LABELLING

def emit_rowheads(rs):
    for i, row in enumerate(rs):
       try:
           head = row['list'][0]
           if head:
              yield i, head              
       except:
           pass   
   
def is_matched(head, line):
    if line:
        return head.startswith(line)
    else:
        return False  
  
def assign_parsing_specification_by_row(rs, default_spec, segment_specs):
    
    in_segment = False
    current_end_line = None
    current_spec = default_spec
    
    for i, head in emit_rowheads(rs):
        # are we in the default spec?
        if not in_segment:
            if segment_specs:
              # do we have to switch to a custom spec?
              for start_line, end_line, seg_spec in segment_specs:
                  if is_matched(head,start_line):
                      # Yes!
                      in_segment = True
                      current_spec = seg_spec
                      current_end_line = end_line
                      break
        else:
            # we are in custom spec. do we have to switch to the default spec? 
            if is_matched(head,current_end_line):
                in_segment = False
                current_spec = default_spec
                current_end_line = None                
                
            if segment_specs:    
              # ... or do we have to switch to a new custom one?                  
              for start_line, end_line, seg_spec in segment_specs:
                  if is_matched(head,start_line):
                      # Yes!
                      in_segment = True
                      current_spec = seg_spec
                      current_end_line = end_line
                      break
                
        #finished adjusting specification for i-th row 
        rs[i]['spec'] = current_spec
    return rs

# -----------------------------------------------------------------------------
#  Adjust lables based on spec dictionaries

def adjust_labels(line, cur_labels, spec_dicts):
       
    # TODO: adjust varnames and description use head_label, header_dict, unit_lable, unit_dict     
    dict_headline = spec_dicts[0]
    dict_support  = spec_dicts[1]

    """Set new primary and secondary label based on *line* contents. *line* is first element of csv row.    

    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment                                                
    causes change in primary label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon
    causes change in secondary label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file (may not be true, need to use segments then)
      - primary label followed by secondary label 
      - secondary label always at start of the line 
    """
    
    labels = cur_labels
    
    # Does anything from 'dict_headline' appear in 'line'?
    pri_and_sec_labels = get_label_in_text(line, dict_headline)
    
    # Does anything from 'dict_support' appear at the start of 'line'?    
    sec_label = get_label_on_start(line, dict_support) 
        
    if pri_and_sec_labels is not None:            
       # new variable detected! - must change both pri and sec label
       # pri_and_sec_labels, if not None, contains primary label like "PROD" and secondary lable like "yoy"                
       labels[0] = pri_and_sec_labels[0]
       labels[1] = pri_and_sec_labels[1]             
    elif sec_label is not None:
       # change sec label
       # sec_label, if not None, contains secondary lable like "yoy"
       labels[1] = sec_label
    else: 
       # this unknown variable, we reset labels
       labels = UNKNOWN_LABELS[:]
       
    return labels    

# -----------------------------------------------------------------------------
#  Extract labels from text

def get_label_on_start(text, lab_dict):         
     def _search_func_at_start(text, pat):
         return text.strip().startswith(pat)
       
     return get_label(text, lab_dict, _search_func_at_start)

def get_label_in_text(text, lab_dict):    
     def _search_func_anywhere(text, pat):
          return pat in text
       
     return get_label(text, lab_dict, _search_func_anywhere)

def get_label(text, label_dict, is_label_found_func):
    """Search function for labels. Returns new label for *text*  based on *lab_dict* and *is_label_found_func*"""    
    for pat in label_dict.keys():
        if is_label_found_func(text, pat): 
            return label_dict[pat]
    return None

# -----------------------------------------------------------------------------
# Label rowsystem

def label_rowsystem(rs, default_spec, segment_specs = None):
    """Label data rows in rowsystems *rs* using markup information from *dicts*.
       Returns *rs* with labels added in 'head_label' and 'unit_label'. 
    """

    rs = assign_parsing_specification_by_row(rs, default_spec, segment_specs)
    
    # run label adjuster     
    cur_labels = UNKNOWN_LABELS[:]    
    for i, row in enumerate(rs):
       if is_textinfo_row(row):            
              new_labels = adjust_labels(line=row['string'], 
                                         cur_labels=cur_labels, 
                                         spec_dicts=row['spec'])
              # set labels in current row of rowssystem
              rs[i]['head_label'] = new_labels[0]
              rs[i]['unit_label'] = new_labels[1]
              cur_labels = new_labels[:]
       else:
              # set labels in current row of rowssystem
              rs[i]['head_label'] = cur_labels[0]
              rs[i]['unit_label'] = cur_labels[1]
              
    return rs

# END LABELLING
# =============================================================================


# =============================================================================
# QUERY ROWSYSTEM

# ------------------------------------------------------------------------------
# Read rows by annual, qtr, month section 
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

'''
	Год Year	Янв. Jan.	Янв-фев. Jan-Feb	I квартал Q1	Янв-апр. Jan-Apr	Янв-май Jan-May	I полугод. 1st half year	Янв-июль Jan-Jul	Янв-авг. Jan-Aug	Янв-cент. Jan-Sent	Янв-окт. Jan-Oct	Янв-нояб. Jan-Nov
Консолидированные бюджеты субъектов Российской Федерации, млрд.рублей / Consolidated budgets of constituent entities of the Russian Federation, bln rubles												
1999	653,8	22,7	49,2	91,5	138,7	185,0	240,0	288,5	345,5	400,6	454,0	528,0
   0	    1	   2       3 	   4	    5	    6	    7	    8	    9	   10	   11	   12
'''

def split_row_fiscal(row):         
    return int(row[0]), [row[x] for x in [3,6,9,1]], row[2:2+11] + row[1]

def special_case_testing(row):         
    return int(row[0]), row[1], None, None

#test_row = "1999	653,8	22,7	49,2	91,5	138,7	185,0	240,0	288,5	345,5	400,6	454,0	528,0"
#print(split_row_fiscal(test_row))
#TODO: ERROR - cannot read fiscal indicators because their length is same monthly, but order of columns is diffferent
    
ROW_LENGTH_TO_FUNC = { 1+1+4+12: split_row_by_periods, 
                           1+12: split_row_by_months,
                         1+1+12: split_row_by_months_and_annual,
                            1+4: split_row_by_accum_qtrs,
                          1+1+4: split_row_by_year_and_qtr,
                            1+1: special_case_testing
}

def get_reader_func_by_row_length(row):
    return ROW_LENGTH_TO_FUNC[len(row)]       

# ------------------------------------------------------------------------------
# Filter data on db import

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
       
# ---------------------------------------------------
# Get dataframes 

def is_labelled(rs):
    labs = [row['head_label'] for row in get_raw_data_rows(rs) if row['head_label'] is not None]
    return len(labs) > 0
 
# yeild all data rows from rowsystem
def get_raw_data_rows(rs):
   for row in rs:
      if is_data_row(row):
          yield row

def get_labelled_rows_by_component(rs):
   for row in get_raw_data_rows(rs):
         if row['head_label'] == UNKNOWN_LABELS[0]:
             pass
         else:
             var_name = row['head_label'] + "_" + row['unit_label']
             filtered_list = [filter_value(x) for x in row['list']]
             reader = get_reader_func_by_row_length(filtered_list)            
             year, annual_value, qtr_values, monthly_values = reader(filtered_list)
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
 
def db_tuple_to_dict(db_tuple):
    return {'freq'    :db_tuple[0],
            'varname' :db_tuple[1],
            'year'    :db_tuple[2],
            'qtr'     :db_tuple[3],
            'month'   :db_tuple[4],
            'value'   :db_tuple[5]}

def stream_flat_data(rs):
     """Emit varname-labeled rows as flat database-ready rows."""
     for row_tuple in get_labelled_rows_by_component(rs):
         for db_row in yield_flat_tuples(row_tuple):
             yield db_row 

def data_stream(rs, freq, keys):
   # MAY DO: raise excetion if not labelled
   for db_row in stream_flat_data(rs):
          d = db_tuple_to_dict(db_row)
          if d['freq'] == freq:
              yield {k: d[k] for k in keys}

def annual_data_stream(rs):
     return data_stream(rs, 'a', ['varname', 'year', 'value'])

def qtr_data_stream(rs):
     return data_stream(rs, 'q', ['varname', 'year', 'qtr', 'value'])

def monthly_data_stream(rs):
     return data_stream(rs, 'm', ['varname', 'year', 'month', 'value'])
   
def get_annual_df(rs):
    """Returns pandas dataframe with annual data from labelled rowsystem *rs*."""
    # MAYDO: raise excetion if not labelled
    
    def duplicate_labels(df):
           r = df[df.duplicated(['varname','year']) == True]
           return r['varname'].unique()
       
    def check_for_dups(df): 
           dups = duplicate_labels(df)
           if len(dups) > 0:
               raise Exception("Duplicate labels: " + " ".join(dups))

    flat_df = pd.DataFrame(annual_data_stream(rs))
    dfa = flat_df.pivot(columns='varname', values='value', index='year')
    #TODO: 
    #check_for_dups(dfa)
    return dfa

def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])
    
def get_qtr_df(rs):
    """Returns pandas dataframe with QUARTERLY data from labelled rowsystem *rs*."""
    
    # get datastream     
    dfq = pd.DataFrame(qtr_data_stream(rs))
    
    # add time index
    dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
    dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")

    # reshape
    dfq = dfq.pivot(columns='varname', values='value', index='time_index')
    
    # add extra columns
    dfq.insert(0, "year", dfq.index.year)    
    dfq.insert(1, "qtr", dfq.index.quarter)
    return dfq

def get_monthly_df(rs):
    """Returns pandas dataframe with MONTHLY data from labelled rowsystem *rs*."""
    # get datastream     
    dfm = pd.DataFrame(monthly_data_stream(rs))
    
    # add time index
    dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
    dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")

    # reshape
    dfm = dfm.pivot(columns='varname', values='value', index='time_index')
    
    # add extra columns
    dfm.insert(0, "year", dfm.index.year)
    dfm.insert(1, "month", dfm.index.month)
    return dfm
    
def dfs(rs):
    dfa = get_annual_df(rs)
    dfq = get_qtr_df(rs)
    dfm = get_monthly_df(rs)
    return dfa, dfq, dfm

def unique(x):
    return list(set(x))
    
def collect_full_labels(rs):
    assert is_labelled(rs)
    varnames = unique(db_tuple_to_dict(t)['varname'] for t in stream_flat_data(rs))
    return sorted(varnames)    

def collect_head_labels(rs):
    return sorted(unique(spec_io.get_var_abbr(name) for name in collect_full_labels(rs)))
    
# END QUERY ROWSYSTEM
# =============================================================================


# --- classes ---

#rs = RowSystem(csv_input) # read raw csv into class instance
#rs.label(dicts) #add lables to csv rows based on dicts  
#rs.label(dicts, segments) #add lables to csv rows based on core dicts and segments information
#dfa = rs.dfa( # get annual dataframe from labelled rows
#dfq = rs.dfq() # get quarterly dataframe from labelled rows
#dfm = rs.dfm() # get monthly dataframe from labelled rows


'''
class RowSystem:

   def __init__(self, doc):
       # parse dataframe
       self.dataframe = # parsed dataframe

   def label(self, dicts):
       # Process self.dataframe
       self.dataframe = # replace self.dataframe

   def annual(self):
       # same as label
'''