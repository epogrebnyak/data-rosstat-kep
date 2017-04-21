"""Read parsing specification from yaml file.

Usage:
    
    pdef = ParsingDefinition(path=get_default_spec_path())
    
    Attributes for *pdef*:
       .start
       .end
       .splitter_func_name
       .units
       .headers
       .labels
       
"""

from collections import OrderedDict
import yaml

from config import get_default_spec_path, get_all_spec_paths
from files import File


def get_definitions():
    return {'default': ParsingDefinition(path=get_default_spec_path()),
            'additional': [ParsingDefinition(path) for path in get_all_spec_paths()]
            }

# Make yaml load dicts as OrderedDicts - start
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def _dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def _dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


yaml.add_representer(OrderedDict, _dict_representer)
yaml.add_constructor(_mapping_tag, _dict_constructor)
# ----------------------------------------------------- end

# ----------------------------------------------------- constants
#
# Keep YAML_SAMPLE and CONTENT constants here for quick reference
#
#

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

CONTENT_2 = [
        OrderedDict([('start line', '2.1.1. Доходы (по данным Федерального казначейства)'),
            ('end line', 'Удельный вес в общем объеме доходов соответствующего бюджета'),
            ('special reader', 'fiscal'),
        ]),
        OrderedDict(),
        OrderedDict([('Консолидированный бюджет', ['GOV_CONSOLIDATED_REVENUE_ACCUM', 'bln_rub'])]),
    ]

# ------------------------------------------------------------ end of constants


class ParsingDefinition():
    """Read parsing instruction from yaml file.
    
       Valid specification yaml in YAML_SAMPLE constants above:
           
          YAML_SAMPLE_1 - parsing instruction with no start and end line and no special reader,
          YAML_SAMPLE_2 - parsing instruction with start and end line and special reader."""

    def __init__(self, path: str):
        """Read data from file at *path*"""
        yaml_string = File(path).read_text()
        self.content = self.from_yaml(yaml_string)
        self.check_parsed_yaml(self.content) 
        self.attrs = {'start': self.content[0]['start line'],
                      'end': self.content[0]['end line'],
                      'splitter_func_name': self.content[0]['special reader'],
                      'units': self.content[1],
                      # WONTFIX variable names are a list now, but can be a label dict for easier handling later
                      'headers': self.content[2],
                      'labels': [v[0] for v in self.content[2].values()]
                      }

    @staticmethod
    def check_parsed_yaml(content):
        """Check data structure after reading yaml."""
        try:
            # yaml was read as a list         
            assert isinstance(content, list)
            # yaml has 3 docs
            assert len(content) == 3
            # every doc is an ordered dict
            for part in content:
                assert isinstance(part, OrderedDict)
            # first doc has reserved keys 
            for kw in ['start line', 'end line', 'special reader']:
                assert content[0].keys().__contains__(kw)
        except:
            # WONTFIX: may have better handling of errors if not isinstance(content, list): raise Exception
            print("-----------------------")
            print(content)
            print("-----------------------")
            raise Exception("Wrong format for parsing specification")

    @staticmethod
    def from_yaml(yaml_string):
        content = list(yaml.load_all(yaml_string))
        # replace every occurence of None with empty OrderedDict
        content = [x if x is not None else OrderedDict() for x in content]
        return content

    def __getattr__(self, name):
        try:
            return self.attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __eq__(self, obj):
        return self.content == obj.content

    def __repr__(self):
        return self.content.__repr__()

# --------------------------------------------------------------------- Testing

from files import Tempfile 
import unittest
    
class TestCaseParsingDefinition(unittest.TestCase):
    
    def test_read_empty_yaml(self):
        content = ParsingDefinition.from_yaml("---\n---\n---")
        assert [OrderedDict(), OrderedDict(), OrderedDict()] == content

    def test_read_yaml(self):
        for yaml_string in YAML_SAMPLE_1, YAML_SAMPLE_2:
             content = ParsingDefinition.from_yaml(yaml_string)
             ParsingDefinition.check_parsed_yaml(content)     
    
    def test_yaml_string_to_content(self):        
        test_data = [(YAML_SAMPLE_1, CONTENT_1),
                    (YAML_SAMPLE_2, CONTENT_2)]
        
        for yaml_string, loaded_content in test_data:
            assert loaded_content == ParsingDefinition.from_yaml(yaml_string)
            
    def test_string_to_file_to_content(self):
        with Tempfile(content_string=YAML_SAMPLE_1) as path:
            assert ParsingDefinition(path).content == CONTENT_1
    
        with Tempfile(content_string=YAML_SAMPLE_2) as path:
            assert ParsingDefinition(path).content == CONTENT_2


if __name__ == '__main__':
    unittest.main()    