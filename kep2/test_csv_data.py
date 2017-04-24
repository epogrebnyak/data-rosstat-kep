# -*- coding: utf-8 -*-
"""Test csv data import."""

import unittest
import tempfile
import os

import csv_data as cd


class TestCSV_doc_to_lists(unittest.TestCase):
    def test_doc_to_lists(self):
        assert cd.doc_to_lists("2015\t99,2\t99,9\n2016\t101,3\t101,1") == \
               [['2015', '99,2', '99,9'],
                ['2016', '101,3', '101,1']]


class TestCSV_row_as_dict(unittest.TestCase):
    def setUp(self):
        self.row = ['2013', '10', '20', '30', '40']

    def test_datarow_head_and_data(self):
        assert cd.row_as_dict(self.row)['head'] == '2013'
        assert cd.row_as_dict(self.row)['data'] == ['10', '20', '30', '40']

    def test_textrow_head(self):
        assert cd.row_as_dict(['1. Сводные показатели', '', ''])['head'] == '1. Сводные показатели'

    def test_empty_label_always_added(self):
        assert cd.row_as_dict(self.row)['label'] == {'unit': '', 'var': ''}


class Match_CSV_Content(unittest.TestCase):
    """Fixtures for string-to-variables and file-to-varibales testing."""

    def setUp(self):
        self._csv_content = """\tГод / Year\tКварталы / Quarters\t\t\t
Объем ВВП, млрд.рублей /GDP, bln rubles\t\t\t\t\t
2013\t71017\t15892\t17015\t18543\t19567
Комментарий:"""

        self._dicts = [{'head': 'Объем ВВП, млрд.рублей /GDP, bln rubles',
                        'data': ['', '', '', '', ''],
                        'label': {'unit': '', 'var': ''}},
                       {'head': '2013',
                        'data': ['71017', '15892', '17015', '18543', '19567'],
                        'label': {'unit': '', 'var': ''}},
                       {'head': 'Комментарий:',
                        'data': [],
                        'label': {'unit': '', 'var': ''}}]

        self._rows = [['', 'Год / Year', 'Кварталы / Quarters', '', '', ''],
                      ['Объем ВВП, млрд.рублей /GDP, bln rubles', '', '', '', '', ''],
                      ['2013', '71017', '15892', '17015', '18543', '19567'],
                      ['Комментарий:']]

    def test_sample_dict_and_rows_lengths(self):
        assert len(self._dicts) == 3
        assert len(self._rows) == 4
        # skipping rows with empty 'head' - dicts count is fewer than rows count
        assert len(self._dicts) < len(self._rows)


class TestCSV_yield_from_string(Match_CSV_Content):
    def test_yield_from_string(self):
        assert list(cd.yield_dicts_from_string(self._csv_content)) == self._dicts


class TestCSV_Reader(Match_CSV_Content):

    @staticmethod
    def make_file(content_string):
        with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as fp:
            fp.write(content_string)
        return fp.name

    def setUp(self):
        super().setUp()
        self.filename1 = self.make_file(self._csv_content)

    def tearDown(self):
        os.remove(self.filename1)

    def test_csv_dummy_content_reading_as_class(self):
        cr = cd.CSV_Reader(path=self.filename1)
        assert cr.rows == self._rows
        assert list(cr.yield_dicts()) == self._dicts


class TestCSV_Default_DataSource(unittest.TestCase):

    def setUp(self):
        import config
        self.csv_path = config.get_default_csv_path()

    def test_reading_default_csv(self):
        cr = cd.CSV_Reader(path=self.csv_path)
        assert len(cr.rows) > 4600
        csv_dicts = list(cr.yield_dicts())
        assert len(csv_dicts) > 4300


if __name__ == "__main__":
    unittest.main()