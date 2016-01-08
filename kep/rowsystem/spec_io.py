# -*- coding: utf-8 -*-
"""YAML import: spec and cfg files

Entry functions:
   load_spec(filename)
   load_cfg(filename)
"""

import yaml
import os
import io
import itertools

#------------------------------------------------------------------------------
#  Variable label manipulation
#------------------------------------------------------------------------------
def get_var_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))
assert get_var_abbr('PROD_E_TWh') == 'PROD_E' 

def get_unit_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))
assert get_unit_abbr('PROD_E_TWh') == 'TWh'

#------------------------------------------------------------------------------
#  Filename conventions 
#------------------------------------------------------------------------------

def get_filenames(data_folder):
    """Filename conventions"""
    # MAYDO: also check these files exist
    csv  = os.path.join(data_folder, "tab.csv")
    spec = os.path.join(data_folder, "tab_spec.txt")
    cfg =  os.path.join(data_folder, "tab_cfg.txt")
    return csv, spec, cfg
 
#------------------------------------------------------------------------------
#  Root io functions with encoding 
#------------------------------------------------------------------------------

ENCODING = 'utf8' #'cp1251'
       
def w_open(file):
    return open(file, 'w', encoding = ENCODING)

def r_open(file):
    return open(file, 'r', encoding = ENCODING)

def readfile(file):    
    with r_open(file) as f:
        content = f.readlines()
    return content       
    
    
def _get_yaml(filename):
    with r_open(filename) as file:
        return list(yaml.load_all(file))   

def get_yaml(filename):        
    try:
        return _get_yaml(filename)
    except FileNotFoundError:
        raise FileNotFoundError ("YAML file not found: " + filename)
    #except:
    #    raise Exception ("Error parsing YAML file: " + filename)    

def write_file(filename, docstring):
    with w_open(filename) as f:
        f.write(docstring) 
    return filename    
        
spec_file_sample = write_file("_spec.txt", """
# segment information
start line : null
end line : null
special reader: null

---
# units (several)
unit of measurement 1: unit_abbr1
unit of measurement 2: unit_abbr2

---
# headlines (many lines)
table headline A:
   - var_A
   - main_unit_abbr_for_A
table headline B:
   - var_B
   - main_unit_abbr_for_B
""")    
   
def load_spec(filename):
    """Returns 3 specification dictionaries from a YAML file"""
    spec = get_yaml(filename)
    start_end_reader = spec[0]    
    unit_dict = spec[1]
    headline_dict = spec[2]
    return headline_dict, unit_dict, start_end_reader

assert load_spec(spec_file_sample) == ({'table headline B': ['var_B', 'main_unit_abbr_for_B'], 'table headline A': ['var_A', 'main_unit_abbr_for_A']}, 
{'unit of measurement 2': 'unit_abbr2', 'unit of measurement 1': 'unit_abbr1'}, 
{'special reader': None, 'end line': None, 'start line': None})

	
def _adjust_path(template_path, filename):
    folder = os.path.split(template_path)[0]
    return os.path.join(folder, filename)

    
cfg_file_sample = write_file("_cfg.txt", """
- _spec.txt
- _spec.txt
""")     
    
def preload_cfg(cfg_path):
    for spec_file in get_yaml(cfg_path)[0]:
       adjusted_spec_path = _adjust_path(cfg_path, spec_file)
       segment_dicts = load_spec(adjusted_spec_path)
       yield [segment_dicts[2]['start line'], segment_dicts[2]['end line'], segment_dicts] 
    
def load_cfg(cfg_path):
    return list(preload_cfg(cfg_path))
    
assert load_cfg(cfg_file_sample) == [[None, None, ({'table headline B': ['var_B', 'main_unit_abbr_for_B'], 'table headline A': ['var_A', 'main_unit_abbr_for_A']}, {'unit of measurement 2': 'unit_abbr2', 'unit of measurement 1': 'unit_abbr1'}, {'special reader': None, 'end line': None, 'start line': None})], [None, None, ({'table headline B': ['var_B', 'main_unit_abbr_for_B'], 'table headline A': ['var_A', 'main_unit_abbr_for_A']}, {'unit of measurement 2': 'unit_abbr2', 'unit of measurement 1': 'unit_abbr1'}, {'special reader': None, 'end line': None, 'start line': None})]]

    