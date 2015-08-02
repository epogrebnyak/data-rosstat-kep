# -*- coding: cp1251 -*-
"""
Created on Sun Aug  2 13:25:18 2015

@author: Евгений
"""

import yaml as ya

def load_spec_from_yanl(p):
    spec = [d for d in ya.load_all(p)]
    return spec[0], spec[1]     


 # todo: dump to yaml

# todo: dump to yaml
label_dict = {
"1.7. Инвестиции в основной капитал":  ['I','bln_rub'],
"1.14. Объем платных услуг населению": ['Uslugi','bln_rub']
 }
 
sec_label_dict =    {
 "в % к соответствующему периоду предыдущего года": 'yoy',
 "в % к предыдущему периоду": 'rog'
 }

 
# print(ya.dump_all([sec_label_dict,label_dict], allow_unicode=True))
 
doc1 = """
в % к соответствующему периоду предыдущего года : yoy
в % к предыдущему периоду : rog
---
""" 

doc2 = """
1.7. Инвестиции в основной капитал :
 - I
 - bln_rub 
1.14. Объем платных услуг населению : 
 - Uslugi
 - bln_rub 
---
"""

doc3 = doc1+doc2

 
spec = [d for d in ya.load_all(doc3)]
assert spec[0] == sec_label_dict
assert spec[1] == label_dict

with open("1-07_spec.txt","w") as file:
    file.write(doc3)
