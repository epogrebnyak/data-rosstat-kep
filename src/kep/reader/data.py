# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:38:37 2017

@author: PogrebnyakEV
"""

import json
from pathlib import Path
import csv
import re
from enum import Enum, unique

ENC = 'utf-8'
CSV_FORMAT = dict(delimiter='\t', lineterminator='\n')

# read and write json files
def as_json(x):    
    return json.dumps(x, ensure_ascii=False, indent=4)

def to_json(x, path):
    path.write_text(as_json(x), encoding = ENC)
    return path
    
def from_json(path):
    return json.load(path.open(encoding = ENC))     

# csv file access
def to_csv(rows, path):
    """Accept iterable of rows *rows* and write in to *csv_path*"""
    with path.open('w', encoding=ENC) as csvfile:
        filewriter = csv.writer(csvfile, **CSV_FORMAT)
        for row in rows:
            filewriter.writerow(row)
    return path

def from_csv(path):
    """Get iterable of rows from *csv_path*"""
    with path.open(encoding=ENC) as csvfile:
       csvreader = csv.reader(csvfile, **CSV_FORMAT)
       for row in csvreader:
             yield row  
         
def to_dict(row):
    """Make dictionary based on non-empty *row*"""
    if row and row[0]:
       return dict(head=row[0], data=row[1:])
    else:
       return None
    
def read_csv(path):
    """Yield non-empty dictionaries with 'head' and 'data' keys from *path*"""
    raw = from_csv(path)
    csv_dicts = map(to_dict, raw)    
    return filter(lambda x: x is not None, csv_dicts) 

#FIXME: *validate_ends* must be part of definition

def validate_ends(self, start, end):
    if self.is_matched(start, end) or self.is_matched(end, start):
        print("***  ERROR: start and end lines not unique***")
        print(start)
        print(end)

#holder class for csv rows

def is_matched(pat, textline):
    pat = pat.replace('"','') 
    textline = textline.replace('"','')
    if pat:
        return textline.startswith(pat)
    else:
        return False 

class DictStream():    
    def __init__(self, csv_dicts):
        # consume *csv_dicts*, myabe it is a generator
        self.csv_dicts = [x for x in csv_dicts]
    
    def is_found(self, pat):
        for csv_dict in self.csv_dicts:
            if is_matched(pat, csv_dict['head']):
                return True
        return False
          
    def remaining_csv_dicts(self):
        return self.csv_dicts

    def pop(self, pdef):
        for marker in pdef['markers']:
            s = marker['start'] 
            e = marker['end'] 
            if self.is_found(s) and self.is_found(e):
                return self.pop_segment(s, e)
        self.echo_error_ends_not_found(pdef)
        return []    
        
    def echo_error_ends_not_found(self, pdef):
        print("ERROR: start or end line not found in *csv_dicts*")              
        for marker in pdef['marker_lines']:
            s = marker['start'] 
            e = marker['end'] 
            print("   ", self.is_found(s), "<{}>".format(s))
            print("   ", self.is_found(e), "<{}>".format(e))                       
    
    def pop_segment(self, start, end):
        """Pops elements of self.csv_dicts between [start, end). 
           Recognises occurences by index *i*."""           
        remaining_csv_dicts = self.csv_dicts.copy()
        we_are_in_segment = False
        segment = []
        i = 0
        while i < len(remaining_csv_dicts):
            row = remaining_csv_dicts[i]
            line = row['head']
            if is_matched(start, line):
                we_are_in_segment = True
            if is_matched(end, line):
                break
            if we_are_in_segment:
                segment.append(row)
                del remaining_csv_dicts[i]
            else:    
                # else is very important, wrong indexing without it
                i += 1
        self.csv_dicts = remaining_csv_dicts
        return segment

def get_year(cell: str):
    """Extract year from string *s*. Return None if year is invalid 
       or not in plausible range."""

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


class Header():
    def __init__(self, csv_dicts, pdef, units):
        self.varname = None
        self.unit = None        
        self.textlines_original = [d['head'] for d in csv_dicts]
        self.textlines = [d['head'] for d in csv_dicts]                
        self.set_varname(pdef, units)       
        self.set_unit(units)
    
    def set_varname(self, pdef, units):
        for line in self.textlines:
            for pat in pdef['headers'].keys():
                if pat in line:
                    self.textlines.remove(line) 
                    self.varname = pdef['headers'][pat]
                    self.unit = get_unit(line, units)
                    assert self.unit is not None                    
                    
    def set_unit(self, units):
        for line in self.textlines:            
            unit = get_unit(line, units)
            if unit:
                self.unit = unit
                for pat in units.keys():
                   if line.startswith(pat):
                      self.textlines.remove(line)
                
    
    def unknown_lines(self):
        return len(self.textlines)
    
    def __str__(self):
        return ("<{}>".format("\n".join(self.textlines_original)) +
                "\ntotal lines: {1}, unknown: {0}".format(self.unknown_lines(), len(self.textlines_original)) +
                "\nvarname: {}, unit: {}".format(self.varname, self.unit)
                )
                   
def get_unit(line, units):
    for k in units.keys():
        if k in line:  
            return units[k]
    return None

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
    
def split_to_tables(csv_dicts):
    datarows = []
    headers = []
    state = State.INIT
    for d in csv_dicts: 
        if is_data_row(d):
            datarows.append(d)
            state = State.DATA
        else:
            if state == State.DATA: # table ended
                yield Table(headers, datarows)
                headers = []
                datarows = []
            headers.append(d)
            state = State.UNKNOWN
    # still have some data left
    if len(headers) > 0 and len(datarows) > 0:
        yield Table(headers, datarows)
        
class Table():

    def __init__(self, textrows, data_rows):
        self.textrows = textrows
        self.datarows = data_rows
        if self.datarows:
             self.coln = max([len(d['data']) for d in self.datarows])        
        else:
             self.coln = 0
        
    def parse(self, pdef, units):
        self.header = Header(self.textrows, pdef, units)        
        funcname = pdef['reader']
        return self  
        # FIXME: add splitter
        #if funcname:
        #    self.splitter_func = splitter.get_custom_splitter(funcname)
        #else:
        #                    
        #    self.splitter_func = splitter.get_splitter(coln)           

    @property
    def label(self): 
        vn = self.header.varname
        u = self.header.unit
        if vn and u:
            return vn + "_" + u

    def __str__(self):
        return self.header.__str__() + "\nlabel: {}".format(self.label) 

def fix_multitable_units(blocks):
    """For those blocks which do not have parameter definition,
       but do not have any unknown rows, copy parameter from previous block
    """
    for prev_block, block in zip(blocks, blocks[1:]):
        if block.header.unknown_lines() == 0 and \
           block.header.varname is None:
           block.header.varname = prev_block.header.varname
            
def get_tables(csv_dicts, pdef, units):
    tables = [t.parse(pdef, units) for t in split_to_tables(csv_dicts)]
    fix_multitable_units(tables)
    # TODO: move "___"-commment strings around
    return tables


if __name__=="__main__": 
    assert get_year("19991)") == 1999
        
    doc = """1.9. Внешнеторговый оборот – всего1), млрд.долларов США / Foreign trade turnover – total1), bln US dollars																	
