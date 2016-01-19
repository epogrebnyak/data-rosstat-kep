import os

RESERVED_FILENAMES = {'csv':"tab.csv", 'spec':"__tab_spec.txt", 'cfg':"__tab_cfg.txt"}  

def current_folder():
    curpath = os.path.realpath(__file__)
    return os.path.dirname(curpath)

def level_up(path, n = 1):
    for i in range(n):
        path = os.path.split(path)[0]
    return path

# root folders
PROJECT_SRC_FOLDER = current_folder()    
PROJECT_ROOT_PATH = level_up(current_folder(), n = 1)

#testfolder
TESTFILE_DIR    = os.path.join(PROJECT_ROOT_PATH, 'rowsystem', 'tests', 'temp')

#testfolder
TEST_SQLITE_FILE    = os.path.join(PROJECT_SRC_FOLDER, "database", "test.sqlite3")
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