from unittest import TestCase

from kep.database.db import stream_to_database
from kep.importer.parser.stream import stream_flat_data
from kep.query.save import get_reshaped_dfs
from kep.test.unittest.conftest import get_labelled_rows, raw_data_file, spec_file, cfg_file
# using fixtures: yes (labelled_rows)
# comment: very weak test, possibly to be revised


class TestDatabase(TestCase):

    def test_database(self):
        gen = list(stream_flat_data(get_labelled_rows(raw_data_file(), spec_file(), cfg_file())))
        stream_to_database(gen)
        dfa, dfq, dfm = get_reshaped_dfs()
        self.assertEqual(dfa.loc[2014, 'I_yoy'], 97.3)
