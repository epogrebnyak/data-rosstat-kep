# -*- coding: utf-8 -*-
"""CSV input/output, docstring to temp file and filenames."""

import csv
import os
import itertools

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

#------------------------------------------------------------------------------
#  Filename conventions 
#------------------------------------------------------------------------------

def get_filenames(data_folder):
    """Filename conventions"""
    # TODO: also check these files exist
    csv  = os.path.join(data_folder, "tab.csv")
    spec = os.path.join(data_folder, "tab_spec.txt")
    cfg =  os.path.join(data_folder, "tab_cfg.txt")
    return csv, spec, cfg
 
#------------------------------------------------------------------------------
#  Root io functions with encoding 
#------------------------------------------------------------------------------

ENCODING = 'utf8' #'cp1251'
       
def w_open(file):
    return open(file, 'w', encoding = ENCODING)

def r_open(file):
    return open(file, 'r', encoding = ENCODING)
    
#------------------------------------------------------------------------------
# CSV IO 
#------------------------------------------------------------------------------

# todo later: recyle  delimiter='\t', lineterminator='\n'

def dump_iter_to_csv(iterable, csv_filename):
    """Copy generator *iterable* into file *csv_filename*. """    
    with w_open(csv_filename) as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row)
    return csv_filename

def yield_csv_rows(csv_filename):
    """Open csv file named *c* and return an iterable."""
    with r_open(csv_filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row

            
#------------------------------------------------------------------------------
# Dump files in test subfolder
#------------------------------------------------------------------------------

# WARNING: always assume we are in parent direcory of 'kep'
SUBFOLDER = "kep\\test\\temp"

def write_file(docstring, path):
    with w_open(path) as f:
        f.write(docstring)   

def docstring_to_file(docstring, filename):
    if os.path.exists(SUBFOLDER):
        path = os.path.join(os.getcwd(), SUBFOLDER, filename)
    else:
        path = filename
    write_file(docstring, path)
    return path

def delete_file(path):
    os.remove(path) 
    



