# -*- coding: utf-8 -*-
""" Gerente variable list. Entry point: 
    dump_var_list_explained() writes output/varnames.md
"""
import itertools
import tabulate
from common import docstring_to_file

FILLER = "<...>"

from query import get_dfm
df = get_dfm()
var_names = list(df.columns)

# ----------------------------------------------------------------------------

from common import get_filenames
data_folder = "../data/ind09/"
csv, spec, cfg = get_filenames(data_folder)

from load_spec import load_spec
default_dicts = load_spec(spec)

# ----------------------------------------------------------------------------

def get_var_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))
assert get_var_abbr('PROD_E_TWh') == 'PROD_E' 

def get_unit_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))
assert get_unit_abbr('PROD_E_TWh') == 'TWh'

# ----------------------------------------------------------------------------

def get_title(name, ddict = default_dicts):
    title_abbr = get_var_abbr(name)
    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr == two_labels_list[0]:
            return title
    return FILLER       
assert get_title('CONSTR_yoy') == 'Объем работ по виду деятельности "Строительство"'
assert get_title('I_bln_rub') == 'Инвестиции в основной капитал'

# ----------------------------------------------------------------------------
    
inspection = dict((v[1], k.split(",")[-1]) for k,v in default_dicts[0].items())

UNITS_ABBR = {
# --- part from default_dicts [0]
    'rog':'в % к предыдущему периоду',
    'rub':'рублей',
    'yoy':'в % к аналог. периоду предыдущего года' ,
# --- part from default_dicts [1],
     #'bln t-km': 'млрд. т-км',
    'bln_t_km': 'млрд. т-км',
    'percent': '%',
    'bln_rub': 'млрд. руб.',
     #'bln rub': 'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'mln': 'млн. человек',
    'mln_t': 'млн. т',
    'TWh': 'млрд. кВт·ч',
    'eop': 'на конец периода',
    'bln': 'млрд.',
    'units': 'штук',
    'th': 'тыс.',
}

def get_unit(name):
    unit_abbr = get_unit_abbr(name)
    if unit_abbr in UNITS_ABBR.keys():
        return UNITS_ABBR[unit_abbr]
    else:
        return FILLER 
assert get_unit('CONSTR_yoy') == 'в % к аналог. периоду предыдущего года'
assert get_title('I_yoy') == 'Инвестиции в основной капитал'

# ----------------------------------------------------------------------------

def get_var_list_components():
    df = get_dfm()
    var_names = list(df.columns)
    return [[vn, get_title(vn), get_unit(vn)] for vn in var_names]

def dump_var_list_explained():
    table = get_var_list_components()
    tab_table = tabulate.tabulate(table, ["Код", "Описание", "Ед.изм."], 
                                  tablefmt="pipe")   
    docstring_to_file(tab_table, "varnames.md", "output")

if __name__ == "__main__":
    print(default_dicts)
    dump_var_list_explained()

# NOTE: not using additional dictionaries yet
# from label_csv import _get_segment_specs_no_header_doc
# segment_specs = _get_segment_specs_no_header_doc(cfg)
# print(segment_specs)