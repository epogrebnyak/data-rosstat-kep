# -*- coding: utf-8 -*-

from collections import OrderedDict
import unittest
import tempfile
import os

from kep.reader.parsing_definitions import StringAsYAML, ParsingDefinition, Label
import kep.ini as ini

EMPTY = """start line : 
end line : 
special reader: 
---

---"""

EMPTY_CONTENT = [OrderedDict([('start line', None),
                  ('end line', None),
                  ('special reader', None)]),
                 OrderedDict(),  
                 OrderedDict()]

MINIMAL = """start line : a 
end line : b
special reader: c
---
e: eee 
j: jjj
---
m:
 - nnn
 - p
r:
 - sss
 - t"""

#  YAML_1 - parsing instruction with no start and end line and no special reader,
YAML_1 = """
# scope 
start line: null       # 'start_line'
end line: null         # 'end_line'
special reader: null   # 'reader_func'
---
# 'units' section 
в % к предыдущему периоду: rog
период с начала отчетного года в % к соответствующему периоду предыдущего года: ytd
в % к соответствующему периоду предыдущего года: yoy
---
# 'headers' section 
Объем ВВП: 
 - GDP
 - bln_rub
Индекс физического объема произведенного ВВП:
 - GDP
 - rog
Индекс промышленного производства:
 - IND_PROD
"""

CONTENT_1 = [
        OrderedDict([('start line', None), ('end line', None), ('special reader', None)]),
        OrderedDict([('в % к предыдущему периоду', 'rog'),
            ('период с начала отчетного года в % к соответствующему периоду предыдущего года', 'ytd'),
            ('в % к соответствующему периоду предыдущего года', 'yoy'),
        ]),
        OrderedDict([('Объем ВВП', ['GDP', 'bln_rub']),
            ('Индекс физического объема произведенного ВВП', ['GDP', 'rog']),
            ('Индекс промышленного производства', ['IND_PROD']),
        ]),
    ]

          
#  YAML_2 - parsing instruction with start and end line and special reader.
YAML_2 = """
# scope and reader defined
start line : 2.1.1. Доходы (по данным Федерального казначейства)
end line : Удельный вес в общем объеме доходов соответствующего бюджета
special reader: fiscal
---
# units skipped
---
# headers: one variable to be read
Консолидированный бюджет : 
 - GOV_CONSOLIDATED_REVENUE_ACCUM
 - bln_rub 
"""

CONTENT_2 = [
        OrderedDict([('start line', '2.1.1. Доходы (по данным Федерального казначейства)'),
            ('end line', 'Удельный вес в общем объеме доходов соответствующего бюджета'),
            ('special reader', 'fiscal'),
        ]),
        OrderedDict(),
        OrderedDict([('Консолидированный бюджет', ['GOV_CONSOLIDATED_REVENUE_ACCUM', 'bln_rub'])]),
    ]


class Test_StringAsYAML(unittest.TestCase):
        
    @staticmethod
    def read_and_check(yaml_string):                
       yaml_content =  StringAsYAML.from_yaml(yaml_string)
       StringAsYAML.check_parsed_yaml(yaml_content)

    def test_read_yaml_and_check(self):       
       self.read_and_check(YAML_1)
       self.read_and_check(YAML_2)
       self.read_and_check(EMPTY)
       self.read_and_check(MINIMAL)
       
    @staticmethod
    def string_to_content(_string, _content):
       assert StringAsYAML.from_yaml(_string) == _content                                        
    
    def test_yaml_string_to_content(self):
        assert StringAsYAML(YAML_1).headers == \
              OrderedDict([('Объем ВВП', Label(varname='GDP', unit='bln_rub')),
                           ('Индекс физического объема произведенного ВВП',
                                         Label(varname='GDP', unit='rog')),
                           ('Индекс промышленного производства',
                                         Label(varname='IND_PROD', unit=None))])
    
    def test_attributes(self):
       z = StringAsYAML(MINIMAL)
       assert z.units == OrderedDict([('e', 'eee'), ('j', 'jjj')])
       # TODO: make more tests like this to check label
       assert z.headers == OrderedDict([('m', Label(varname='nnn', unit='p')),
                                        ('r', Label(varname='sss', unit='t'))])
       assert z.start == 'a'
       assert z.end == 'b'
       assert z.reader == 'c'
       assert z.all_labels == ['nnn', 'sss']
       assert set(z.unique_labels) == set(['nnn', 'sss'])
       

class Test_ParsingDefintion(unittest.TestCase):
    
    @staticmethod
    def make_file(content_string):
        with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as fp:
            fp.write(content_string)
        return fp.name    
    
    def setUp(self):
        self.filename1 = self.make_file(YAML_1)
        self.filename2 = self.make_file(YAML_2)
        self.filename3 = self.make_file(EMPTY)       
        
    def tearDown(self):    
        for fn in (self.filename1, self.filename2, self.filename3):
            os.remove(fn)
    
    @staticmethod
    def filename_to_content(_filename, _content):
        assert ParsingDefinition(path=_filename).content == _content       
        
    def test_string_to_file_to_content(self):       
        self.filename_to_content(self.filename1, CONTENT_1)
        self.filename_to_content(self.filename2, CONTENT_2)
        self.filename_to_content(self.filename3, EMPTY_CONTENT)
    
class Test_Get_Definitions(unittest.TestCase):
    
    def test_main_specification_file_exists(self):
        _fp = ini.get_mainspec_filepath().__str__()
        assert os.path.exists(_fp)
        
        p0 = ParsingDefinition(path=_fp)        
        assert isinstance(p0, ParsingDefinition)
        
if __name__ == '__main__':
    unittest.main()