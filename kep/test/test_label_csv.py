import os

from kep.file_io.common import delete_file
from kep.file_io.specification import load_spec, load_cfg
from kep.importer.parser.label_csv import get_labelled_rows

from kep.test.hardcoded import pass_csv_and_data, pass_spec_and_data, pass_cfg_and_data


# TODO: lots of copypaste here, should use test class or something

def get_test_labelled_rows():
    raw_data_file, data_as_list = pass_csv_and_data()
    spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
    cfg_file, ref_cfg_list = pass_cfg_and_data()
    return get_labelled_rows(raw_data_file, spec_file, cfg_file)

def test_import():
    raw_data_file, data_as_list = pass_csv_and_data()
    spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
    cfg_file, ref_cfg_list = pass_cfg_and_data()
    assert os.path.exists(raw_data_file)
    assert os.path.exists(spec_file)
    assert os.path.exists(cfg_file)

# testing with spec only   ------------------------- 
def test_specs():
    spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
    header_dict, unit_dict = load_spec(spec_file)
    assert header_dict == ref_header_dict
    assert unit_dict == ref_unit_dict

def test_label_csv1():
    raw_data_file, data_as_list = pass_csv_and_data()
    spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file)

# testing with spec and cfg -----------------------     
def test_segment_specs():
    cfg_file, ref_cfg_list = pass_cfg_and_data()
    assert ref_cfg_list == load_cfg(cfg_file)

def test_label_csv2():
    raw_data_file, data_as_list = pass_csv_and_data()
    spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
    cfg_file, ref_cfg_list = pass_cfg_and_data()
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file, cfg_file)
    
# TODO: this should be a last call, but not a test, using test_*() function is a stub. 
#       If left plainly in code it is executed before fucntions are called and files are deleted before tests are run.
def test_cleanup():
    raw_data_file, data_as_list = pass_csv_and_data()
    spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
    cfg_file, ref_cfg_list = pass_cfg_and_data()
    for f in (raw_data_file, spec_file, cfg_file):
       delete_file(f)
    assert True