from enum import Enum, unique
from typing import Optional
import re

from config import get_default_csv_path
from csv_data import CSV_Reader

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

def is_top_section_name(s: str)->bool:
    """Check if string is section name.
    >>> is_top_section_name('1. Сводные показатели')
    True
    >>> is_top_section_name('2016')
    False
    """
    # Regex: one or more digits, than dot
    # than space than one or more symbols
    if re.match(r'^(\d+)\. .+$', s):
        return True
    else:
        return False    

def is_other_section_name(s: str)->bool:
    """Check if string is section name.
    >>> is_other_section_name('1. Сводные показатели')
    False
    >>> is_other_section_name('2016')
    False
    >>> is_other_section_name('4.8 Численность населения с денежными доходами')
    True
    >>> is_other_section_name('4.8. Численность населения с денежными доходами')
    True
    """
    # Regex: number, than (dot followed by number) repeated 1-3 times
    # that maybe dot
    # than space than one or more symbols
    if re.match(r'^\d+(\.\d+){1,3}\.? .+$', s):
        return True
    else:
        return False

def echo(h: str):
    try:
        print(h)
    except UnicodeEncodeError:
        print (h[:5] + "...")
    
@unique
class RowType(Enum):
    UNKNOWN = 0
    DATA = 1
    TOP_SECTION_NAME = 2
    OTHER_SECTION_NAME = 3

@unique
class State(Enum):
    INIT = 1
    DATA = 2
    UNKNOWN = 3

def get_row_type(row):
    if is_year(row['head']):
        return RowType.DATA
    if is_top_section_name(row['head']):
        return RowType.TOP_SECTION_NAME
    if is_other_section_name(row['head']):
        return RowType.OTHER_SECTION_NAME
    return RowType.UNKNOWN

def print_datarow_count(rows):
    n = len(rows)
    if n > 0:
        print(n, "data rows")
    print("--------------------------------------------------")

if __name__ == "__main__":

    #import doctest
    #doctest.testmod()

    import itertools

    text_block = {'labels':[], 'datarows':[]}
    datarows = []
    state = State.INIT

    for d in csv_dicts: #itertools.islice(csv_dicts):
        row_type = get_row_type(d)
        if row_type == RowType.DATA:
            datarows.append(d)
            state = State.DATA
        else:
            h = d['head']
            text_block['labels'].append(h)
            if state == State.DATA:
                print_datarow_count(datarows)
            echo("%s: %s" % (row_type.name, h))
            state = State.UNKNOWN
            datarows = []
    if state == State.DATA:
        print_datarow_count(datarows)
