# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# needs python 3.6 to run (StringIO, variable type guidance)


"""
Apply parsing instructions to csv content proxy to get streams of annual, 
quarterly and monthly datapoints. 

Points of entry retrun stream of dictionaries:
    
    gen1 = stream_by_freq(freq)
    
    d = Datapoints(raw_data=get_rows(), parsing_instructions=get_parsing_instructions())
    gen2 = d.emit(freq)
    
    freq is 'a', 'q' or 'm'  
    
"""

import pandas as pd
import numpy as np
from stunt import get_rows1, get_parsing_instructions1



# -----------------------------------------------------------------------------
#
# Variable label handling
#
# -----------------------------------------------------------------------------

EMPTY_LABEL = {'var': '', 'unit': ''}

def concat_label(label: dict)-> str:
    """Return string repesenting *label* dictionary.
    
    >>> concat_label({'var': 'GDP', 'unit': 'yoy'})
    'GDP_yoy'"""
    
    return label['var'] + "_" + label['unit']

# TODO (EP) MEDIUM: bring back splitting label to head and unit

# ------------------------------------------------------------------------------
#
# Converting non-empty rows to 'head', 'data', 'label' dictionaries
#
# ------------------------------------------------------------------------------

def row_as_dict(row: list) -> dict:
    """Represents csv *row* content as a dictionary with following keys:
    
       'head' - string, first element in list *row* (may be year or table header)
       'data' - list, next elements in list *row*, ususally data elements like ['15892', '17015', '18543', '19567']
       'label' - placeholder for row label. Label is a dictionary like dict(var="GDP", unit="bln_rub")
    Examples:
    
    >>> row_as_dict(['1. Сводные показатели', '', ''])['head']
    '1. Сводные показатели'
    >>> row_as_dict(['2013', '15892', '17015', '18543', '19567'])['head']
    '2013'
    >>> row_as_dict(['2013', '15892', '17015', '18543', '19567'])['data']
    ['15892', '17015', '18543', '19567']
    >>> row_as_dict(['2013', '15892', '17015', '18543', '19567'])['label'] == {'unit': '', 'var': ''}
    True"""
    return dict(head=row[0],
                data=row[1:],
                label=EMPTY_LABEL)


def yield_rows_as_dicts(rows: list) -> iter:
    """Yield non-empty csv rows as dictionaries. """
    for r in rows:
        # check if list is not empty and first element is not empty
        if r and r[0]:
            yield row_as_dict(r)


def get_year(s: str) -> int:
    """Extract year from string *s*.
    >>> get_year('2015')  # most cases
    2015
    >>> get_year('20161)') # some cells
    2016"""
    # first 4 symbols
    # NOT TODO: Maybe generate warning if there are more than 4 digits
    return int(s[:4])    


# WONTFIX: for more robustness should also check if year is in plausible range

def is_year(s: str) -> bool:
    """Check if *s* contains year number.
    >>> is_year('1. Сводные показатели')
    False
    >>> is_year('20151)')
    True"""
    try:
        get_year(s)
        return True
    except:
        return False

# ------------------------------------------------------------------------------
#
# Assigning labels (row['label']) to rows
#
# ------------------------------------------------------------------------------

def detect(line: str, patterns: list) -> (bool, str):
    """Check if any string from *patterns* list is present in *text* string.
    
       param line: string to check against *patterns* strings
       param patterns: list of strings
       
       Returns tuple with boolean flag and first pattern found
    
    Example:
       >>> detect("Canada", ["ana", "bot"])
       'ana'
       >>> detect("Canada", ["bot", "ana"])
       'ana'
       >>> detect("Canada", ["dog", "bot"]) is None
       True
       """

    for p in patterns:
        if p in line: # Return eary
            return p
    return None 


