"""test_mwe.py is minimum working example, end-to-end test that parses raw test string (INVESTMENT_DOC), similar to ones in project data CSV files, using specification format defined by two dictionaraies (REF_HEADER_DICT, REF_UNIT_DICT) to obtain parsed labelled rows (INVESTMENT_PARSED), flat database rows (INVESTMENT_FLAT_ROW), and later  annual, quarterly and monthly pandas dataframes (REF_DFA, REF_DFQ, REF_DFM). These dataframes are the resulting ouput of data import and retrieval, they are further used in economic modelling.

Test varieties are based on complexity of data imported and parsed. test_mwe.py is the simplest test example. It uses hardcoded variables and applies one markup specification for entire raw data string. Other tests will differ in following ways:
- test inputs can be hardcoded variables or files containing data (csv) or specification (yaml); 
- raw data file my be read in segments with own markup for each segment.

Note: for tests A2, B2, C2 can also do testing loaders that check if variables are read in a proper way from data (csv) or specification (yaml) files.

The end-to-end testing unverse is described in table below. Real-world application is C2.  

      test group: | A               | B                 | C                |                 
 testing options: | core algorithm  | + many variables  | + segments       |
            file: | test_mwe.py     | *.py              | *.py             |   
  # of variables: | 1               |               1+                     |
# of time series: | 3               |               3+                     |

inputs and test ids:
-- test as vars -- 
         test id: | A1 <DONE>       | B1 <TODO>          | C1  <TODO>      |
     data source: | text string     |           long text string           | 
   specification: | 2 dictionaries  | 2 dicts, more keys | list, each element is (segment boundaries, 2 dictionaries)  
 
-- test as files --
                  | A2 <TODO>       | B2 <TODO>          | C2 <TODO>       |
     data source: | short csv file  |           longer csv file            | 
   specification: | short spec file | long spec file     | main spec + supplementary specs + config file |
     config file: | no              | no                 | yes             | 

         outputs: 
   - parsed rows: | always a list of lists
     - flat rows: | always a list of tuples
    - dataframes: | 3 dataframes

"""
import pytest
import os
from pandas.core.frame import DataFrame

# testable functions - variables
from kep.importer.parser.label_csv import raw_to_labelled_rows
from kep.importer.parser.stream import stream_flat_data
from kep.database.db import stream_to_database # not tested, just used to import data to sqlite 
from kep.query.save import get_dfs

# testable fucntions - input from files 
from kep.database.db import wipe_db_tables # also not tested
from kep.file_io.common import yield_csv_rows
from kep.file_io.specification import load_spec, load_cfg
from kep.importer.csv2db import to_database
from kep.importer.parser.label_csv import get_labelled_rows

# input and output during test
from kep.file_io.common import docstring_to_file

# data processing - read string as csv input
def doc_as_iterable(doc):
    for row in doc.split("\n"):
         yield row.split("\t")

# VARIABLES(CONSTANTS) USED IN TESTING

# inputs

INVESTMENT_DOC= """1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles																	
2014	13527,7	1863,8	2942,0	3447,6	5274,3	492,2	643,2	728,4	770,4	991,1	1180,5	1075,1	1168,5	1204,0	1468,5	1372,5	2433,3
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2014	97,3	94,7	98,1	98,5	97,2	92,7	95,5	95,3	97,4	97,3	99,3	99,1	98,4	98,1	99,2	92,2	98,9
в % к предыдущему периоду  / percent of previous period																	
2014		35,7	158,2	114,9	149,9	21,1	129,6	114,5	106,6	127,0	119,0	90,5	107,1	103,3	121,6	92,7	173,8"""

DOC_YAML_SPECIFICATION = """# Раздел 1. Специальная/дополнительная информация 
# Section 1. Auxillary information 
RUR_USD : read13

---
# Раздел 2. Единицы измерении
# Section 2. Units of measurement

в % к предыдущему периоду': 'rog' 
в % к соответствующему периоду предыдущего года': 'yoy'

---
# Раздел 3. Определения переменных
# Section 3. Variable definitions
# 
# Формат:
# Часть названия таблицы :
# - VAR_LABEL # sample label
# - bln_rub # sample units

#1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles

Инвестиции в основной капитал : 
 - I
 - bln_rub
"""

