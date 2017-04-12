"""File paths for CSV file and parsing definitions."""

import os

# datafile location

def get_default_csv_path():
    """Source data CSV file"""
    return os.path.join('data','tab.csv')


# specfile locations

PARSING_DEFINITIONS_FOLDER = 'parsing_definitions'
DEFAULT_SPEC_FILE = "__spec.txt"
SPEC_FILENAME_MUST_CONTAIN = "spec"

def get_default_spec_path():
    """Returns default parsing instruction filepath."""
    return os.path.join(PARSING_DEFINITIONS_FOLDER, DEFAULT_SPEC_FILE)

           
def get_all_spec_paths():
    """Returns list of additional parsing instructions filepaths."""
    paths = [os.path.join(PARSING_DEFINITIONS_FOLDER ,f) 
             for f in os.listdir(PARSING_DEFINITIONS_FOLDER )             
             if SPEC_FILENAME_MUST_CONTAIN in f
             and f != DEFAULT_SPEC_FILE]    
    return [p for p in paths if os.path.isfile(p)]