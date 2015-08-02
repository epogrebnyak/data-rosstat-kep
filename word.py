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
import os
import csv
import re
import sqlite3

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
    # must also quit somewhere: app.Quit() like in http://bytes.com/topic/python/answers/23946-closing-excel-application

def open_doc(path, word):
    word.Documents.Open(path)
    return word.ActiveDocument

def get_table_count(doc):
    return doc.Tables.count    

#______________________________________________________________________________
#
#  Utilities
#______________________________________________________________________________


def change_extension(p, newext):
    if not newext.startswith("."):
        newext = "." + newext
    return os.path.splitext(p)[0] + newext

def get_basename(p):
    return os.path.splitext(p)[0]

def is_year(s):
    try:
        int(s)
        return True        
    except:
        return False

#______________________________________________________________________________
#
#  Table iterators
#______________________________________________________________________________

def get_cell_value(table, i, j):
    try:
       return table.Cell(Row = i, Column= j).Range.Text
    except:
       return ""
      
def get_filtered_cell_value(table, i, j):
     replacements = [('\r\x07', '')    # delete this symbol
                   , ('\x0c',   ' ')   # sub with space
                   , ('\x0b',   ' ')   # sub with space
                   , ('\r',     ' ')]  # sub with space
     cell_value = get_cell_value(table, i, j)
     for a, b in replacements: 
          cell_value = cell_value.replace(a, b)
     return cell_value.strip()     
     
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
#  Document-level iterators
#______________________________________________________________________________

def query_all_tables(p, func = cell_iter):
    word = open_ms_word()
    doc = open_doc(p, word) 
    for table in doc.Tables:
        yield func(table)    
    close_ms_word(word)


def yield_continious_rows(p):
    for y in query_all_tables(p, func = row_iter):
        for row in y:
           yield row
     
def yield_continious_cells(p):
    for y in query_all_tables(p, func = cell_iter):
        for cell in y:
           yield cell           
  
#______________________________________________________________________________
#
#  CSV IO functions
#______________________________________________________________________________

def dump_iter_to_csv(iterable, csv_filename):
    with open(csv_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row) 