REF_HEADER_DICT = {'Инвестиции в основной капитал': ['I', 'bln_rub']}
REF_UNIT_DICT = {'в % к предыдущему периоду': 'rog', 
'в % к соответствующему периоду предыдущего года': 'yoy'}

# results (intermediate and final)

INVESTMENT_PARSED = [
 ['I', 'bln_rub', '2014', '13527,7', '1863,8', '2942,0', '3447,6', '5274,3', '492,2', '643,2', '728,4', '770,4', '991,1', '1180,5', '1075,1', '1168,5', '1204,0', '1468,5', '1372,5', '2433,3']
,['I', 'yoy', '2014', '97,3', '94,7', '98,1', '98,5', '97,2', '92,7', '95,5', '95,3', '97,4', '97,3', '99,3', '99,1', '98,4', '98,1', '99,2', '92,2', '98,9']
,['I', 'rog', '2014', '', '35,7', '158,2', '114,9', '149,9', '21,1', '129,6', '114,5', '106,6', '127,0', '119,0', '90,5', '107,1', '103,3', '121,6', '92,7', '173,8']
]

INVESTMENT_FLAT_ROW = [('a', 'I_bln_rub', 2014, -1, -1, 13527.7), ('q', 'I_bln_rub', 2014, 1, -1, 1863.8), ('q', 'I_bln_rub', 2014, 2, -1, 2942.0), ('q', 'I_bln_rub', 2014, 3, -1, 3447.6), ('q', 'I_bln_rub', 2014, 4, -1, 5274.3), ('m', 'I_bln_rub', 2014, -1, 1, 492.2), ('m', 'I_bln_rub', 2014, -1, 2, 643.2), ('m', 'I_bln_rub', 2014, -1, 3, 728.4), ('m', 'I_bln_rub', 2014, -1, 4, 770.4), ('m', 'I_bln_rub', 2014, -1, 5, 991.1), ('m', 'I_bln_rub', 2014, -1, 6, 1180.5), ('m', 'I_bln_rub', 2014, -1, 7, 1075.1), ('m', 'I_bln_rub', 2014, -1, 8, 1168.5), ('m', 'I_bln_rub', 2014, -1, 9, 1204.0), ('m', 'I_bln_rub', 2014, -1, 10, 1468.5), ('m', 'I_bln_rub', 2014, -1, 11, 1372.5), ('m', 'I_bln_rub', 2014, -1, 12, 2433.3), ('a', 'I_yoy', 2014, -1, -1, 97.3), ('q', 'I_yoy', 2014, 1, -1, 94.7), ('q', 'I_yoy', 2014, 2, -1, 98.1), ('q', 'I_yoy', 2014, 3, -1, 98.5), ('q', 'I_yoy', 2014, 4, -1, 97.2), ('m', 'I_yoy', 2014, -1, 1, 92.7), ('m', 'I_yoy', 2014, -1, 2, 95.5), ('m', 'I_yoy', 2014, -1, 3, 95.3), ('m', 'I_yoy', 2014, -1, 4, 97.4), ('m', 'I_yoy', 2014, -1, 5, 97.3), ('m', 'I_yoy', 2014, -1, 6, 99.3), ('m', 'I_yoy', 2014, -1, 7, 99.1), ('m', 'I_yoy', 2014, -1, 8, 98.4), ('m', 'I_yoy', 2014, -1, 9, 98.1), ('m', 'I_yoy', 2014, -1, 10, 99.2), ('m', 'I_yoy', 2014, -1, 11, 92.2), ('m', 'I_yoy', 2014, -1, 12, 98.9), ('q', 'I_rog', 2014, 1, -1, 35.7), ('q', 'I_rog', 2014, 2, -1, 158.2), ('q', 'I_rog', 2014, 3, -1, 114.9), ('q', 'I_rog', 2014, 4, -1, 149.9), ('m', 'I_rog', 2014, -1, 1, 21.1), ('m', 'I_rog', 2014, -1, 2, 129.6), ('m', 'I_rog', 2014, -1, 3, 114.5), ('m', 'I_rog', 2014, -1, 4, 106.6), ('m', 'I_rog', 2014, -1, 5, 127.0), ('m', 'I_rog', 2014, -1, 6, 119.0), ('m', 'I_rog', 2014, -1, 7, 90.5), ('m', 'I_rog', 2014, -1, 8, 107.1), ('m', 'I_rog', 2014, -1, 9, 103.3), ('m', 'I_rog', 2014, -1, 10, 121.6), ('m', 'I_rog', 2014, -1, 11, 92.7), ('m', 'I_rog', 2014, -1, 12, 173.8)]

