# -*- coding: utf-8 -*-
"""CSV input/output."""

import csv
import os
   
def infolder(folder, file):
   path = os.path.join(folder, file)
   if os.path.isfile(path):
       return path 
   else:
       raise FileNotFoundError(path)

        
#______________________________________________________________________________
#
#  Basic CSV IO functions
#______________________________________________________________________________


def dump_iter_to_csv(iterable, csv_filename):
    """Copy generator *iterable* into file *csv_filename*. """    
    with open(csv_filename, 'w', encoding = ENCODING) as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row)
    return csv_filename

def yield_csv_rows(csv_filename):
    """Open csv file named *c* and return an iterable."""
    with open(csv_filename, 'r', encoding = ENCODING) as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row

#------------------------------------------------------------------------------
# Dump of test files
#------------------------------------------------------------------------------

ENCODING = 'utf8' #'cp1251'
SUBFOLDER = "test_txt_files"

def docstring_to_file(docstring, filename, subfolder = SUBFOLDER):
    path = os.path.join(subfolder, filename)
    with open(path,"w", encoding = ENCODING) as f:
        f.write(docstring)
    return path

#------------------------------------------------------------------------------

import yaml as ya

def _get_yaml(filename):
    with open(filename, 'r', encoding = ENCODING) as file:
        spec = ya.load_all(file) # [d for d in ya.load_all(file)]
        return list(spec)   

#______________________________________________________________________________
#
#  CSV slicing 
#______________________________________________________________________________

def yield_csv_rows_between_labels(csv_filename, start_label, end_label):
    """Yield part of csv file, marked by *start_label* and *end_label*"""
    must_emit = False
    for row in yield_csv_rows(csv_filename):
        if start_label in row[0]:
            must_emit = True
        if end_label in row[0]:
            must_emit = False
        if must_emit:
            yield row
            
            
if __name__ == "__main__":
    p = docstring_to_file("Текст", "test.txt")
    z = [x for x in yield_csv_rows(p)]
    print(z)
    

