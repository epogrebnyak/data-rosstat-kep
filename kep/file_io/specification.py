# -*- coding: utf-8 -*-
"""YAML import: spec and cfg files

Entry functions:
   load_spec(filename)
   load_cfg(filename)
"""

import yaml
import os
from kep.file_io.common import r_open
   
def load_spec(filename):
    """Returns 2 specification dictionaries from a YAML file with following structure:

        # readers (very little lines) - to be depreciated 
        -----
        # units (a bit more lines)
        -----
        # headlines (many lines)"""
    spec = get_yaml(filename)     
    # depreciated_reader_dict = spec[0]    
    unit_dict = spec[1]
    headline_dict = spec[2]
    return headline_dict, unit_dict

def _chg(template_path, filename):
    folder = os.path.split(template_path)[0]
    return os.path.join(folder, filename)
# TODO: move this assert to unit tests
assert _chg(os.path.join('temp', '_config.txt'), 'new.txt') == os.path.join('temp', 'new.txt')

def inline_spec_load(cfg_filename, spec_file):
    return load_spec(_chg(cfg_filename, spec_file))
    
def load_cfg(cfg_filename):
    yaml = get_yaml(cfg_filename)    
    return list([start_line, end_line, inline_spec_load(cfg_filename, spec_file)]
                 for start_line, end_line, spec_file in yaml)
    
def _get_yaml(filename):
    with r_open(filename) as file:
        return list(yaml.load_all(file))   

def get_yaml(filename):        
    try:
        return _get_yaml(filename)
    except FileNotFoundError:
        raise FileNotFoundError ("YAML file not found: " + filename)
    except:
        raise Exception ("Error parsing YAML file: " + filename)
        
if __name__ == "__main__":
    fn = "kep/test/temp/test_cfg.txt"
    import os
    print(os.path.exists(fn))
    obj = [["1", "2", "3"], ["5","6","7"]]
    print(yaml.dump_all(obj))
    z = _get_yaml(fn)
    print(z)