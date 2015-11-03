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

ENCODING = 'utf8' #'cp1251'

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
        if emit:
            yield row
