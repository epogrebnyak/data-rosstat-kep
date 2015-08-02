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
    total_tables = get_table_count(doc)
    for i, table in enumerate(doc.Tables):
        print("Reading table {} of {}...".format(i+1, total_tables))
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


#def dump_all_tables(p, word):
#    doc = open_doc(p, word) 
#    for i, table in enumerate(doc.Tables):
#        csv_filename = get_basename(p) + "_" + str(i) + ".csv"
#        dump_table_to_csv(table, csv_filename)    

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
        
from rowlabel import is_year
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
#  Make CSV with labelled rows 
#______________________________________________________________________________

from rowlabel import yield_row_with_labels
                
def make_labelled_csv(source_csv_filename, output_csv_filename, headline_dict, support_dict):
                                              
    # open csv
    gen_in = yield_csv_rows(source_csv_filename)
    # produce new rows    
    gen_out = yield_row_with_labels(gen_in, headline_dict, support_dict)
    # save to file    
    dump_iter_to_csv(gen_out, output_csv_filename)

         
#______________________________________________________________________________
#
#  Filter data on db import
#______________________________________________________________________________
         
def test_row_split1():   
    row = [2007, 6716.2, 897.6, 1414.4, 1744.1, 2660.1, 255.3, 298.0, 344.3, 364.5, 
       472.2, 577.7, 543.1, 584.2, 616.8, 684.7, 740.4, 1235.0]
    y, a, q, m = split_row_by_periods(row)
    assert y == 2007
    assert len (q) == 4
    assert len (m) == 12    
    assert sum (q) == a
    assert sum (m) == a

def test_row_split2():   
    row = ['1999', '196.9', '203.3', '207.6', '213.1', '216.7', '220.7', '226.5', '221.0', '162.0', '157.1', '150.5', '136.5']
    y, a, q, m = reader12(row)
    assert y == '1999'
    assert q == None
    assert a == None    
    assert len (m) == 12   
    

def reader12(row):           
    return row[0], None, None, row[1:12+1]
            
def split_row_by_periods(row):           
    return row[0], row[1], row[2:2+4], row[2+4:(2+4+12)]

COMMENT_CATCHER = re.compile("(\S*)\s*\d\)")

def filter_comment(text):    
    return COMMENT_CATCHER.match(text).groups()[0]
    
def test_filter_comment():
    assert filter_comment("20.5 3)") == "20.5"
    
def test_filter_value():
    assert filter_value("20.5 3)") == 20.5    
    assert filter_value ('6512.3 6762.31)') == 6512.3
    
    
def filter_value(text):
   text = text.replace(",",".")
   print_flag = False
   if ')' in text:
       print("\nCell with comment:", text)
       print_flag = True
       if " " in text:
           # if there is mess like '6512.3 6762.31)' in  cell, retrun first value
           text = filter_value(text.split(" ")[0])
       else:
          text = filter_comment(text)
          
   if text!="":
       if print_flag:
          print("Changed to:", float(text))
       return float(text)

   else:
       return None

#______________________________________________________________________________
#
#  Write labelled CSV to database 
#______________________________________________________________________________

DB_FILE = 'kep.sqlite'

CODE_TO_FUNC =  {'read12': reader12}
                
def yield_vars(path, reader = split_row_by_periods): 
    reader_dict = load_reader_dict(path)
    
    for row in yield_csv_rows(path):
        var_label = row[0]
        if var_label in reader_dict.keys():
            reader = CODE_TO_FUNC[reader_dict[var_label]]         
        if var_label != "unknown_var":
            var_name = row[0] + "_" + row[1]
            
            mod_row = [filter_value(x) for x in row[2:]]        
            y, a, qs, ms = reader(mod_row)
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

def load_reader_dict(p):
    full_dict, unit_dict, reader_dict = load_spec(p)
    return reader_dict
    
def load_spec(p):
    """Wrapper for load_spec_from_yaml()"""
    f = get_basename(p) + "_spec.txt"
    return load_spec_from_yaml(f)

def load_spec_from_yaml(p):
    """Returns dictionaries of specifications. 
       
       Unpacking:
          full_dict, unit_dict, reader_dict = load_spec_from_yaml(p)
    """
    try:
        with open(p, 'r') as file:
            spec = [d for d in ya.load_all(file)]
        return spec[2], spec[1], spec[0]       
    except FileNotFoundError:
        print ("Configurations file not found:", p)
    except:
        print ("Error parsing configurations file:", p)
             
#______________________________________________________________________________
#
#  Batch jobs 
#______________________________________________________________________________
                
def make_raw_csv_and_headers(p):
    print ("\nFile:\n    ", p)
    
    c = dump_doc_to_single_csv_file(p)
    print ("Finished writing csv dump:\n    ", c)
    
    h = make_headers(c)
    print ("Finished writing headers:\n    ", h)
    
    return c, h

def make_readable_csv(src_csv):
    
    label_dict, sec_label_dict, reader_dict = load_spec(src_csv)

    out_csv = change_extension(src_csv,"txt")
    make_labelled_csv(src_csv, out_csv, label_dict, sec_label_dict)

    print ("Finished writing csv with labels:\n    ", out_csv)
    return out_csv

def csv_to_database(t):
    push_to_database(t)
    print ("Pushed csv to database:\n    ", t)

def doc_to_database(p):
    c, h = make_raw_csv_and_headers(p)
    t = make_readable_csv(c)
    csv_to_database(t) 
    
def doc_to_database_silent(p):
    c, h = dump_doc_to_single_csv_file(p)
    label_dict, sec_label_dict, reader_dict = load_spec(p)
    out_csv = change_extension(p,"txt")
    t = make_labelled_csv(c, out_csv, label_dict, sec_label_dict)
    push_to_database(t)

#______________________________________________________________________________
#      
          
if __name__ == "__main__":
    test_row_split()
    test_row_split2()
    test_filter_comment()
    test_filter_value()
    
    src_doc = ["data/1-07/1-07.doc", "data/ind06/tab.doc", "data/minitab/minitab.doc"] 
    


    