import os

from preclasses import RESERVED_FILENAMES, File, YAML, CSV, Segment, SegmentList, InputDefinition

fn1 = 'add_spec1.txt' 
fn2 = 'add_spec2.txt' 
temp = "temp.txt"

LINE_1 = 'line1 more text'
CSV_TXT =  "{}\n line2 \t even more text".format(LINE_1) 
SPEC_TXT = "start line: {}    \nend line: 5. line2  \nspecial reader: null   \n---\n  u : 1  \n---\n  h : 2".format(LINE_1)
CFG_TXT =  "- {0}\n- {1}".format(fn1, fn2)

def setup_module(module):
    """Write files for input testing."""
    File(RESERVED_FILENAMES['csv'] ).save_text(CSV_TXT)
    File(RESERVED_FILENAMES['spec']).save_text(SPEC_TXT)
    File(RESERVED_FILENAMES['cfg'] ).save_text(CFG_TXT)
    File(fn1                       ).save_text(SPEC_TXT)
    File(fn2                       ).save_text(SPEC_TXT) 

def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    for fn in [fn1, fn2, temp] + [RESERVED_FILENAMES[key] for key in ['csv', 'spec', 'cfg']]:
       os.remove(fn)

def test_definition_components():  
    assert LINE_1 == CSV(CSV_TXT).rows[0]
    assert LINE_1 == Segment(SPEC_TXT).start_line   
    assert 2 == len(SegmentList(CFG_TXT).segments)
    assert SegmentList(CFG_TXT).segments[0] == Segment(SPEC_TXT)

def test_InputDefinition():
    assert LINE_1 == InputDefinition(CSV_TXT, SPEC_TXT).default_spec.start_line    
    assert LINE_1 == InputDefinition(CSV_TXT, SPEC_TXT, CFG_TXT).segments[0].start_line 
    # read as variables + read from file and compare
    def1 = InputDefinition(CSV_TXT, SPEC_TXT, CFG_TXT)
    def2 = InputDefinition(os.path.dirname(os.path.realpath(__file__)))
    assert def1 == def2
  
def test_File():
    # NOTE: works unless last line is \n 
    testline = """123\n\n456"""      
    assert testline == File(File('temp.txt').save_text(testline)).read_text()

def test_YAML():        
    txt = """a: 1\nb: 2\n---\n ddd"""
    file = File(temp).save_text(txt)
    assert YAML(txt).content == YAML(file).content
        
def test_CSV():        
    test_list = ["123","456"] # NOTE: fails when \n inside list 
    test_string = "\n".join(test_list)
    assert test_list == CSV(test_string).rows 

# ----------------------------------------------------------------------------------
# Validate config files TODO`     
def untest_cfg_import():
    write_spec_files()
    cfg = write_cfg()    
    assert SegmentList(cfg).segments == cfg_list    
    
def cmp_spec(doc,var):
    cnt = Segment(doc)._as_load_spec 
    #import pdb; pdb.set_trace()
    assert var == cnt
            
from testdata import spec_ip_doc, spec_ip_trans_inv_doc, spec_cpi_block, spec_food_block, header_dicts, common_unit_dict, unit_dicts, null_segment_dict, cpi_segment_dict,  food_segment_dict
from testdata import join_header_dicts
def test_spec():
    cmp_spec(doc=spec_ip_doc, var=(header_dicts['ip'], unit_dicts['ip'], null_segment_dict))
    
    cmp_spec(doc=spec_ip_trans_inv_doc, 
             var=(join_header_dicts(['ip','trans','investment']),
                  common_unit_dict, null_segment_dict))
                  
    cmp_spec(doc=spec_cpi_block, 
             var=(header_dicts['cpi_block'], unit_dicts['cpi_block'], cpi_segment_dict))

    cmp_spec(doc=spec_food_block, 
             var=(header_dicts['food_block'], unit_dicts['food_block'], food_segment_dict))
