# -*- coding: cp1251 -*-
"""
Test yaml input / config file.
"""

import yaml as ya

reader_dict = {
  'CPI' : 'read12'
 }


label_dict = {
"1.7. Инвестиции в основной капитал":  ['I','bln_rub'],
"1.14. Объем платных услуг населению": ['Uslugi','bln_rub']
 }
 
sec_label_dict =    {
 "в % к соответствующему периоду предыдущего года": 'yoy',
 "в % к предыдущему периоду": 'rog'
 }
 
doc1 = """в % к соответствующему периоду предыдущего года : yoy
в % к предыдущему периоду : rog""" 
    
doc2 = """1.7. Инвестиции в основной капитал :
  - I
  - bln_rub 
1.14. Объем платных услуг населению : 
  - Uslugi
  - bln_rub
"""

def test_docs():
    assert ya.load(doc1) == sec_label_dict
    assert ya.load(doc2) == label_dict

doc3 = doc1+"\n---\n"+doc2  

doc4 = "CPI : read12" 

doc5 = doc4 + "\n---\n"+doc3 

def test_with_doc():
    spec = [d for d in ya.load_all(doc5)]
    assert spec[0] == reader_dict
    assert spec[1] == sec_label_dict
    assert spec[2] == label_dict

from word import load_spec_from_yaml

import pytest

@pytest.fixture(scope="module")
def filename(request):
    p = "sample_spec.txt"
    with open(p,"w") as file:
        file.write(doc5)
    def fin():
        import os
        os.remove(p)
    request.addfinalizer(fin)    
    return p
  
def test_with_file(filename):    
    d1, d2, d3 = load_spec_from_yaml(filename)
    assert d1 == label_dict
    assert d2 == sec_label_dict
    assert d3 == reader_dict

if __name__ == "__main__":
    test_docs()  
    test_with_doc()
    p = filename()
    test_with_file(p)   