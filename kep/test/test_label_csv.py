import os

from kep.file_io.specification import load_spec, load_cfg
from kep.importer.parser.label_csv import get_labelled_rows


def test_import(raw_data_file, spec_file, cfg_file):
    assert os.path.exists(raw_data_file)
    assert os.path.exists(spec_file)
    assert os.path.exists(cfg_file)

# testing with spec only   -------------------------
def test_specs(ref_header_dict, ref_unit_dict, spec_file):
    header_dict, unit_dict = load_spec(spec_file)
    assert header_dict == ref_header_dict
    assert unit_dict == ref_unit_dict

def test_label_csv1(raw_data_file, spec_file, data_as_list):
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file)

# testing with spec and cfg -----------------------     
def test_segment_specs(cfg_file, ref_cfg_list):
    assert ref_cfg_list == load_cfg(cfg_file)

def test_label_csv2(raw_data_file, spec_file, cfg_file, data_as_list):
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file, cfg_file)
