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
#  File utilities
#______________________________________________________________________________


def change_extension(p, newext):
    if not newext.startswith("."):
        newext = "." + newext
    return os.path.splitext(p)[0] + newext

def get_basename(p):
    return os.path.splitext(p)[0]


#______________________________________________________________________________
#
#  Word table iterators
#______________________________________________________________________________

def get_cell_value(table, i, j):
    try:
       return table.Cell(Row = i, Column= j).Range.Text
    except:
       return ""

def delete_double_space(line):
    return " ".join(line.split())
      
def get_filtered_cell_value(table, i, j):
     replacements = [('\r\x07', '')    # delete this symbol
                   , ('\x0c',   ' ')   # sub with space
                   , ('\x0b',   ' ')   # sub with space
                   , ('\r',     ' ')]  # sub with space
     cell_value = get_cell_value(table, i, j)    
     for a, b in replacements: 
          cell_value = cell_value.replace(a, b)
     cell_value = delete_double_space(cell_value.strip())      
     return cell_value     
     
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
#  CSV IO functions
#______________________________________________________________________________

def dump_iter_to_csv(iterable, csv_filename):
    """Copy generator *iterable* into file *csv_filename*. """    
    with open(csv_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row) 

def yield_csv_rows(c):
    """Open csv file named *c* as iterable. Returns generator."""
    with open(c, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row

#______________________________________________________________________________
#
#  Dump doc files to csv 
#______________________________________________________________________________

def dump_table_to_csv(table, csv_filename):
    iterable = row_iter(table)   
    dump_iter_to_csv(iterable, csv_filename)

def dump_doc_to_single_csv_file(p):
    csv_filename = change_extension(p, ".csv")
    #              get_basename(p) + ".csv"
    many_rows_iter = yield_continious_rows(p)
    dump_iter_to_csv(many_rows_iter, csv_filename) 
    return csv_filename

def dump_doc_files_to_csv(file_list, csv):
    """Write tables from .doc in *file_list* into *csv* file. """

    def yield_folder(file_list):
        """Iterate by row over .doc files in *file_list* """
        print()
        for p in file_list:
            print("File:", p)
            for row in yield_continious_rows(p):
                yield row

    folder_iter = yield_folder(file_list)
    dump_iter_to_csv(folder_iter, csv) 
    return csv        
        
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
                
def make_labelled_csv(source_csv_filename, headline_dict, support_dict):
    # open csv
    gen_in = yield_csv_rows(source_csv_filename)
    # produce new rows    
    gen_out = yield_row_with_labels(gen_in, headline_dict, support_dict)
    # make filename
    output_csv_filename = change_extension(source_csv_filename,"txt")    
    # save to file    
    dump_iter_to_csv(gen_out, output_csv_filename)
    return output_csv_filename 


#______________________________________________________________________________
#
#  Read rows by annual, qtr, month section 
#______________________________________________________________________________
    
def reader12(row):         
    """Year M*12"""
    return row[0], None, None, row[1:12+1]
            
def split_row_by_periods(row):           
    """Year Annual Q Q Q Q M*12"""
    return row[0], row[1], row[2:2+4], row[2+4:(2+4+12)]


#______________________________________________________________________________
#
#  Filter data on db import
#______________________________________________________________________________

COMMENT_CATCHER = re.compile("(\S*)\s*\d\)")

def kill_comment(text):    
    return COMMENT_CATCHER.match(text).groups()[0]
    
def filter_value(text):
   text = text.replace(",",".")

   if ')' in text:
       # Logging capability
       f = open_file()
       log_comment(f, text)       
       
       # if there is mess like '6512.3 6762.31)' in  cell, return first value
       if " " in text:
          text = filter_value(text.split(" ")[0])
          log_changed(f, text)
       # otherwise just through away comment   
       else:
          text = kill_comment(text)          
          log_changed(f, text)
       f.close()
       
   if text == "":       
       return None
   else:       
       return float(text)

#______________________________________________________________________________
#
#  Logger 
#______________________________________________________________________________

def log_changed(f, text):
    f.write("\nChanged to: " + str(text))       

def log_comment(f, text):
    f.write("\n\nCell with comment: " + str(text)) 

def open_file():
   return open('log.txt', 'a')

from time import strftime
def start_log(path):
   with open('log.txt', 'w') as f:       
       statement = "[{}] Started writing to:\n    {}".format(strftime("%Y-%m-%d %H:%M:%S"), path)
       f.write(statement)

#______________________________________________________________________________
#
#  Write labelled CSV to database 
#______________________________________________________________________________

DB_FILE = 'kep.sqlite'

def wipe_db_tables(file = DB_FILE):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.executescript("""
    DELETE FROM "main"."quarterly";
    DELETE FROM "main"."monthly";
    DELETE FROM "main"."annual";
    """)
    conn.commit()
    conn.close()

CODE_TO_FUNC =  {'read12': reader12}
                
def yield_vars(path):
    
    start_log(path)
    
    default_reader = split_row_by_periods
    reader_dict = load_reader_dict(path)
    
    for row in yield_csv_rows(path):

        var_label = row[0]
        if var_label != "unknown_var":

            if var_label in reader_dict.keys():
                reader = CODE_TO_FUNC[reader_dict[var_label]]
            else:
                reader = default_reader 
                
            var_name = row[0] + "_" + row[1]                     
            mod_row = [filter_value(x) for x in row[2:]]        
            y, a, qs, ms = reader(mod_row)
            # print("Sending variable to database: ", var_name, "Year:", int(y))   
            yield var_name, int(y), a, qs, ms            

      
def get_an_gen(path):
    for vn, y, a, qs, ms in yield_vars(path):
        if a is not None:
            yield (vn, y, a)

def get_q_gen(path):
    for vn, y, a, qs, ms in yield_vars(path):
        if qs is not None:         
            for i, val in enumerate(qs):
                if val is not None:
                   yield (vn,y,i+1,val)

def get_m_gen(path):
    for vn, y, a, qs, ms in yield_vars(path):
        if ms is not None:         
            for i, val in enumerate(ms):
                if val is not None:
                    yield (vn,y,i+1,val)

def write_to_database(path):
    conn = sqlite3.connect(DB_FILE)
    an_gen = get_an_gen(path)
    q_gen  = get_q_gen(path)
    m_gen  = get_m_gen(path)   
    conn.executemany("INSERT OR REPLACE INTO annual VALUES (?, ?,  ?)", an_gen)
    conn.commit() 
    conn.executemany("INSERT OR REPLACE INTO quarterly VALUES (?, ?, ?, ?)", q_gen)
    conn.commit() 
    conn.executemany("INSERT OR REPLACE INTO monthly VALUES (?, ?, ?, ?)", m_gen)
    conn.commit()    
    conn.close() 

def write_csv_to_csv_debug(path):
    an_gen = get_an_gen(path)
    csv_filename = change_extension(path, ".txt2")
    dump_iter_to_csv(an_gen, csv_filename)
    
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
        raise FileNotFoundError ("Configurations file not found:" + p)
    except:
        raise Exception ("Error parsing configurations file:" + p)
             
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
    out_csv = make_labelled_csv(src_csv, label_dict, sec_label_dict)

    print ("Finished writing csv with labels:\n    ", out_csv)
    return out_csv

def csv_to_database(t):
    write_to_database(t)
    print ("Pushed csv to database:\n    ", t)

def doc_to_database(p):
    c, h = make_raw_csv_and_headers(p)
    t = make_readable_csv(c)
    csv_to_database(t) 
    
def doc_to_database_silent(p):
    c = dump_doc_to_single_csv_file(p)
    label_dict, sec_label_dict, reader_dict = load_spec(p)
    t = make_labelled_csv(c, label_dict, sec_label_dict)
    write_to_database(t)

#______________________________________________________________________________
#      
      
if __name__ == "__main__":
    pass