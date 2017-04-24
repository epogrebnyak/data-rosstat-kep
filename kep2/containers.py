from enum import Enum, unique
from pprint import pprint
import re
from typing import Optional

from config import get_default_csv_path
from csv_data import CSV_Reader
from parsing_definitions import get_definitions
from datapoints import detect

# data
csv_path = get_default_csv_path()
# FIXME is list needed here? Should work fine with generator
csv_dicts = list(CSV_Reader(csv_path).yield_dicts())

def get_year(s: str) -> Optional[int]:
    """Extract year from string *s*.
    Return None if year is invalid or not in plausible range.
    >>> get_year('2015')  # most cases
    2015
    >>> get_year('20161)') # some cells with comment
    2016
    >>> get_year('20161)2)') # some cells with two comments
    2016
    >>> get_year(' 20161)2)') is None # will not match with extra space
    True
    >>> get_year('1. Сводные показатели') is None # not valid year
    True
    >>> get_year('27000,1-45000,0') is None # not valid year
    True"""
    # Regex: 4 digits, than any number of comments
    # then any number of whitespaces
    # comment is 1 or more digits followed by symbol ')'
    match = re.match(r'(\d{4})(\d+\))*\s*', s)
    if match:
        year = int(match.group(1))
        if year > 1900 and year < 2050:
            return year
    return None

def is_year(s: str) -> bool:
    """
    >>> is_year('20161)2)') # some cells with two comments
    True"""
    return get_year(s) is not None

def is_numeric(s: str)->bool:
    # replace all digits and see what remains
    pass

def parse_section_name(s: str)->bool:
    """Check if string is section name.
    >>> parse_section_name('1. Сводные показатели')
    '1'
    >>> parse_section_name('2016') is None
    True
    >>> parse_section_name('4.8 Численность населения с денежными доходами')
    '4.8'
    >>> parse_section_name('4.8. Численность населения с денежными доходами')
    '4.8'
    """
    # Regex: number, than (dot followed by number) repeated 1-3 times
    # that maybe dot
    # than space than one or more symbols
    match = re.match(r'^(\d+(\.\d+){0,3})\.? .+$', s)
    if match:
        return match.group(1)
    else:
        return None

def parse_header(s, pdef):
    header = detect(s, pdef.headers.keys())
    if header is not None:
        header = pdef.headers[header]
    unit = detect(s, pdef.units.keys())
    if unit is not None:
        unit = pdef.units[unit]
    return (header, unit)

def echo(h: str):
    try:
        print(h)
    except UnicodeEncodeError:
        print (h[:5] + "...")
    
@unique
class RowType(Enum):
    UNKNOWN = 0
    DATA = 1
    SECTION = 2
    HEADER = 4

@unique
class State(Enum):
    INIT = 1
    DATA = 2
    UNKNOWN = 3

def get_row_type(row, pdef):
    if is_year(row['head']):
        return RowType.DATA, None
    section = parse_section_name(row['head'])
    header_parse_result = parse_header(row['head'], pdef)
    if header_parse_result[0] is not None or header_parse_result[1] is not None:
        return RowType.HEADER, (header_parse_result[0], header_parse_result[1], section)
    if section:
        return RowType.SECTION, section
    return RowType.UNKNOWN, None

def print_datarow_count(rows, header, unit):
    n = len(rows)
    if n > 0:
        print(n, "data rows, header: ", header, ", unit:", unit)
    print("--------------------------------------------------")

if __name__ == "__main__":

    #import doctest
    #doctest.testmod()

    import itertools

    text_block = {'labels':[], 'datarows':[]}
    datarows = []
    state = State.INIT
    parse_def = get_definitions()['default']
    #pprint(parse_def, indent=4)
    header = unit = None

    for d in csv_dicts: #itertools.islice(csv_dicts):
        row_type, data = get_row_type(d, parse_def)
        if row_type == RowType.DATA:
            datarows.append(d)
            state = State.DATA
        else:
            h = d['head']
            text_block['labels'].append(h)
            if state == State.DATA:
                print_datarow_count(datarows, header, unit)
                unit = None
            if data is not None:
                echo("%s(%s): %s" % (row_type.name, data, h))
            else:
                echo("%s: %s" % (row_type.name, h))
            state = State.UNKNOWN
            datarows = []
            if row_type == RowType.HEADER:
                if data[0] is not None:
                    header = data[0]
                if data[1] is not None:
                    unit = data[1]
            if row_type == RowType.UNKNOWN or row_type == RowType.SECTION:
                header = unit = None
    if state == State.DATA:
        print_datarow_count(datarows, header, unit)
