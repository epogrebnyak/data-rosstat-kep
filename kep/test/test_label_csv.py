import os

from kep.io.common import delete_file
from kep.io.specification import load_spec, load_cfg
from kep.parser.label_csv import get_labelled_rows

from kep.test.hardcoded import pass_csv_and_data, pass_spec_and_data, pass_cfg_and_data
raw_data_file, data_as_list = pass_csv_and_data() 
spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
cfg_file, ref_cfg_list = pass_cfg_and_data()

def test_import():
    assert os.path.exists(raw_data_file)
    assert os.path.exists(spec_file)
    assert os.path.exists(cfg_file)

def test_specs():
    header_dict, unit_dict = load_spec(spec_file)
    assert header_dict == ref_header_dict
    assert unit_dict == ref_unit_dict

def test_label_csv1():
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file)
    
def test_segment_specs():
    assert ref_cfg_list == load_cfg(cfg_file)
    # from hardcoded import REF_SEGMENT_SPEC, init_config_yaml
    # CFG_FILE = init_config_yaml()
    # segment_specs = _get_segment_specs_no_header_doc(CFG_FILE)
    # assert segment_specs == REF_SEGMENT_SPEC

def test_label_csv2():
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file, cfg_file)
    
# def test_label_csv2():
    # from hardcoded import PARSED_RAW_FILE_AS_LIST
    # labelled_rows = get_test_labelled_rows()
    # assert PARSED_RAW_FILE_AS_LIST == labelled_rows
    
# def get_test_labelled_rows():
    # from hardcoded import init_config_yaml, init_raw_csv_file, init_main_yaml
    # RAW_FILE = init_raw_csv_file()        
    # SPEC_FILE = init_main_yaml()    
    # CFG_FILE = init_config_yaml()
    # return list(get_labelled_rows(RAW_FILE, spec_file = SPEC_FILE, 
                                             # cfg_file = CFG_FILE))    

# if __name__ == "__main__":
    # test_label_csv1()
    # test_segment_specs()
    # test_label_csv2()

# TODO: this should be a last call, but not a test, using test_*() function is a stub. 
#        If left in code it is executed before fucntions are called
def test_cleanup():
    for f in (raw_data_file, spec_file, cfg_file):
       delete_file(f)
    assert True
    
