import re
import sys
from enum import Enum, unique
from typing import Optional

import kep.parser.row_utils.splitter as splitter 
import kep.util.seq as util

HEAD_UNIT_SEPARATOR = "__"

def get_year(cell: str) -> Optional[int]:
    """Extract year from string *s*.
    Return None if year is invalid or not in plausible range."""

    # Regex: 
    #   (\d{4})    4 digits
    #   \d+\)      comment like "1)"
    #   (\d+\))*   any number of comments 
    #   \s*        any number of whitespaces
    match = re.match(r'(\d{4})(\d+\))*\s*', cell)
    if match:
        year = int(match.group(1))
        if year >= 1991:
            return year
    return None

def is_year(s: str) -> bool:
    return get_year(s) is not None

   
def is_data_row(row):
    return is_year(row['head'])

    
class Segmenter():
    """
    Segmenter is used in parsing of sequence of headers. 
    
    It holds information  about what parsing specification (segment) 
    applies to current row. The specification switches between current 
    and alternative segments, depending on headers. 
    
    Method .assign_parsing_definitions(heads) yeilds modified csv_dicts.    
    """
    
    DEFAULT_STATE = 1
    ALT_STATE = 0

    def __init__(self, spec):
        
        self.default_spec = spec.main
        self.specs = spec.extras
        self.__reset_to_default_state__()
      
    def update_on_entering_custom_segment(self, head):
        for spec in self.specs:
            if head.startswith(spec.start):
                self.__enter_segment__(spec)

    def update_on_leaving_custom_segment(self, head):
        if head.startswith(self.current_end_line):
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


def detect(line: str, patterns: list) -> (bool, str):
    """Check if any string from *patterns* list is present in *text* string.
    
       :param line: string that may contain strings from *patterns*
       :param patterns: list of strings
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
    HEADER = 3

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
        if self.datarows:
            self.coln = max([len(d['data']) for d in self.datarows])        
        else:
            self.coln = 0  
        self.parse_def = parse_def        
        self.__set_splitter_func__()
        self.__parse_headers__()        
    
    def __set_splitter_func__(self):
        funcname = self.parse_def.reader
        if funcname:
            self.splitter_func = splitter.get_custom_splitter(funcname)
        else:
            self.splitter_func = splitter.get_splitter(self.coln)
            
    def __parse_headers__(self):        
        # get variable label and flag (if unidentified line is present in self.headers)
        label, unit, self.has_unknown_textline = extract_label_from_headers(self.headers, self.parse_def)
        # if label found in header is not none, use its varname
        self.varname = label and label.varname
        # if unit is not none, then use it
        # otherwise use second element of label unit (if label is present)
        self.unit = unit or (label and label.unit)   

                
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

        has_unknown_textline_str = 'has_unknown_textline: ' + str(self.has_unknown_textline)
        coln = 'columns: ' + str(self.coln)
        data_str = '-'*30 + '\n' + '\n'.join(["%s | %s" % (x['head'], ' '.join(x['data'])) for x in self.datarows])
        return '\n'.join([header_str, varname_str, unit_str, 
                          coln, has_unknown_textline_str, data_str])

def fix_multitable_units(blocks):
    """For those blocks which do not have parameter definition,
       but do not have any unknown rows, copy parameter from previous block
    """
    for prev_block, block in zip(blocks, blocks[1:]):
        if not block.has_unknown_textline and block.varname is None:
            block.varname = prev_block.varname

           
def get_blocks(csv_dicts, spec):
    csv_dicts = Segmenter(spec).assign_parsing_definitions(csv_dicts)
    blocks = list(split_to_blocks(csv_dicts))
    fix_multitable_units(blocks)
    # TODO: move "___"-commment strings around
    return blocks


def defined_blocks(blocks):
     for b in blocks:
         if b.varname and b.unit:
             yield b            

def get_flat_headers(blocks):
    for b in blocks:
        for h in b.headers:
            yield h['head']              

def show_coverage(blocks):
    total = len(blocks)  
    defined_tables = len([True for b in blocks if b.varname and b.unit])
    undefined_tables = len([True for b in blocks if not b.varname or not b.unit])
    assert total == defined_tables + undefined_tables
    print("Total blocks              ",  total)
    print("  with defined labels     ", "{:>3}".format(defined_tables))
    print("  labels not defined      ", "{:>3}".format(undefined_tables))
    cov_pct = int(defined_tables/total*100)
    print("\nCoverage                  ", "{:>2}%".format(cov_pct ), "(full coverage not targeted)")

def show_duplicates(blocks):    
    varnames = [b.label for b in defined_blocks(blocks)]
    dups = util.duplicates(varnames)
    print("\nDuplicate varnames:\n  " + ", ".join(dups))

def show_unknowns(blocks):     
    unknown_lines = len([True for b in blocks if b.has_unknown_textline])    
    # IDEA: drop unknown flag for unit headers
    print("\nBlocks with unrecognised lines:", "{:>3}".format(unknown_lines))
    return unknown_lines

def show_parsing_matches_definition(blocks, spec):    
    vn_found = util.unique([b.varname for b in defined_blocks(blocks)])
    vn_defined = util.unique(spec.varnames)
    not_found = [vh for vh in vn_defined if vh not in vn_found]                  
    print("\nUnique varnames")
    print("  In definition:  ", len(vn_defined))
    print("  Ready to import:", len(vn_found))
    print("  Not found:      ", len(not_found))
    assert len(vn_defined) == len(vn_found) + len(not_found)    
    msg =", ".join(not_found)
    print("  " + msg)
    
def show_stats(blocks, spec):
    show_coverage(blocks)  
    show_duplicates(blocks)
    show_unknowns(blocks)
    show_parsing_matches_definition(blocks, spec)   

 
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    """Safe print() to console. Adopted from from http://stackoverflow.com/a/29988426"""                    
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

    # read blocks
    blocks = get_blocks(csv_dicts, spec)
    for b in blocks:
        #uprint(b)
        #print('\n')
        pass
        
    # show_stats(blocks, spec)
    
    headers = list(get_flat_headers(blocks))
    lines = [s.start for s in spec.extras] + [s.start for s in spec.extras]
    def inc(line, headers):
        for h in headers:
            if line in h:
                return True
        return False
    for line in lines:
        print(inc(line, headers), line)
        
    a = '2.1.2. Расходы (по данным Федерального казначейства)1) / Expenditures (data of the Federal Treasury)1)'
    b = '2.1.2. Расходы (по данным Федерального казначейства)'
            
# ERROR 1 - CRITICAL: some spec.extras[] defintions not found in file while parsing 
    labels = [b.label for b in blocks if b.label is not None]   
    assert "GOV_SUBFEDERAL_SURPLUS_ACCUM__bln_rub" in labels
    
    varheads = [b.varname for b in blocks if b.varname is not None] 
    assert "RETAIL_SALES_NONFOOD_GOODS" in varheads