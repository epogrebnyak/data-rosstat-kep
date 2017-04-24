# -*- coding: utf-8 -*-
"""Test csv data import."""

import unittest
import tempfile
import os

import csv_data as cd

class test_CSV_Reader_support_funcs(unittest.TestCase):
        
    def test_doc_to_lists(self):
        assert cd.doc_to_lists("2015\t99,2\t99,9\n2016\t101,3\t101,1") == \
                                    [['2015', '99,2', '99,9'], 
                                     ['2016', '101,3', '101,1']]  
                                    
    def test_row_as_dict(self):
        
        assert '1. Сводные показатели' == \
               cd.row_as_dict(['1. Сводные показатели', '', ''])['head']
               
        row = ['2013', '10', '20', '30', '40']      
        assert '2013' == cd.row_as_dict(row)['head']
        assert ['10', '20', '30', '40'] == cd.row_as_dict(row)['data']
        assert {'unit': '', 'var': ''} == cd.row_as_dict(row)['label']

class test_CSV_Reader(unittest.TestCase):
    
    @staticmethod
    def make_file(content_string):
        with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as fp:
            fp.write(content_string)
        return fp.name    
    
    def setUp(self):
        CSV_CONTENT = """	Год / Year	Кварталы / Quarters			
Объем ВВП, млрд.рублей /GDP, bln rubles					
2013	71017	15892	17015	18543	19567
Комментарий:"""
        self.filename1 = self.make_file(CSV_CONTENT)
        
    def tearDown(self):    
        os.remove(self.filename1)
            
    def test_dummy_content_reading(self):
        cr = cd.CSV_Reader(path = self.filename1)
        
        assert cr.rows == [['', 'Год / Year', 'Кварталы / Quarters', '', '', ''],
                           ['Объем ВВП, млрд.рублей /GDP, bln rubles', '', '', '', '', ''],
                           ['2013', '71017', '15892', '17015', '18543', '19567'],                          
                           ['Комментарий:']]
        
        assert list(cr.yield_dicts()) == [{'data': ['', '', '', '', ''],
               'head': 'Объем ВВП, млрд.рублей /GDP, bln rubles',
               'label': {'unit': '', 'var': ''}},
        
               {'data': ['71017', '15892', '17015', '18543', '19567'],
                'head': '2013',
                'label': {'unit': '', 'var': ''}},
                
               {'data': [], 
                'head': 'Комментарий:', 
                'label': {'unit': '', 'var': ''}}               
               ]
        
        
    def test_reading_default_csv(self):
        import config
        cr = cd.CSV_Reader(path = config.get_default_csv_path())   
        assert len(cr.rows) > 4600
        csv_dicts = list(cr.yield_dicts())
        assert len(csv_dicts) > 4300    


if __name__ == "__main__":
    unittest.main()