# Expected pandas DataFrame in to_csv() form
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


# A1. TESTING CORE ALGORITHM 

def check_final_dataframes():
    # Note: this function is used twice in this file
    
    # generate dataframes
    dfa, dfq, dfm = get_dfs()
    # check pandas DataFrame class type
    assert isinstance(dfa, DataFrame)
    assert isinstance(dfq, DataFrame)
    assert isinstance(dfm, DataFrame)
    # check dataframe contents
    assert dfa.to_csv() == REF_DFA
    assert dfq.to_csv() == REF_DFQ
    assert dfm.to_csv() == REF_DFM

def test_dataframes():
    # setup test data
    wipe_db_tables()  # WARNING: kills existing database data
    labelled_rows = raw_to_labelled_rows(raw_rows=doc_as_iterable(INVESTMENT_DOC), spec_dicts=(REF_HEADER_DICT, REF_UNIT_DICT))
    assert labelled_rows == INVESTMENT_PARSED
    flat_rows = list(stream_flat_data(labelled_rows))
    assert flat_rows == INVESTMENT_FLAT_ROW
    stream_to_database(flat_rows)
    # check user-end output
    check_final_dataframes()

# A2. TESTING CORE ALGORITHM WITH FILE INTERFACE

# write INVESTMENT_DOC to temp file as fixture + read from this file + compare iterables (raw rows)

def csvfile():
    filename = "testable_csv.txt"
    string = INVESTMENT_DOC
    return docstring_to_file(string, filename)

def test_raw_data_import_from_csv_file():
    csvpath = csvfile()
    raw_rows = list(yield_csv_rows(csv_filename=csvpath))
    for i_raw_rows, j_investment_doc in zip(raw_rows, doc_as_iterable(INVESTMENT_DOC)):
        assert i_raw_rows == j_investment_doc
    os.remove(csvpath)

# make specfile text for REF* dictionaries + write to temp file as fixture + test import of this spec file
def specfile():
    filename = "testable_spec.txt"
    string = DOC_YAML_SPECIFICATION
    return docstring_to_file(string, filename)

def file_cleanup():
    os.remove(csvfile())
    os.remove(specfile())

def test_specification_import_from_yaml_file():
    specpath = specfile()
    header_dict, unit_dict = load_spec(filename = specpath)
    assert header_dict == REF_HEADER_DICT
    assert unit_dict == REF_UNIT_DICT
    os.remove(specpath)

# run functions get labelled rows form data file and specfile + assert labelled rows are the same
def test_lab_rows_obtained_from_files():
    lab_rows = get_labelled_rows(raw_data_file=csvfile(), spec_file=specfile(), cfg_file=None)
    assert lab_rows == INVESTMENT_PARSED
    file_cleanup()

# test dataframes obtained from temp data file and temp specfile are equal to refrence dataframes
def test_dataframes_obtained_from_files(): 
    to_database(raw_data_file=csvfile(), spec_file=specfile())
    check_final_dataframes()
    file_cleanup()

# not todo: test update(testfolder), obtain testfolder from path using os.path.split
# End of test A2 ------------------------------------------------------------------

# later in testing:
# several variables + one segment
# several variables + several segments
# cfg -> full specification 
# actual files

# may change in project - something I do not like:
#   explicit names for default data and specfiles
#   format of specfile (no first yaml document)
#   use different sqlite files for testing and 'production'
#   segment may not end with file end
#   different parsing functions for whole file and segments - better use one
#   move csv2db to importer. - one level up
#   find where full import of specification is located, move to 
#   wipe_db_tables() not tested but very sensitive when using cache

if __name__ == "__main__":
    test_dataframes()
