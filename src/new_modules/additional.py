# -*- coding: utf-8 -*-
"""Compact representation of raw csv import and transformation controlled by yaml config files"""

from common import yield_csv_rows
from load_spec import load_spec
from label_csv import is_year, adjust_labels, UNKNOWN_LABELS

###############################################################################
from hardcoded import init_raw_csv_file, init_main_yaml, init_config_yaml, init_additional_yaml
from hardcoded import PARSED_RAW_FILE_AS_LIST
RAW_FILE = init_raw_csv_file()        
SPEC_FILE = init_main_yaml()

ADDITIONAL_SPEC_FILE = init_additional_yaml()
CFG_FILE = init_config_yaml()


def get_labelled_rows(raw_csv_filename, segment_info_yaml_filename):
    raw_rows = read_raw_csv_as_list(raw_csv_filename)    
    default_spec  = get_default_spec(segment_info_yaml_filename)
    segment_specs = get_segment_specs(segment_info_yaml_filename)
    labelled_rows = label_raw_rows_by_spec(raw_rows, default_spec, segment_specs)
    return labelled_rows 

def read_raw_csv_as_list(raw_csv_filename):
    return list(yield_csv_rows(raw_csv_filename))    

#--------------------
# Импорт спецификации по сегментам - см. hardcoded.py

REF_HEADER_DICT = {'Производство транспортных средств и оборудования': ['PROD_TRANS', 'yoy'], 
'1.7. Инвестиции в основной капитал': ['I', 'bln_rub'], 
'1.2. Индекс промышленного производства': ['PROD', 'yoy']}

REF_UNIT_DICT = {'период с начала отчетного года': 'rytd', 
'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy', 
'отчетный месяц в % к предыдущему месяцу': 'rog', 
'в % к предыдущему периоду': 'rog', 
'в % к соответствующему месяцу предыдущего года': 'yoy', 
'в % к соответствующему периоду предыдущего года': 'yoy'}

from load_spec import _get_safe_yaml
def get_default_spec(segment_info_yaml_filename):
    yaml = _get_safe_yaml(segment_info_yaml_filename)
    return load_spec(yaml[0])

default_spec = get_default_spec(CFG_FILE)
assert REF_HEADER_DICT == default_spec[0]
assert REF_UNIT_DICT == default_spec[1]


def get_segment_specs(segment_info_yaml_filename):
    yaml = _get_safe_yaml(segment_info_yaml_filename)
    return [[start_line, end_line, load_spec(specfile)]
            for start_line, end_line, specfile in yaml[1:]]

segment_specs = get_segment_specs(CFG_FILE)

expected_segment_specs = [# список
 
[  # первая и вторая строка сегмента
  'Производство транспортных средств и оборудования', 
  '1.7. Инвестиции в основной капитал', 
  # кортеж из словарей header dict и unit dict 
  ({'1.2. Индекс промышленного производства': ['PROD', 'yoy'], 
   'Производство транспортных средств и оборудования': ['PROD_TRANS', 'yoy'], 
   '1.7. Инвестиции в основной капитал': ['I', 'bln_rub']}, 
  {'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy', 
  'отчетный месяц в % к предыдущему месяцу': 'rog', 'в % к предыдущему периоду': 'rog', 
  'период с начала отчетного года': 'rytd', 
  'в % к соответствующему месяцу предыдущего года': 'yoy', 
  'в % к соответствующему периоду предыдущего года': 'yoy'})]]

assert segment_specs == expected_segment_specs

#--------------------


def label_raw_rows_by_spec(raw_rows, default_spec, segment_specs):
    labels = UNKNOWN_LABELS[:]

    in_segment = False
    current_spec = default_spec
    current_end_line = None

    labelled_rows = []

    for row in raw_rows:
        if not row[0]:
            # junk row
            continue

        # Are we in the default spec?
        if not in_segment:
            # Do we have to switch to a custom one?
            for start_line, end_line, spec in segment_specs:
                if row[0].startswith(start_line):
                    # Yes!
                    in_segment = True
                    current_spec = spec
                    current_end_line = end_line
                    break
        else:
            # We are in a custom spec. Do we have to switch to the default one?
            if row[0].startswith(current_end_line):
                in_segment = False
                current_spec = default_spec
                current_end_line = None

        # Spec has been possibly switched, now may have to adjust labels
        if not is_year(row[0]):
            # label-switching row
            labels = adjust_labels(row[0], labels, current_spec[0], current_spec[1])
        else:
            # data row
            labelled_rows.append(labels + row)

    return labelled_rows

raw_csv = read_raw_csv_as_list(RAW_FILE)
labelled_rows = label_raw_rows_by_spec(raw_csv, default_spec, segment_specs)
assert labelled_rows == PARSED_RAW_FILE_AS_LIST
