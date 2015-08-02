# -*- coding: cp1251 -*-
"""
Created on Sun Aug  2 13:25:18 2015

@author: Евгений
"""

import yaml as ya


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

def test_with_doc():
    spec = [d for d in ya.load_all(doc3)]
    assert spec[0] == sec_label_dict
    assert spec[1] == label_dict

def load_spec_from_yaml(p):
    """Returns two dictionaries of label specifications. 
       
       Unpacking:
          full_dict, unit_dict = load_spec_from_yaml(p)
    """
    with open(p, 'r') as file:
        spec = [d for d in ya.load_all(file)]
    return spec[1], spec[0]    

# print(ya.dump_all([sec_label_dict,label_dict], allow_unicode=True))

  
def test_with_file(p):
    d1, d2 = load_spec_from_yaml(p)
    assert d1 == label_dict
    assert d2 == sec_label_dict

if __name__ == "__main__":
    test_docs()  
    test_with_doc()
    
    p = "sample_spec.txt"
    with open(p,"w") as file:
        file.write(doc3)
        
    test_with_file(p)

    