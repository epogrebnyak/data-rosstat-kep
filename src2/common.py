# -*- coding: utf-8 -*-
"""CSV input/output."""

import csv
import os
 
def get_filenames(data_folder):
    csv  = os.path.join(data_folder, "tab.csv")
    spec = os.path.join(data_folder, "tab_spec.txt")
    сfg =  os.path.join(data_folder, "tab_cfg.txt")
    return csv, spec, сfg
 
#def infolder(folder, file):
#   path = os.path.join(folder, file)
#   if os.path.isfile(path):
#       return path 
#   else:
#       raise FileNotFoundError(path)

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
# Dump of test files in subfolder
#------------------------------------------------------------------------------

SUBFOLDER = "temp"

def docstring_to_file(docstring, filename, subfolder = SUBFOLDER):
    path = os.path.join(subfolder, filename)
    with w_open(path) as f:
        f.write(docstring)
    return path

#------------------------------------------------------------------------------
# YAML import 
#------------------------------------------------------------------------------

import yaml 

def _get_yaml(filename):
    with r_open(filename) as file:
        spec = yaml.load_all(file) 
        return list(spec)   

def _get_safe_yaml(filename):        
    try:
        return _get_yaml(filename)
    except FileNotFoundError:
        raise FileNotFoundError ("YAML file not found: " + filename)
    except:
        raise Exception ("Error parsing YAML file: " + filename)

#------------------------------------------------------------------------------
# Testing            
#------------------------------------------------------------------------------

def test_io():
    doc = """- Something looking like a yaml
- Но обязательно с русским текстом
---
key1 : with two documents 
key2 : который будет глючить с кодировкой."""
    p = docstring_to_file(doc, "doc.txt")
    assert doc == "\n".join([x[0] for x in yield_csv_rows(p)])
    y = _get_yaml(p)
    assert y[0][0] == 'Something looking like a yaml'
    
#------------------------------------------------------------------------------
            
if __name__ == "__main__":
    test_io()