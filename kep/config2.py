"""Project paths and filenames:
    
data-rosstat-kep
  \kep (=> ROOT_DIR)
    \src (=> CODE_FOLDER)
      \config.py (=> this file)
  \data 
      \YYYY\indXX (=> get_data_folder(year=YYYY, month=XX))
  \output
      \png
      
"""

import os

# USER INPUT: change this when new data arrives
CURRENT_MONTH = 2016, 7

# TODO - may list last available month based on local file availability

#------------------------------------------------------------------------------
# DO NOT EDIT BELOW

# locate current file config.py
CODE_FOLDER, _ = os.path.split(__file__)

# one level up from this file 
ROOT_DIR, _ = os.path.split(CODE_FOLDER)

# data dir is in root folder
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# use template to obtain this month folder
def get_data_folder(year, month):
    return os.path.join(DATA_DIR, str(year), 'ind' + str(month).zfill(2))
    
CURRENT_MONTH_DATA_FOLDER = get_data_folder(*CURRENT_MONTH)
TOC_FILE = os.path.join(CURRENT_MONTH_DATA_FOLDER, "toc.txt")

# parsing defiitions
PARSING_DEFINITIONS_FOLDER = os.path.join(DATA_DIR, 'parsing_definitions')

# filenames
RESERVED_FILENAMES = {'csv':'tab.csv', 'cfg':'cfg.txt'}  

##  output
OUTPUT_DIR    = os.path.join(ROOT_DIR, 'output')
PNG_FOLDER    = os.path.join(OUTPUT_DIR, 'png')
PDF_FILE      = os.path.join(OUTPUT_DIR, 'monthly.pdf')
MD_FILE       = os.path.join(OUTPUT_DIR, 'images.md')
VARNAMES_FILE = os.path.join(OUTPUT_DIR, 'varnames.md')

## xls(x) output
XLSX_FILE   = os.path.join(OUTPUT_DIR, 'kep.xlsx' )
XLS_FILE    = os.path.join(OUTPUT_DIR, 'kep.xls')

## csv output
A_CSV = 'data_annual.txt'
Q_CSV = 'data_quarter.txt'
M_CSV = 'data_monthly.txt'

def get_csv_filename(freq):    
    return {'a': os.path.join(OUTPUT_DIR, A_CSV), 
            'q': os.path.join(OUTPUT_DIR, Q_CSV), 
            'm': os.path.join(OUTPUT_DIR, M_CSV)}[freq]


# check valid paths 
# TODO - move to tests
assert os.path.exists(CURRENT_MONTH_DATA_FOLDER)
assert os.path.exists(get_csv_filename('a'))


## toc file 
#TOC_FILE = os.path.join(CURRENT_MONTH_DATA_FOLDER, "toc.txt")
#
#
#
## data folder - change here for next month --------------------------------------------
##
#CURRENT_MONTH_DATA_FOLDER = os.path.join(_PROJECT_ROOT_DIR, 'data', '2016', 'ind07')
##
## --------------------------------------------------------------------------------------
#
##test folder
#TESTDATA_DIR = os.path.join(_PROJECT_SRC_DIR, "tests", "temp")        
#
##databases
#DATABASE_DIR        = os.path.join(_PROJECT_SRC_DIR, "database")
#TEST_SQLITE_FILE    = os.path.join(DATABASE_DIR, "test.sqlite3")
#DEFAULT_SQLITE_FILE = os.path.join(DATABASE_DIR, "kep.sqlite3")
#
## toc file 
#TOC_FILE = os.path.join(CURRENT_MONTH_DATA_FOLDER, "toc.txt")
#
## graphic output
#OUTPUT_DIR    = os.path.join(_PROJECT_ROOT_DIR, 'output')
#PNG_FOLDER    = os.path.join(OUTPUT_DIR, 'png')
#PDF_FILE      = os.path.join(OUTPUT_DIR, 'monthly.pdf')
#MD_FILE       = os.path.join(OUTPUT_DIR, 'images.md')
#VARNAMES_FILE = os.path.join(OUTPUT_DIR, 'varnames.md')
#
## xls and csv output
#XLSX_FILENAME = 'kep.xls' 
#XLS_FILENAME  = 'kep.xlsx'   
#XLSX_FILE   = os.path.join(OUTPUT_DIR, XLSX_FILENAME)
#XLS_FILE    = os.path.join(OUTPUT_DIR, XLS_FILENAME)
#
#A_CSV = 'data_annual.txt'
#Q_CSV = 'data_quarter.txt'
#M_CSV = 'data_monthly.txt'
#
#def dataframe_dump_csv_filenames(folder):    
#    return {'a': os.path.join(folder, A_CSV), 
#            'q': os.path.join(folder, Q_CSV), 
#            'm': os.path.join(folder, M_CSV)}
#
#DATABASE_CSV_FILENAMES   = dataframe_dump_csv_filenames(DATABASE_DIR)
#OUTPUTDIR_CSV_FILENAMES = dataframe_dump_csv_filenames(OUTPUT_DIR)         