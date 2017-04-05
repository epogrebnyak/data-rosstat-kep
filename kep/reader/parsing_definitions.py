"""Read parsing specification from yaml file ('specfile')."""

import yaml
import os
from pprint import pprint

from kep.config import PARSING_DEFINITIONS_FOLDER, DEFAULT_SPEC_FILE, SPEC_FILENAME_MUST_CONTAIN 
from kep.common import File

# -----------------------------------------------------------------------------
#
# Reminder about how YAML works
#
# assert yaml.load("""
# в % к соответствующему периоду предыдущего года : yoy
# """) == {"в % к соответствующему периоду предыдущего года" : "yoy"}
#           
#
# assert list(yaml.load_all("""
# a: 2
# ---
# b: 3""")) == [{'a': 2}, {'b': 3}]
#
# -----------------------------------------------------------------------------

def parse_spec_text(yaml_string):  
    
    content = list(yaml.load_all(yaml_string))
    return { 'scope': { 'start_line':  content[0]['start line'],
                          'end_line':  content[0]['end line']},
             'reader_func': content[0]['special reader'],
             'units':   content[1],
             'table_headers': content[2]
             }


def get_parsing_definition(yaml_filepath):
    yaml_string = File(yaml_filepath).read_text()
    return parse_spec_text(yaml_string)  
 

def get_default_definition():
    _f = os.path.join(PARSING_DEFINITIONS_FOLDER, DEFAULT_SPEC_FILE)
    return get_parsing_definition(_f) 
           
    
def get_specfiles_paths():    
    _dir = PARSING_DEFINITIONS_FOLDER    
    paths = [os.path.join(_dir,f) 
             for f in os.listdir(_dir)             
             if SPEC_FILENAME_MUST_CONTAIN in f
             and f != DEFAULT_SPEC_FILE]    
    return [p for p in paths if os.path.isfile(p)]


def get_definitions():
    return {'default': get_default_definition(),
            'additional': [get_parsing_definition(f) for f in get_specfiles_paths()]
            }

if __name__ == "__main__":
    pprint(get_definitions())
