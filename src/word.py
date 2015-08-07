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
#  Project filenames
#______________________________________________________________________________

def get_doc_filename(f):
    return change_extension(f, "doc")
    
def get_raw_csv_filename(f):
    return change_extension(f, "csv")

def get_labelled_csv_filename(f):
    return change_extension(f, "txt")

def get_spec_filename(f):
    if "_spec" not in f:
        return get_basename(f) + "_spec.txt"
    else:
        return f        
        
def get_headers_filename(f):    
    return get_basename(f) + "_headers.txt"
    
def get_reference_csv_filename(f):    
    return get_basename(f) + "_reference_dataset.txt"
    
def get_varname_filename(f): 
    if "_spec" in f:
        return f.replace("_spec", "_var_list")
    else:         
        return get_basename(f) + "_var_list.txt"

#______________________________________________________________________________
#
#  Cell value filter
#______________________________________________________________________________


def delete_double_space(line):
    return " ".join(line.split())

REPLACEMENTS = [('\r\x07', '')    # delete this symbol
                , ('\x0c',   ' ')   # sub with space
                , ('\x0b',   ' ')   # sub with space
                , ('\r',     ' ')]  # sub with space
     
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
#  CSV IO functions
#______________________________________________________________________________

def dump_iter_to_csv(iterable, csv_filename):
    """Copy generator *iterable* into file *csv_filename*. """    
    with open(csv_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row)
    return csv_filename

def yield_csv_rows(c):
    """Open csv file named *c* and return an iterable."""
    with open(c, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row
            
def yield_csv_rows_between_labels(c, start_label, end_label):
    """Yield part of csv file, marked by *start_label* and *end_label*"""
    emit = False
    with open(c, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            if start_label in row[0]:
                emit = True
            if emit:
                yield row
            if end_label in row[0]:
                emit = False

def get_labels_from_iter(gen):
    return set(row[0] in gen)

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

def dump_doc_files_to_csv(file_list, csv = None):
    """Write tables from .doc in *file_list* into *csv* file. """

    if csv is None:
        csv = get_raw_csv_filename(file_list[0])

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
#  Inspection into headers 
#______________________________________________________________________________
        
from rowlabel import is_year

def make_headers(p):
    """Makes a list of docfile table headers and footers in txt file.
    Used to review file contents and manually make label dictionaries""" 
    
    out = get_headers_filename()    
    with open(out, "w") as file:
       for row in yield_csv_rows(p):
           if not is_year(row[0]) and len(row[0]) > 0:
                file.write(row[0] + "\n")
                
#______________________________________________________________________________
#
#  Make CSV with labelled rows 
#______________________________________________________________________________

from rowlabel import yield_row_with_labels

def get_csv_filnames(f):
    return get_raw_csv_filename(f), get_labelled_csv_filename(f)

def get_dicts(f):
    headline_dict, support_dict, reader_dict = load_spec(f)
    return headline_dict, support_dict

def get_labelled_rows_from_incoming_generator(f, gen_in):
    headline_dict, support_dict = get_dicts(f)
    return yield_row_with_labels(gen_in, headline_dict, support_dict)
    
def dump_labelled_rows_to_csv(f):
    infile, outfile = get_csv_filnames(f)
    # open csv
    gen_in = yield_csv_rows(infile)
    #produce new rows
    gen_out = get_labelled_rows_from_incoming_generator(f, gen_in)
    # save to file    
    r = dump_iter_to_csv(gen_out, outfile)
    return r

def make_labelled_csv(f, headline_dict, support_dict):
    infile = get_raw_csv_filename(f)
    outfile = get_labelled_csv_filename(f)
    # open csv
    gen_in = yield_csv_rows(infile)
    # produce new rows    
    gen_out = yield_row_with_labels(gen_in, headline_dict, support_dict)
    # save to file    
    dump_iter_to_csv(gen_out, outfile)
    return outfile 

def list_as_string(l):
    return  " ".join(sorted(l))

def check_vars_not_in_labelled_csv(f):
    """Returns varnames not written to labelled csv file. Prints explaination."""     
    infile, outfile = get_csv_filnames(f)
    gen_in = yield_csv_rows(infile)
    gen_out = get_labelled_rows_from_incoming_generator(f, gen_in)

    headline_dict, support_dict = get_dicts(f)    
    z2 = list(v[0] for k,v in headline_dict.items())
    print ("\nVars in raw csv:")
    print(list_as_string(z2))
    
    z1 = list(set(row[0] for row in gen_out))
    print ("\nVars in labelled csv:")
    print(list_as_string(z1))
     
    not_in_file = [x for x in z2 if x not in z1] 
    
    print ("\nNot loaded to labelled csv:")
    for g in not_in_file :
        print (g)
    
    return not_in_file 

#______________________________________________________________________________
#
#  Filter data on db import
#______________________________________________________________________________

COMMENT_CATCHER = re.compile("(\S*)\s*\d\)")
# About comment catcher

def kill_comment(text):    
    return COMMENT_CATCHER.match(text).groups()[0]

def process_text_with_bracket(text):
    
   # Logging capability
   with open_file() as f:
       
       log_comment(f, text)       
       
       # if there is mess like '6512.3 6762.31)' in  cell, return first value
       if " " in text:
          text = filter_value(text.split(" ")[0])
          
       # otherwise just through away comment   
       else:
          text = kill_comment(text)          
    
       log_changed(f, text)

   return text

def filter_value(text):
    
   text = text.replace(",",".")
   if ')' in text:
       text = process_text_with_bracket(text)

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
#  Read rows by annual, qtr, month section 
#______________________________________________________________________________

def reader12_with_annual(row):         
    """Year Annual M*12"""
    return row[0], row[1], None, row[2:12+2]
    
def reader12(row):         
    """Year M*12"""
    return row[0], None, None, row[1:12+1]
            
def split_row_by_periods(row):           
    """Year Annual Q Q Q Q M*12"""
    return row[0], row[1], row[2:2+4], row[2+4:(2+4+12)]

CODE_TO_FUNC =  {'read12': reader12, 'read13': reader12_with_annual}
                
def get_reader_func(var_label, reader_dict):
    if var_label in reader_dict.keys():
        return CODE_TO_FUNC[reader_dict[var_label]]
    else:
        return split_row_by_periods

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

from rowlabel import PRINT_ALL 

def yield_vars(path):
    
    start_log(path)
    
    reader_dict = load_reader_dict(path)
    
    for row in yield_csv_rows(path):
        var_label = row[0]
        if var_label != "unknown_var":

            var_name = row[0] + "_" + row[1]                     
            mod_row = [filter_value(x) for x in row[2:]]        
            
            reader = get_reader_func(var_label, reader_dict)
            y, a, qs, ms = reader(mod_row)
            
            if PRINT_ALL:
                print(var_name, y, a, qs, ms)                
            
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

#def write_csv_to_csv_debug(path):
#    an_gen = get_an_gen(path)
#    csv_filename = change_extension(path, ".txt2")
#    dump_iter_to_csv(an_gen, csv_filename)
    
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
    return load_spec_from_yaml(p)

def load_spec_from_yaml(p):
    """Returns dictionaries of specifications.        
       Unpacking:
          full_dict, unit_dict, reader_dict = load_spec_from_yaml(p)
    """
    p = get_spec_filename(p)
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