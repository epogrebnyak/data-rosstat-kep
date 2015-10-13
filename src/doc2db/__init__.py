# -*- coding: utf-8 -*-

"""API interface to doc2db module."""

#______________________________________________________________________________
#
#  Functions in package
#______________________________________________________________________________

import os  
                
try:
    from .word import dump_doc_files_to_csv, dump_doc_to_single_csv_file, make_headers 
    from .label_csv import dump_labelled_rows_to_csv, check_vars_not_in_labelled_csv
    from .database import wipe_db_tables, write_to_database
    from .query import db2xl as database_to_xl   

except ImportError:
    from word import dump_doc_files_to_csv, dump_doc_to_single_csv_file, make_headers 
    from label_csv import dump_labelled_rows_to_csv, check_vars_not_in_labelled_csv   
    from database import wipe_db_tables, write_to_database
    from query import db2xl as database_to_xl   

#______________________________________________________________________________
#
#  Supplemntary function
#______________________________________________________________________________


def make_headers_and_message(c):
    h = make_headers(c)
    print ("Finished writing headers:\n    ", h)
 
def message(text, c):
    print ("\n" + text + ":\n    ", c)
    
#______________________________________________________________________________
#
#  Folder-level batch job 
#______________________________________________________________________________
      

def make_file_list(folder):
    files = ["tab" + str(x) + ".doc" for x in range(0,5)] 
    files[0] = "tab.doc"
    return  [os.path.abspath(os.path.join(folder, fn)) for fn in files]        

def folder_to_csv(folder):
    """Make single csv based on all STEI .doc files in *folder*. """    
    print ("\nFolder:\n    ", folder)
    file_list = make_file_list(folder)    
    c = dump_doc_files_to_csv(file_list)
    message("Finished creating raw CSV file", c)
    make_headers_and_message(c)  
   
#______________________________________________________________________________
#
#  File-level batch jobs 
#______________________________________________________________________________

def doc_to_csv(p):
    """ Convert tables from doc file to raw csv and make headers """
    message("File", p)    
    c = dump_doc_to_single_csv_file(p)
    message("Finished creating raw CSV file", c)
    make_headers_and_message(c)

def labelize_csv(p):
    """ Convert raw csv to csv with labels """
    t = dump_labelled_rows_to_csv(p)
    message("Finished writing labelled CSV file", t)

def csv_to_database(p):
    """ Load csv with labels to database """
    write_to_database(p)
    message("Pushed CSV to database", p)   
    