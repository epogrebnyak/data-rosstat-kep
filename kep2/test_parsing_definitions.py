# -*- coding: utf-8 -*-

from collections import OrderedDict
import unittest
import tempfile
import os

import parsing_definitions as pdef
   

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


class Test_StringAsYAML(unittest.TestCase):
        
    @staticmethod
    def read_and_check(yaml_string):                
       yaml_content =  pdef.StringAsYAML.from_yaml(yaml_string)
       pdef.StringAsYAML.check_parsed_yaml(yaml_content)

    def test_read_yaml_and_check(self):       
       self.read_and_check(pdef.YAML_1)
       self.read_and_check(pdef.YAML_2)
       self.read_and_check(EMPTY)
       self.read_and_check(MINIMAL)
       
    @staticmethod
    def string_to_content(_string, _content):
       assert pdef.StringAsYAML.from_yaml(_string) == _content                                        
    
    def test_yaml_string_to_content(self):
       self.string_to_content(EMPTY, EMPTY_CONTENT)
       self.string_to_content(pdef.YAML_1, pdef.CONTENT_1)
       self.string_to_content(pdef.YAML_2, pdef.CONTENT_2)
       
    def test_attributes(self):
       z = pdef.StringAsYAML(MINIMAL)
       assert z.units == OrderedDict([('e', 'eee'), ('j', 'jjj')])
       assert z.headers == OrderedDict([('m', ['nnn', 'p']), ('r', ['sss', 't'])])
       assert z.start == 'a'
       assert z.end == 'b'
       assert z.reader == 'c'
       assert z.labels == ['nnn', 'sss']
       

class Test_ParsingDefintion(unittest.TestCase):
    
    @staticmethod
    def make_file(content_string):
        with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as fp:
            fp.write(content_string)
        return fp.name    
    
    def setUp(self):
        self.filename1 = self.make_file(pdef.YAML_1)
        self.filename2 = self.make_file(pdef.YAML_2)
        self.filename3 = self.make_file(EMPTY)       
        
    def tearDown(self):    
        for fn in (self.filename1, self.filename2, self.filename3):
            os.remove(fn)
    
    @staticmethod
    def filename_to_content(_filename, _content):
        assert pdef.ParsingDefinition(path=_filename).content == _content       
        
    def test_string_to_file_to_content(self):       
        self.filename_to_content(self.filename1, pdef.CONTENT_1)
        self.filename_to_content(self.filename2, pdef.CONTENT_2)
        self.filename_to_content(self.filename3, EMPTY_CONTENT)

if __name__ == '__main__':
    unittest.main()       