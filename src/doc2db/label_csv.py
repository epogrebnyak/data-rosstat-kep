# -*- coding: utf-8 -*-
"""
"""

from common import get_raw_csv_filename, get_labelled_csv_filename
from common import yield_csv_rows, dump_iter_to_csv
from spec import load_spec

#______________________________________________________________________________
#
#  Make CSV with labelled rows 
#______________________________________________________________________________

def yield_labelled_rows(p):
    f = get_raw_csv_filename(p)
    # open csv
    gen_in = yield_csv_rows(f)
    # produce new rows
    headline_dict, support_dict = load_spec(p)    
    return yield_row_with_labels(gen_in, headline_dict, support_dict)
    
def dump_labelled_rows_to_csv(p):
    gen_out = yield_labelled_rows(p)
    # save to file    
    f = get_labelled_csv_filename(p)
    r = dump_iter_to_csv(gen_out, f)
    return r
 
#______________________________________________________________________________
#
#  Inspection functions
#______________________________________________________________________________

def list_as_string(l):
    return  " ".join(sorted(l))

def check_vars_not_in_labelled_csv(p):
    """Returns varnames not written to labelled csv file. Prints explaination."""     
    infile = get_raw_csv_filename(p)
    headline_dict, support_dict = load_spec(p)    
    gen_in = yield_csv_rows(infile)
    gen_out = yield_row_with_labels(gen_in, headline_dict, support_dict)

    z2 = list(v[0] for k,v in headline_dict.items())
    print ("\nVars in spec:")
    print(list_as_string(z2))
    
    z1 = list(set(row[0] for row in gen_out))
    print ("\nVars in labelled csv:")
    print(list_as_string(z1))
     
    not_in_file = [x for x in z2 if x not in z1] 
    
    if not_in_file:
        print ("\nNot loaded to labelled csv:")
        print (list_as_string(not_in_file))
    else:
        print ("\nVariables in spec and in labelled csv file match.\n")
        
    return not_in_file 
    
def inspect_labelled_output(p):
    f = get_raw_csv_filename(p)
    # open csv
    gen_in = yield_csv_rows(f)
    # produce new rows
    headline_dict, support_dict = load_spec(p)    
    print_rows_with_labels(gen_in, headline_dict, support_dict)

#______________________________________________________________________________
#
#  Rows with assigned labels
#______________________________________________________________________________

def yield_row_with_labels(incoming_rows, dict_headline, dict_support):
    """ Return data rows with assigned labels."""
    for incoming_row, labels, data_row in yield_row_with_labels_core(incoming_rows, 
                                                                     dict_headline, dict_support):
        if data_row is not None:
            yield labels + data_row

def print_rows_with_labels(incoming_rows, dict_headline, dict_support):
    for row, labels, data_row in yield_row_with_labels_core(incoming_rows, 
                                                                     dict_headline, dict_support):

        def _console_filter(s):
            s = s.replace("\u201c", '"')
            s = s.replace("\u201d", '"')
            s = s.replace("\u2026", "***")
            return s
            
        print("\nIncoming row:", [_console_filter(x) for x in row])
        print("Elements in row:", len(row))
        if data_row is None:
            if labels:
                print("Labels:", labels)
            else:
                print("Length of first element in row is 0.")
        else:
            print("Emitted data row:", labels + data_row)

UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]
            
def yield_row_with_labels_core(incoming_rows, dict_headline, dict_support):
    """ Returns (incoming_row, labels, data_row) tuple.
    Useful data is when *data_row* is not None. 
    Rest of slack is for verbose printing in yield_row_with_labels_with_print(). 
    """
    labels = [x for x in UNKNOWN_LABELS]
    # unpack incoming iterator
    for row in incoming_rows:
        if len(row[0]) > 0:
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
    except:
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
      - pri label followed by sec label 
    """
    
    labels = cur_labels
    # Does anything from 'dict_headline' appear in 'line'?
    z = get_label_in_text(line, dict_headline)
    # Does anything from 'dict_support' appear at the start of 'line'?    
    w = get_label_on_start(line, dict_support) 
        
    if z:            
       # reset to new var - change both pri and sec label               
       labels[0], labels[1] = z            
    elif w:
       # change sec label
       labels[1] = w
    else: 
       # unknown var, reset labels
       labels = [x for x in UNKNOWN_LABELS]

    return labels    
                
#______________________________________________________________________________
#
#  Extract labels from text based on dictionaries 
#______________________________________________________________________________

# End-use wrappers        
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
    # False will not cause change in labels    
    return False

#______________________________________________________________________________

doc = """1.10. Внешнеторговый оборот – всего1),  млрд.долларов США / Foreign trade turnover – total1),  bln US dollars																	
1999	115,1	24,4	27,2	28,4	35,1	7,2	7,9	9,3	9,8	8,0	9,3	9,5	9,3	9,6	10,4	11,1	13,7"""

def test_iter():
    for row in [x.split("\t") for x in doc.split("\n")]:
        yield row
        

if __name__ == "__main__":
#    import os
#    p = os.path.abspath("../data/1-07/1-07.txt")
#    gen = yield_labelled_rows(p)
#    for x in gen:
#        print(x)
#
#    inspect_labelled_output(p)
    import os
    p = os.path.abspath("../data/minitab/minitab.csv")
    f = get_raw_csv_filename(p)
    # open csv
    gen_in = test_iter()
    # produce new rows
    headline_dict, support_dict = load_spec(p)    
    print_rows_with_labels(gen_in, headline_dict, support_dict)