def label_rows(rows: iter, parsing_instructions: list) -> iter:
    """Returns iterable of dictionaries, where 'label' key is filled.
    
    Adds label to every row in *rows* iterable based on row content and 
    *parsing_instructions*.
    
    rows: iterable of dictionaries with 'head', 'label' and 'data' keys
    parsing_instructions: list of header dict, units dict and (optional) 
                          splitter function name"""
    
    headers, units, _ = parsing_instructions
    current_label = EMPTY_LABEL

    for row in rows:
        if is_year(row['head']):
            row['label'] = current_label
        else:
            current_header = detect(row['head'], headers.keys())
            if current_header:
                # use label specified in 'headers'
                current_label = headers[current_header]
            unit = detect(row['head'], units.keys())
            if unit:
                # only change unit in current label
                current_label['unit'] = units[unit]
            row['label'] = current_label
        yield row


# ------------------------------------------------------------------------------
#
# Splitter functions extract annual, quarterly and monthly values from data row
#
# ------------------------------------------------------------------------------

def split_row_by_periods(row):    
    """Values format:
    A Q Q Q Q M*12
    
    >>> split_row_by_periods(['2015','a','b','c','d',1,2,3,4,5,6,7,8,9,10,11,12])
    ('2015', ['a', 'b', 'c', 'd'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])"""
        
    return row[0], row[1:1 + 4], row[1 + 4:1 + 4 + 12]


def split_row_by_year_and_qtr(row):
    """Values format:
    A Q Q Q Q
    
    >>> split_row_by_year_and_qtr(['85881', '18561', '19979', '22190', ''])
    ('85881', ['18561', '19979', '22190', ''], None)"""
    
    return row[0], row[1:1 + 4], None


# TODO HIGH (EP)
# add more splitter funcs from https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/stream.py
# warning: must adjust key by 1

ROW_LENGTH_TO_FUNC = {1 + 4 + 12: split_row_by_periods,
                      1 + 4: split_row_by_year_and_qtr}


# ------------------------------------------------------------------------------
#
# Emitting datapoints from data row
#
# ------------------------------------------------------------------------------

def get_splitter_func(row: dict, parsing_instructions: list) -> object:
    """Return custom splitter function from *parsing_instructions* if defined.
       Otherwise, choose splitter function based on number of elements in *row*
       using ROW_LENGTH_TO_FUNC dictionary.
# FIXME LOW: rewrite this docstring
       """
    _, _, custom_splitter_func = parsing_instructions
    if custom_splitter_func:
        # FIXME CRITICAL: will not work, need dictionary
        return custom_splitter_func
    else:
        cnt = len(row['data'])
        return ROW_LENGTH_TO_FUNC[cnt]


def get_datapoints(row: dict, parsing_instructions: list) -> iter:
    splitter_func = get_splitter_func(row, parsing_instructions)
    return yield_datapoints(row_tuple=splitter_func(row['data']),
                            year=get_year(row['head']),
                            varname=concat_label(row['label']))


def filter_value(x):
    # TODO(EP) HIGH: reuse code can be more complex as in https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/stream.py#L74-L108
    return float(x.replace(",", "."))


def yield_datapoints(row_tuple: list, varname: str, year: int) -> iter:
    """Yield dictionaries containing individual datapoints based on *row_tuple* content.
    :param row_tuple: tuple with annual value and lists of quarterly and monthly values
    :param varname: string like 'GDP_yoy'
    :param year: int
    :return: dictionaries ready to feed into pd.Dataframe
    """
    # a - annual value, just one number
    # qs - quarterly values, list of 4 elements
    # ms - monthly values, list of 12 elements
    a, qs, ms = row_tuple

    # annual value, yield if present
    if a:
        yield {'freq': 'a',
               'varname': varname,
               'year': year,
               'value': filter_value(a)}
    # quarterly values, yield if present
    if qs:
        for i, val in enumerate(qs):
            if val:
                yield {'freq': 'q',
                       'varname': varname,
                       'year': year,
                       'qtr': i + 1,
                       'value': filter_value(val)}
    # quarterly values, yield if present
    if ms:
        for j, val in enumerate(ms):
            if val:
                yield {'freq': 'm',
                       'varname': varname,
                       'year': year,
                       'month': j + 1,
                       'value': filter_value(val)}


