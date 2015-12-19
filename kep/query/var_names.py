# -*- coding: utf-8 -*-
""" Generate variable list. 

Entry point: 
    dump_var_list_explained() writes output/varnames.md
"""
import itertools
import pandas as pd

from kep.file_io.common import write_file, get_filenames
from kep.file_io.specification import load_spec
from kep.database.db import get_unique_labels
from kep.inspection.var_check import get_complete_dicts
DATA_FOLDER = "data/2015/ind10"
default_dicts = get_complete_dicts(DATA_FOLDER)

from kep.file_io.common import get_var_abbr, get_unit_abbr
assert get_var_abbr('PROD_E_TWh') == 'PROD_E' 
assert get_unit_abbr('PROD_E_TWh') == 'TWh'

FILLER = "<...>"
VARNAMES_FILE = "output/varnames.md"

# ----------------------------------------------------------------------------

# TODO: add freq. 
def get_varnames(freq = None):
    if freq is 'a':
        return get_unique_labels()
    elif freq is 'q':
        return get_unique_labels()
    elif freq is 'm':
        return get_unique_labels()
    else:
        return get_unique_labels()

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
assert get_title('I_yoy') == 'Инвестиции в основной капитал'

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

TABLE_HEADER = ["Код", "Описание", "Ед.изм."]

def get_var_list_components():
    """
    Returns a list of lists each containing variable name,
    text description and unit of measurement.
    """
    return [[var_name, get_title(var_name), get_unit(var_name)]
            for var_name in get_unique_labels()]

def get_max_widths(table):
    """
    For a table with N columns, returns list of N integers,
    where each element is the maximum width of the corresponding column.

    Supports incomplete rows with less than N elements.
    """
    max_widths = []
    column_count = 0
    for row in table:
        if len(row) > column_count:
            max_widths.extend([0 for i in range(len(row) - column_count)])
            column_count = len(max_widths)
        for i, value in enumerate(row):
            max_widths[i] = max(max_widths[i], len(value))
    return max_widths

def pure_tabulate(table, header=TABLE_HEADER):
    """
    Returns nicely formatted table as a string.
    """
    # Calculate column widths
    widths = get_max_widths(itertools.chain([header], table))
    # Template for header and rows.
    # | Text      | Another text |
    template = '| ' + ' | '.join(('{:<%s}' % x) for x in widths) + ' |'
    # Special string for the separator line below header.
    # |:----------|:-------------|
    header_separator_line = '|:' + '-|:'.join('-' * x for x in widths) + '-|'
    # Format and combine all rows into table
    rows = itertools.chain([template.format(*header), header_separator_line],
                           (template.format(*row) for row in table))
    return '\n'.join(rows)

# TODO: move it to tests
_TEST_RESULT = '''
| Код       | Описание                      | Ед.изм.                                |
|:----------|:------------------------------|:---------------------------------------|
| I_bln_rub | Инвестиции в основной капитал | млрд. руб.                             |
| I_rog     | Инвестиции в основной капитал | в % к предыдущему периоду              |
| I_yoy     | Инвестиции в основной капитал | в % к аналог. периоду предыдущего года |
'''.strip()

def test_pure_tabulate():
    table = [
        ['I_bln_rub', 'Инвестиции в основной капитал', 'млрд. руб.'],
        ['I_rog', 'Инвестиции в основной капитал', 'в % к предыдущему периоду'],
        ['I_yoy', 'Инвестиции в основной капитал', 'в % к аналог. периоду предыдущего года']
    ]
    assert pure_tabulate(table, TABLE_HEADER) == _TEST_RESULT

def get_table():
    table = get_var_list_components()
    return pure_tabulate(table)
	
def get_var_table_as_dataframe():
    """Not tested. This is for issue #36"""
    list_ = get_var_list_components()
    return pd.DataFrame(list_, columns = TABLE_HEADER)

def dump_var_list_explained():
    """Writes table of variables (label, desciption, unit) to src/output/varnames.md"""    
    tab_table = get_table()
    write_file(tab_table, VARNAMES_FILE)

if __name__ == "__main__":
    print(default_dicts)
    print()
    print(get_table())
    dump_var_list_explained() 

    inspection = dict((v[1], k.split(",")[-1]) for k,v in default_dicts[0].items())

	
# NOTE 1: not using additional dictionaries yet
# from label_csv import _get_segment_specs_no_header_doc
# segment_specs = _get_segment_specs_no_header_doc(cfg)
# print(segment_specs)

# NOTE 2: presence of variable in this table in does not guarantee 
# it is filled with data at all or at particular frequency (e.g. monthly).