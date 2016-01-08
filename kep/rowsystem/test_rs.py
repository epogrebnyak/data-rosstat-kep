import pandas as pd
from pprint import pprint

# --- hardcoded constrants for testing ---
# 1. csv input
predoc = ["1. Gross domestic product at current prices", "billion ruble",
          "\tYEAR\tVALUE", "2013\t61500", "2014\t64000",
          "percent change from previous year - annual basis", "2013\t1.013", "2014\t1.028"]
CSV_DOC = "\n".join(predoc)

# 2. markup dictionaries 
header_dict = {"Gross domestic product": ["GDP", "bln_rub"]}
unit_dict =   {'billion ruble'                   : 'bln_rub',
               'percent change from previous year' : 'yoy'}
special_reader = None
SPEC1 = header_dict, unit_dict, special_reader

# 3. labelled rowsystem
LABELLED_RS = [
       {'string':"1. Gross domestic product at current prices",
          'list':["1. Gross domestic product at current prices"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
        
        {'string':"billion ruble",
          'list':["billion ruble"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},          
        
        {'string':"\tYEAR\tVALUE",
          'list':["", "YEAR", "VALUE"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
          
        {'string':"2013\t61500",
          'list':["2013", "61500"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
                    
        {'string':"2014\t64000",
          'list':["2014", "64000"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
          
         {'string': "percent change from previous year - annual basis",
          'list': ["percent change from previous year - annual basis"],
          'head_label': 'GDP',
          'unit_label': 'yoy',
          'spec': SPEC1},
          
        {'string':"2013\t1.013",
          'list':["2013", "1.013"],
          'head_label':'GDP',
          'unit_label':'yoy',
          'spec': SPEC1},

        {'string':"2014\t1.028",
          'list':["2014", "1.028"],
          'head_label':'GDP',
          'unit_label':'yoy',
          'spec': SPEC1}         
]

# resulting dataframe
DFA = pd.DataFrame.from_items([
                                 ('GDP_bln_rub', [61500.0, 64000.0])
                                ,('GDP_yoy', [1.013, 1.028])
                                 ])             
DFA.index = [2013,2014]                             

segment_info_dict = {
  'start line' : None,
  'end line' : None,
  'special reader': 'read_special'}

# --- testing ---
from rowsystem import doc_to_rowsystem, label_rowsystem, get_annual_df

def test_overall():
    rs1 = doc_to_rowsystem(CSV_DOC)
    rs2 = label_rowsystem(rs1, SPEC1)
    
    try:
        assert rs2 == LABELLED_RS
    except:
        for i in range(len(rs2)):
           print(i, rs2[i] == LABELLED_RS[i])
    
    df = get_annual_df(rs2)
    # MAYDO: lousy comaprison 
    assert 'year'+DFA.to_csv() == df.to_csv()

test_overall()

def emit_rowheads_for_segmentation(rs):
    for i, row in enumerate(rs):
        # if not row['list']:
        #     pass
        # if len(row['list']) == 0:
        #    # TODO: add zero-length row string for testing 
        #    pass
        # elif not row['list'][0]:
        #    pass
        try:
            head = row['list'][0]
            if head:
                yield i, head              
        except:
            pass

RS_SEG_TEST = [{'list':['string1 + more text'],      'spec': None}
             , {'list':[''],                         'spec': None}
             , {'list':[None],                       'spec': None}
             , {'list':None,                         'spec': None}
             , {'list':[],                           'spec': None}
             , {'list':['string2 + even more text'], 'spec': None}
             , {'list':['string3 with some text'],   'spec': None}
             , {'list':['string4 and that is it'],   'spec': None}
             ]

RS_SEG_TEST_OUTPUT = [{'list': ['string1 + more text'], 'spec': 1},
 {'list': [''], 'spec': None},
 {'list': [None], 'spec': None},
 {'list': None, 'spec': None},
 {'list': [], 'spec': None},
 {'list': ['string2 + even more text'], 'spec': 0},
 {'list': ['string3 with some text'], 'spec': 2},
 {'list': ['string4 and that is it'], 'spec': 3}]

SEG_SPEC1S_TEST = [('string1 + more text',   'string2 + even more text', 1)
                 ,('string3 with some text', 'string4 and that is it',  2)
                 ,('string4 and that is it', None,                      3)]

DEFAULT_DICTS = 0 

def assign_parsing_specification_by_row(rs, default_spec, segment_specs):
    
    def is_matched(head, line):
        if line:
            return head.startswith(line)
        else:
            return False           
            
    in_segment = False
    current_end_line = None
    current_spec = default_spec
    for i, head in emit_rowheads_for_segmentation(rs):
        # are we in the default spec?
        if not in_segment:
            # do we have to switch to a custom spec?
            for start_line, end_line, seg_spec in segment_specs:
                if is_matched(head,start_line):
                    # Yes!
                    in_segment = True
                    current_spec = seg_spec
                    current_end_line = end_line
                    break
        else:
            # we are in custom spec. do we have to switch to the default spec? 
            if is_matched(head,current_end_line):
                in_segment = False
                current_spec = default_spec
                current_end_line = None                
                
            # ... or do we have to switch to a new custom one?                  
            for start_line, end_line, seg_spec in segment_specs:
                if is_matched(head,start_line):
                    # Yes!
                    in_segment = True
                    current_spec = seg_spec
                    current_end_line = end_line
                    break
                
        #finished adjusting specification for i-th row 
        rs[i]['spec'] = current_spec
    return rs

assert RS_SEG_TEST_OUTPUT == assign_parsing_specification_by_row(RS_SEG_TEST, DEFAULT_DICTS, SEG_SPEC1S_TEST)