# ------------------------------------------------------------------------------
#
# Generating stream of datapoints from csv and parsing instructions
#
# ------------------------------------------------------------------------------


def is_datarow(row):
    return is_year(row['head'])

# FIXME CRITICAL - injection of temporary data 
def stream_by_freq(freq: str,
                   raw_data: list = get_rows1(),
                   parsing_instructions: list = get_parsing_instructions1()):
    """Return a stream of dictionaries containing datapoints from *raw_data* 
       csv file content parsed using *parsing_instructions*.
      
    param freq: 'a', 'q' or 'm' literal
    param raw_data: list of lists, csv file content, each row is a list of csv
                    row elements
    param parsing_instructions: list of header dict, units dict and (optional) 
                                splitter func name
    
    Returns generator of dictionaries as formatted by yield_datapoints()
    """
    # wrap csv content as a stream of dictionaries
    gen = yield_rows_as_dicts(raw_data)
    # add variable labels to each row dictionary using parsing_instructions
    rows = label_rows(gen, parsing_instructions)
    # stream all rows
    for row in filter(is_datarow, rows):
        # stream individual datapoints from each row
        for p in get_datapoints(row, parsing_instructions):
            # trim by frequency: 'a', 'q' or 'm'
            if p['freq'] == freq:
                # 'freq' key will be redundant for dataframe, drop it
                p.pop('freq')
                yield p

# REVIEW: ------------------------------------------------------------------

class Datapoints():

    def __init__(self, raw_data: list, parsing_instructions: list):
       
        # wrap csv content as a stream of dictionaries
        gen = yield_rows_as_dicts(raw_data)
        
        # assign labels and filter datarows only
        rows = filter(is_datarow, label_rows(gen, parsing_instructions))
        
        # walk by row and row elements
        # FIXME - maybe some expression without loop? using itertools?
        # TODO EP: add comments from upwork
        def consume_datapoints():
            for row in rows:
                for p in get_datapoints(row, parsing_instructions):
                    yield p  
                    
        # save all datapoints as list           
        self.datapoints = list(consume_datapoints())

    def emit(self, freq):
         if freq in 'aqm':
             for p in self.datapoints:
                 if p['freq'] == freq:
                     # 'freq' key will be redundant for dataframe, drop it
                     # Note: EP - without copy() changes self.datapoints 
                     z = p.copy()
                     z.pop('freq')
                     yield z
         else:
             raise ValueError(freq)

# END REVIEW ------------------------------------------------------------------


def print_dataframe_difference(df1, df2):
    """Prints difference in two dataframes, row by row."""
    difference_locations = np.where(df1 != df2)
    changed_from = df1.values[difference_locations]
    changed_to = df2.values[difference_locations]
    changed = pd.DataFrame({'from': changed_from, 'to': changed_to})
    print(changed)


