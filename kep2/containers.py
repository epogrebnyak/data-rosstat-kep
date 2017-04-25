from collections import namedtuple
from enum import Enum, unique
import itertools
from pprint import pprint
import re
from typing import Optional

from config import get_default_csv_path
from csv_data import CSV_Reader
from parsing_definitions import get_definitions
from datapoints import detect

ParseResult = namedtuple('ParseResult', ['header', 'units', 'section_number'])

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
    units = detect(s, pdef.units.keys())
    if units is not None:
        units = pdef.units[units]
    section_number = parse_section_name(s)
    return ParseResult(header, units, section_number)

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

def is_data_row(row):
    return is_year(row['head'])

def get_row_type(row, pdef):
    if is_data_row(row):
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

def split_blocks(csv, pdef):
    datarows = []
    headers = []
    state = State.INIT

    for d in csv_dicts: #itertools.islice(csv_dicts):
        if is_data_row(d):
            datarows.append(d)
            state = State.DATA
        else:
            if state == State.DATA: # table ended
                block = DataBlock(headers, datarows, pdef)
                yield block
                headers = []
                datarows = []
            headers.append(d)
            state = State.UNKNOWN
    # still have some data left
    if len(headers) > 0 and len(datarows) > 0:
        yield DataBlock(headers, datarows, pdef)

class DataBlock():

    def __init__(self, headers, datarows, pdef):
        self.headers = headers
        self.datarows = datarows
        self.pdef = pdef
        self.parse_headers()

    def parse_headers(self):
        units = header = None
        # There can be more than one section number in block, keep all for now
        section_numbers = []
        self.has_unknown = False
        for row in self.headers:
            parse_result = parse_header(row['head'], self.pdef)
            new_header = parse_result.header
            if new_header is not None:
                header = new_header
            new_units = parse_result.units
            if new_units is not None:
                units = new_units
            new_section_number = parse_result.section_number
            if new_section_number is not None:
                section_numbers.append(new_section_number)
            if new_units is None and new_header is None:
                self.has_unknown = True
        self.raw_header = header
        self.raw_units = units
        # if units are not none, than use it
        # else use second element of header (in case header is not none itself)
        self.units = units or (header and header[1])
        # if header is not none, use it's first element
        self.parameter = header and header[0]
        self.sections = section_numbers

    def __str__(self):
        header_str = '\n'.join([x['head'] for x in self.headers])
        parameter_str = 'parameter: ' + str(self.parameter)
        units_str = 'units: ' + str(self.units)
        sections_str = 'sections: ' + ', '.join(self.sections)
        has_unknown_str = 'has_unknown: ' + str(self.has_unknown)
        data_str = '-'*30 + '\n' + '\n'.join(["%s | %s" % (x['head'], ' '.join(x['data'])) for x in self.datarows])
        return '\n'.join([header_str, parameter_str, units_str, sections_str, has_unknown_str, data_str])

def fix_multitable_units(blocks):
    """For those blocks which do not have parameter definition,
    but do not have any unknown rows, copy parameter from previous block
    """
    for prev_block, block in zip(blocks, blocks[1:]):
        if not block.has_unknown and block.parameter is None:
            block.parameter = prev_block.parameter

if __name__ == "__main__":

    #import doctest
    #doctest.testmod()

    # data
    csv_path = get_default_csv_path()
    csv_dicts = CSV_Reader(csv_path).yield_dicts()

    parse_def = get_definitions()['default']
    blocks = list(split_blocks(csv_dicts, parse_def))
    # count unknown units
    u_number = len([True for b in blocks if b.units is None])
    # count unknown parameters before fix
    p1_number = len([True for b in blocks if b.parameter is None])
    fix_multitable_units(blocks)
    # count unknown parameters after fix
    p2_number = len([True for b in blocks if b.parameter is None])
    # count blocks with unparsed rows
    unp_number = len([True for b in blocks if b.has_unknown])
    for b in blocks:
        print(str(b), '\n')
    print("Total blocks:", len(blocks))
    print("Unknown units:", u_number)
    print("Unknown parameters before fix:", p1_number)
    print("Unknown parameters after fix:", p2_number)
    print("Blocks with unparsed lines:", unp_number)
