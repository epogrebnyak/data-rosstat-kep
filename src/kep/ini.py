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
        
        
# csv file parameters
ENCODING = 'utf8'
CSV_FORMAT = dict(delimiter='\t', lineterminator='\n')

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

# IDEA: dir structure from "datadriven"

"""
\data
  \raw      
      \word
  \interim
      \parsing_definitions
      \sample
      \csv          
  \processed
      \latest
      \2017
      \...
"""


# TODO: output directory locations

import os
from pathlib import Path


# folder structure
me = Path(os.path.abspath(__file__))
levels_up = 2
data_folder = me.parents[levels_up] / 'data' 
rosstat_folder = data_folder / 'source_csv_rosstat'
spec_folder = data_folder / 'parsing_definitions'
PREFIX = "ind"

# raw data
class RawDataLocations():
    
    def __init__(self, folder, prefix = PREFIX):
        self.folder = folder
        self.prefix = prefix
        
    def max_year(self):
        dirs = [f for f in self.folder.iterdir() if f.is_dir()]
        gen = [int(f.name) for f in dirs]
        return max(gen)
        
    def max_month(self):
        subfolder = self.folder / str(self.max_year())
        dirs = [f for f in subfolder.iterdir() if f.is_dir()]        
        gen = [int(f.name.replace(self.prefix,'')) 
               for f in dirs if f.name.startswith(self.prefix)]
        return max(gen) 
    
    def get_latest(self):
        return self.max_year(), self.max_month()

def get_latest():
    loc = RawDataLocations(rosstat_folder)
    return loc.max_year(), loc.max_month()

# CSV files 
def get_path_csv_sample(version = 0):
    """Return sample source CSV file path (e.g. tab0.csv)
       Used in testing."""
    path = data_folder / 'source_csv_sample' / 'tab{}.csv'.format(version)
    return __safe_file__(path)


def get_path_csv_data(year=None, month=None):
    """Return CSV file path based on year and month"""
    if not year or not month:
        year, month = get_latest()
    month_dir = PREFIX+str(month).zfill(2)
    return rosstat_folder / str(year) / month_dir / 'tab.csv'

# specfile locations
DEFAULT_SPEC_FILE = '__spec.txt'
SPEC_FILENAME_PATTERN = '*spec*.txt'


def __locate_mainspec__(folder):
    """Find MAIN parsing definition text file in *folder*."""
    path = folder / DEFAULT_SPEC_FILE
    return __safe_file__(path)

    
def __locate_additional_specs__(folder):
    """Return list of ADDITIONAL specifications filepaths in *folder*."""
    for f in folder.glob(SPEC_FILENAME_PATTERN):
        if f.is_file() and f.name != DEFAULT_SPEC_FILE:
            yield f


def get_mainspec_filepath():
    return str(__locate_mainspec__(spec_folder))

    
def get_additional_filepaths():
    return  [str(fn) for fn in __locate_additional_specs__(spec_folder)]  
    

if __name__ == '__main__':
    z = get_additional_filepaths()