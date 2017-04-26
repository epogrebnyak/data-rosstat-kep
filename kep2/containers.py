""""""
from enum import Enum, unique
import re
from typing import Optional

from config import get_default_csv_path
from csv_data import CSV_Reader
from parsing_definitions import get_definitions

# from collections import namedtuple
# Note: use more often, may replace ParsingDefinition class
# ParseResult = namedtuple('ParseResult', ['header', 'units', 'section_number'])
# a = ParseResult(1,2,3)

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
    
# SUGGETED, NOT RUN ---------------
def detect(line: str, patterns: list) -> (bool, str):
    """Check if any string from *patterns* list is present in *text* string.
    
       :param line: string tat may contain strings from *patterns*
       :param patterns: list of strings
    
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

def get_varname(textline, pdef):
    header_key_found = detect(textline, pdef.headers.keys())
    if header_key_found:
        return pdef.headers[header_key_found]
    else: 
        return None
    
def get_unit(textline, pdef):
    unit_key_found = detect(textline, pdef.units.keys())
    if unit_key_found:
        return pdef.units[unit_key_found]
    else:
        return None
    
#def parse_table_header(textline, pdef):
#    # replace def parse_header(s, pdef):
#    header = get_varname(textline, pdef)
#    unit = get_unit(textline, pdef)
#    section_number = parse_section_name(textline)
#    return ParseResult(header, unit, section_number)    
#
## -----------------------------------------------------------
#
#
#def parse_header(s, pdef):
#    header = detect(s, pdef.headers.keys())
#    if header is not None:
#        header = pdef.headers[header]
#    units = detect(s, pdef.units.keys())
#    if units is not None:
#        units = pdef.units[units]
#    section_number = parse_section_name(s)
#    return ParseResult(header, units, section_number)

#def echo(h: str):
#    try:
#        print(h)
#    except UnicodeEncodeError:
#        print (h[:5] + "...")
#    
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

#def get_row_type(row, pdef):
#    if is_data_row(row):
#        return RowType.DATA, None
#    section = parse_section_name(row['head'])
#    header_parse_result = parse_header(row['head'], pdef)
#    if header_parse_result[0] is not None or header_parse_result[1] is not None:
#        return RowType.HEADER, (header_parse_result[0], header_parse_result[1], section)
#    if section:
#        return RowType.SECTION, section
#    return RowType.UNKNOWN, None

#def print_datarow_count(rows, header, unit):
#    n = len(rows)
#    if n > 0:
#        print(n, "data rows, header: ", header, ", unit:", unit)
#    print("--------------------------------------------------")

def split_blocks(csv, pdef):
    datarows = []
    headers = []
    state = State.INIT

    for d in csv_dicts: 
        if is_data_row(d):
            datarows.append(d)
            state = State.DATA
        else:
            if state == State.DATA: # table ended
                yield DataBlock(headers, datarows, pdef)
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
        unit = varname = None
        # WARNING: there can be more than one section number in block, keep all for now
        section_numbers = []
        self.has_unknown_textline = False
        for row in self.headers:
            textline = row['head']
            new_varname = get_varname(textline, self.pdef)
            # replace header
            if new_varname:
                varname = new_varname
            # new unit always updated to last value detected
            new_unit = get_unit(textline, self.pdef)
            if new_unit:
                unit = new_unit
            # update section number
            new_section_number = parse_section_name(textline)
            if new_section_number:
                section_numbers.append(new_section_number)
            # raise flag if unidentified line is present in self.headers
            if new_unit is None and new_varname is None:
                self.has_unknown_textline = True
        # for inspection 
        self.__raw_header__ = varname
        self.__raw_unit__ = unit
        # if unit is none, then use it
        # else use second element of header (in case header is not none itself)
        self.unit = unit or (varname and varname[1])
        # if header is not none, use it's first element
        self.varname = varname and varname[0]
        self.sections = section_numbers

    def __str__(self):
        header_str = '\n'.join([x['head'] for x in self.headers])
        varname_str = 'varname: ' + str(self.varname)
        unit_str = 'unit: ' + str(self.unit)
        sections_str = 'sections: ' + ', '.join(self.sections)
        has_unknown_textline_str = 'has_unknown_textline: ' + str(self.has_unknown_textline)
        data_str = '-'*30 + '\n' + '\n'.join(["%s | %s" % (x['head'], ' '.join(x['data'])) for x in self.datarows])
        return '\n'.join([header_str, varname_str, unit_str, sections_str, has_unknown_textline_str, data_str])

def fix_multitable_units(blocks):
    """For those blocks which do not have parameter definition,
    but do not have any unknown rows, copy parameter from previous block
    """
    for prev_block, block in zip(blocks, blocks[1:]):
        if not block.has_unknown_textline and block.varname is None:
            block.varname = prev_block.varname
    # SUGGESTION = maybe yield here and blocks = fix_multitable_units(blocks)
    #              uncoforatable that func changes global var *blocks*.
    

if __name__ == "__main__":
    # inputs
    csv_path = get_default_csv_path()
    csv_dicts = CSV_Reader(csv_path).yield_dicts()
    parse_def = get_definitions()['default']
    # 
    blocks = list(split_blocks(csv_dicts, parse_def))
    # count unknown units
    u_number = len([True for b in blocks if b.unit is None])
    # count unknown parameters before fix
    p1_number = len([True for b in blocks if b.varname is None])
    fix_multitable_units(blocks)
    # count unknown parameters after fix
    p2_number = len([True for b in blocks if b.varname is None])
    anti_p2_number = len([True for b in blocks if b.varname is not None])
    p3_number = len([True for b in blocks if b.varname is not None and b.unit is not None])
    # count blocks with unparsed text rows
    unp_number = len([True for b in blocks if b.has_unknown_textline])
    for b in blocks:
        print(str(b), '\n')
    total = len(blocks)  
    print("Total blocks:", total)
    print("Unknown units:", u_number)
    print("Unknown variables before fix:", p1_number)
    print("Unknown variables after fix:", p2_number)
    print("Known variables after fix:", anti_p2_number)
    print("Ready to import", p3_number)
    print("Blocks with unparsed lines:", unp_number)
    assert p3_number == anti_p2_number  
    assert total == p2_number + anti_p2_number
