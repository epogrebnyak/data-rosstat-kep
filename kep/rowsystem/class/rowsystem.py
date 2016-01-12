# -*- coding: utf-8 -*-

import re
import os
from pprint import pprint
import itertools

import pandas as pd
from pandas.util.testing import assert_frame_equal

from definitions import InputDefinition
from rs_label import label_rowsystem
from rs_stream import dicts_as_stream

#UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]
#SAFE_NONE = -1

class RowSystem():
    
    def read_definition(self, *arg):
        folder = arg[0] 
        self.in_def = InputDefinition(folder)
        self.rs = doc_to_rowsystem(in_def)    
    
    def label(self):
        self.rs = label_rowsystem(self.rs, self.in_def)
    
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
# END EMIT DATA FROM ROWSYSTEM
#--------------------------------------------------------------
             


# =============================================================================    
# QUERY LABELS
# temp_query_lables.py
# =============================================================================    
