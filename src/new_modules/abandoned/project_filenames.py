"""Project filename conventions"""

# -*- coding: utf-8 -*-

import csv
import os

#______________________________________________________________________________
#
#  Project filenames
#______________________________________________________________________________

def get_doc_filename(f):
    return change_extension(f, "doc")
    
def get_raw_csv_filename(f):
    return change_extension(f, "csv")

def get_labelled_csv_filename(f):
    return change_extension(f, "txt")

def get_spec_filename(f):
    if "_spec" not in f:
        return get_basename(f) + "_spec.txt"
    else:
        return f        
        
def get_headers_filename(f):    
    return get_basename(f) + "_headers.txt"
    
def get_reference_csv_filename(f):    
    return get_basename(f) + "_reference_dataset.txt"
    
def get_varlist_filename(f): 
    if "_spec" in f:
        return f.replace("_spec", "_var_list")
    else:         
        return get_basename(f) + "_var_list.txt"
#______________________________________________________________________________
#
#  Filename manipulation
#______________________________________________________________________________

def change_extension(p, newext):
    if not newext.startswith("."):
        newext = "." + newext
    return os.path.splitext(p)[0] + newext

def get_basename(p):
    return os.path.splitext(p)[0]
        
