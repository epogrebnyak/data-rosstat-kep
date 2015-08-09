# -*- coding: utf-8 -*-
"""
"""

#______________________________________________________________________________
#
#  Folder-level batch job 
#______________________________________________________________________________
                
from word import dump_doc_files_to_csv
import os        

def make_file_list(folder):
    files = ["tab" + str(x) + ".doc" for x in range(0,5)] 
    files[0] = "tab.doc"
    return  [os.path.abspath(os.path.join(folder + fn)) for fn in files]
        

def make_csv_in_stei_folder(folder):
    """Make single csv based on all STEI .doc files in *folder*. 
       *.doc -> raw csv + headers """    
    file_list = make_file_list(folder)
    csv = dump_doc_files_to_csv(file_list)
    make_headers(csv)    
   
#______________________________________________________________________________
#
#  File-level batch jobs 
#______________________________________________________________________________
                
from word import dump_doc_to_single_csv_file, make_headers 
from label_csv import dump_labelled_rows_to_csv 
from stream import emit_flat_data
from database import write_to_database

def doc_to_database(p):
    """ .doc -> db """
    c, h = doc_to_raw_csv(p)
    t = label_csv(c)
    csv_to_database(t) 
    
def raw_csv_to_database(p):
    t = dump_labelled_rows_to_csv(p)
    gen = emit_flat_data(t)
    write_to_database(gen)
    
def doc_to_raw_csv(p):
    """ .doc -> raw csv + headers """
    print ("\nFile:\n    ", p)
    c = dump_doc_to_single_csv_file(p)
    print ("Finished writing csv dump:\n    ", c)
    h = make_headers(c)
    print ("Finished writing headers:\n    ", h)
    return c, h

def label_csv(p):
    """ raw csv -> csv with labels """
    t = dump_labelled_rows_to_csv(p)
    print ("Finished writing csv with labels:\n    ", t)
    return t

def csv_to_database(p):
    """ csv with labels -> db"""
    gen = emit_flat_data(p)
    write_to_database(gen)
    print ("Pushed csv to database:\n    ", p)