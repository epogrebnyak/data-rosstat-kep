# -*- coding: utf-8 -*-
import itertools

# TODO: нужен список переменных с текстовыми названиями, сформированный по фактическому импорту данных
#2- нужны функции get_unit(name), get_title()

from query import get_dfm
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
    # We have a somewhat inconvenient system of naming variables
    # where the uppercase initial part is an abbreviation of the variable title
    # and the lowercase final part is an abbreviation of the variable units.
    # All words in the abbreviation are separated by underscores.
    # Therefore, in order to obtain the title, one can split the whole
    # name into words and then take the longest prefix that contains
    # only uppercase words.
    words = name.split('_')
    title_abbr = '_'.join(itertools.takewhile(lambda word: word.isupper(), words))

    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr == two_labels_list[0]:
            return title
    raise ValueError("The provided headline_dict does not contain an entry for name %s" % name)

     
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
    # See the comment in get_title
    words = name.split('_')
    unit_abbr = '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))

    support_dict = ddict[1]
    for unit, sec_label in support_dict.items():
        if unit_abbr == sec_label:
            return unit
    raise ValueError("The provided support_dict does not contain an entry for name %s" % name)

assert get_title('CONSTR_yoy') == 'Объем работ по виду деятельности "Строительство"'
assert get_unit('CONSTR_yoy') == 'в % к аналогичному периоду предыдущего года' 



# note: not using additional dictionaries yet
#from label_csv import _get_segment_specs_no_header_doc
#segment_specs = _get_segment_specs_no_header_doc(cfg)
#print(segment_specs)

