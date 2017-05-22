"""File paths for:
    - CSV files (sample and actual data)
    - parsing definition
    - output directories

Assume following directory structure:

<REPO_FOLDER>\src\kep          
                     \ini.py
                     \*.py
             \data    
                  \source_csv_rosstat
                                     \YYYY
                                          \ind<MM>
                  \source_csv_sample
                                    \tab0.csv 
                  \parsing_definitions
"""

# TODO: output directory locations

import os
from pathlib import Path

me = Path(os.path.abspath(__file__))
data_folder = me.parents[2] / 'data' 
rosstat_folder = data_folder / 'source_csv_rosstat'
spec_folder = data_folder / 'parsing_definitions'

DEFAULT_SPEC_FILE = '__spec.txt'
SPEC_FILENAME_PATTERN = '*spec*.txt'


def __safe_file__(path):
    if path.exists() and path.is_file():
        return path
    else:
        raise FileNotFoundError(path.__str__())

        
def __safe_dir__(path):
    if path.exists() and path.is_dir():
        return path
    else:
        raise FileNotFoundError(path.__str__())        
        

def get_path_csv_sample(version = 0):
    """Return sample source CSV file path (used in testing).
       *version* allows to access files like tab0.csv, tab1.csv, etc"""
    path = data_folder / 'source_csv_sample' / 'tab{}.csv'.format(version)
    return __safe_file__(path)


def get_path_csv_data(year, month):
    """Return CSV file path based on year and month"""
    month_dir = 'ind'+str(month).zfill(2)
    path = rosstat_folder / str(year) / month_dir / 'tab.csv'
    return __safe_file__(path)

def max_year():
    gen = [int(f.name) for f in rosstat_folder.iterdir() if f.is_dir()]
    return max(gen)
    
def max_month():
    folder = rosstat_folder / str(max_year())
    gen = [int(f.name.replace('ind','')) 
           for f in folder.iterdir() 
           if f.is_dir() and f.name.startswith("ind")]
    return max(gen)  
    
def get_latest():
    return max_year(), max_month()
    

# specfile locations
def __locate_mainspec__(folder):
    """Generic search for MAIN parsing definition text file."""
    path = folder / DEFAULT_SPEC_FILE
    return __safe_file__(path)

    
def __locate_additional_specs__(folder):
    """Generic search for ADDITIONAL parsing definitions text files. 
       
       Returns list of filepaths for additional parsing definitions 
       found in *folder*."""
    for f in folder.glob(SPEC_FILENAME_PATTERN):
        if f.is_file() and f.name != DEFAULT_SPEC_FILE:
            yield f
#TODO: __locate_additional_specs__ not used.
            
            
def get_default_spec_folder():
    return __safe_dir__(spec_folder)   


def get_mainspec_filepath():
    return __locate_mainspec__(spec_folder).__str__()  

    
def get_additional_filepaths():
    return  [fn.__str__() for fn in __locate_additional_specs__(spec_folder)]  
    
    
if __name__ == '__main__':
    z = get_additional_filepaths()