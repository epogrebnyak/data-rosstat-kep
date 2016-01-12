# -*- coding: utf-8 -*-

import re
import os
from pprint import pprint
import itertools

import pandas as pd
from pandas.util.testing import assert_frame_equal

from definitions import InputDefinition
from label import label_rs
from stream import dicts_as_stream

#UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]
#SAFE_NONE = -1

class RowSystem():
    
    def read_definition(self, *arg):
    	folder = arg[0] 
	self.in_def = InputDefinition(folder)
	self.rs = doc_to_rowsystem(in_def)    
	
    def label(self):
    	self.rs = label_rs(self.rs, sekf.in_def)
    
    def __init__(*arg):
        # read definition
        self.read_definition(*arg)
        # label rows
        self.label()
        # allow call like rs.data.dfa()
        self.data = DataframeEmitter(self.dicts_as_iter())

    def dicts_as_iter(self):
    	return dicts_as_stream(self.rs)

    def save(self):
        DefaultDatabase().save_stream(gen = self.dicts_as_iter())
    
       
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

def doc_to_rowsystem(input_definition):
    """Import CSV file contents from *input_definition* and return corresponding rowsystem,
       where each line(row) from *input_definition,rows* is presented as a dictionary containing 
       raw data and supplementary information."""
       
    rowsystem = []
    for row in input_definition.rows:
       rs_item = {   'string': row,  # raw string
       #MAYDO: remove 'list'
                       'list': row.split('\t'),  # string separated coverted to list  
                      'label': None, # placeholder for parsing result
                       'spec': None} # placeholder parsing input (specification)
       rowsystem.append(rs_item)
    return rowsystem

# END READING ROWSYSTEM
# =============================================================================


# =============================================================================
# LABELLING

# label.py

# END LABELLING
# =============================================================================


# =============================================================================
# EMIT DATA FROM ROWSYSTEM

# stream.py

#END EMIT DATA FROM ROWSYSTEM
#--------------------------------------------------------------
             


# =============================================================================    
# QUERY LABELS

#------------------------------------------------------------------------------
#  Variable label manipulation
#------------------------------------------------------------------------------
def get_var_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))
assert get_var_abbr('PROD_E_TWh') == 'PROD_E' 

def get_unit_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))
assert get_unit_abbr('PROD_E_TWh') == 'TWh'

     
def unique(x):
    return sorted(list(set(x)))

# labels in rowsystem data    
def rowsystem_full_labels(rs):
    assert is_labelled(rs)
    varnames = unique(db_tuple_to_dict(t)['varname'] for t in stream_flat_data(rs))
    return sorted(varnames)    
    
def rowsystem_head_labels(rs):
    return unique([get_var_abbr(name) for name in rowsystem_full_labels(rs)])


folder = os.path.dirname(os.path.realpath(__file__))
rs = init_rowsystem_from_folder(folder)
print(rowsystem_head_labels(rs))    

    
    
# labels in definition files    
def definition_full_labels(folder):
     pass
     
def definition_full_labels(folder):
     pass

def get_user_defined_full_labels(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return unique(hdr+seg)

def get_user_defined_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return unique(hdr+seg)

def get_spec_and_cfg_varnames(data_folder):
    csv, default_spec, segments = get_folder_definitions(folder)
    header_dict = default_spec[0]
    hdr = unpack_header_dict(header_dict)
    seg = unpack_segments(segments)
    return hdr, seg
    
def unpack_header_dict(header_dict):
   """Get varnames from header_dict"""
   return list(x[0] for x in header_dict.values())

def unpack_segments(segments):
   """Get varnames from segments"""
   var_list = []
   for seg in segments:
       seg_var_list =  unpack_header_dict(seg[2][0])       
       var_list.extend(seg_var_list)
   return var_list    

    
# =============================================================================    
