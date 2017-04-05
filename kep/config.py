import os

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


#find latest data folder

def subdirectories(root_dir):
    return [f for f in os.listdir(root_dir)
           if not os.path.isfile(os.path.join(root_dir,f))]


def max_year():
    dirs = subdirectories(DATA_FOLDER)
    return max([int(f) for f in dirs if f.startswith("20")])


def max_month():
    year_dir = os.path.join(DATA_FOLDER, str(max_year()))
    dirs = subdirectories(year_dir)
    return max([int(f.replace('ind','')) for f in dirs if f.startswith("ind")])


def current_month_data_dir(year, month):
    month_dir = 'ind'+str(month).zfill(2)
    return os.path.join(DATA_FOLDER, str(year), month_dir)

CURRENT_MONTH = max_year(), max_month()
# may override manually below
# CURRENT_MONTH = 2017, 2

CURRENT_MONTH_DATA_FOLDER = current_month_data_dir(*CURRENT_MONTH)
CSV_FILENAME = 'tab.csv'
CSV_PATH = os.path.join(CURRENT_MONTH_DATA_FOLDER, CSV_FILENAME)

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