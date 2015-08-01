# -*- coding: utf-8 -*-
"""
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

def get_cell_value(table, i, j):
    try:
       return table.Cell(Row = i, Column= j).Range.Text
    except:
       return ""
      
def get_filtered_cell_value(table, i, j):
     cell_value = get_cell_value(table, i, j)
     replacements = [('\r\x07', '')    # delete this symbol
                   , ('\x0c',   ' ')   # sub with space
                   , ('\x0b',   ' ')   # sub with space
                   , ('\r',     ' ')]  # sub with space
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
       
def dump_table_to_csv(table, csv_filename):
    iterable = row_iter(table)   
    dump_iter_to_csv(iterable, csv_filename)

def dump_iter_to_csv(iterable, csv_filename):
    with open(csv_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row) 

def get_basename(p):
    return os.path.splitext(os.path.basename(p))[0]

def dump_all_tables(p, word):
    doc = open_doc(p, word) 
    for i, table in enumerate(doc.Tables):
        csv_filename = get_basename(p) + "_" + str(i) + ".csv"
        dump_table_to_csv(table, csv_filename)    

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
 
def is_year(s):
    try:
        int(s)
        return True        
    except:
        return False
        
def dump_doc_to_single_csv_file(p):
    csv_filename = get_basename(p) + ".csv"
    many_rows_iter = yield_continious_rows(p)
    dump_iter_to_csv(many_rows_iter, csv_filename)    
        
def yield_csv_rows(path):
    with open(path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row
        
def make_headers(p):
    out = get_basename(p) + "headers.txt"
    with open(out, "w") as file:
       for row in yield_csv_rows(p):
           if not is_year(row[0]) and len(row[0]) > 0:
                file.write(row[0] + "\n")

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
             pass # nothing in this row
         
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
    
    
def filter_value2(text):
   text = text.replace(",",".")
   if ')' in text:
       text = filter_comment(text)
   if text!="":
       return float(text)
   else:
       return None

def yield_vars(path):      
    for row in yield_csv_rows(path):
        var_name = row[0] + "_" + row[1]
        
        mod_row = [filter_value2(x) for x in row[2:]]        
        y, a, qs, ms = split_row_by_periods(mod_row)
        yield var_name, int(y), a, qs, ms 
        
def push_annual(cursor, var_name, year, val):
    cursor.execute("INSERT OR REPLACE INTO annual VALUES (?, ?,  ?)", (var_name, year, val))

def push_quarter(cursor, var_name, year, quarter, val):
    cursor.execute("INSERT OR REPLACE INTO quarterly VALUES (?, ?, ?, ?)", (var_name, year, quarter, val))

def push_monthly(cursor, var_name, year, month, val):
    cursor.execute("INSERT OR REPLACE INTO monthly VALUES (?, ?, ?, ?)", (var_name, year, month, val))


def push_to_database(path):

    conn = sqlite3.connect('kep.sqlite')
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
    
    
if __name__ == "__main__":
    test_row_split()
    test_filter_comment()
        
    p1 = os.path.abspath("tab.doc")
    p2 = os.path.abspath("1-07.doc")
    #dump_doc_to_single_csv_file(p2)
    #dump_doc_to_single_csv_file(p1)
    c1 = os.path.abspath("tab.csv")
    c2 = os.path.abspath("1-07.csv")
    t2 = "1-07.txt" 
    
    label_dict = {
    "1.7. Инвестиции в основной капитал":  ['I','bln_rub'],
    "1.14. Объем платных услуг населению": ['Usl','bln_rub']
     }
     
    sec_label_dict =    {
     "в % к соответствующему периоду предыдущего года": 'yoy',
     "в % к предыдущему периоду": 'rog'
     }
     
    gen = labelled_row_iter(c2, label_dict, sec_label_dict)
    dump_iter_to_csv(gen, t2)
    push_to_database(t2)
    

                
 






           
            

    
    
    
    
    
    
    
    
    

    