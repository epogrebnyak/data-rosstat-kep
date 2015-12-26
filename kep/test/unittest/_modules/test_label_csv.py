import os
from unittest import TestCase

from kep.file_io.specification import load_spec, load_cfg
from kep.importer.parser.label_csv import get_labelled_rows
from kep.test.unittest.conftest import raw_data_file, spec_file, cfg_file, ref_unit_dict, ref_header_dict, ref_cfg_list, data_as_list


class TestLabelCsv(TestCase):

    def test_import(self):
        self.assertTrue(os.path.exists(raw_data_file()))
        self.assertTrue(os.path.exists(spec_file()))
        self.assertTrue(os.path.exists(cfg_file()))

    # testing with spec only   -------------------------
    def test_specs(self):
        header_dict, unit_dict = load_spec(spec_file())
        self.assertEqual(header_dict, ref_header_dict())
        self.assertEqual(unit_dict, ref_unit_dict())

    def test_label_csv1(self):
        self.assertEqual(data_as_list(), get_labelled_rows(raw_data_file(), spec_file()))

    # testing with spec and cfg -----------------------
    def test_segment_specs(self):
        self.assertEqual(ref_cfg_list(), load_cfg(cfg_file()))

    def test_label_csv2(self):
        self.assertEqual(data_as_list(), get_labelled_rows(raw_data_file(), spec_file(), cfg_file()))
