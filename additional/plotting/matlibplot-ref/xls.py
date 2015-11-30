"""Usage:
   xls2csv.py filename [sheet] [header_row] [data_row_start] [data_row_end] 
"""
# Issues:
# It is cleaner to cut extra empty or NaN rows at the end of csv file

# Not todo:
# Docopt interface

# Solved:
# Column cells in subheader (cells above dates, A4:A5 in sa2.xls!Dbase) must be non-empty
# Column cell in header row must be empty

import sys
import os
import pandas as pd
#import numpy as np
from pprint import pprint

NA_LIST = ['NA', "#Н/Д"]
SHOW_MESSAGES = False

def get_file_path_in_project_directory(filename):
    """
    Get full path for a file, which is located in the same directory 
    with this python script.
    """  
    DIR = os.path.dirname(os.path.abspath("__file__"))       
    path = os.path.join(DIR, filename)
    return path

def check_sheet(path, sheet):
    """
    Raises error if sheet name is not present in file.
    """     
    xl = pd.ExcelFile(path)
    if sheet not in xl.sheet_names:
        raise ValueError("Invalid sheet name \'" + sheet +"\'")        
    
def get_arguments(verbose = False):
    """
    Uses sys.argv to aceess command line arguements and assign values to following variables: 
       path, sheet, header_row, data_row_start, data_row_end
    """    
    a = sys.argv        
    
    if len(a) == 5+1:
        data_row_end = int(a[5])
    else: data_row_end = None 
    
    if len(a) >= 3+1:
        header_row = int(a[3])
    else: header_row = 0 
    
    if len(a) >= 4+1:
        data_row_start = int(a[4])
    else: data_row_start = header_row + 1 

    if len(a) >= 2+1:
        sheet = a[2]
    else: sheet = 0 

    filename  = a[1]    
    path = get_file_path_in_project_directory(filename)
    check_sheet(path, sheet)

    if verbose is True:        
        print("")
        print("Full path:", path)
        print("Filename:", filename)    
        print("Sheet:", sheet)
        print("Header starts in row " + str(header_row) + ".")
        if data_row_end is not None: 
            msg = "Data ends in row " + str(data_row_end) + "."
        else: msg = "Data end row not defined."
        print("Data starts in row " + str(data_row_start)+ ". " + msg)
        print("Date index in column A by default.")       
        
    return (path, sheet, header_row, data_row_start, data_row_end)
    
def get_skip_footer_length(path, sheet, header_row, data_row_end, verbose = False):
    """
    Returns value for 'skip_footer' parameter in read_excel(), calculated as: 
         (full_row_count - data_row_end + header_row)
    This value is needed to trim read_excel() reading of Excel sheet up to 'data_row_end' row.
    """          
    if data_row_end is not None:        
        df = pd.read_excel(path, sheet, header = header_row - 1)
        full_row_count = df.shape[0]
        # Need clarification: formula tested in real sheets, but not clear        
        skip_footer_nrows = max(0, full_row_count + header_row - data_row_end )        
        if verbose is True:
            print("")
            print("Row count on sheet \'" + sheet + "\': " + str(full_row_count))
            print("Skipping last " + str(skip_footer_nrows) + " rows.") 
    else:
        skip_footer_nrows = 0
        if verbose is True:
            print("")
            print("Skipping last " + str(skip_footer_nrows) + " rows.") 
    return skip_footer_nrows

def filter_index_column(df, verbose = False):
    """
    Changes index column to intergers 0, 1, 2... if first index is NaN
    """  
    index_starts_with_nan = pd.isnull(df.index)[0]
    if index_starts_with_nan:
        full_row_count = df.shape[0]
        df.index = list(range(full_row_count))
        if verbose is True:
           print("")
           print("Index changed. New dataframe index: ", df.index)
    return df
    
def get_dataframe(path, sheet, header_row, data_row_start, data_row_end):
    """
    Reads Excel sheet into panda DataFrame
    """  
    
    skip_footer_nrows = get_skip_footer_length(path, sheet, header_row, data_row_end, verbose = SHOW_MESSAGES)
        
    # read data from sheet     
    df = pd.read_excel(path, sheet, index_col=0, header=header_row-1, na_values=NA_LIST, skip_footer = skip_footer_nrows)
                      
    # cut rows between 'header_row' and 'data_row_start'
    row_slice_index = data_row_start - header_row - 1        
    try: 
        df = df[row_slice_index:]
    except:
        # assignment above fails on NaN values in index, so we change index to sequence of intergers in this case
        df = filter_index_column(df, verbose = SHOW_MESSAGES)
        df = df[row_slice_index:]    
    return df   
    
def print_dataframe(df):
    """
    Prints head and tail for sort long dataframe, all dataframe for short one.
    """
    print ("")
    if df.shape[0] > 20:
        print (df.head())
        print (df.tail())
    else:    
        print (df)
        
def make_new_path(path, postfix = "", ext = ""):
    """
    Modify file path using postfix to basename and new file extension.
    """
    dir = os.path.split(path)[0]
    old_basename, old_ext = os.path.splitext(path)
    new_basename = old_basename + "_" + postfix
    new_path = os.path.join(dir, new_basename + "." + ext)
    return new_path


def dump_to_csv(df, path, sheet):
    # save to basename_sheet.csv
    csv_path = make_new_path(path, postfix = sheet, ext = "csv")
    df.to_csv(csv_path)     
    
def dump_to_xls(df, path, sheet):
    # save to basename.xls
    xl_path = make_new_path(path, postfix = "new", ext = "xlsx")
    df.to_excel(xl_path, sheet)  
    
    # TODO - xlwings / xlsxwriter
    # Range('A1').number_format     
    
def dump_sheet(df, path, sheet): 
    dump_to_csv(df, path, sheet)  
    dump_to_xls(df, path, sheet)    
    
def cut_frame_tail(df):
    """
    Cut row with missing values at non-existing dates.
    Delete rows with NaT in index column.
    """
    # TODO
    return df

def xls(path, sheet, header_row, data_row_start, data_row_end):
    df = get_dataframe(path, sheet, header_row, data_row_start, data_row_end)
    # TODO 
    # path may need to work over
    dump_sheet(df, path, sheet)

if __name__ == '__main__':
    SHOW_MESSAGES = True
    path, sheet, header_row, data_row_start, data_row_end = get_arguments(verbose = SHOW_MESSAGES)           
    df = get_dataframe(*get_arguments())        
    print_dataframe(df)
    dump_sheet(df, path, sheet)    