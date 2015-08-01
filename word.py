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
     replacements = [('\r\x07', '')  # delete this symbol
                   , ('\x0c',   ' ') # sub with space
                   , ('\x0b',   ' ')
                   , ('\r',     ' ')]
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
    with open(csv_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in row_iter(table):        
             spamwriter.writerow(row)    

def get_basename(p):
    return os.path.splitext(os.path.basename(p))[0]

def dump_all_tables(p, word):
    doc = open_doc(p, word) 
    for i, table in enumerate(doc.Tables):
        csv_filename = get_basename(p) + "_" + str(i) + ".csv"
        dump_table_to_csv(table, csv_filename)    

def split_row_by_periods(row):
    return row[0], row[1], row[2:2+4], row[2+4:(2+4+12)]
  
def test_row_split():   
    row = [2007, 6716.2, 897.6, 1414.4, 1744.1, 2660.1, 255.3, 298.0, 344.3, 364.5, 
       472.2, 577.7, 543.1, 584.2, 616.8, 684.7, 740.4, 1235.0]
    y, a, q, m = split_row_by_periods(row)
    assert y == 2007
    assert len (q) == 4
    assert len (m) == 12    
    assert sum (q) == a
    assert sum (m) == a
      
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
 
def dump_doc_to_single_csv_file(p):
    csv_filename = get_basename(p) + ".csv"
    row_iter = yield_continious_rows(p)
    with open(csv_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in row_iter:        
             spamwriter.writerow(row)            

if __name__ == "__main__":
    test_row_split()
    p = os.path.abspath("1-07.doc")    
 
    tablename =  ["1.7. Инвестиции в основной капитал",    
        ("в % к соответствующему периоду предыдущего года",
         "в % к предыдущему периоду")]
    
    gov = ""    
    for row in yield_continious_rows(p):
        if tablename[0] in row[0]:
            gov = ["I", "bln rubles"]
          
        if tablename[1][0] in row[0]:
            gov[1] = "yoy"

        if tablename[1][1] in row[0]:
            gov[1] = "rog"

        print(gov)





           
            

    
    
    
    
    
    
    
    
    

    