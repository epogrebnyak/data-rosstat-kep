"""Very small example of raw data and parsing specification."""

from inputs import TempfolderFile
from config import RESERVED_FILENAMES
from rs import CSV, Segment, InputDefinition

def setup_module(module):
    write_temp_files()

def teardown_module(module):
    remove_temp_files()
    
# -------------------------------------------------------------------
#
#    Data used for min working example of end-to-end testing 
#
# -------------------------------------------------------------------
     
fn1 = 'spec1.txt' 
fn2 = 'spec2.txt' 
tempfile ='temp.txt'

T1 = 'Main header line1, bln usd'
T2 = '(more text)'

CSV_TXT = """{}
2014\t355

\t
в процентах
2014\t100,3""" .format(T1 + '\t' + T2) 

SPEC_TXT = """start line: {0}
end line: null  
special reader: null   
---
"в процентах" : rog
---
{0}: 
 - VARNAME
 - usd""".format(T1)

CFG_TXT =  """- {0}
- {1}""".format(fn1, fn2)

def write_temp_files():
    """Write files for input testing."""
    a = TempfolderFile(RESERVED_FILENAMES['csv']).save_text(CSV_TXT)
    b = TempfolderFile(RESERVED_FILENAMES['cfg']).save_text(CFG_TXT)
    c = TempfolderFile(fn1                      ).save_text(SPEC_TXT)
    d = TempfolderFile(fn2                      ).save_text(SPEC_TXT)
    e = TempfolderFile(tempfile                 ).save_text("")
    return a.folder
    
def remove_temp_files():
    """Delete input testing files."""
    pass
    # import os 
    # folder = write_temp_files()
    # for f in os.listdir(): #http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python 
       # os.remove(f)  # may do: any way to pass a list of created files to remove_temp_files() and not delete all files? (not critical)

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