def yield_csv_rows(path):
    with open(path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row

#______________________________________________________________________________
#
#  CSV IO functions
#______________________________________________________________________________

     
def dump_table_to_csv(table, csv_filename):
    iterable = row_iter(table)   
    dump_iter_to_csv(iterable, csv_filename)


def dump_all_tables(p, word):
    doc = open_doc(p, word) 
    for i, table in enumerate(doc.Tables):
        csv_filename = get_basename(p) + "_" + str(i) + ".csv"
        dump_table_to_csv(table, csv_filename)    

def dump_doc_to_single_csv_file(p):
    csv_filename = change_extension(p, ".csv")
    #              get_basename(p) + ".csv"
    many_rows_iter = yield_continious_rows(p)
    dump_iter_to_csv(many_rows_iter, csv_filename) 
    return csv_filename
        
#______________________________________________________________________________
#
#  File management 
#______________________________________________________________________________
        
def make_headers(p):
    """Makes a list of docfile table headers and footers in txt file.
    Used to review file contents and manually make label dictionaries""" 
    
    out = get_basename(p) + "_headers.txt"
    with open(out, "w") as file:
       for row in yield_csv_rows(p):
           if not is_year(row[0]) and len(row[0]) > 0:
                file.write(row[0] + "\n")
    return out
                
#______________________________________________________________________________
#
#  Make CSV with labelled rows and filtered values. 
#______________________________________________________________________________
                
def make_labelled_csv(source_csv_filename, output_csv_filename, 
                                          full_dict, unit_dict): 
    gen = labelled_row_iter(source_csv_filename, label_dict, sec_label_dict)
    dump_iter_to_csv(gen, output_csv_filename)

def get_label(text, lab_dict):
    for pat in lab_dict.keys():
        if pat in text: 
            return lab_dict[pat]
    else:
         return None  

def labelled_row_iter(path, full_dict, unit_dict):
    labels = ["unknown_var", "unknown_unit"]
    for row in yield_csv_rows(path):
         text = row[0]
         if len(text) > 0:
             if not is_year(text):
                 if get_label(text, full_dict) is not None:
                     labels = get_label(text, label_dict)
                 elif get_label(text, unit_dict) is not None:
                     labels[1] = get_label(text, sec_label_dict)
                 else:
                     labels = ["unknown_var", "unknown_unit"]
             else:
                 yield(labels + row)
         else:
             pass # there is nothing in this row, len is 0
         
def test_row_split():   
    row = [2007, 6716.2, 897.6, 1414.4, 1744.1, 2660.1, 255.3, 298.0, 344.3, 364.5, 
       472.2, 577.7, 543.1, 584.2, 616.8, 684.7, 740.4, 1235.0]
    y, a, q, m = split_row_by_periods(row)
    assert y == 2007
    assert len (q) == 4
    assert len (m) == 12    
    assert sum (q) == a
    assert sum (m) == a
        
def split_row_by_periods(row):           
    return row[0], row[1], row[2:2+4], row[2+4:(2+4+12)]

COMMENT_CATCHER = re.compile("(\S*)\s*\d\)")

def filter_comment(text):
    return COMMENT_CATCHER.match(text).groups()[0]
    
def test_filter_comment():
    assert filter_comment("20.5 3)") == "20.5"
    
    
def filter_value(text):
   text = text.replace(",",".")
   if ')' in text:
       text = filter_comment(text)
   if text!="":
       return float(text)
   else:
       return None

#______________________________________________________________________________
#
#  Write labelled CSV to database 
#______________________________________________________________________________

DB_FILE = 'kep.sqlite'
                
def yield_vars(path):      
    for row in yield_csv_rows(path):
        var_name = row[0] + "_" + row[1]
        
        mod_row = [filter_value(x) for x in row[2:]]        
        y, a, qs, ms = split_row_by_periods(mod_row)
        yield var_name, int(y), a, qs, ms 
        
def push_annual(cursor, var_name, year, val):
    cursor.execute("INSERT OR REPLACE INTO annual VALUES (?, ?,  ?)", (var_name, year, val))

def push_quarter(cursor, var_name, year, quarter, val):
    cursor.execute("INSERT OR REPLACE INTO quarterly VALUES (?, ?, ?, ?)", (var_name, year, quarter, val))

def push_monthly(cursor, var_name, year, month, val):
    cursor.execute("INSERT OR REPLACE INTO monthly VALUES (?, ?, ?, ?)", (var_name, year, month, val))

def push_to_database(path):

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    for vn, y, a, qs, ms in yield_vars(path):
        if a is not None:
            push_annual(c,vn,y,a)
        for i, val in enumerate(qs):
            if val is not None:
              push_quarter(c,vn,y,i+1,val)
        for i, val in enumerate(ms):
            if val is not None:              
              push_monthly(c,vn,y,i+1,val)        
        # Save (commit) the changes
        conn.commit()
        
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    
#______________________________________________________________________________
#
#  Read specification
#______________________________________________________________________________
 
import yaml as ya

def load_spec(p):
    """Wrapper for load_spec_from_yaml()"""
    f = get_basename(p) + "_spec.txt"
    return load_spec_from_yaml(f)

def load_spec_from_yaml(p):
    """Returns two dictionaries of label specifications. 
       
       Unpacking:
          full_dict, unit_dict = load_spec_from_yaml(p)
    """
    with open(p, 'r') as file:
        spec = [d for d in ya.load_all(file)]
    return spec[1], spec[0]     

             
#______________________________________________________________________________
#
#  Batch jobs 
#______________________________________________________________________________
                
def make_reabable_csv_and_headers(p):
    print ("File:", p)
    
    c = dump_doc_to_single_csv_file(p)
    print ("Finished writing csv dump:", c)
    
    h = make_headers(c)
    print ("Finished writing headers:", h)
    
    return c
                
if __name__ == "__main__":
    test_row_split()
    test_filter_comment()
    
    src_doc = ["data/1-07/1-07.doc", "ind06/tab.doc", "minitab/minitab.doc"] 
    p = os.path.abspath(src_doc[0])
    s = make_reabable_csv_and_headers(p)
    
    # todo: dump to yaml
    label_dict, sec_label_dict = load_spec(p)

    t = change_extension(s,"txt")
    make_labelled_csv(s, t, label_dict, sec_label_dict)
    print ("Finished writing:", t)
    
    push_to_database(t)
    print ("Pushed to database:", t)
    
    
    
    