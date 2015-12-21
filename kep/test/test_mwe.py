from pandas.core.frame import DataFrame

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

# ------------------------------------------
# Expected pandas DataFrame in to_csv() form
# ------------------------------------------

REF_DFA = '''
year,I_bln_rub,I_yoy
2014,13527.7,97.3
'''.lstrip()

REF_DFQ = '''
time_index,I_bln_rub,I_rog,I_yoy
2014-03-31,1863.8,35.7,94.7
2014-06-30,2942.0,158.2,98.1
2014-09-30,3447.6,114.9,98.5
2014-12-31,5274.3,149.9,97.2
'''.lstrip()

REF_DFM = '''
time_index,I_bln_rub,I_rog,I_yoy
2014-01-31,492.2,21.1,92.7
2014-02-28,643.2,129.6,95.5
2014-03-31,728.4,114.5,95.3
2014-04-30,770.4,106.6,97.4
2014-05-31,991.1,127.0,97.3
2014-06-30,1180.5,119.0,99.3
2014-07-31,1075.1,90.5,99.1
2014-08-31,1168.5,107.1,98.4
2014-09-30,1204.0,103.3,98.1
2014-10-31,1468.5,121.6,99.2
2014-11-30,1372.5,92.7,92.2
2014-12-31,2433.3,173.8,98.9
'''.lstrip()

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
    # WARNING: kills existing database data
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
    # Check that it returns pandas DataFrame
    assert isinstance(dfa, DataFrame)
    assert isinstance(dfq, DataFrame)
    assert isinstance(dfm, DataFrame)
    # Check contents
    assert dfa.to_csv() == REF_DFA
    assert dfq.to_csv() == REF_DFQ
    assert dfm.to_csv() == REF_DFM

if __name__ == "__main__":
    dfa, dfq, dfm = get_dataframes() 
    #test_dataframes()