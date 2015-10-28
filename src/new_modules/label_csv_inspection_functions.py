# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:47:43 2015

@author: EP
"""

    
###############################################################################
# DO NOT CHECK CODE BELOW THIS LINE - it is inspection functions 
    
    
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
    gen_out = yield_valid_rows_with_labels(gen_in, headline_dict, support_dict)

    z2 = list(v[0] for k,v in headline_dict.items())
    print ("\nVars in spec:")
    print(list_as_string(z2))
    
    z1 = list(set(row[0] for row in gen_out))
    print ("Vars in labelled csv:")
    print(list_as_string(z1))
     
    not_in_file = [x for x in z2 if x not in z1] 
    
    if not_in_file:
        print ("Not loaded to labelled csv:")
        print (list_as_string(not_in_file))
    else:
        print ("Variables in spec and in labelled csv file match.\n")
        
    return not_in_file 
    
def inspect_labelled_output(p):
    f = get_raw_csv_filename(p)
    # open csv
    gen_in = yield_csv_rows(f)
    # produce new rows
    headline_dict, support_dict = load_spec(p)    
    print_rows_with_labels(gen_in, headline_dict, support_dict)
    
def print_rows_with_labels(incoming_rows, dict_headline, dict_support):
    for row, labels, data_row in yield_all_rows_with_labels(incoming_rows, 
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

#______________________________________________________________________________
#
#  Make CSV with labelled rows - using segmentation
#______________________________________________________________________________

def _yield_segment_from_stream(source_stream, start_line, end_line):
    pass

def _label_stream(stream, headline_dict, support_dict):
    return yield_valid_rows_with_labels(stream, headline_dict, support_dict)

def _label_segment(raw_stream, list_of_boundary_lines, list_of_specification_dicts):
    headline_dict = specification['headline']
    support_dict  = specification['support']
    # obtain filename
    f = get_raw_csv_filename(p)
    # open csv
    gen_in = yield_csv_rows(f)
    # read specification
    headline_dict, support_dict = load_spec(p)    
    # produce rows with labels
    return yield_valid_rows_with_labels(gen_in, headline_dict, support_dict)
