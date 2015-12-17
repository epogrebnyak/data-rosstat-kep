# -------------------- 
# inputs

INVESTMENT= """1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles																	
2014	13527,7	1863,8	2942,0	3447,6	5274,3	492,2	643,2	728,4	770,4	991,1	1180,5	1075,1	1168,5	1204,0	1468,5	1372,5	2433,3
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2014	97,3	94,7	98,1	98,5	97,2	92,7	95,5	95,3	97,4	97,3	99,3	99,1	98,4	98,1	99,2	92,2	98,9
в % к предыдущему периоду  / percent of previous period																	
2014		35,7	158,2	114,9	149,9	21,1	129,6	114,5	106,6	127,0	119,0	90,5	107,1	103,3	121,6	92,7	173,8"""

REF_HEADER_DICT = {'Инвестиции в основной капитал': ['I', 'bln_rub']}
REF_UNIT_DICT = {'в % к предыдущему периоду': 'rog', 
'в % к соответствующему периоду предыдущего года': 'yoy'}

# -------------------- 
# results (intermediate and final)

PARSED_INVESTMENT = [
 ['I', 'bln_rub', '2014', '13527,7', '1863,8', '2942,0', '3447,6', '5274,3', '492,2', '643,2', '728,4', '770,4', '991,1', '1180,5', '1075,1', '1168,5', '1204,0', '1468,5', '1372,5', '2433,3']
,['I', 'yoy', '2014', '97,3', '94,7', '98,1', '98,5', '97,2', '92,7', '95,5', '95,3', '97,4', '97,3', '99,3', '99,1', '98,4', '98,1', '99,2', '92,2', '98,9']
,['I', 'rog', '2014', '', '35,7', '158,2', '114,9', '149,9', '21,1', '129,6', '114,5', '106,6', '127,0', '119,0', '90,5', '107,1', '103,3', '121,6', '92,7', '173,8']
]

# todo 1: add expected results
# flat_stream_trans = []

# todo 2: add expected results
# pandas dataframes
#dfa = 
#dfq =
#dfm =

# -------------------- 
# data processing jobs 

from kep.importer.parser.label_csv import raw_to_labelled_rows

def doc_as_iterable(doc):
    for row in doc.split("\n"):
         yield row.split("\t")

def get_raw_rows():
    return doc_as_iterable(INVESTMENT)

def get_labelled_rows():
    raw_rows = get_raw_rows()
    spec_dicts = (REF_HEADER_DICT, REF_UNIT_DICT)
    return raw_to_labelled_rows(raw_rows, spec_dicts) 

def get_flat_rows():
    # todo 3
    pass   

def get_dataframes():
    # todo 4
    dfa = None
    dfq = None
    dfm = None
    return dfa, dfq, dfm        
    
# -------------------- 
# assertions
          
def test_raw_to_labelled_rows():
    assert get_labelled_rows() == PARSED_INVESTMENT  
    
def test_flat_rows():
    # todo 5:
    pass    
    
def test_dataframes():
    # todo 6:
    # note: will need to compare by element
    pass