# -*- coding: utf-8 -*-
"""Paths and filenames."""

import os
from kep.common.inputs import Folder

# filenames
RESERVED_FILENAMES = {'csv':'tab.csv', 'cfg':'cfg.txt'}  

# root folders
# one level up from this file 
_PROJECT_SRC_DIR  = Folder(__file__).path
_PROJECT_ROOT_DIR = Folder(__file__).up(1).path

# data folder - change here for next month --------------------------------------------
#
CURRENT_MONTH_DATA_FOLDER = os.path.join(_PROJECT_ROOT_DIR, 'data', '2016', 'ind02')
#
# --------------------------------------------------------------------------------------

#test folder
TESTDATA_DIR = os.path.join(_PROJECT_SRC_DIR, "tests", "temp")        

#databases
DATABASE_DIR        = os.path.join(_PROJECT_SRC_DIR, "database")
TEST_SQLITE_FILE    = os.path.join(DATABASE_DIR, "test.sqlite3")
DEFAULT_SQLITE_FILE = os.path.join(DATABASE_DIR, "kep.sqlite3")

# toc file 
TOC_FILE = os.path.join(CURRENT_MONTH_DATA_FOLDER, "toc.txt")

# graphic output
OUTPUT_DIR    = os.path.join(_PROJECT_ROOT_DIR, 'output')
PNG_FOLDER    = os.path.join(OUTPUT_DIR, 'png')
PDF_FILE      = os.path.join(OUTPUT_DIR, 'monthly.pdf')
MD_FILE       = os.path.join(OUTPUT_DIR, 'images.md')
VARNAMES_FILE = os.path.join(OUTPUT_DIR, 'varnames.md')

# xls and csv output
XLSX_FILENAME = 'kep.xls' 
XLS_FILENAME  = 'kep.xlsx'   
XLSX_FILE   = os.path.join(OUTPUT_DIR, XLSX_FILENAME)
XLS_FILE    = os.path.join(OUTPUT_DIR, XLS_FILENAME)

A_CSV = 'data_annual.txt'
Q_CSV = 'data_quarter.txt'
M_CSV = 'data_monthly.txt'

def dataframe_dump_csv_filenames(folder):    
    return {'a': os.path.join(folder, A_CSV), 
            'q': os.path.join(folder, Q_CSV), 
            'm': os.path.join(folder, M_CSV)}

DATABASE_CSV_FILENAMES   = dataframe_dump_csv_filenames(DATABASE_DIR)
OUTPUTDIR_CSV_FILENAMES = dataframe_dump_csv_filenames(OUTPUT_DIR) 
        