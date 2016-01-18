# -*- coding: utf-8 -*-
""" Generate variable list. 

Entry point: 
    dump_var_list_explained() writes output/varnames.md
"""
import pandas as pd

from kep.file_io.common import write_file
from kep.database.db import get_unique_labels
from kep.inspection.var_check import get_complete_dicts
from kep.paths import VARNAMES_FILE, CURRENT_MONTH_DATA_FOLDER
default_dicts = None

from kep.file_io.common import get_var_abbr, get_unit_abbr
from kep.file_io.tabulate import pure_tabulate, TABLE_HEADER

FILLER = "<...>"

# ----------------------------------------------------------------------------

# TODO: add frequencies
def get_varnames(freq = None):
    if freq is 'a':
        return get_unique_labels()
    elif freq is 'q':
        return get_unique_labels()
    elif freq is 'm':
        return get_unique_labels()
    else:
        return get_unique_labels()

# TODO: generalise to 3 columns
# ERROR: add extra line in some consoles
def print_varlist_two_columns():
    # list of variables in two colums, similar to Windows 'dir /D'
    print()
    vn = get_varnames()
    N = len(vn)
    if round(N/2) != N/2:
       vn = vn + ['']
    z = iter(vn)
    i = 0
    while i < N:
       print ("%-40.40s %-40.40s" % (next(z), next(z)))
       i += 2
    print()
        
# ----------------------------------------------------------------------------

def get_title(name, ddict=None):
    if ddict is None:
        global default_dicts
        if default_dicts is None:
            default_dicts = get_complete_dicts(CURRENT_MONTH_DATA_FOLDER)
        ddict = default_dicts
    title_abbr = get_var_abbr(name)
    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr == two_labels_list[0]:
            return title
    return FILLER

# ----------------------------------------------------------------------------

UNITS_ABBR = {
# --- part from default_dicts [0]
    'rog':'в % к предыдущему периоду',
    'rub':'рублей',
    'yoy':'в % к аналог. периоду предыдущего года' ,
# --- part from default_dicts [1],
    'bln_t_km': 'млрд. т-км',
    'percent': '%',
    'bln_rub': 'млрд. руб.',
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

# ----------------------------------------------------------------------------

def get_var_list_components():
    """
    Returns a list of lists each containing variable name,
    text description and unit of measurement.
    """
    return [[var_name, get_title(var_name), get_unit(var_name)]
            for var_name in get_unique_labels()]

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
    
# NOTE 1: presence of variable in this table in does not guarantee 
# it is filled with data at all or at particular frequency (e.g. monthly).