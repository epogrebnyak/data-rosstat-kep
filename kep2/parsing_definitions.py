"""Read parsing specification from yaml file ('specfile')."""

import yaml
import os
from pprint import pprint

from csv_data import File

"""
YAML files
==========

    1. Production:
    - YAML files at one folder 
        
    2. Testing:
    - one YAML file (one segment)
    - group of YAML files (many segments) 
    - text string with YAML content     
    - dictionary with parsing definition
  
"""  

# file locations

PARSING_DEFINITIONS_FOLDER = 'parsing_definitions'
DEFAULT_SPEC_FILE = "__spec.txt"
SPEC_FILENAME_MUST_CONTAIN = "spec"


def get_default_definition():
    _f = os.path.join(PARSING_DEFINITIONS_FOLDER, DEFAULT_SPEC_FILE)
    return get_parsing_definition(_f) 
           
def get_specfiles_paths():
    paths = [os.path.join(PARSING_DEFINITIONS_FOLDER ,f) 
             for f in os.listdir(PARSING_DEFINITIONS_FOLDER )             
             if SPEC_FILENAME_MUST_CONTAIN in f
             and f != DEFAULT_SPEC_FILE]    
    return [p for p in paths if os.path.isfile(p)]

def get_definitions():
    return {'default': get_default_definition(),
            'additional': [get_parsing_definition(f) for f in get_specfiles_paths()]
            }

# yaml parsing

def parse_spec_text(yaml_string):  
    """Read parsing defintion from YAML document to dictionary."""    
    content = list(yaml.load_all(yaml_string))
    return { 'scope': { 'start_line': content[0]['start line'],
                          'end_line': content[0]['end line']},
    
             'instruction': {
                           'headers': content[2], # FIXME it is a list now, but can be a dict
                             'units': content[1],                  
                     'splitter_func': content[0]['special reader']}
             }
             
def get_parsing_definition(yaml_filepath):
    yaml_string = File(yaml_filepath).read_text()
    return parse_spec_text(yaml_string)  
 

if __name__ == "__main__":
    dd = get_default_definition()
    assert 'instruction' in dd.keys()
    assert 'scope' in dd.keys()
    #pprint(get_default_definition()['instruction'])