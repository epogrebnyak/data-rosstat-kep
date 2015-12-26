# kep.importer.csv2db.import_csv() logic:
# - reads specification files spec and cfg <- this is inspect_db().udf_vars 
# - labels rows read from CSV file <- need check here
# - flattens rows into stream <- need check here
# - reads stream in database <- inspect_db() checks variables here

# using fixtures: no
# comment: very weak test, possibly to be revised
# todo: change data_folder 
from unittest import TestCase

from kep.importer.parser.label_csv import get_labelled_rows
from kep.file_io.common import get_filenames
from kep.paths import DATA_FOLDER

class TestLabRows(TestCase):

    @staticmethod
    def slice_lab_rows(tag, lab_rows):
        for x in lab_rows:
            if x[0] == tag:
                yield x

    @staticmethod
    def row_exists(tag, lab_rows):
        return len([x for x in TestLabRows.slice_lab_rows(tag, lab_rows)]) > 0

    def test_lab_rows(self):
        csv, spec, cfg = get_filenames(DATA_FOLDER)
        lab_rows = get_labelled_rows(csv, spec, cfg)
        self.assertTrue(TestLabRows.row_exists('PROD_AUTO_TRUCKS_AND_CHASSIS', lab_rows))
