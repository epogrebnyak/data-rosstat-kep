"""Read parsing definition and csv file."""

import kep.ini as ini
from kep.reader.csv_data import csv_file_to_dicts
from kep.reader.parsing_definitions import ParsingDefinition, Specification

# 1. NOT TODO: use Path access methods to read file contents instead on custom File() class
# 2. MAYDO: use csv module to read and write csv filed in 
# 3. TODO: integrate word2csv with kep.ini file location. Aim - generate many csv files for different days.
# 4. TODO: unzip/unrar word files 
# 5. TODO: move Tempfile to tests

def get_pdef():
    """Return parsing definition."""
    spec_path = ini.get_mainspec_filepath().__str__()
    return ParsingDefinition(path=spec_path)

def get_spec():
    """Return extended parsing definition."""
    return Specification(path=ini.get_mainspec_filepath(), 
                         pathlist=ini.get_additional_filepaths())   
    
    
def get_csv_dicts(year=None, month=None):
    """Get CSV data. Defaults to most recent locally saved dataset."""
    if not year or not month:
        year, month = ini.get_latest()
    csv_path = ini.get_path_csv_data(year, month).__str__()
    return csv_file_to_dicts(csv_path)