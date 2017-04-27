# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apply *parsing instruction* to *csv_dicts* to get a stream of datapoints. 

Entry:
   gen = Datapoints(csv_dicts, parsing_instruction).emit("a")
    
"""

import re

from label import EMPTY_LABEL, make_label, concat_label
import splitter


# ------------------------------------------------------------------------------
#
# Year value checks 
#
# ------------------------------------------------------------------------------

def get_year(s: str) -> int:
    """Extract year from string *s*.
    >>> get_year('2015')  # most cases
    2015
    >>> get_year('20161)') # some cells with comment
    2016
    >>> get_year('20161)2)') # some cells with two comments
    2016"""
    
    #>>> get_year('27000,1-45000,0') # will raise ValueError    
    #ValueError: 27000,1-45000,0is not a year.
    
    if is_year(s):
        return int(s[:4])
    else:
        raise ValueError(s + " is not a year.")

def is_year(s: str)->bool:
    """Check if *s* contains year number.
    >>> is_year('1. Сводные показатели')
    False
    >>> is_year('20151)')
    True"""
    try:
        x = int(s[:4])
        if x > 1900 and x < 2050 and '-' not in s and "." not in s:
            return True
        else:
            return False
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
# Emitting datapoints from data row
#
# ------------------------------------------------------------------------------

def get_datapoints(row: dict, custom_splitter_func_name: str) -> iter:
    splitter_func = splitter.get_splitter_func(row, custom_splitter_func_name)
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
        custom_splitter_func_name = spec.reader

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

    import doctest
	# Executing doctest
    # WONTFIX: doctest not running on IPython, throws many errors
    doctest.testmod()