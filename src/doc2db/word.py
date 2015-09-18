# -*- coding: utf-8 -*-
"""Dumps data from tables in Word document to csv file.

API:
  https://msdn.microsoft.com/en-us/library/office/ff837519.aspx

Examples:
http://stackoverflow.com/questions/10366596/reading-table-contetnts-in-ms-word-file-using-python

See also:
https://python-docx.readthedocs.org/en/latest/
"""

import win32com.client as win32

try:
    from .common import get_raw_csv_filename, get_headers_filename
    from .common import dump_iter_to_csv, yield_csv_rows
    from .label_csv import is_year
except:
    from common import get_raw_csv_filename, get_headers_filename
    from common import dump_iter_to_csv, yield_csv_rows
    from label_csv import is_year
    

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
    # ISSUE:
    # must also quit somewhere by calling app.Quit() 
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
    except:
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
#  Dump doc files to csv 
#______________________________________________________________________________

def dump_table_to_csv(table, csv_filename):
    iterable = row_iter(table)   
    dump_iter_to_csv(iterable, csv_filename)

def dump_doc_to_single_csv_file(p):
    csv_filename = get_raw_csv_filename(p)
    many_rows_iter = yield_continious_rows(p)
    dump_iter_to_csv(many_rows_iter, csv_filename) 
    return csv_filename

def yield_rows_from_many_files(file_list):
    """Iterate by row over .doc files in *file_list* """
    print()
    for p in file_list:
        print("File:", p)
        for row in yield_continious_rows(p):
            yield row
                
def dump_doc_files_to_csv(file_list, csv = None):
    """Write tables from .doc in *file_list* into *csv* file. """
    if csv is None:
        csv = get_raw_csv_filename(file_list[0])
    folder_iter = yield_rows_from_many_files(file_list)
    dump_iter_to_csv(folder_iter, csv) 
    return csv        
        
#______________________________________________________________________________
#
#  Inspection into headers (varnames)
#______________________________________________________________________________
        
def make_headers(p):
    """Makes a list of docfile table headers and footers in txt file.
    Used to review file contents and manually make label dictionaries."""    
    f = get_headers_filename(p)    
    with open(f, "w") as file:
       for row in yield_csv_rows(p):
           if not is_year(row[0]) and len(row[0]) > 0:
                file.write(row[0] + "\n")
    return f 

if __name__ == "__main__":
    pass