1999	115,1	24,4	27,2	28,4	35,1	7,2	7,9	9,3	9,8	8,0	9,3	9,5	9,3	9,6	10,4	11,1	13,7
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
1999	86,9	68,1	75,5	87,0	125,3	63,5	68,3	72,1	80,5	68,6	77,0	78,4	83,7	102,2	117,9	127,4	129,8
в % к предыдущему периоду / percent of previous period																	
1999		87,0	111,5	104,3	123,9	68,1	109,5	118,0	105,7	81,5	116,7	101,8	97,4	103,2	108,2	106,9	123,9
в том числе:																	
экспорт товаров – всего, млрд.долларов США																	
/ of which: export of goods – total, bln US dollars																	
1999	75,6	15,3	17,1	18,9	24,3	4,5	4,9	5,8	6,6	5,1	5,4	6,3	6,2	6,4	7,0	7,6	9,7
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
1999	101,5	85,1	91,6	98,5	130,1	79,0	86,8	89,0	106,4	84,9	83,8	94,4	99,8	101,5	119,0	132,3	137,5
в % к предыдущему периоду / percent of previous period																	
1999		81,7	111,9	110,5	128,8	63,7	109,5	118,3	112,4	78,3	105,1	116,4	98,2	104,4	108,4	109,0	127,9
импорт товаров – всего, млрд.долларов США																	
/ import of goods – total, bln US dollars																	
1999	39,5	9,1	10,1	9,5	10,8	2,7	3,0	3,5	3,3	2,9	4,0	3,2	3,1	3,1	3,4	3,5	4,0
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
1999	68,1	51,1	58,1	70,6	115,8	47,8	50,3	54,7	54,2	51,0	69,3	58,9	63,4	103,5	115,7	117,7	114,3
в % к предыдущему периоду / percent of previous period																	
1999		97,4	110,9	93,8	114,2	77,0	109,7	117,6	94,5	87,8	137,3	81,9	96,0	100,9	107,7	102,5	115,3
1.9.1. Внешнеторговый оборот со странами дальнего зарубежья – всего, млрд.долларов США / Foreign trade turnover with far abroad countries – total, bln US dollars"""
    
         
    pdef = dict(labels=["EXPORT_GOODS_TOTAL_bln_usd", #assumed variable labels 
                          "IMPORT_GOODS_TOTAL_bln_usd"],
               #start and end lines
               markers=[dict(start="1.9. Внешнеторговый оборот – всего",
                               end="1.9.1. Внешнеторговый оборот со странами дальнего зарубежья"),
                        dict(start="1.10. Внешнеторговый оборот – всего",
                               end="1.10.1. Внешнеторговый оборот со странами дальнего зарубежья")],
               # table headers to variable names               
               headers={"экспорт товаров – всего": "EXPORT_GOODS_TOTAL"
                       , "импорт товаров – всего": "IMPORT_GOODS_TOTAL"},
               #special column reader func name        
               reader=None)
     
    units = {'млрд.долларов': 'bln_usd',
             'в % к ВВП': 'gdp_percent',
             'в % к декабрю предыдущего года': 'ytd',
             'в % к предыдущему месяцу': 'rog',
             'в % к предыдущему периоду': 'rog',
             'в % к соответствующему месяцу предыдущего года': 'yoy',
             'в % к соответствующему периоду предыдущего года': 'yoy',
             'млн.рублей': 'mln_rub',
             'отчетный месяц в % к предыдущему месяцу': 'rog',
             'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy',
             'период с начала отчетного года': 'ytd',
             'рублей / rubles': 'rub'}
    
    
    cur_dir = Path(__file__).parent
    pdef_path = cur_dir / "pdef.json"
    units_path = cur_dir / "units.json" 
    csv_path = cur_dir / "data.csv" 
    Path(csv_path).write_text(doc, encoding=ENC)
    
    assert from_json(to_json(pdef, pdef_path)) == pdef
    assert from_json(to_json(units, units_path)) == units    
                    
    pdef = from_json(pdef_path)                    
    units = from_json(units_path)                
    csv_dicts = read_csv(csv_path)
    
    ds = DictStream(csv_dicts)
    csv_segment = ds.pop(pdef)
    csv_rem = ds.remaining_csv_dicts()    

    tables = get_tables(csv_segment, pdef, units)
    for t in tables:
        print(t, "\n")
    
    # add splitters    
    # emit data from blocks
    # check control values