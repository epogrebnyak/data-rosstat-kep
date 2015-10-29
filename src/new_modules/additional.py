# -*- coding: utf-8 -*-
"""Compact representation of raw csv import and transformation controlled by yaml config files"""

from common import yield_csv_rows

###############################################################################
from hardcoded import init_raw_csv_file, init_main_yaml, init_config_yaml, init_additional_yaml
RAW_FILE = init_raw_csv_file()        
SPEC_FILE = init_main_yaml()

ADDITIONAL_SPEC_FILE = init_additional_yaml()
CFG_FILE = init_config_yaml()


def get_labelled_rows (raw_csv_filename, segment_info_yaml_filename):
    raw_rows = read_raw_csv_as_list(raw_csv_filename)    
    default_spec  = get_default_spec(segment_info_yaml_filename)
    segment_specs = get_segment_specs(segment_info_yaml_filename)
    labelled_rows = label_raw_raws_by_spec(raw_rows, default_spec, segment_specs)    
    return labelled_rows 

def read_raw_csv_as_list(raw_csv_filename):
    return list(yield_csv_rows(raw_csv_filename))    

#--------------------
# Импорт спецификации по сегментам - см. hardcoded.py
# Не делать - код и тесты потом можно перенести в load_spec.py

from load_spec import _get_safe_yaml
def get_default_spec(segment_info_yaml_filename):
    yaml = _get_safe_yaml(segment_info_yaml_filename)
    return load_spec(yaml[0])

def get_segment_specs(segment_info_yaml_filename):
    yaml = _get_safe_yaml(segment_info_yaml_filename)
    return [[start_line, end_line, load_spec(specfile)] \
        for start_line, end_line, specfile in yaml[1:]]
        
REF_HEADER_DICT = {'Производство транспортных средств и оборудования': ['PROD_TRANS', 'yoy'], 
'1.7. Инвестиции в основной капитал': ['I', 'bln_rub'], 
'1.2. Индекс промышленного производства': ['PROD', 'yoy']}

REF_UNIT_DICT = {'период с начала отчетного года': 'rytd', 
'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy', 
'отчетный месяц в % к предыдущему месяцу': 'rog', 
'в % к предыдущему периоду': 'rog', 
'в % к соответствующему месяцу предыдущего года': 'yoy', 
'в % к соответствующему периоду предыдущего года': 'yoy'}

default_spec = get_default_spec(CFG_FILE)
assert REF_HEADER_DICT == default_spec[0]
assert REF_UNIT_DICT == default_spec[1]

segment_specs = get_segment_specs(CFG_FILE)

