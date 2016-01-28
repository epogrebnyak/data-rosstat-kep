# -*- coding: utf-8 -*-
"""Paths and filenames."""

import os
from kep.common.inputs import Folder

RESERVED_FILENAMES = {'csv':'tab.csv', 'cfg':'__cfg.txt'}  

# root folders

# one level up from this file 
_PROJECT_SRC_DIR  = Folder(__file__).path
_PROJECT_ROOT_DIR = Folder(__file__).up(1).path

#test folder
TESTDATA_DIR = os.path.join(_PROJECT_SRC_DIR, "tests", "temp")        

#databases
DATABASE_DIR        = os.path.join(_PROJECT_SRC_DIR, "database")
TEST_SQLITE_FILE    = os.path.join(DATABASE_DIR, "test.sqlite3")
DEFAULT_SQLITE_FILE = os.path.join(DATABASE_DIR, "kep.sqlite3")

# data
CURRENT_MONTH_DATA_FOLDER = os.path.join(_PROJECT_ROOT_DIR, 'data', '2015', 'ind12')
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
ANNUAL_CSV  = os.path.join(OUTPUT_DIR, 'data_annual.txt')
QUARTER_CSV = os.path.join(OUTPUT_DIR, 'data_quarter.txt')
MONTHLY_CSV = os.path.join(OUTPUT_DIR, 'data_monthly.txt')

# NOTE: mixed use of 'folder' and 'dir' is variable names (not critical)