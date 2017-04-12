"""Read parsing specification from yaml file ('specfile')."""

import yaml
import tempfile
import os
from csv_data import File

from config import get_default_spec_path, get_all_spec_paths
 
def get_definitions():
    return {'default': ParsingInstruction(path=get_default_spec_path()),
            'additional': [ParsingInstruction(path) for path in get_all_spec_paths()]
            }    
    
class ParsingInstruction():
    """Read parsing instruction from yaml file.
    
       Valid specification yaml looks like YAML_SAMPLE below."""

    #  parsing instruction with no start and end line and no special reader
    YAML_SAMPLE_1 = """
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

    # parsing instruction with start and end line and special reader
    YAML_SAMPLE_2 = """
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
   
    def __init__(self, path: str):
        """Read data from *path* file"""
        yaml_string = File(path).read_text()
        self.content = self.load_yaml_string(yaml_string)
        # FIXME
        #self.check()
        self.attrs = {'start':     self.content[0]['start line'],
             'end':                self.content[0]['end line'],
             'splitter_func_name': self.content[0]['special reader'],
             'units':              self.content[1],
             # FIXME variable names are a list now, but can be a label dict
             'headers':            self.content[2], 
             'labels':             [v[0] for v in self.content[2].values()]
             }   
        
    @staticmethod    
    def load_yaml_string(yaml_string):
        return list(yaml.load_all(yaml_string))      
    
    @staticmethod 
    def check_parsed_yaml(content):
        """Check specification data structure"""
        try: 
            # TODO: restore checks
            # yaml was read as a list         
            assert isinstance(content, list)
            # yaml has 3 docs
            #assert len(self.content) == 3
            # every doc is a dict
            #for part in self.content:
            #    assert isinstance(part, dict)
            # first doc has reserved keys 
            #for kw in ['start line', 'end line', 'special reader']:
            #    assert self.content[0].keys().__contains__(kw)
        except:
            raise Exception("Wrong format for parsing specification")
             
    def __getattr__(self, name):
        try:
            return self.attrs[name]        
        except KeyError:
            raise AttributeError(name)

    def __eq__(self, obj):
         return self.content == obj.content
         
    def __repr__(self):
        return self.content.__repr__()
    
class Tempfile():
    """Mimic file with *yaml_string* content."""
    
    def __init__(self, yaml_string):
        with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as fp:
           fp.write(yaml_string)
        self.path = fp.name
        
    def __enter__(self):
        return self.path
    
    def __exit__(self, type, value, traceback):
        os.remove(self.path)


if __name__ == "__main__":
    
    #testing    
    CONTENT_1 = [
 {'start line': None, 'end line': None, 'special reader': None}, 
 {'в % к предыдущему периоду': 'rog', 
 'период с начала отчетного года в % к соответствующему периоду предыдущего года': 'ytd', 
 'в % к соответствующему периоду предыдущего года': 'yoy'}, 
 {'Объем ВВП': ['GDP', 'bln_rub'], 
 'Индекс физического объема произведенного ВВП': ['GDP', 'rog'], 
 'Индекс промышленного производства': ['IND_PROD']}]

    CONTENT_2 = [
            {'start line': '2.1.1. Доходы (по данным Федерального казначейства)', 
            'end line': 'Удельный вес в общем объеме доходов соответствующего бюджета',
            'special reader': 'fiscal'}, 
             # ERROR must convert none to empty dict
             None, 
             {'Консолидированный бюджет': ['GOV_CONSOLIDATED_REVENUE_ACCUM', 'bln_rub']}]

    test_data = [(ParsingInstruction.YAML_SAMPLE_1, CONTENT_1),
                 (ParsingInstruction.YAML_SAMPLE_2, CONTENT_2)]
    
    for yaml_string, loaded_content in test_data:
        assert loaded_content == ParsingInstruction.load_yaml_string(yaml_string)
    
    with Tempfile(yaml_string=ParsingInstruction.YAML_SAMPLE_1) as path:
       assert ParsingInstruction(path).content == CONTENT_1
                                
    with Tempfile(yaml_string=ParsingInstruction.YAML_SAMPLE_2) as path:
       assert ParsingInstruction(path).content == CONTENT_2
   
    # entry example
    pi = ParsingInstruction(path=get_default_spec_path())