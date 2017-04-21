# -*- coding: utf-8 -*-

from files import File
from label import EMPTY_LABEL

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

def doc_to_lists(doc: str) -> list:
    """Splits string by EOL and tabs, returns list of lists."""
    return [r.split('\t') for r in doc.split('\n')]

def row_as_dict(row: list) -> dict:
    """Represents csv *row* content as a dictionary with following keys:
    
       'head' - string, first element in list *row* (may be year or table header)
       'data' - list, next elements in list *row*, ususally data elements like ['15892', '17015', '18543', '19567']
       'label' - placeholder for row label. Label is a dictionary like dict(var="GDP", unit="bln_rub")
    
    Examples:
    
    >>> row_as_dict(['1. Сводные показатели', '', ''])['head']
    '1. Сводные показатели'
    >>> row_as_dict(['2013', '15892', '17015', '18543', '19567'])['head']
    '2013'
    >>> row_as_dict(['2013', '15892', '17015', '18543', '19567'])['data']
    ['15892', '17015', '18543', '19567']
    >>> row_as_dict(['2013', '15892', '17015', '18543', '19567'])['label'] == {'unit': '', 'var': ''}
    True"""
    return dict(head=row[0],
                data=row[1:],
                label=EMPTY_LABEL)


def yield_rows_as_dicts(rows: list) -> iter:
    """Yield non-empty csv rows as dictionaries. """
    for r in rows:
        # check if list is not empty and first element is not empty
        if r and r[0]:
            yield row_as_dict(r)

class CSV_Reader():
    
    def __init__(self, path: str):
        """Read data from *path* file"""
        doc = File(path).read_text()
        self.rows = doc_to_lists(doc)
        
    def yield_dicts(self): 
        """Iterator used to work with file contents."""
        return yield_rows_as_dicts(self.rows)        

# 
# TODO: for testing we will need to dump string to temp file as Tempfile class in parsing_definitions.py
# 
#def save_to_temp_csv_file(string): 
#    path = "tmp.txt"
#    return path
# 


if __name__ == "__main__":
    
    # entry
    from config import get_default_csv_path
    csv_path = get_default_csv_path()
    csv_dicts = list(CSV_Reader(csv_path).yield_dicts())
    
    # testing
    assert doc_to_lists("2015\t99,2\t99,9\n2016\t101,3\t101,1") == [['2015', '99,2', '99,9'], ['2016', '101,3', '101,1']]    
    assert len(CSV_Reader(csv_path).rows) > 4600
    assert len(csv_dicts) > 4300