# -*- coding: utf-8 -*-
"""Dumps data from tables in Word document to csv file.

Call:
   make_csv(data_folder)
"""

import win32com.client as win32
import os

from kep.file_io.common import dump_iter_to_csv
     
#______________________________________________________________________________
#
#  Apllication management
#______________________________________________________________________________

def open_ms_word():
    word = win32.Dispatch("Word.Application")
    word.Visible = 0
    return word

def close_ms_word(app):
    app.Quit()
    # ISSUE: must also quit somewhere by calling app.Quit() 
    # like in http://bytes.com/topic/python/answers/23946-closing-excel-application

def open_doc(path, word):
    word.Documents.Open(path)
    return word.ActiveDocument

def get_table_count(doc):
    return doc.Tables.count    

#______________________________________________________________________________
#
#  Cell value filter
#______________________________________________________________________________


def delete_double_space(line):
    return " ".join(line.split())

REPLACEMENTS = [('\r\x07', '')      # delete this symbol
                , ('\x0c',   ' ')   # sub with space
                , ('\x0b',   ' ')   # sub with space
                , ('\r',     ' ')   # sub with space
                , ("\u201c", '"')
                , ("\u201d", '"') 
                ]  
     
def filter_cell_contents(cell_value):
     for a, b in REPLACEMENTS: 
          cell_value = cell_value.replace(a, b)
     cell_value = delete_double_space(cell_value.strip())      
     return cell_value     

def get_filtered_cell_value(table, i, j):
    val = get_cell_value(table, i, j)
    return filter_cell_contents(val)
              
#______________________________________________________________________________
#
#  Word table iterators
#______________________________________________________________________________

def get_cell_value(table, i, j):
    try:
       return table.Cell(Row = i, Column= j).Range.Text
    # ISSUE: which specific exceptions can it throw?
    except Exception:
       return ""
    
def cell_iter(table):
    for i in range(1,table.rows.count + 1):
        for j in range(1,table.columns.count + 1):              
              yield i, j, get_filtered_cell_value(table, i, j)

def row_iter(table):
    for i in range(1,table.rows.count + 1):
        row = []        
        for j in range(1,table.columns.count + 1):
            row = row + [get_filtered_cell_value(table, i, j)]  
        yield row

#______________________________________________________________________________
#
#  Document-level iterators for .doc files
#______________________________________________________________________________

def query_all_tables(p, func):
    word = open_ms_word()
    doc = open_doc(p, word) 
    total_tables = get_table_count(doc)
    for i, table in enumerate(doc.Tables):
        print("Reading table {} of {}...".format(i+1, total_tables))
        yield func(table)    
    close_ms_word(word)

def yield_continious_rows(p):
    for y in query_all_tables(p, func = row_iter):
        for row in y:
           yield row
     
#______________________________________________________________________________
#
#  Folder-level batch job 
#______________________________________________________________________________

def yield_rows_from_many_files(file_list):
    """Iterate by row over .doc files in *file_list* """
    print("Starting reading .doc files...")
    for p in file_list:
        print("File:", p)
        for row in yield_continious_rows(p):
            yield row
                
def get_csv_filename(folder):
    return os.path.join(folder, "tab.csv")
				
def dump_doc_files_to_csv(file_list, csv):
    """Write tables from .doc in *file_list* into one *csv* file. """
    folder_iter = yield_rows_from_many_files(file_list)
    dump_iter_to_csv(folder_iter, csv) 
    return csv        
      
def make_file_list(folder):
    files = ["tab.doc"] + ["tab%d.doc" % x for x in range(1,5)] 
    return [os.path.abspath(os.path.join(folder, fn)) for fn in files]        

def folder_to_csv(folder):
    """Make single csv based on all STEI .doc files in *folder*. """    
    print ("\nFolder:\n    ", folder)
    file_list = make_file_list(folder)
    csv_filename = get_csv_filename(folder)     
    dump_doc_files_to_csv(file_list, csv_filename)
    print("Finished creating raw CSV file:", csv_filename)

def make_csv(data_folder, overwrite = False):
    csv = get_csv_filename(data_folder)
    if os.path.exists(csv) and overwrite is False:
        print ("CSV file already exists:", csv, " (use option 'overwrite = True' to force start converter")
    else:
        if os.path.exists(data_folder):  
            folder_to_csv(data_folder)
        else:
            raise FileNotFoundError("\nWe are in " + os.getcwd() + "\nCannot find " + data_folder)

#  More info on...
#   API:
#   https://msdn.microsoft.com/en-us/library/office/ff837519.aspx
#   Examples:
#   http://stackoverflow.com/questions/10366596/reading-table-contetnts-in-ms-word-file-using-python
