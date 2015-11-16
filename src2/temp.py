# -*- coding: utf-8 -*-
import itertools
import tabulate
from common import docstring_to_file

FILLER = "<...>"

from query import get_dfm
df = get_dfm()
var_names = list(df.columns)

# ----------------- 
from csv2db import get_filenames
data_folder = "../data/ind09/"
csv, spec, cfg = get_filenames(data_folder)

from load_spec import load_spec
default_dicts = load_spec(spec)
print(default_dicts)
# -----------------

def get_title(name, ddict = default_dicts):
    words = name.split('_')
    title_abbr = '_'.join(itertools.takewhile(lambda word: word.isupper(), words))
    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr in two_labels_list[0]:
            return title
    return FILLER       
    
inspection = dict((v[1], k.split(",")[-1]) for k,v in default_dicts[0].items())

UNITS_ABBR = {
# --- part from default_dicts [0]
  'rog':'в % к предыдущему периоду'
, 'rub':'рублей'
, 'yoy':'в % к аналог. периоду предыдущего года' 
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

def get_unit(name):
    words = name.split('_')
    unit_abbr = '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))
    if unit_abbr in UNITS_ABBR.keys():
        return UNITS_ABBR[unit_abbr]
    else:
        return FILLER 

assert get_title('CONSTR_yoy') == 'Объем работ по виду деятельности "Строительство"'
assert get_unit('CONSTR_yoy') == 'в % к аналогичному периоду предыдущего года' 

def get_var_list_components():
    df = get_dfm()
    var_names = list(df.columns)
    return [[vn, get_title(vn), get_unit(vn)] for vn in var_names]

def dump_var_list_explained():
    table = get_var_list_components()
    tab_table = tabulate.tabulate(table, ["Код", "Описание", "Ед.изм."], 
                                  tablefmt="pipe")   
    docstring_to_file(tab_table, "varnames.md", "output") 

# note: not using additional dictionaries yet
# from label_csv import _get_segment_specs_no_header_doc
# segment_specs = _get_segment_specs_no_header_doc(cfg)
# print(segment_specs)