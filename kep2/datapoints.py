# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apply *parsing instruction* to *csv_dicts* to get a stream of datapoints. 

Entry:
   gen = Datapoints(csv_dicts, parsing_instruction).emit("a")
    
"""

import pandas as pd
import re

from label import EMPTY_LABEL, make_label, concat_label


# ------------------------------------------------------------------------------
#
# Year checks and cell value filter
#
# ------------------------------------------------------------------------------

def get_year(s: str) -> int:
    """Extract year from string *s*.
    >>> get_year('2015')  # most cases
    2015
    >>> get_year('20161)') # some cells
    2016"""
    # first 4 symbols
    # FIXME: Maybe generate warning if there are more than 4 digits
    # EP: that was a **very** good idea!!!
    # TODO:   must catch '27000,1-45000,0'
    if len(s) >= 4 and "-" not in s:
        return int(s[:4])
    else:
        raise ValueError(s)


# FIXME: for more robustness should also check if year is in plausible range
#    EP: again a **very** good idea!!!

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


# -----------------------------------------------------------------------------------------------
#       
# Filter value in cell 
#
# -----------------------------------------------------------------------------------------------

# Allows to catch a value with with comment) or even double comment
_COMMENT_CATCHER = re.compile("\D*([\d.]*)\s*(?=\d\))")


def kill_comment(text):
    return _COMMENT_CATCHER.match(text).groups()[0]


def process_text_with_bracket(text):
    # if there is mess like '6512.3 6762.31)' in  cell, return first value
    if " " in text:
        return filter_value(text.split(" ")[0])
        # otherwise just through away comment
    else:
        return kill_comment(text)


def filter_value(text):
    """Converts *text* to float number assuming it may contain 'comment)'  
       or other unexpected contents."""

    text = text.replace(",", ".")
    if ')' in text:
        text = process_text_with_bracket(text)
    if text == "" or text == "…":
        return None
    else:
        try:
            return float(text)
        # FIXME LOW: bad error handling
        except ValueError:
            return "### This value encountered error on import - refer to stream.filter_value() for code ###"


# ------------------------------------------------------------------------------
#
# Assigning labels by row
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
        if p in line:  # Return eary
            return p
    return None


def label_rows(rows: iter, headers: dict, units: dict) -> iter:
    """Returns iterable of dictionaries, where 'label' key is filled with value.    
   
    rows: iterable of dictionaries with 'head', 'label' and 'data' keys
    headers: dict
    units: dict
    """

    current_label = EMPTY_LABEL

    for row in rows:
        if is_year(row['head']):
            row['label'] = current_label
        else:
            current_header = detect(row['head'], headers.keys())
            if current_header:
                # use label specified in 'headers'
                var = headers[current_header][0]
                if len(headers[current_header]) > 1:
                    unit = headers[current_header][1]
                else:
                    unit = ""
                current_label = make_label(var, unit)
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


def split_row_by_months(row):
    """Year M*12"""
    # TODO add doctest
    return None, None, row[0:12]


def split_row_by_months_and_annual(row):
    """ A M*12"""
    # TODO add doctest
    return row[0], None, row[1:12 + 1]


def split_row_by_accum_qtrs(row):
    """Annual AccumQ1 AccumH1 Accum9mo"""
    # TODO add doctest
    #  Year	I квартал Q 1	I полугодие 1st half-year	Январь-сентябрь January-September   
    return row[0], row[1:1 + 3] + [row[0]], None


def emit_nones(row):
    print("WARNING: unexpected number of columns - {}".format(len(row)))
    print(row)
    return None, None, None


ROW_LENGTH_TO_FUNC = {1 + 4 + 12: split_row_by_periods,
                      1 + 4: split_row_by_year_and_qtr,
                      1 + 12: split_row_by_months_and_annual,
                      12: split_row_by_months,
                      4: split_row_by_accum_qtrs}


# --------------------------------
# TODO MEDIUM Add custom splitter functions
#
## fiscal row sample
# '''
#	Год Year	Янв. Jan.	Янв-фев. Jan-Feb	I квартал Q1	Янв-апр. Jan-Apr	Янв-май Jan-May	I полугод. 1st half year	Янв-июль Jan-Jul	Янв-авг. Jan-Aug	Янв-cент. Jan-Sent	Янв-окт. Jan-Oct	Янв-нояб. Jan-Nov
# Консолидированные бюджеты субъектов Российской Федерации, млрд.рублей / Consolidated budgets of constituent entities of the Russian Federation, bln rubles
# 1999	653,8	22,7	49,2	91,5	138,7	185,0	240,0	288,5	345,5	400,6	454,0	528,0
#   0	    1	   2       3 	   4	    5	    6	    7	    8	    9	   10	   11	   12
# '''

# must down index by 1!
# def split_row_fiscal(row):
#    return int(row[0]), row[1], [row[x] for x in [3,6,9,1]], row[2:2+11] + [row[1]]
#
#
# SPECIAL_FUNC_NAMES_TO_FUNC = {'fiscal': split_row_fiscal}
#
# --------------------------------

# --------------------------------
# FIX ME move splitters to separate module
# --------------------------------

def get_splitter_func(row: dict, custom_splitter_func_name=None) -> object:
    """Return custom splitter function from *parsing_instructions* if defined.
       Otherwise, choose splitter function based on number of elements in *row*
       using ROW_LENGTH_TO_FUNC dictionary.
       # FIXME LOW: rewrite this docstring
       """

    if custom_splitter_func_name:
        # FIXME YIGH: will not work, need dictionary
        #   elif reader in SPECIAL_FUNC_NAMES_TO_FUNC.keys():
        #        return SPECIAL_FUNC_NAMES_TO_FUNC[reader]        
        # return custom_splitter_func
        pass
    else:
        cnt = len(row['data'])
        if cnt in ROW_LENGTH_TO_FUNC.keys():
            return ROW_LENGTH_TO_FUNC[cnt]
        else:
            print("WARNING: unexpected row with length {}: ".format(cnt) + row['head'])
            # import pdb; pdb.set_trace()
            raise ValueError(row)


# ------------------------------------------------------------------------------
#
# Emitting datapoints from data row
#
# ------------------------------------------------------------------------------

def get_datapoints(row: dict, custom_splitter_func_name: str) -> iter:
    splitter_func = get_splitter_func(row, custom_splitter_func_name)
    return yield_datapoints(row_tuple=splitter_func(row['data']),
                            year=get_year(row['head']),
                            varname=concat_label(row['label']))


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


class Datapoints():
    """Emit a stream datapoints from *rows* according to *parsing_instructions*."""

    def __init__(self, row_dicts: iter, spec: object):
        """
        row_dicts: iterable of dictionaries with csv file content by row, 
              each dictionary has 'head', 'data', 'label'
              iterable generated by CSV_Reader(path).yield_dicts()              
        spec: object containing header dict, units dict and splitter func name
              object generated by ParsingDefinition(path)
        """

        # unpack parsing defintion
        headers = spec.headers
        units = spec.units
        custom_splitter_func_name = spec.splitter_func_name

        # assign labels
        self.row_dicts = label_rows(row_dicts, headers, units)

        def consume_datapoints():
            """Walks by rows and emits row elements as dictionaries 
               in yield_datapoints() format.
               
               Note: this function can be written as generator comprehension 
                     expression, but loop is more explicit."""

            # limit stream to datarows only
            for rowd in filter(is_datarow, self.row_dicts):
                for p in get_datapoints(rowd, custom_splitter_func_name):
                    yield p

        # save all datapoints as list as we will need to reuse it with .emit()
        self.datapoints = list(consume_datapoints())

    def emit(self, freq):
        """Returns generator of dictionaries of datapoints as formatted 
           by yield_datapoints().
           
           param freq: 'a', 'q' or 'm' 
        """
        if freq in 'aqm':
            for p in self.datapoints:
                if p['freq'] == freq:
                    # Note: (1) 'freq' key will be redundant for later use in
                    #           dataframe, drop it
                    #       (2) without copy() pop() changes self.datapoints
                    z = p.copy()
                    z.pop('freq')
                    yield z
        else:
            raise ValueError(freq)


if __name__ == "__main__":

    # ENTRY EXAMPLE
    from config import get_default_spec_path, get_default_csv_path
    from parsing_definitions import ParsingDefinition
    from csv_data import CSV_Reader

    # data 
    csv_path = get_default_csv_path()
    csv_dicts = list(CSV_Reader(csv_path).yield_dicts())

    # parsing instruction 
    specfile_path = get_default_spec_path()
    pi = ParsingDefinition(specfile_path)
    d = Datapoints(csv_dicts, pi)

    # BOILERPLATE
    # truncate csv_dicts, too many errors in whole file  
    output = list(d.emit('a'))[:140]

    for z in output:
        if z['year'] == 2016:
            print(z.__repr__() + ",")

    testpoints = [
        {'varname': 'GDP_bln_rub', 'year': 2016, 'value': 85881.0},
        {'varname': 'GDP_rog', 'year': 2016, 'value': 99.8},
        {'varname': 'IND_PROD_yoy', 'year': 2016, 'value': 101.3},
        # ERROR CRITICAL: - same label, header or unti did not switch
        {'varname': 'IND_PROD_yoy', 'year': 2016, 'value': 104.8},
        {'varname': 'PROD_AGRO_MEAT_th_t', 'year': 2016, 'value': 13939.0},
        {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 103.4},
        # ERROR CRITICAL: - same label, header or unti did not switch
        {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 30724.0},
        # ERROR CRITICAL: - same label, header or unti did not switch
        {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 99.8},
    ]

    for t in testpoints:
        assert t in output



        #    OLD TESTS
        #    TODO: restore tests

        #    from stunt import get_rows1, get_parsing_instructions1
        #    SRC = {'raw_data': get_rows1(), 'parsing_instructions': get_parsing_instructions1()}
        #
        #
        #    d = Datapoints(**SRC)
        #    for f in 'aqm':
        #       assert list(d.emit(f)) == list(stream_by_freq(f, **SRC))
        #
        #    import doctest
        #
        #    # ERROR: doctest not running on IPython, throws many errors
        #
        #    #doctest.testmod()
        #
        #    from io import StringIO
        #
        #    # EP: added column order to match DFA, DFQ, DFM constants
        #    dfa = pd.DataFrame(stream_by_freq('a', **SRC))[['value', 'varname', 'year']]
        #    dfq = pd.DataFrame(stream_by_freq('q', **SRC))[['qtr', 'value', 'varname', 'year']]
        #    dfm = pd.DataFrame(stream_by_freq('m', **SRC))[['month', 'value', 'varname', 'year']]
        #
        #    DFA = pd.read_csv(StringIO(
        #        ',value,varname,year\n0,71017.0,GDP_bln_rub,2013\n1,79200.0,GDP_bln_rub,2014\n2,83233.0,GDP_bln_rub,2015\n3,85881.0,GDP_bln_rub,2016\n4,101.3,GDP_rog,2013\n5,100.7,GDP_rog,2014\n6,97.2,GDP_rog,2015\n7,99.8,GDP_rog,2016\n8,99.2,IND_PROD_yoy,2015\n9,101.3,IND_PROD_yoy,2016\n')
        #        , index_col=0)
        #    DFQ = pd.read_csv(StringIO(
        #        ',qtr,value,varname,year\n0,1,15892.0,GDP_bln_rub,2013\n1,2,17015.0,GDP_bln_rub,2013\n2,3,18543.0,GDP_bln_rub,2013\n3,4,19567.0,GDP_bln_rub,2013\n4,1,17139.0,GDP_bln_rub,2014\n5,2,18884.0,GDP_bln_rub,2014\n6,3,20407.0,GDP_bln_rub,2014\n7,4,21515.0,GDP_bln_rub,2014\n8,1,18210.0,GDP_bln_rub,2015\n9,2,19284.0,GDP_bln_rub,2015\n10,3,21294.0,GDP_bln_rub,2015\n11,4,22016.0,GDP_bln_rub,2015\n12,1,18561.0,GDP_bln_rub,2016\n13,2,19979.0,GDP_bln_rub,2016\n14,3,22190.0,GDP_bln_rub,2016\n15,1,100.6,GDP_rog,2013\n16,2,101.1,GDP_rog,2013\n17,3,101.2,GDP_rog,2013\n18,4,102.1,GDP_rog,2013\n19,1,100.6,GDP_rog,2014\n20,2,101.1,GDP_rog,2014\n21,3,100.9,GDP_rog,2014\n22,4,100.2,GDP_rog,2014\n23,1,97.2,GDP_rog,2015\n24,2,95.5,GDP_rog,2015\n25,3,96.3,GDP_rog,2015\n26,4,96.2,GDP_rog,2015\n27,1,98.8,GDP_rog,2016\n28,2,99.4,GDP_rog,2016\n29,3,99.6,GDP_rog,2016\n30,1,99.9,IND_PROD_yoy,2015\n31,2,98.3,IND_PROD_yoy,2015\n32,3,99.5,IND_PROD_yoy,2015\n33,4,99.1,IND_PROD_yoy,2015\n34,1,101.1,IND_PROD_yoy,2016\n35,2,101.5,IND_PROD_yoy,2016\n36,3,101.0,IND_PROD_yoy,2016\n37,4,101.7,IND_PROD_yoy,2016\n38,1,82.8,IND_PROD_rog,2015\n39,2,102.6,IND_PROD_rog,2015\n40,3,103.9,IND_PROD_rog,2015\n41,4,112.3,IND_PROD_rog,2015\n42,1,84.4,IND_PROD_rog,2016\n43,2,103.1,IND_PROD_rog,2016\n44,3,103.3,IND_PROD_rog,2016\n45,4,113.1,IND_PROD_rog,2016\n')
        #        , index_col=0)
        #    DFM = pd.read_csv(StringIO(
        #        ',month,value,varname,year\n0,1,100.0,IND_PROD_yoy,2015\n1,2,98.2,IND_PROD_yoy,2015\n2,3,101.2,IND_PROD_yoy,2015\n3,4,98.2,IND_PROD_yoy,2015\n4,5,97.6,IND_PROD_yoy,2015\n5,6,99.1,IND_PROD_yoy,2015\n6,7,98.5,IND_PROD_yoy,2015\n7,8,100.2,IND_PROD_yoy,2015\n8,9,99.7,IND_PROD_yoy,2015\n9,10,98.4,IND_PROD_yoy,2015\n10,11,101.0,IND_PROD_yoy,2015\n11,12,98.1,IND_PROD_yoy,2015\n12,1,99.2,IND_PROD_yoy,2016\n13,2,103.8,IND_PROD_yoy,2016\n14,3,100.3,IND_PROD_yoy,2016\n15,4,101.0,IND_PROD_yoy,2016\n16,5,101.5,IND_PROD_yoy,2016\n17,6,102.0,IND_PROD_yoy,2016\n18,7,101.4,IND_PROD_yoy,2016\n19,8,101.5,IND_PROD_yoy,2016\n20,9,100.1,IND_PROD_yoy,2016\n21,10,101.6,IND_PROD_yoy,2016\n22,11,103.4,IND_PROD_yoy,2016\n23,12,100.2,IND_PROD_yoy,2016\n24,1,102.3,IND_PROD_yoy,2017\n25,2,97.3,IND_PROD_yoy,2017\n26,1,73.9,IND_PROD_rog,2015\n27,2,99.8,IND_PROD_rog,2015\n28,3,112.5,IND_PROD_rog,2015\n29,4,95.6,IND_PROD_rog,2015\n30,5,97.6,IND_PROD_rog,2015\n31,6,103.2,IND_PROD_rog,2015\n32,7,100.5,IND_PROD_rog,2015\n33,8,101.4,IND_PROD_rog,2015\n34,9,103.1,IND_PROD_rog,2015\n35,10,105.0,IND_PROD_rog,2015\n36,11,101.9,IND_PROD_rog,2015\n37,12,109.1,IND_PROD_rog,2015\n38,1,74.7,IND_PROD_rog,2016\n39,2,104.4,IND_PROD_rog,2016\n40,3,108.8,IND_PROD_rog,2016\n41,4,96.3,IND_PROD_rog,2016\n42,5,98.1,IND_PROD_rog,2016\n43,6,103.8,IND_PROD_rog,2016\n44,7,99.9,IND_PROD_rog,2016\n45,8,101.5,IND_PROD_rog,2016\n46,9,101.7,IND_PROD_rog,2016\n47,10,106.6,IND_PROD_rog,2016\n48,11,103.6,IND_PROD_rog,2016\n49,12,105.8,IND_PROD_rog,2016\n50,1,76.2,IND_PROD_rog,2017\n51,2,99.4,IND_PROD_rog,2017\n52,1,100.0,IND_PROD_ytd,2015\n53,2,99.1,IND_PROD_ytd,2015\n54,3,99.9,IND_PROD_ytd,2015\n55,4,99.4,IND_PROD_ytd,2015\n56,5,99.1,IND_PROD_ytd,2015\n57,6,99.1,IND_PROD_ytd,2015\n58,7,99.0,IND_PROD_ytd,2015\n59,8,99.1,IND_PROD_ytd,2015\n60,9,99.2,IND_PROD_ytd,2015\n61,10,99.1,IND_PROD_ytd,2015\n62,11,99.3,IND_PROD_ytd,2015\n63,12,99.2,IND_PROD_ytd,2015\n64,1,99.2,IND_PROD_ytd,2016\n65,2,101.5,IND_PROD_ytd,2016\n66,3,101.1,IND_PROD_ytd,2016\n67,4,101.1,IND_PROD_ytd,2016\n68,5,101.1,IND_PROD_ytd,2016\n69,6,101.3,IND_PROD_ytd,2016\n70,7,101.3,IND_PROD_ytd,2016\n71,8,101.3,IND_PROD_ytd,2016\n72,9,101.2,IND_PROD_ytd,2016\n73,10,101.2,IND_PROD_ytd,2016\n74,11,101.4,IND_PROD_ytd,2016\n75,12,101.3,IND_PROD_ytd,2016\n76,1,102.3,IND_PROD_ytd,2017\n77,2,99.7,IND_PROD_ytd,2017\n')
        #        , index_col=0)
        #
        #    assert DFA.equals(dfa)
        #    assert DFQ.equals(dfq)
        #    assert DFM.equals(dfm)
