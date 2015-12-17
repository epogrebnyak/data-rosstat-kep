
from kep.importer.parser.label_csv import raw_to_labelled_rows
from kep.importer.parser.stream import stream_flat_data
from kep.database.db import stream_to_database
from kep.database.db import wipe_db_tables
from kep.query.save import get_dfs

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

FLAT_ROW_INVESTMENT = [('a', 'I_bln_rub', 2014, -1, -1, 13527.7), ('q', 'I_bln_rub', 2014, 1, -1, 1863.8), ('q', 'I_bln_rub', 2014, 2, -1, 2942.0), ('q', 'I_bln_rub', 2014, 3, -1, 3447.6), ('q', 'I_bln_rub', 2014, 4, -1, 5274.3), ('m', 'I_bln_rub', 2014, -1, 1, 492.2), ('m', 'I_bln_rub', 2014, -1, 2, 643.2), ('m', 'I_bln_rub', 2014, -1, 3, 728.4), ('m', 'I_bln_rub', 2014, -1, 4, 770.4), ('m', 'I_bln_rub', 2014, -1, 5, 991.1), ('m', 'I_bln_rub', 2014, -1, 6, 1180.5), ('m', 'I_bln_rub', 2014, -1, 7, 1075.1), ('m', 'I_bln_rub', 2014, -1, 8, 1168.5), ('m', 'I_bln_rub', 2014, -1, 9, 1204.0), ('m', 'I_bln_rub', 2014, -1, 10, 1468.5), ('m', 'I_bln_rub', 2014, -1, 11, 1372.5), ('m', 'I_bln_rub', 2014, -1, 12, 2433.3), ('a', 'I_yoy', 2014, -1, -1, 97.3), ('q', 'I_yoy', 2014, 1, -1, 94.7), ('q', 'I_yoy', 2014, 2, -1, 98.1), ('q', 'I_yoy', 2014, 3, -1, 98.5), ('q', 'I_yoy', 2014, 4, -1, 97.2), ('m', 'I_yoy', 2014, -1, 1, 92.7), ('m', 'I_yoy', 2014, -1, 2, 95.5), ('m', 'I_yoy', 2014, -1, 3, 95.3), ('m', 'I_yoy', 2014, -1, 4, 97.4), ('m', 'I_yoy', 2014, -1, 5, 97.3), ('m', 'I_yoy', 2014, -1, 6, 99.3), ('m', 'I_yoy', 2014, -1, 7, 99.1), ('m', 'I_yoy', 2014, -1, 8, 98.4), ('m', 'I_yoy', 2014, -1, 9, 98.1), ('m', 'I_yoy', 2014, -1, 10, 99.2), ('m', 'I_yoy', 2014, -1, 11, 92.2), ('m', 'I_yoy', 2014, -1, 12, 98.9), ('q', 'I_rog', 2014, 1, -1, 35.7), ('q', 'I_rog', 2014, 2, -1, 158.2), ('q', 'I_rog', 2014, 3, -1, 114.9), ('q', 'I_rog', 2014, 4, -1, 149.9), ('m', 'I_rog', 2014, -1, 1, 21.1), ('m', 'I_rog', 2014, -1, 2, 129.6), ('m', 'I_rog', 2014, -1, 3, 114.5), ('m', 'I_rog', 2014, -1, 4, 106.6), ('m', 'I_rog', 2014, -1, 5, 127.0), ('m', 'I_rog', 2014, -1, 6, 119.0), ('m', 'I_rog', 2014, -1, 7, 90.5), ('m', 'I_rog', 2014, -1, 8, 107.1), ('m', 'I_rog', 2014, -1, 9, 103.3), ('m', 'I_rog', 2014, -1, 10, 121.6), ('m', 'I_rog', 2014, -1, 11, 92.7), ('m', 'I_rog', 2014, -1, 12, 173.8)]

# todo 1: add expected results as pandas dataframes
# these results are as retruned by '''dfa, dfq, dfm = get_dataframes()''' - see below
REF_DFA = None
REF_DFQ = None
REF_DFM = None

# -------------------- 
# data processing jobs 

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
    lab_rows = get_labelled_rows()
    return list(stream_flat_data(lab_rows))

def populate_database():
    # WARNING: kills existing database data!!!
    wipe_db_tables()
    db_rows = get_flat_rows()
    stream_to_database(db_rows)

def get_dataframes():
    populate_database()
    return get_dfs()   
    
# -------------------- 
# assertions
          
def test_raw_to_labelled_rows():
    assert get_labelled_rows() == PARSED_INVESTMENT  
    
def test_flat_rows():
    assert get_flat_rows() == FLAT_ROW_INVESTMENT
    
def test_dataframes():
    dfa, dfq, dfm = get_dataframes()
    # todo 2: change comaprison method - will need to compare as dataframes 
    assert dfa == REF_DFA
    assert dfq == REF_DFQ
    assert dfm == REF_DFM

if __name__ == "__main__":
    dfa, dfq, dfm = get_dataframes() 
    #test_dataframes()