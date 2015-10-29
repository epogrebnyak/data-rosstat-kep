# -*- coding: cp1251 -*-
"""
   Read configuration from yaml file.
"""

import yaml as ya

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

comments = ["\n# Configuration file\n# 1. Names of special reader functions for some variables. Used for uncoventional tables."
           , "\n# 2. Unit headers <-> unit names"
           , "\n# 3. Main headers <-> variable names + default unit names"]
comments_and_docs = ["\n".join([c,d]) for c, d in zip(comments, docs)]
yaml_doc = "\n---\n".join(comments_and_docs)

def test_in_one_doc():
    spec = list(ya.load_all(yaml_doc))
    assert spec[0] == reader_dict
    assert spec[1] == unit_dict
    assert spec[2] == header_dict

########### Test 3 - reading docs as a file
def _write_doc_to_file(doc, filename):
    with open(filename,"w") as f:
        f.write(doc)

def test_with_file():    
    filename = "load_spec_sample.txt"
    _write_doc_to_file(yaml_doc, filename)
    
    d1, d2, d3 = load_spec_from_yaml(filename)
    assert d1 == header_dict
    assert d2 == unit_dict
    assert d3 == reader_dict
    
    d1, d2 = load_spec(filename)
    assert d1 == header_dict
    assert d2 == unit_dict

########### Code itself: load_spec

def load_spec(filename):
    """Entry point wrapper for load_spec_from_yaml()"""
    headline_dict, support_dict, reader_dict = load_spec_from_yaml(filename)
    return headline_dict, support_dict

def _get_yaml(filename):
    with open(filename, 'r') as file:
        spec = ya.load_all(file) # [d for d in ya.load_all(file)]
        return list(spec)    
        
def _get_safe_yaml(filename):        
    try:
        return _get_yaml(filename)
    except FileNotFoundError:
        raise FileNotFoundError ("Configurations file not found: " + filename)
    except:
        raise Exception ("Error parsing configurations file: " + filename)
        

def load_spec_from_yaml(filename):
    """Returns specification dictionaries as a tuple. 
       Unpacking:
          header_dict, unit_dict, reader_dict = load_spec_from_yaml(filename)
    """  
    """Returns headline, unit and reader dictionaries from a yaml file containing:    
        # readers (very little lines)
        -----
        # units (a bit more lines)
        -----
        # headlines (many lines)"""
    spec = _get_safe_yaml(filename)     
    return spec[2], spec[1], spec[0]       




        
if __name__ == "__main__":
    test_individial_docs_and_dicts()
    test_in_one_doc()
    test_with_file() 