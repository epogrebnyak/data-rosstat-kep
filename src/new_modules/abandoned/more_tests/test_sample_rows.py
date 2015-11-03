# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 14:32:29 2015

@author: Евгений
"""
 
from ..label_csv import yield_row_with_labels_core,  print_rows_with_labels
from ..common import yield_csv_rows
from ..label_csv import adjust_labels, get_label_in_text, get_label_on_start, UNKNOWN_LABELS


rows1 = [['1.2. Индекс промышленного производства1) / Industrial Production index1)', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
       , ['1.2.1. Индексы производства по видам деятельности (без исключения сезонности и фактора времени) / Industrial Production indices by Industry (without seasonal and time factor adjustment)', '', '', '', '', '', '', '', '', '', '', '', '']
]

dict_headline = {"Индекс промышленного производства":  ['I_PP','prev']
#, "Индексы производства по видам деятельности": ['ZZZ','bln_rub']
 }
 
dict_support =   { "в % к соответствующему периоду предыдущего года": 'yoy',
 "в % к предыдущему периоду": 'rog'
 }

def emit_rows(sample):
    for row in sample:
        yield row

def test_unknown():
    line = '1.2.1. Индексы производства по видам деятельности (без исключения сезонности и фактора времени) '
    cur_labels = ['I_PP', 'prev']
    assert adjust_labels(line, cur_labels, dict_headline, dict_support) == ['unknown_var', 'unknown_unit']