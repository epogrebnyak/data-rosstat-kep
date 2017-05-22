"""File paths for CSV file and parsing definitions.

Assume following directory structure:
  <REPO_FOLDER>\src\kep       <- this is <PACKAGE_FOLDER>
               \data          <- this is <DATA_FOLDER>
                    \source_csv_rosstat
                    \source_csv_sample
                    \parsing_definitoins

"""

import os

def level_up(_dir):
    """Get parent directory of *_dir*."""
    upper_dir, _ = os.path.split(_dir)
    return upper_dir


# locate current file config.py
PACKAGE_FOLDER, _ = os.path.split(__file__)
# two levels up
REPO_FOLDER = level_up(level_up(PACKAGE_FOLDER))
# data dir is in repo root folder
DATA_FOLDER = os.path.join(REPO_FOLDER, 'data')


# datafile location
def get_default_csv_path():
    """Source data CSV file"""
    return os.path.join(DATA_FOLDER,'sample_csv','tab.csv')


# specfile locations
PARSING_DEFINITIONS_FOLDER = os.path.join(DATA_FOLDER,'parsing_definitions')
DEFAULT_SPEC_FILE = "__spec.txt"
SPEC_FILENAME_MUST_CONTAIN = "spec"

def get_default_spec_folder():
    return PARSING_DEFINITIONS_FOLDER 

def locate_mainspec(folder):
    path = os.path.join(folder, DEFAULT_SPEC_FILE)
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError(path)

def get_mainspec_filepath():
    folder = get_default_spec_folder()
    return locate_mainspec(folder)
        
def locate_additional_specs(folder):
    """Returns list of filepaths for additional parsing definitions
       found in *folder*."""
    paths = [os.path.join(folder, f) 
             for f in os.listdir(folder)             
             if SPEC_FILENAME_MUST_CONTAIN in f
             and f != DEFAULT_SPEC_FILE]
    return [p for p in paths if os.path.isfile(p)]


# TODO - move to test_config.py

import unittest
class TestPaths(unittest.TestCase):
    
    def test_default_dir(self):
        _dir = get_default_spec_folder()
        assert get_main_spec_filepath(_dir) == 'parsing_definitions\\__spec.txt'
        assert get_additional_specs_filepaths(_dir) == ['parsing_definitions\\__spec_budget_expense.txt',
 'parsing_definitions\\__spec_budget_revenue.txt',
 'parsing_definitions\\__spec_budget_surplus.txt',
 'parsing_definitions\\__spec_cpi.txt',
 'parsing_definitions\\__spec_foreign_trade.txt',
 'parsing_definitions\\__spec_invest_src.txt',
 'parsing_definitions\\__spec_overdue.txt',
 'parsing_definitions\\__spec_profit.txt',
 'parsing_definitions\\__spec_receivable.txt',
 'parsing_definitions\\__spec_retail.txt']
    
if __name__ == '__main__':
    unittest.main()