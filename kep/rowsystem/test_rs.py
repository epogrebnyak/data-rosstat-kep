import pandas as pd
from pprint import pprint



# --- hardcoded constrants for testing ---
# 1. csv input
predoc = ["1. Gross domestic product at current prices", "billion ruble",
          "\tYEAR\tVALUE", "2013\t61500", "2014\t64000",
          "percent change from previous year - annual basis", "2013\t1.013", "2014\t1.028"]
CSV_DOC = "\n".join(predoc)

# 2.1 specification = markup dictionaries and reader function
header_dict = {"Gross domestic product": ["GDP", "bln_rub"]}
unit_dict = {'billion ruble':'bln_rub',
             'percent change from previous year':'yoy'}
special_reader = {'reader': None}

# 2.2 specs


SPEC1 = header_dict, unit_dict, {'reader': None}
SPEC2 = header_dict, unit_dict, {'reader': 'read_special'}

#************** TODO **************
# make spec and cfg file for this, improt them

# already used, see below:

segment_info_dict = {
      'start line' : 'percent change',
      'end line' : None,
      'special reader': 'read_special'}

#_________________________________________________


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
          'spec': None},
          
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

LABELLED_WITH_SEGMENTS = [{'head_label': 'GDP',
  'list': ['1. Gross domestic product at current prices'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'reader': None}),
  'string': '1. Gross domestic product at current prices',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['billion ruble'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'reader': None}),
  'string': 'billion ruble',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['', 'YEAR', 'VALUE'],
  'spec': None,
  'string': '\tYEAR\tVALUE',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['2013', '61500'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'reader': None}),
  'string': '2013\t61500',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['2014', '64000'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'reader': None}),
  'string': '2014\t64000',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['percent change from previous year - annual basis'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'reader': 'read_special'}),
  'string': 'percent change from previous year - annual basis',
  'unit_label': 'yoy'},
 {'head_label': 'GDP',
  'list': ['2013', '1.013'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'reader': 'read_special'}),
  'string': '2013\t1.013',
  'unit_label': 'yoy'},
 {'head_label': 'GDP',
  'list': ['2014', '1.028'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'reader': 'read_special'}),
  'string': '2014\t1.028',
  'unit_label': 'yoy'}]


# resulting dataframe
DFA = pd.DataFrame.from_items([
                                 ('GDP_bln_rub', [61500.0, 64000.0])
                                ,('GDP_yoy', [1.013, 1.028])
                                 ])             
DFA.index = [2013,2014]                             




# --- testing ---
from rowsystem import doc_to_rowsystem, label_rowsystem, get_annual_df
from spec_io import write_file

def _comp(rs):
    try:
        assert rs == LABELLED_RS
    except:
        for i in range(len(rs)):
           print(i, rs[i] == LABELLED_RS[i])

def test_file_csv_import():    
    csvfile = write_file("_csv.txt", CSV_DOC) 
    rs = doc_to_rowsystem(csvfile)
    rs = label_rowsystem(rs, SPEC1)
    #print("File import")
    _comp(rs)
    
def test_param_import():    
    default_spec = load_spec(spec_filename)
    segments = load_segments(cfg_filename)    

def test_overall():
    rs1 = doc_to_rowsystem(CSV_DOC)
    rs2 = label_rowsystem(rs1, SPEC1)    
    _comp(rs2)    
    df = get_annual_df(rs2)
    # MAYDO: lousy comparison 
    assert 'year'+DFA.to_csv() == df.to_csv()

def test_with_segments():
    SEG = [('percent change', None, SPEC2)]
    rs1 = doc_to_rowsystem(CSV_DOC)
    assert LABELLED_WITH_SEGMENTS == label_rowsystem(rs1, SPEC1, SEG)

test_overall()
test_file_csv_import()
test_with_segments()

#-------------------------------------------------------------------------------------

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

SEG_SPEC_TEST = [('string1 + more text',   'string2 + even more text', 1)
                 ,('string3 with some text', 'string4 and that is it',  2)
                 ,('string4 and that is it', None,                      3)]

DEFAULT_DICTS = 0 

from rowsystem import assign_parsing_specification_by_row
assert RS_SEG_TEST_OUTPUT == assign_parsing_specification_by_row(RS_SEG_TEST, DEFAULT_DICTS, SEG_SPEC_TEST)

#-------------------------------------------------------------------------------------

