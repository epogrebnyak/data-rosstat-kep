# -*- coding: utf-8 -*-
"""
"""
#todo:
#1 - добавить api2.py в конец query.py, поменять ссылки import на query в дригих файлах


# нужен список переменных с текстовыми названиями, сформированный по фактическому импорту данных
#2- нужны функции get_unit(name), get_title()

from api2 import get_dfm
df = get_dfm()
var_names = list(df.columns)

from csv2db import get_filenames
data_folder = "../data/ind09/"
csv, spec, cfg = get_filenames(data_folder)

from load_spec import load_spec
default_dicts = load_spec(spec)
print(default_dicts)

name = df['CONSTR_yoy'].name

def get_title(name, ddict = default_dicts):
    return 'Объем работ по виду деятельности "Строительство"'


     
# inspection = dict((v[1], k.split(",")[-1]) for k,v in default_dicts[0].items())

UNITS_ABBR = {
# --- part from default_dicts [0]
  'rog':'в % к предыдущему периоду'
, 'rub':'рублей'
, 'yoy':'в % к аналогичному периоду предыдущего года' 
# --- part from default_dicts [1]
, 'bln t-km': 'млрд. т-км'
, 'bln_t-km': 'млрд. т-км'
, 'percent': '%'
, 'bln_rub': 'млрд. руб.'
, 'bln rub': 'млрд. руб.'
, 'bln_rub_fix': 'млрд. руб. (в фикс. ценах)'
, 'mln_t': 'млн. т'
, 'TWh': 'млрд. кВт·ч'
, 'eop': 'на конец периода'
, 'bln': 'млрд.'
, 'units': 'штук'
, 'th': 'тыс.'
}

def get_unit(name, ddict = default_dicts):
    return UNITS_ABBR['yoy']

assert get_title('CONSTR_yoy') == 'Объем работ по виду деятельности "Строительство"'
assert get_unit('CONSTR_yoy') == 'в % к аналогичному периоду предыдущего года' 



# note: not using additional dictionaries yet
#from label_csv import _get_segment_specs_no_header_doc
#segment_specs = _get_segment_specs_no_header_doc(cfg)
#print(segment_specs)

