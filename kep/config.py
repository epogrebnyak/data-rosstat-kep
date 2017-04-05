import os

# USER INPUT: change this when new data arrives
CURRENT_MONTH = 2017, 2

"""Project paths and filenames:
    
data-rosstat-kep => PROJECT_FOLDER
  \output
    \png      
  \data
     \YYYY\indXX => get_data_folder(year=YYYY, month=XX)
  \kep => CODE_FOLDER
     \config.py => this file
     
"""

# locate current file config.py
CODE_FOLDER, _ = os.path.split(__file__)
# one level up
PROJECT_FOLDER, _ = os.path.split(CODE_FOLDER)
# data dir is in root folder
DATA_FOLDER = os.path.join(PROJECT_FOLDER, 'data')

# use template to obtain current month folder
def __get_data_folder__(year, month):
    return os.path.join(DATA_FOLDER, str(year), 'ind' + str(month).zfill(2))
    
CURRENT_MONTH_DATA_FOLDER = __get_data_folder__(*CURRENT_MONTH)
CSV_PATH = os.path.join(CURRENT_MONTH_DATA_FOLDER, 'tab.csv')

# not used in trimmed version 
# TOC_FILE = os.path.join(CURRENT_MONTH_DATA_FOLDER, 'toc.txt')

# parsing defiitions
PARSING_DEFINITIONS_FOLDER = os.path.join(DATA_FOLDER, 'parsing_definitions')
DEFAULT_SPEC_FILE = "__spec.txt"
SPEC_FILENAME_MUST_CONTAIN = "spec"

##  output
OUTPUT_DIR = os.path.join(PROJECT_FOLDER, 'output')
PNG_FOLDER = os.path.join(OUTPUT_DIR, 'png')
PDF_FILE   = os.path.join(OUTPUT_DIR, 'monthly.pdf')
MD_FILE    = os.path.join(OUTPUT_DIR, 'images.md')
# VARNAMES_FILE = os.path.join(OUTPUT_DIR, 'varnames.md')

## xls(x) output
XLSX_FILE = os.path.join(OUTPUT_DIR, 'kep.xlsx' )
XLS_FILE  = os.path.join(OUTPUT_DIR, 'kep.xls')

## csv output
A_CSV = 'data_annual.txt'
Q_CSV = 'data_quarter.txt'
M_CSV = 'data_monthly.txt'

def get_csv_filename(freq):    
    return {'a': os.path.join(OUTPUT_DIR, A_CSV), 
            'q': os.path.join(OUTPUT_DIR, Q_CSV), 
            'm': os.path.join(OUTPUT_DIR, M_CSV)}[freq]
