# -*- coding: utf-8 -*-

# from word import get_label, yield_row_with_labels


def get_label(text, lab_dict, search_function):
    """Return new label for 'text' based on 'lab_dict' and 'search_function'
    """    
    for pat in lab_dict.keys():
        if search_function(text, pat): 
            return lab_dict[pat]            
            
    # this 'text' value will not cause change in labels    
    return False

# search functions
def sf_start(text, pat):
   return text.strip().startswith(pat)

def sf_anywhere(text, pat):
   return pat in text   

# wrappers        
def get_label_on_start(text, lab_dict):    
     return get_label(text, lab_dict, sf_start)

def get_label_in_text(text, lab_dict):    
     return get_label(text, lab_dict, sf_anywhere)

# *****************************************************************************    

def adjust_labels(line, cur_labels, dict_headline, dict_support):
    """Set new primary and secondary label based on 'line' contents.

    'line' is first element of csv row, for example:    

    Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
    (causes change in primary label)
    
    or    
    
    отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon
    (causes change in secondary label)
    
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
       labels = ["unknown_var", "unknown_unit"]
    return labels    
   
# *****************************************************************************    

def is_year(s):
    try:
        int(s)
        return True        
    except:
        return False
        
def yield_row_with_labels(incoming_rows, dict_headline, dict_support):
    """ Return data rows with assigned labels."""
    labels = ["unknown_var", "unknown_unit"]
    for row in incoming_rows:
        if len(row[0]) > 0:
            if not is_year(row[0]):
                # not a data row, change label
                labels = adjust_labels(row[0], labels, dict_headline, dict_support)
            else:
                # data, row assign label and yield
                yield(labels + row)
                

# *****************************************************************************                   