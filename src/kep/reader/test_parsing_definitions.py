from collections import OrderedDict
import unittest
import tempfile
import os

from kep.reader.parsing_definitions import BaseYAML, ParsingDefinition, Specification
from kep.reader.label import Label
import kep.ini as ini


"""Tests:
- EMPTY vs EMPTY_CONTENT
- MINIMAL vs values
- YAML_1 vs CONTENT_1
- YAML_2 vs CONTENT_2
"""

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

def read_and_validate(yaml_string):
    yaml_content =  BaseYAML.from_yaml(yaml_string)
    BaseYAML.validate(yaml_content)
    

class Test_BaseYAML(unittest.TestCase):        

    def test_read_yaml_string_and_validate(self):
       for yaml_string in [YAML_1, YAML_2, EMPTY, MINIMAL]:       
          read_and_validate(yaml_string)
                                     
    
    def test_yaml_string_to_content(self):
        assert BaseYAML(YAML_1).headers == \
              OrderedDict([('Объем ВВП', Label(varname='GDP', unit='bln_rub')),
                           ('Индекс физического объема произведенного ВВП',
                                         Label(varname='GDP', unit='rog')),
                           ('Индекс промышленного производства',
                                         Label(varname='IND_PROD', unit=None))])
    
    def test_attributes(self):
       z = BaseYAML(MINIMAL)
       assert z.units == OrderedDict([('e', 'eee'), ('j', 'jjj')])
       assert z.headers == OrderedDict([('m', Label(varname='nnn', unit='p')),
                                        ('r', Label(varname='sss', unit='t'))])
       assert z.start == 'a'
       assert z.end == 'b'
       assert z.reader == 'c'
       assert z.varnames == ['nnn', 'sss']
       

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
    
    def test_string_to_file_to_content(self):       
        assert ParsingDefinition(path=self.filename1).content == CONTENT_1
        assert ParsingDefinition(path=self.filename2).content == CONTENT_2
        assert ParsingDefinition(path=self.filename3).content == EMPTY_CONTENT
    
class Test_Specfiles_Exist_and_Readable(unittest.TestCase):
    
    def setUp(self):
        self.specpath_main = ini.get_mainspec_filepath()                
        self.specpaths_extras = ini.get_additional_filepaths()
    
    def test_main_specification_file_exists(self):
        assert os.path.exists(self.specpath_main)

    def test_main_specification_file_readable(self):
        p = ParsingDefinition(path=self.specpath_main)        
        assert isinstance(p, ParsingDefinition)

    def test_extra_specification_files_exist(self):
        for fp in self.specpaths_extras:
            assert os.path.exists(fp)
            
    def test_extra_specification_files_readable(self):
        for fp in self.specpaths_extras:
            p = ParsingDefinition(path=fp) 
            assert isinstance(p, ParsingDefinition)

class Test_Specification(Test_Specfiles_Exist_and_Readable):

    def setUp(self):
        super().setUp()
        self.spec = Specification(path=self.specpath_main, 
                                  pathlist=self.specpaths_extras)
    
    def test_specification_readable(self):
        assert isinstance(self.spec, Specification)

    def test_specification_has_main_and_extras(self):
        assert isinstance(self.spec.main, ParsingDefinition)
        for d in self.spec.extras:
            assert isinstance(d, ParsingDefinition)
    
    def test_specification_has_string_varnames(self):
        # make sure self.varnames is flat list of strings
        for vn in self.spec.varnames:
            assert isinstance(vn, str)  
            
    def test_specification_has_specific_varnames(self):
        for vn in ['GOV_CONSOLIDATED_EXPENSE_ACCUM', 'NONFINANCIALS_PROFIT_POWER_GAS_WATER']:
           assert vn in self.spec.varnames     
            
if __name__ == "__main__":
    unittest.main()        
    # FIXME: test runs very slow: 2.242s
    main_def = ParsingDefinition(path=ini.get_mainspec_filepath())
    more_def = [ParsingDefinition(path) for path in ini.get_additional_filepaths()]
    spec = Specification(path=ini.get_mainspec_filepath(), pathlist=ini.get_additional_filepaths())
    

    
  
    
    
    
    
    