# -*- coding: utf-8 -*-
"""Read raw CSV file and write a file with labelled rows."""

#try:
#    from .common import get_raw_csv_filename, get_labelled_csv_filename
#    from .common import yield_csv_rows, dump_iter_to_csv
#    from .spec import load_spec
#except SystemError:

from common import get_raw_csv_filename, get_labelled_csv_filename, get_spec_filename
from common import yield_csv_rows, dump_iter_to_csv
from load_spec import load_spec
    
#______________________________________________________________________________
#
#  Make CSV with labelled rows - entry functions
#______________________________________________________________________________

def yield_labelled_rows(p):
    # obtain filenames
    raw_file = get_raw_csv_filename(p)
    spec_file = get_spec_filename(p)
    # get labelled rows as iterator
    return _get_labelled_rows_as_iterator_based_on_specfile(raw_file, spec_file)

def dump_labelled_rows_to_csv(p):
    gen_out = yield_labelled_rows(p)
    # obtain filename    
    f = get_labelled_csv_filename(p)
    # save to file
    dump_iter_to_csv(gen_out, f)

def _get_labelled_rows_as_iterator_based_on_specfile(raw_file, spec_file):
    raw_rows_iterator = yield_csv_rows(raw_file)
    headline_dict, support_dict = load_spec(spec_file)
    return yield_valid_rows_with_labels(raw_rows_iterator, headline_dict, support_dict)

def get_labelled_rows(raw_file, spec_file):
    labelled_rows_iterator = _get_labelled_rows_as_iterator_based_on_specfile(raw_file, spec_file)
    return list(labelled_rows_iterator)

#______________________________________________________________________________
#
#  Get rows with assigned labels
#______________________________________________________________________________

UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]

def yield_valid_rows_with_labels(incoming_rows, dict_headline, dict_support):
    """ Return non-empty data rows with assigned labels."""
    for incoming_row, labels, data_row in yield_all_rows_with_labels(incoming_rows, 
                                                  dict_headline, dict_support):
        if data_row is not None:
            yield labels + data_row
      
def yield_all_rows_with_labels(incoming_rows, dict_headline, dict_support):
    """ Returns (incoming_row, labels, data_row) tuple. """
    
    # copying the list to different variable, cannot assign by '=' only
    labels = UNKNOWN_LABELS[:] # [x for x in UNKNOWN_LABELS]
    
    # unpack incoming iterator
    for row in incoming_rows:
        if row[0]:
            if not is_year(row[0]):
                # not a data row, change label
                labels = adjust_labels(row[0], labels, dict_headline, dict_support)
                yield row, labels, None
            else:
                # data row, assign label and yield                
                yield row, labels, row
        else:
            yield row, None, None

def is_year(s):    
    # "20141)"    
    s = s.replace(")", "")
    try:
        int(s)
        return True        
    except ValueError:
        return False
        
def adjust_labels(line, cur_labels, dict_headline, dict_support):
    """Set new primary and secondary label based on *line* contents.
    *line* is first element of csv row.    

    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
    causes change in primary label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon
    causes change in secondary label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file
      - primary label followed by secondary label 
      - secondary label always at start of the line 
    """
    
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
    return labels    
                
#______________________________________________________________________________
#
#  Extract labels from text based on dictionaries 
#______________________________________________________________________________

# wrappers        
def get_label_on_start(text, lab_dict):    
     return get_label(text, lab_dict, sf_start)

def get_label_in_text(text, lab_dict):    
     return get_label(text, lab_dict, sf_anywhere)

# *is_label_found_func* search functions
def sf_start(text, pat):
   return text.strip().startswith(pat)

def sf_anywhere(text, pat):
   return pat in text   

# search function for labels
def get_label(text, label_dict, is_label_found_func):
    """Return new label for *text* based on *lab_dict* and *is_label_found_func*
    """    
    for pat in label_dict.keys():
        if is_label_found_func(text, pat): 
            return label_dict[pat]
    return None

# --------------------------------------------------------------
# Testing 

def print_rows(list_):
    print("Printing list by row in compact form:")
    for row in list_:
         print(" ".join(row[0:6]) + ' ... ' + row[-1])

def test_label_csv():
    from hardcoded import init_raw_csv_file, init_main_yaml, PARSED_RAW_FILE_AS_LIST
    RAW_FILE = init_raw_csv_file()        
    SPEC_FILE = init_main_yaml()
    
    labelled_rows_as_list = get_labelled_rows(RAW_FILE, SPEC_FILE)
    assert labelled_rows_as_list == PARSED_RAW_FILE_AS_LIST    

    print("Import ok...\n")
    print_rows(labelled_rows_as_list)    

if __name__ == "__main__":
    test_label_csv()