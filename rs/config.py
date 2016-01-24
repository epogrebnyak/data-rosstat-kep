"""Paths and filenames for this project."""

# maydo: mixed use of 'folder' and 'dir' is variable names (not critical)

import os
from inputs import Folder, CurrentFolder

RESERVED_FILENAMES = {'csv':'tab.csv', 'cfg':'__cfg.txt'}  

# root folders
PROJECT_SRC_FOLDER = CurrentFolder().path
PROJECT_ROOT_PATH = CurrentFolder().up(1).path

#test folder
TESTDATA_DIR = os.path.join(PROJECT_SRC_FOLDER, "tempfile")        

#databases
TEST_SQLITE_FILE    = os.path.join(PROJECT_SRC_FOLDER, "database", "test.sqlite3")   #may use Folder(PROJECT_SRC_FOLDER).join(...).path
DEFAULT_SQLITE_FILE = os.path.join(PROJECT_SRC_FOLDER, "database", "kep.sqlite3")

# data
CURRENT_MONTH_DATA_FOLDER = os.path.join(PROJECT_ROOT_PATH, 'data', '2015', 'ind11')

# graphic output
OUTPUT_DIR    = os.path.join(PROJECT_ROOT_PATH, 'output')
PDF_FILE      = os.path.join(OUTPUT_DIR, 'monthly.pdf')
MD_FILE       = os.path.join(OUTPUT_DIR, 'images.md')
PNG_FOLDER    = os.path.join(OUTPUT_DIR, 'png')
VARNAMES_FILE = os.path.join(OUTPUT_DIR, 'varnames.md')

# xls and csv output
XLSX_FILE   = os.path.join(OUTPUT_DIR, 'kep.xlsx')
XLS_FILE    = os.path.join(OUTPUT_DIR, 'kep.xls')
ANNUAL_CSV  = os.path.join(OUTPUT_DIR, 'data_annual.txt')
QUARTER_CSV = os.path.join(OUTPUT_DIR, 'data_quarter.txt')
MONTHLY_CSV = os.path.join(OUTPUT_DIR, 'data_monthly.txt')