"""Small example of raw data and parsing specification.

data -> write temp files (FILE_CONTENT) -> folder -> RowSystem -> values 

"""

from kep.common.inputs import TempfolderFile, CSV
from kep.config import RESERVED_FILENAMES, TESTDATA_DIR
from kep.reader.rs import Segment, SegmentsList, InputDefinition, RowSystem
from kep.extract.dataframes import DictsAsDataframes

def setup_module(module):
    write_temp_files()

def teardown_module(module):
    remove_temp_files()
    
# -------------------------------------------------------------------
#
#    Data used for min working example of end-to-end testing 
#
# -------------------------------------------------------------------


T1 = 'Main header line1, bln usd'
T2 = '(more text)'

CSV_TXT = """{}
2009\t1850
2010\t2022

\t
в процентах
2009\t99,5
2010\t100,3""" .format(T1 + '\t' + T2) 

SPEC_TXT = """start line: {0}
end line: null  
special reader: null   
---
"в процентах" : rog
---
{0}: 
 - VARNAME
 - usd
some missing header:
 - NO_VAR
 - usd""".format(T1)

fn1 = 'spec1.txt' 
fn2 = 'spec2.txt' 
CFG_TXT =  """- {0}
- {1}""".format(fn1, fn2)

tempfile ='temp.txt'

FILE_CONTENT = {
     RESERVED_FILENAMES['csv']: CSV_TXT
   , RESERVED_FILENAMES['cfg']: CFG_TXT
   , fn1                      : SPEC_TXT
   , fn2                      : SPEC_TXT
   , tempfile                 : ""}

def get_rs():
    folder = write_temp_files()  
    assert folder == TESTDATA_DIR    
    return RowSystem(folder)
   
def write_temp_files(fc = FILE_CONTENT):
    """Write files for input testing."""
    for k, v in fc.items():
        z = TempfolderFile(k).save_text(v)
    return z.folder
    
def remove_temp_files(fc = FILE_CONTENT):
    """Delete input testing files."""
    for k, v in fc.items():
        TempfolderFile(k).remove()
    
# ---------------------------------------------------------------------
#
#    Tests
#
# ---------------------------------------------------------------------
     
def test_definition_components():
    folder = write_temp_files()  
    assert T1 == CSV(CSV_TXT).rows[0][0]
    assert T1 == Segment(SPEC_TXT).start_line   
    assert 'NO_VAR' in Segment(SPEC_TXT).head_labels
    assert 'VARNAME' in Segment(SPEC_TXT).head_labels
    assert 2 == len(SegmentsList(CFG_TXT, folder).yaml_string_list)
    assert SegmentsList(CFG_TXT, folder).yaml_string_list[0] == SPEC_TXT
    assert SegmentsList(CFG_TXT, folder).yaml_string_list[1] == SPEC_TXT
    remove_temp_files()

def test_InputDefinition():
    folder = write_temp_files()
    def0 = InputDefinition(CSV_TXT, [SPEC_TXT, SPEC_TXT])
    def1 = InputDefinition(RESERVED_FILENAMES['csv'], RESERVED_FILENAMES['cfg'], folder)
    def2 = InputDefinition(CSV_TXT, CFG_TXT, folder)
    def3 = InputDefinition(folder)
    assert def0 == def1     
    assert def1 == def2
    assert def2 == def3
    # some random parameter reading from definiton
    assert T1 == def0.segments[0].start_line
    
def test_rs1():
    z = get_rs()
    assert list(z.dicts()) == \
    [{'freq': 'a', 'month': -1, 'varname': 'VARNAME_usd', 'qtr': -1, 'year': 2009, 'value': 1850.0}, 
     {'freq': 'a', 'month': -1, 'varname': 'VARNAME_usd', 'qtr': -1, 'year': 2010, 'value': 2022.0}, 
     {'freq': 'a', 'month': -1, 'varname': 'VARNAME_rog', 'qtr': -1, 'year': 2009, 'value': 99.5}, 
     {'freq': 'a', 'month': -1, 'varname': 'VARNAME_rog', 'qtr': -1, 'year': 2010, 'value': 100.3}]  
    
    assert DictsAsDataframes(z.dicts()).annual_df().to_csv() == 'year,VARNAME_rog,VARNAME_usd\n2009,99.5,1850.0\n2010,100.3,2022.0\n'

    assert z.data.annual_df().to_csv() == 'year,VARNAME_rog,VARNAME_usd\n2009,99.5,1850.0\n2010,100.3,2022.0\n'

    assert z.__len__() == {'vars': 2, 'heads': 1, 'points': 4, 'total_ts':2}

    assert z.not_imported() == ['NO_VAR']
    assert z.folder == TESTDATA_DIR
    
    assert 'VARNAME_rog' in z.varnames()
    assert 'VARNAME_usd' in z.varnames()
    assert len(z.varnames()) == 2
    
    assert z.headnames() == ['VARNAME'] 
    
    assert 'NO_VAR' in z.definition_headnames()
    assert 'VARNAME' in z.definition_headnames()
    assert len(z.definition_headnames()) == 2
    
    
if __name__ == "__main__":
    import pprint
    z = get_rs()
    print("\nRowsystem content")
    for frow in z.full_rows:
        pprint.pprint(frow)  
    test_rs1()
    
