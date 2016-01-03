# -*- coding: utf-8 -*-
"""Read raw CSV file and emit labelled rows based on specification.

get_labelled_rows(raw_data_file, spec_file, cfg_file = None) 
    # Returns a list of labelled rows    
    #  raw_data_file - raw csv file with data
    #  spec_file     - header and unit definitions
    #  config_file   - segment information: start rows, end rows, spec files for each segment"""


import os
from pprint import pprint
from kep.file_io.common import yield_csv_rows
from kep.file_io.specification import load_spec, load_cfg

UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]

#------------------------------------------------------------------------------
#  label_csv main function
#------------------------------------------------------------------------------

def get_labelled_rows(raw_data_file, spec_file, cfg_file = None):
    """ Returns a list of labelled rows    
       raw_data_file - raw csv file with data
       spec_file     - header and unit definitions
       config_file   - segment information: start rows, end rows, spec files for each segment"""

    #  the difference between calls is cfg file     
    if cfg_file is not None:
        return get_labelled_rows_by_segment(raw_data_file, spec_file, cfg_file)
    else:
        return get_labelled_rows_no_segments(raw_data_file, spec_file)

#------------------------------------------------------------------------------
#  Labelize based on single spec file - get_labelled_rows_no_segments()
#------------------------------------------------------------------------------

def get_labelled_rows_no_segments(raw_data_file, yaml_spec_file):
    raw_rows = yield_csv_rows(raw_data_file)
    spec_dicts = load_spec(yaml_spec_file)
    return raw_to_labelled_rows(raw_rows, spec_dicts)

def raw_to_labelled_rows(raw_rows, spec_dicts):
    return list(yield_valid_rows_with_labels(raw_rows, spec_dicts))
    
def yield_valid_rows_with_labels(incoming_rows, spec_dicts):
    """ Return non-empty data rows with assigned labels."""
    for incoming_row, labels, data_row in yield_all_rows_with_labels(incoming_rows, spec_dicts):
        if data_row is not None:
            yield labels + data_row
      
def yield_all_rows_with_labels(incoming_rows, spec_dicts):
    """ Returns (incoming_row, labels, data_row) tuple. """
    labels = UNKNOWN_LABELS[:] 
    for row in incoming_rows:
        if row[0]:
            if not is_year(row[0]):
                # not a data row, change label
                labels = adjust_labels(row[0], labels, spec_dicts)
                yield row, labels, None
            else:
                # data row, use current label and yield                
                yield row, labels, row
        else:
            yield row, None, None
            
#------------------------------------------------------------------------------
#  Labelize based both on spec and config file -  get_labelled_rows_by_segment()
#------------------------------------------------------------------------------

def get_labelled_rows_by_segment(raw_data_file, yaml_spec_file, yaml_cfg_file):
    raw_rows = list(yield_csv_rows(raw_data_file))     
    default_dicts = load_spec(yaml_spec_file)
    segment_specs = load_cfg(yaml_cfg_file)
    return label_raw_rows_by_segment(raw_rows, default_dicts, segment_specs)

#------------------------------------------------------------------------------
#  For file inspection
#------------------------------------------------------------------------------
    
def emit_raw_non_data_rows(raw_data_file):
    for row in yield_csv_rows(raw_data_file):
        if not is_year(row[0]):
            yield row

def get_nondata_rows(raw_data_file):
    return list(emit_raw_non_data_rows(raw_data_file))            
    
#------------------------------------------------------------------------------
#    Read segments from config file
#------------------------------------------------------------------------------

def label_raw_rows_by_segment(raw_rows, default_dicts, segment_specs):
    """Returns list of labelled rows, based on default specification and segment info."""
    labelled_rows = []
    labels = UNKNOWN_LABELS[:]    
    for row, spec_dicts in emit_row_and_spec(raw_rows, default_dicts, segment_specs):
        if not is_year(row[0]):
            # label-switching row
            labels = adjust_labels(row[0], labels, spec_dicts)
        else:
            # data row
            labelled_rows.append(labels + row)
    return labelled_rows
    
