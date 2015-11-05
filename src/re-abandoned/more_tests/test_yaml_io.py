# -*- coding: cp1251 -*-
"""
   Read configuration from yaml file.
"""

import yaml as ya
import pytest

########### Header labels
doc_header = """1.7. Инвестиции в основной капитал :
  - I
  - bln_rub 
1.14. Объем платных услуг населению : 
  - Uslugi
  - bln_rub"""

header_dict = {
"1.7. Инвестиции в основной капитал":  ['I','bln_rub'],
"1.14. Объем платных услуг населению": ['Uslugi','bln_rub']
 }

########### Unit labels
doc_unit  = """в % к соответствующему периоду предыдущего года : yoy
в % к предыдущему периоду : rog""" 
unit_dict =    {
"в % к соответствующему периоду предыдущего года": 'yoy',
"в % к предыдущему периоду": 'rog'
}
 
########### Special readers for some variables
doc_reader = "CPI : read12" 
reader_dict = {'CPI' : 'read12'}

########### Test 1 - reading docs individually
docs = [doc_reader, doc_unit, doc_header] 
dicts = [reader_dict, unit_dict, header_dict]

def test_individial_docs_and_dicts():
    for _doc, _dict in zip(docs, dicts):
        assert ya.load(_doc) == _dict

########### Test 2 - reading docs together
yaml_doc = "\n---\n".join(docs)

def test_in_one_doc():
    spec = [d for d in ya.load_all(yaml_doc)]
    assert spec[0] == reader_dict
    assert spec[1] == unit_dict
    assert spec[2] == header_dict

########### Test 3 - reading docs as a file
def _write_doc_to_file(doc, filename):
    with open(filename,"w") as f:
        f.write(doc)

def test_with_file():    
    filename = "sample_spec.txt"
    _write_doc_to_file(yaml_doc, filename)
    
    d1, d2, d3 = load_spec_from_yaml(filename)
    assert d1 == header_dict
    assert d2 == unit_dict
    assert d3 == reader_dict

########### Code itself

def load_spec(filename):
    """Wrapper for load_spec_from_yaml()"""
    headline_dict, support_dict, reader_dict = load_spec_from_yaml(p)
    return headline_dict, support_dict

def _import_specification(filename):
    """ Returns headline, unit and reader dictionaries from a yaml file containing:    
        # readers (very little lines)
        -----
        # units (a bit more lines)
        -----
        # headlines (many lines)"""
    with open(filename, 'r') as file:
        spec = [d for d in ya.load_all(file)]
    return spec[2], spec[1], spec[0]       

def load_spec_from_yaml(filename):
    """Returns specification dictionaries as a tuple. 
       Unpacking:
          header_dict, unit_dict, reader_dict = load_spec_from_yaml(filename)
    """
    try:
        return _import_specification(filename)
    except FileNotFoundError:
        raise FileNotFoundError ("Configurations file not found: " + filename)
    except:
        raise Exception ("Error parsing configurations file: " + filename)
        
if __name__ == "__main__":
    test_individial_docs_and_dicts()
    test_in_one_doc()
    test_with_file()
    