# -*- coding: utf-8 -*-

import os

"""
CSV files
=========

Possible CSV sources at different abstraction levels are:

    1. Production:
    - CSV file at newest available 'data\YYYY\indMM\' folder **NOT TODO      
    - CSV file in local folder:  get_default_csv_content()
        
    2. Testing:
    - test CSV file 
    - text string with CSV content
    - list of lists, each list containing CSV row elements      

"""    
    
  

ENCODING = 'utf8'

class File():
    """Custom reader for dirty raw CSV file."""
    
    def __init__(self, path: str):
        """Set file path, raise error if file does not exist."""
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError(path)

    def __repr__(self):
        return os.path.normpath(self.path)

    def __yield_lines__(self):
        """Iterate over CSV file by line."""
        with open(self.path, 'r', encoding=ENCODING) as f:
            for line in f:
                if line.endswith('\n'):
                    yield line[0:-1]
                else:
                    yield line

    def read_text(self):
        """Read text from file."""
        return "\n".join(self.__yield_lines__())
        
    def get_raw_data(self):
        """Read csv file content from file."""
        return doc_to_lists(self.read_text())

def doc_to_lists(doc: str) -> list:
    """Splits string by EOL and tabs, returns list of lists."""
    return [r.split('\t') for r in doc.split('\n')]

def get_default_csv_path():
    """Production local CSV file"""
    # FIXME LOW - use custom directory structure to locate CSV
    return 'tab.csv'

def get_default_csv_content():
    path = get_default_csv_path()
    return File(path).get_raw_data()

def read_csv_from_file(path):    
    return File(path).get_raw_data()

def save_to_temp_csv_file(string):
    # FIXME LOW 
    path = "tmp.txt"
    return path

if __name__ == "__main__": 
    assert len(get_default_csv_content()) > 4600
    assert doc_to_lists("2015\t99,2\t99,9\n2016\t101,3\t101,1") == [['2015', '99,2', '99,9'], ['2016', '101,3', '101,1']]