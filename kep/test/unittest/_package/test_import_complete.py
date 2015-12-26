from unittest import TestCase

from kep.inspection.var_check import get_varnames_not_in_db, get_complete_dicts
from kep.importer.csv2db import import_csv
from kep.paths import CURRENT_MONTH_DATA_FOLDER

# NOTE: get_complete_dicts() may be a part of file_io.specification
class TestImportComplete(TestCase):

    def test_get_complete_dicts(self):
        hdr, unit = get_complete_dicts(CURRENT_MONTH_DATA_FOLDER)
        self.assertTrue('CPI_FOOD' in [z[0] for z in hdr.values()])

    def test_import_complete(self):
        # TODO: add config file to import 'PROFIT'
        import_csv(CURRENT_MONTH_DATA_FOLDER, kill_existing_data = True)
        self.assertEqual(len(get_varnames_not_in_db(CURRENT_MONTH_DATA_FOLDER)), 1)
        self.assertEqual(get_varnames_not_in_db(CURRENT_MONTH_DATA_FOLDER), ["PROFIT"])