# ------------------------------------------------------------------------------
#
# Some testing
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":

    d = Datapoints(get_rows1(), get_parsing_instructions1())
    for f in 'aqm':
       assert list(d.emit(f)) == list(stream_by_freq(f))
    
    import doctest

    # ERROR: doctest not running on IPython, throws many errors

    doctest.testmod()

    from io import StringIO

    # EP: added column order to match DFA, DFQ, DFM constants 
    dfa = pd.DataFrame(stream_by_freq('a'))[['value', 'varname', 'year']]
    dfq = pd.DataFrame(stream_by_freq('q'))[['qtr', 'value', 'varname', 'year']]
    dfm = pd.DataFrame(stream_by_freq('m'))[['month', 'value', 'varname', 'year']]

    DFA = pd.read_csv(StringIO(
        ',value,varname,year\n0,71017.0,GDP_bln_rub,2013\n1,79200.0,GDP_bln_rub,2014\n2,83233.0,GDP_bln_rub,2015\n3,85881.0,GDP_bln_rub,2016\n4,101.3,GDP_rog,2013\n5,100.7,GDP_rog,2014\n6,97.2,GDP_rog,2015\n7,99.8,GDP_rog,2016\n8,99.2,IND_PROD_yoy,2015\n9,101.3,IND_PROD_yoy,2016\n')
        , index_col=0)
    DFQ = pd.read_csv(StringIO(
        ',qtr,value,varname,year\n0,1,15892.0,GDP_bln_rub,2013\n1,2,17015.0,GDP_bln_rub,2013\n2,3,18543.0,GDP_bln_rub,2013\n3,4,19567.0,GDP_bln_rub,2013\n4,1,17139.0,GDP_bln_rub,2014\n5,2,18884.0,GDP_bln_rub,2014\n6,3,20407.0,GDP_bln_rub,2014\n7,4,21515.0,GDP_bln_rub,2014\n8,1,18210.0,GDP_bln_rub,2015\n9,2,19284.0,GDP_bln_rub,2015\n10,3,21294.0,GDP_bln_rub,2015\n11,4,22016.0,GDP_bln_rub,2015\n12,1,18561.0,GDP_bln_rub,2016\n13,2,19979.0,GDP_bln_rub,2016\n14,3,22190.0,GDP_bln_rub,2016\n15,1,100.6,GDP_rog,2013\n16,2,101.1,GDP_rog,2013\n17,3,101.2,GDP_rog,2013\n18,4,102.1,GDP_rog,2013\n19,1,100.6,GDP_rog,2014\n20,2,101.1,GDP_rog,2014\n21,3,100.9,GDP_rog,2014\n22,4,100.2,GDP_rog,2014\n23,1,97.2,GDP_rog,2015\n24,2,95.5,GDP_rog,2015\n25,3,96.3,GDP_rog,2015\n26,4,96.2,GDP_rog,2015\n27,1,98.8,GDP_rog,2016\n28,2,99.4,GDP_rog,2016\n29,3,99.6,GDP_rog,2016\n30,1,99.9,IND_PROD_yoy,2015\n31,2,98.3,IND_PROD_yoy,2015\n32,3,99.5,IND_PROD_yoy,2015\n33,4,99.1,IND_PROD_yoy,2015\n34,1,101.1,IND_PROD_yoy,2016\n35,2,101.5,IND_PROD_yoy,2016\n36,3,101.0,IND_PROD_yoy,2016\n37,4,101.7,IND_PROD_yoy,2016\n38,1,82.8,IND_PROD_rog,2015\n39,2,102.6,IND_PROD_rog,2015\n40,3,103.9,IND_PROD_rog,2015\n41,4,112.3,IND_PROD_rog,2015\n42,1,84.4,IND_PROD_rog,2016\n43,2,103.1,IND_PROD_rog,2016\n44,3,103.3,IND_PROD_rog,2016\n45,4,113.1,IND_PROD_rog,2016\n')
        , index_col=0)
    DFM = pd.read_csv(StringIO(
        ',month,value,varname,year\n0,1,100.0,IND_PROD_yoy,2015\n1,2,98.2,IND_PROD_yoy,2015\n2,3,101.2,IND_PROD_yoy,2015\n3,4,98.2,IND_PROD_yoy,2015\n4,5,97.6,IND_PROD_yoy,2015\n5,6,99.1,IND_PROD_yoy,2015\n6,7,98.5,IND_PROD_yoy,2015\n7,8,100.2,IND_PROD_yoy,2015\n8,9,99.7,IND_PROD_yoy,2015\n9,10,98.4,IND_PROD_yoy,2015\n10,11,101.0,IND_PROD_yoy,2015\n11,12,98.1,IND_PROD_yoy,2015\n12,1,99.2,IND_PROD_yoy,2016\n13,2,103.8,IND_PROD_yoy,2016\n14,3,100.3,IND_PROD_yoy,2016\n15,4,101.0,IND_PROD_yoy,2016\n16,5,101.5,IND_PROD_yoy,2016\n17,6,102.0,IND_PROD_yoy,2016\n18,7,101.4,IND_PROD_yoy,2016\n19,8,101.5,IND_PROD_yoy,2016\n20,9,100.1,IND_PROD_yoy,2016\n21,10,101.6,IND_PROD_yoy,2016\n22,11,103.4,IND_PROD_yoy,2016\n23,12,100.2,IND_PROD_yoy,2016\n24,1,102.3,IND_PROD_yoy,2017\n25,2,97.3,IND_PROD_yoy,2017\n26,1,73.9,IND_PROD_rog,2015\n27,2,99.8,IND_PROD_rog,2015\n28,3,112.5,IND_PROD_rog,2015\n29,4,95.6,IND_PROD_rog,2015\n30,5,97.6,IND_PROD_rog,2015\n31,6,103.2,IND_PROD_rog,2015\n32,7,100.5,IND_PROD_rog,2015\n33,8,101.4,IND_PROD_rog,2015\n34,9,103.1,IND_PROD_rog,2015\n35,10,105.0,IND_PROD_rog,2015\n36,11,101.9,IND_PROD_rog,2015\n37,12,109.1,IND_PROD_rog,2015\n38,1,74.7,IND_PROD_rog,2016\n39,2,104.4,IND_PROD_rog,2016\n40,3,108.8,IND_PROD_rog,2016\n41,4,96.3,IND_PROD_rog,2016\n42,5,98.1,IND_PROD_rog,2016\n43,6,103.8,IND_PROD_rog,2016\n44,7,99.9,IND_PROD_rog,2016\n45,8,101.5,IND_PROD_rog,2016\n46,9,101.7,IND_PROD_rog,2016\n47,10,106.6,IND_PROD_rog,2016\n48,11,103.6,IND_PROD_rog,2016\n49,12,105.8,IND_PROD_rog,2016\n50,1,76.2,IND_PROD_rog,2017\n51,2,99.4,IND_PROD_rog,2017\n52,1,100.0,IND_PROD_ytd,2015\n53,2,99.1,IND_PROD_ytd,2015\n54,3,99.9,IND_PROD_ytd,2015\n55,4,99.4,IND_PROD_ytd,2015\n56,5,99.1,IND_PROD_ytd,2015\n57,6,99.1,IND_PROD_ytd,2015\n58,7,99.0,IND_PROD_ytd,2015\n59,8,99.1,IND_PROD_ytd,2015\n60,9,99.2,IND_PROD_ytd,2015\n61,10,99.1,IND_PROD_ytd,2015\n62,11,99.3,IND_PROD_ytd,2015\n63,12,99.2,IND_PROD_ytd,2015\n64,1,99.2,IND_PROD_ytd,2016\n65,2,101.5,IND_PROD_ytd,2016\n66,3,101.1,IND_PROD_ytd,2016\n67,4,101.1,IND_PROD_ytd,2016\n68,5,101.1,IND_PROD_ytd,2016\n69,6,101.3,IND_PROD_ytd,2016\n70,7,101.3,IND_PROD_ytd,2016\n71,8,101.3,IND_PROD_ytd,2016\n72,9,101.2,IND_PROD_ytd,2016\n73,10,101.2,IND_PROD_ytd,2016\n74,11,101.4,IND_PROD_ytd,2016\n75,12,101.3,IND_PROD_ytd,2016\n76,1,102.3,IND_PROD_ytd,2017\n77,2,99.7,IND_PROD_ytd,2017\n')
        , index_col=0)

    assert DFA.equals(dfa)
    assert DFQ.equals(dfq)
    assert DFM.equals(dfm)