def emit_row_and_spec(raw_rows, default_dicts, segment_specs):
    """Yields tuples of valid row and corresponding specification dictionaries.
       Works through segment_specs to determine right spec dict for each row."""       

    in_segment = False
    current_spec = default_dicts
    current_end_line = None

    for row in raw_rows:
        if len(row) == 0:
            # junk/empty row, ignore it, pass 
            continue        
        if not row[0]:
            # junk row, ignore it, pass 
            continue
        # are we in the default spec?
        if not in_segment:
            # Do we have to switch to a custom spec?
            for start_line, end_line, spec in segment_specs:
                if row[0].startswith(start_line):
                    # Yes!
                    in_segment = True
                    current_spec = spec
                    current_end_line = end_line
                    break
        else:
            # We are in a custom spec. Do we have to switch to the default one 
            if row[0].startswith(current_end_line):
                in_segment = False
                current_spec = default_dicts
                current_end_line = None                
                
            # ... or new custom one?                  
            for start_line, end_line, spec in segment_specs:
                if row[0].startswith(start_line):
                    # Yes!
                    in_segment = True
                    current_spec = spec
                    current_end_line = end_line
                    break
             
        yield row, current_spec

# -----------------------------------------------------------------------------
#    Adjust lables based on spec dictionaries
# -----------------------------------------------------------------------------

def adjust_labels(line, cur_labels, spec_dicts):
    dict_headline = spec_dicts[0]
    dict_support  = spec_dicts[1]
    return _adjust_labels(line, cur_labels, dict_headline, dict_support)

def _adjust_labels(line, cur_labels, dict_headline, dict_support):
    """Set new primary and secondary label based on *line* contents.
    *line* is first element of csv row.    

    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
    causes change in primary label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon
    causes change in secondary label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file (often not true)
      - primary label followed by secondary label 
      - secondary label always at start of the line 
    """
    
    print("\n-----------")
    pprint(line)
    pprint(dict_headline)
    pprint(dict_support)
    pprint(cur_labels)
    
    #NOTE: may need to run default dict through the file to see if label is unique
    
    labels = cur_labels
    # Does anything from 'dict_headline' appear in 'line'?
    two_labels_list = get_label_in_text(line, dict_headline)
    # Does anything from 'dict_support' appear at the start of 'line'?    
    sec_label = get_label_on_start(line, dict_support) 
        
    if two_labels_list is not None:            
       # reset to new var - change both pri and sec label
       # two_labels_list, if not None, contains primary label like "PROD" and secondary lable like "yoy"                
       labels[0] = two_labels_list[0]
       labels[1] = two_labels_list[1]             
    elif sec_label is not None:
       # change sec label    
       # sec_label, if not None, contains secondary lable like "yoy"
       labels[1] = sec_label
    else: 
       # unknown var, reset labels
       labels = UNKNOWN_LABELS[:]
    pprint(labels)
    return labels    

def is_year(s):    
    # "20141)"    
    s = s.replace(")", "")
    try:
        int(s)
        return True        
    except ValueError:
        return False

# -----------------------------------------------------------------------------
#  Adjust labels - extract labels from text 
# -----------------------------------------------------------------------------

# end-use wrappers        
def get_label_on_start(text, lab_dict):    
     return get_label(text, lab_dict, sf_start)

def get_label_in_text(text, lab_dict):    
     return get_label(text, lab_dict, sf_anywhere)

# search function for labels
def get_label(text, label_dict, is_label_found_func):
    """Return new label for *text* based on *lab_dict* and *is_label_found_func*
    """    
    for pat in label_dict.keys():
        if is_label_found_func(text, pat): 
            return label_dict[pat]
    return None

# *is_label_found_func* search functions
def sf_start(text, pat):
   return text.strip().startswith(pat)

def sf_anywhere(text, pat):
   return pat in text