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
	
        # units (several)
		unit of measurement 1: unit_abbr1
		unit of measurement 2: unit_abbr2
        -----
        # headlines (many lines)
		table headline A:
		   - var_A
		   - main_unit_abbr_for_A
		table headline B:
		   - var_B
		   - main_unit_abbr_for_B
	
    """
    spec = get_yaml(filename)     
    unit_dict = spec[0]
    headline_dict = spec[1]
    return headline_dict, unit_dict
	
# def load_spec(filename):
    # """Returns 2 specification dictionaries from a YAML file with following structure:

        # # readers (very little lines) - to be depreciated 
        # -----
        # # units (a bit more lines)
        # -----
        # # headlines (many lines)"""
    # spec = get_yaml(filename)     
    # # depreciated_reader_dict = spec[0]    
    # unit_dict = spec[1]
    # headline_dict = spec[2]
    # return headline_dict, unit_dict

def _adjust_path(template_path, filename):
    folder = os.path.split(template_path)[0]
    return os.path.join(folder, filename)

def preload_cfg(cfg_path):
    for section in get_yaml(cfg_path):
       start_line = section[0]
       end_line = section[1]
       spec_file = section[2]
       adjusted_spec_path = _adjust_path(cfg_path, spec_file)
       segment_dicts = load_spec(adjusted_spec_path)
       yield [start_line, end_line, segment_dicts] 
    
def load_cfg(cfg_path):
    return list(preload_cfg(cfg_path))
    
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