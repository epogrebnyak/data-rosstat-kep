"""Project filename conventions and csv input/output."""

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
        
#______________________________________________________________________________
#
#  Basic CSV IO functions
#______________________________________________________________________________

def dump_iter_to_csv(iterable, csv_filename):
    """Copy generator *iterable* into file *csv_filename*. """    
    with open(csv_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row)
    return csv_filename

def yield_csv_rows(c):
    """Open csv file named *c* and return an iterable."""
    with open(c, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row

#______________________________________________________________________________
#
#  CSV slicing 
#______________________________________________________________________________

def yield_csv_rows_between_labels(c, start_label, end_label):
    """Yield part of csv file, marked by *start_label* and *end_label*"""
    emit = False
    with open(c, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            if start_label in row[0]:
                emit = True
            if end_label in row[0]:
                emit = False
            if emit:
                yield row
