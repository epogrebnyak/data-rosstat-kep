import re
import sys
from enum import Enum, unique
from typing import Optional

from kep.parser.row_utils.splitter import get_splitter_func_by_column_count


HEAD_UNIT_SEPARATOR = "__"

def get_year(s: str) -> Optional[int]:
    """Extract year from string *s*.
    Return None if year is invalid or not in plausible range."""

    # Regex: 4 digits, then any number of comments
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

   
def is_data_row(row):
    return is_year(row['head'])

    
class SegmentState():
    """
    SegmentState is used in parsing of sequence of headers. It holds information 
    about what parsing specification (segment) applies to current row. The specification 
    switches between current and alternative segments, depending on headers. 
    
    Method .assign_parsing_definitions(heads) yeilds modified csv_dicts.    
    """
    
    DEFAULT_STATE = 1
    ALT_STATE = 0

    def __init__(self, spec):
        
        self.default_spec = spec.main
        self.specs = spec.extras
        self.__reset_to_default_state__()
      
    @staticmethod
    def is_matched(head, line):
        if line:
            return head.startswith(line)
        else:
            return False

    def update_on_entering_custom_segment(self, head):
        for spec in self.specs:
            if self.is_matched(head, spec.start):
                self.__enter_segment__(spec)

    def update_on_leaving_custom_segment(self, head):
        if self.is_matched(head, self.current_end_line):
            self.__reset_to_default_state__()

    def __reset_to_default_state__(self): 
        # Exit from segment
        self.segment_state = self.DEFAULT_STATE
        self.current_spec = self.default_spec
        self.current_end_line = None

    def __enter_segment__(self, segment_spec):
        self.segment_state = self.ALT_STATE
        self.current_spec = segment_spec
        self.current_end_line = segment_spec.end

    def assign_parsing_definitions(self, csv_dicts):
        for row in csv_dicts:
            if is_data_row(row):
                row.update({'pdef':None})
            else:
                head = row['head']
                if self.segment_state == self.ALT_STATE:
                    self.update_on_leaving_custom_segment(head)
                self.update_on_entering_custom_segment(head)
                row.update({'pdef':self.current_spec})
            yield row




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

def get_label_from_header(textline, pdef):
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

def extract_label_from_headers(headers, parse_def):
    label = unit = None
    has_unknown_line_in_headers = False
    for row in headers:
        textline = row['head']
        # label and unit updated to last value detected
        new_label = get_label_from_header(textline, parse_def)
        if new_label:
            label = new_label
        new_unit = get_unit(textline, parse_def)
        if new_unit:
            unit = new_unit
        if new_unit is None and new_label is None:
            has_unknown_line_in_headers = True    
    return label, unit, has_unknown_line_in_headers 
    
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
    
def split_to_blocks(csv_dicts):
    datarows = []
    headers = []
    state = State.INIT
    for d in csv_dicts: 
        if is_data_row(d):
            datarows.append(d)
            state = State.DATA
        else:
            if state == State.DATA: # table ended
                yield DataBlock(headers, datarows, parse_def=headers[0]['pdef'])
                headers = []
                datarows = []
            headers.append(d)
            state = State.UNKNOWN
    # still have some data left
    if len(headers) > 0 and len(datarows) > 0:
        yield DataBlock(headers, datarows, parse_def=headers[0]['pdef'])
        
