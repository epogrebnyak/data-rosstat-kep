# -*- coding: utf-8 -*-

from files import File


"""Read CSV file as stream of rows.

   Usage:        
       gen =  CSV_Reader(path).yield_dicts()

"""       

def doc_to_lists(doc: str) -> list:
    """Splits string by EOL and tabs, returns list of lists."""
    return [r.split('\t') for r in doc.split('\n')]

def row_as_dict(row: list) -> dict:
    """Represents csv *row* content as a dictionary with following keys:
    
       'head' - string, first element in list *row* (may be year or table header)
       'data' - list, next elements in list *row*, ususally data elements like ['15892', '17015', '18543', '19567']
       'label' - placeholder for row label. Label is a dictionary like dict(var="GDP", unit="bln_rub")
    """
    return dict(head=row[0],
                data=row[1:])


def yield_rows_as_dicts(rows: list) -> iter:
    """Yield non-empty csv rows as dictionaries. """
    for r in rows:
        # check if list is not empty and first element is not empty
        if r and r[0]:
            yield row_as_dict(r)

def yield_dicts_from_file(path):
    doc = File(path).read_text()
    rows = doc_to_lists(doc)
    return yield_rows_as_dicts(rows)
    
def yield_dicts_from_string(doc):
    rows = doc_to_lists(doc)
    return yield_rows_as_dicts(rows)    


class CSV_Reader():
    
    def __init__(self, path: str):
        """Read data from *path* file"""
        doc = File(path).read_text()
        self.rows = doc_to_lists(doc)
        
    def yield_dicts(self): 
        """Iterator used to expose file contents."""
        return yield_rows_as_dicts(self.rows)