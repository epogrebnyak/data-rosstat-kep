# --------------------------------------------------------------
# Testing functions

def print_rows(list_):
    # print("Printing list by row in compact form:")
    for row in list_:
         print(" ".join(row[0:6]) + ' ... ' + row[-1])

def test_label_csv1():
    from hardcoded import init_raw_csv_file, init_main_yaml, PARSED_RAW_FILE_AS_LIST
    raw_data_file = init_raw_csv_file()        
    SPEC_FILE = init_main_yaml()    
    labelled_rows_as_list = get_labelled_rows_no_segments(raw_data_file, SPEC_FILE)
    assert labelled_rows_as_list == PARSED_RAW_FILE_AS_LIST

def test_segment_specs():
    from hardcoded import REF_SEGMENT_SPEC, init_config_yaml
    CFG_FILE = init_config_yaml()
    segment_specs = _get_segment_specs_no_header_doc(CFG_FILE)
    assert segment_specs == REF_SEGMENT_SPEC

def test_label_csv2():
    from hardcoded import PARSED_RAW_FILE_AS_LIST
    labelled_rows = get_test_labelled_rows()
    assert PARSED_RAW_FILE_AS_LIST == labelled_rows
    
def get_test_labelled_rows():
    from hardcoded import init_config_yaml, init_raw_csv_file, init_main_yaml
    RAW_FILE = init_raw_csv_file()        
    SPEC_FILE = init_main_yaml()    
    CFG_FILE = init_config_yaml()
    return list(get_labelled_rows(RAW_FILE, spec_file = SPEC_FILE, 
                                             cfg_file = CFG_FILE))    

if __name__ == "__main__":
    test_label_csv1()
    test_segment_specs()
    test_label_csv2()   