class DataBlock():

    def __init__(self, headers, datarows, parse_def):
        self.headers = headers
        self.datarows = datarows
        self.parse_def = parse_def
        self.__parse_headers__()
        self.__parse_sections__()
        self.__set_splitter_func__()
    
    def __set_splitter_func__(self):
        # get safe length even for self.datarows = []
        if self.datarows:
            self.coln = max([len(d['data']) for d in self.datarows])        
        else:
            self.coln = 0
        self.splitter_func = get_splitter_func_by_column_count(self.coln, 
                             custom_splitter_func_name=self.parse_def.reader)
                
    def __parse_headers__(self):        
        # get variable label and flag (if unidentified line is present in self.headers)
        label, unit, self.has_unknown_textline = extract_label_from_headers(self.headers, self.parse_def)
        # if label found in header is not none, use its varname
        self.varname = label and label.varname
        # if unit is not none, then use it
        # otherwise use second element of label unit (if label is present)
        self.unit = unit or (label and label.unit)
    
    def __parse_sections__(self):
        # get section number
        # there can be more than one section number in block, keep all for now
        self.sections = []
        for row in self.headers:
            # update section number
            new_section_number = parse_section_name(row['head'])
            if new_section_number:
                self.sections.append(new_section_number)
                
    @property
    def label(self): 
        if self.varname and self.unit:
            return self.varname + HEAD_UNIT_SEPARATOR + self.unit 
        else:
            return None

    def __str__(self):
        header_str = '\n'.join([x['head'] for x in self.headers])
        varname_str = 'varname: ' + str(self.varname)
        unit_str = 'unit: ' + str(self.unit)
        sections_str = 'sections: ' + ', '.join(self.sections)
        has_unknown_textline_str = 'has_unknown_textline: ' + str(self.has_unknown_textline)
        coln = 'columns: ' + str(self.coln)
        data_str = '-'*30 + '\n' + '\n'.join(["%s | %s" % (x['head'], ' '.join(x['data'])) for x in self.datarows])
        return '\n'.join([header_str, varname_str, unit_str, sections_str, 
                          coln, has_unknown_textline_str, data_str])

def fix_multitable_units(blocks):
    """For those blocks which do not have parameter definition,
    but do not have any unknown rows, copy parameter from previous block
    """
    for prev_block, block in zip(blocks, blocks[1:]):
        if not block.has_unknown_textline and block.varname is None:
            block.varname = prev_block.varname

# TODO - also move commetns around
            
def get_blocks(csv_dicts, spec):
    csv_dicts = SegmentState(spec).assign_parsing_definitions(csv_dicts)
    blocks = list(split_to_blocks(csv_dicts))
    fix_multitable_units(blocks)
    return blocks


def show_stats(blocks, spec):
    total = len(blocks)  
    defined_tables = len([True for b in blocks if b.varname and b.unit])
    undefined_tables = len([True for b in blocks if not b.varname or not b.unit])
    unknown_lines = len([True for b in blocks if b.has_unknown_textline])
    print("Total blocks               ",  total)
    print("  Ready to import          ", "{:>3}".format(defined_tables))
    print("  Not parsed               ", "{:>3}".format(undefined_tables))
    print("  Blocks with unknown lines", "{:>3}".format(unknown_lines))
    assert total == defined_tables + undefined_tables
    print("\nUnique variable names")
    unique_vn_found = len(set([b.varname for b in blocks if b.varname is not None]))
    # FIXME:
    #unique_vn_defined = len(spec.unique_varheads())
    print("  Ready to import           ", unique_vn_found)
    #print("  In definition             ", unique_vn_defined)
    print()

# from http://stackoverflow.com/a/29988426    
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)    
    
if __name__ == "__main__":
    import kep.reader.access as reader
    csv_dicts = list(reader.get_csv_dicts())   
    spec = reader.get_spec()
    # replaces: 
    #main_def = reader.ParsingDefinition(path=ini.get_mainspec_filepath())
    #more_def = [reader.ParsingDefinition(path) for path in ini.get_additional_filepaths()]
    
    #labs = set([main_def.unique_labels] + [d.unique_labels for d in more_def]) 
    
    # read blocks
    blocks = get_blocks(csv_dicts, spec)
    for b in blocks:
        uprint(b)
        print('\n')
        
    # IDEA: move show_stats() to test
    # FIXME: does not account for *more_def* 
    show_stats(blocks, spec)

    # IDEA: move to tests
    assert max([len(d['data']) for d in blocks[0].datarows]) == blocks[0].coln
    
    varnames = [b.label for b in blocks if b.label is not None]   
    assert "GOV_SUBFEDERAL_SURPLUS_ACCUM__bln_rub" in varnames