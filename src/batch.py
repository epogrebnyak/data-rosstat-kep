# -*- coding: utf-8 -*-
"""
"""

#______________________________________________________________________________
#
#  Folder-level batch job 
#______________________________________________________________________________
                
from word2 import dump_doc_files_to_csv
import os        

def make_csv_in_stei_folder(folder):
    """Make single csv based on all STEI .doc files in *folder*. """
    
    files = ["tab" + str(x) + ".doc" for x in range(0,5)] 
    files[0] = "tab.doc"
    file_list = [os.path.abspath(folder + fn) for fn in files]
    csv = os.path.join(folder, "all_tab.csv")

    dump_doc_files_to_csv(file_list, csv)
    make_headers(csv)
    
   
#______________________________________________________________________________
#
#  File-level batch jobs 
#______________________________________________________________________________
                
from word2 import dump_doc_to_single_csv_file, make_headers 
from label_csv_by_specification import dump_labelled_rows_to_csv 
from stream_from_labelled_csv import emit_flat_data
from database import write_to_database

def make_raw_csv_and_headers(p):
    print ("\nFile:\n    ", p)
    c = dump_doc_to_single_csv_file(p)
    print ("Finished writing csv dump:\n    ", c)
    h = make_headers(c)
    print ("Finished writing headers:\n    ", h)
    return c, h

def make_csv_with_labels(p):
    t = dump_labelled_rows_to_csv(p)
    print ("Finished writing csv with labels:\n    ", t)
    return t

def csv_to_database(p):
    gen = emit_flat_data(p)
    write_to_database(gen)
    print ("Pushed csv to database:\n    ", p)

def doc_to_database(p):
    c, h = make_raw_csv_and_headers(p)
    t = make_csv_with_labels(c)
    csv_to_database(t) 
    
def doc_to_database_silent(p):
    c = dump_doc_to_single_csv_file(p)
    t = dump_labelled_rows_to_csv(c)
    gen = emit_flat_data(t)
    write_to_database(gen)
