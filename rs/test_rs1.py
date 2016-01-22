"""Small example of raw data and parsing specification.

data -> write temp files (FILE_CONTENT) -> folder -> RowSystem -> values 

"""

from inputs import TempfolderFile
from config import RESERVED_FILENAMES, TESTDATA_DIR
from rs import CSV, Segment, InputDefinition, RowSystem

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
2013\t1850
2014\t2022

\t
в процентах
2013\t99,5
2014\t100,3""" .format(T1 + '\t' + T2) 

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
    
    # NOTE: os.listdir() http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python 
    
# ---------------------------------------------------------------------
#
#    Tests
#
# ---------------------------------------------------------------------
     
def test_definition_components():
    write_temp_files()  
    assert T1 == CSV(CSV_TXT).rows[0][0]
    assert T1 == Segment(SPEC_TXT).start_line   
    #assert 2 == len(SegmentList(CFG_TXT).segments)
    #assert SegmentList(CFG_TXT).segments[0] == Segment(SPEC_TXT)
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
    # some random reading from definiton
    assert T1 == def0.segments[0].start_line
    
def test_rs1():
    z = get_rs()
    assert z.data.dicts == \
    [{'freq': 'a', 'month': -1, 'varname': 'VARNAME_usd', 'qtr': -1, 'year': 2013, 'value': 1850.0}, 
     {'freq': 'a', 'month': -1, 'varname': 'VARNAME_usd', 'qtr': -1, 'year': 2014, 'value': 2022.0}, 
     {'freq': 'a', 'month': -1, 'varname': 'VARNAME_rog', 'qtr': -1, 'year': 2013, 'value': 99.5}, 
     {'freq': 'a', 'month': -1, 'varname': 'VARNAME_rog', 'qtr': -1, 'year': 2014, 'value': 100.3}]  
    assert z.data.annual_df().to_csv() == 'year,VARNAME_rog,VARNAME_usd\n2013,99.5,1850.0\n2014,100.3,2022.0\n'
    assert z.__len__() == {'n_vars': 2, 'n_heads': 1, 'n_pts': 4} 
    assert z.__repr__().startswith('\nDataset contains 1 variables, 2 timeseries and 4 data points.\nVariables (1):\n    VARNAME          \nTimeseries (2):\n   VARNAME_rog   VARNAME_usd\n')
    assert z.not_imported() == ['NO_VAR']
    assert z.folder == TESTDATA_DIR
    # may be unstable as these are dictionary keys below - my need use sets to compare content
    assert z.varnames() == ['VARNAME_rog', 'VARNAME_usd']
    assert z.headnames() == ['VARNAME'] 
    assert z.definition_headnames() == ['NO_VAR', 'VARNAME']

    
if __name__ == "__main__":
    import pprint
    z = get_rs()
    print("\nRowsystem content")
    for frow in z.full_rows:
        pprint.pprint(frow)  
    print(z)
    
