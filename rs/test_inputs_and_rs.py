def setup_module(module):
    write_temp_files()

def teardown_module(module):
    remove_temp_files()

# ------------- constants 
     
fn1 = 'spec1.txt' 
fn2 = 'spec2.txt' 
tempfile ='temp.txt'

A1 = 'Header line1'
A2 = 'more text'
LINE_1 = A1 + '\t' + A2

CSV_TXT = """{}
2014\t2065
в процентах
2014\t100,3""" .format(LINE_1) 

SPEC_TXT = """start line: {0}
end line: null  
special reader: null   
---
"в процентах" : rog
---
{0}: 
 - VARNAME
 - usd""".format(A1)

CFG_TXT =  """- {0}
- {1}""".format(fn1, fn2)

def write_temp_files():
    """Write files for input testing."""
    # TODO: now writes dirty to os.get_cwd()
    a = File(RESERVED_FILENAMES['csv'] ).save_text(CSV_TXT)
    b = File(RESERVED_FILENAMES['cfg'] ).save_text(CFG_TXT)
    c = File(fn1                       ).save_text(SPEC_TXT)
    d = File(fn2                       ).save_text(SPEC_TXT)
    e = File(tempfile                  ).save_text("")
    return [a, b, c, d, e] 
    
def remove_temp_files():
    """Delete input testing files."""
    for fn in write_temp_files():
       os.remove(fn.filename) 

# ------------- tests  

def test_File():
    # NOTE: works unless last line is \n 
    testline = """123\n\n456"""      
    assert testline == File(tempfile).save_text(testline).read_text()

def test_YAML():        
    txt = """a: 1\nb: 2\n---\n ddd"""
    file = File(tempfile).save_text(txt).filename
    assert YAML(txt).content == YAML(file).content
    assert YAML(txt).content == [{'a': 1, 'b': 2}, 'ddd']
        
def test_CSV():
    # NOTE: fails when \n inside list         
    test_list = [["123","456"], ["a","b"]] 
    test_string = "123\t456"+"\n"+"a\tb"
    assert test_list == CSV(test_string).rows     
     
def test_definition_components():  
    assert A1 == CSV(CSV_TXT).rows[0][0]
    assert A1 == Segment(SPEC_TXT).start_line   
    assert 2 == len(SegmentList(CFG_TXT).segments)
    assert SegmentList(CFG_TXT).segments[0] == Segment(SPEC_TXT)

def test_InputDefinition():
    assert A1 == InputDefinition(CSV_TXT, CFG_TXT).segments[0].start_line 
    # read as variables + read from file and compare
    def1 = InputDefinition(CSV_TXT, CFG_TXT)
    # WARNING: dirty path
    def2 = InputDefinition(os.getcwd())
    assert def1 == def2  
