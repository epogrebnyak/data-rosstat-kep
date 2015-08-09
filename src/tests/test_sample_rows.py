# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 14:32:29 2015

@author: Евгений
"""

rows1 = [['1.2. Индекс промышленного производства1) / Industrial Production index1)', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
, ['1.2.1. Индексы производства по видам деятельности (без исключения сезонности и фактора времени) / Industrial Production indices by Industry (without seasonal and time factor adjustment)', '', '', '', '', '', '', '', '', '', '', '', '']
]

def emit_rows(sample):
    for row in sample:
        yield row

dict_headline = {"Индекс промышленного производства":  ['I_PP','prev']
#, "Индексы производства по видам деятельности": ['ZZZ','bln_rub']
 }
 
dict_support =   { "в % к соответствующему периоду предыдущего года": 'yoy',
 "в % к предыдущему периоду": 'rog'
 }
 
from label_csv import yield_row_with_labels_core,  print_rows_with_labels

for row in yield_row_with_labels_core(emit_rows(rows1), dict_headline, dict_support):
    pass
#   print(row)

#print_rows_with_labels(emit_rows(rows1), dict_headline, dict_support)


######################################################################################################################

from common import yield_csv_rows

#for row in  yield_csv_rows("sample.csv"):
#    print(row)
    
#print_rows_with_labels(yield_csv_rows("sample.csv"), dict_headline, dict_support)


#################################################################################
from label_csv import adjust_labels, get_label_in_text, get_label_on_start, UNKNOWN_LABELS

def test_unknown():
    line = '1.2.1. Индексы производства по видам деятельности (без исключения сезонности и фактора времени) '
    cur_labels = ['I_PP', 'prev']
    assert adjust_labels(line, cur_labels, dict_headline, dict_support) == ['unknown_var', 'unknown_unit']
