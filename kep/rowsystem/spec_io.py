# -*- coding: utf-8 -*-
"""YAML import: spec and cfg files

Entry functions:
   load_spec(filename)
   load_cfg(filename)
   param_import_from_files(filename)
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

#------------------------------------------------------------------------------
#  Other IO functions  
#------------------------------------------------------------------------------

def readfile(file):    
    with r_open(file) as f:
        content = f.readlines()
    return content       

def write_file(filename, docstring):
    with w_open(filename) as f:
        f.write(docstring) 
    return filename       

def docstring_to_file(docstring,filename):
    return write_file(filename, docstring)    
    
#------------------------------------------------------------------------------
#  Testing  
#------------------------------------------------------------------------------

def fcomp(doc, var, loader_func, fname = None):
    if fname is None:
        fname = "temp.txt"
    path = write_file(fname, doc)
    #import pdb; pdb.set_trace()
    assert loader_func(path) == var
    os.remove(path)
    
#------------------------------------------------------------------------------
#  YAML readers
#------------------------------------------------------------------------------
    
def _get_yaml(filename):
    with r_open(filename) as file:
        return list(yaml.load_all(file))   

def get_yaml(filename):        
    try:
        return _get_yaml(filename)
    except FileNotFoundError:
        raise FileNotFoundError ("YAML file not found: " + filename)
  
def load_spec(filename):
    """Returns 3 specification dictionaries from a YAML file"""
    spec = get_yaml(filename)
    start_end_reader = spec[0]    
    unit_dict = spec[1]
    headline_dict = spec[2]
    return headline_dict, unit_dict, start_end_reader

def _adjust_path(template_path, filename):
    folder = os.path.split(template_path)[0]
    return os.path.join(folder, filename)
    
def preload_cfg(cfg_path):
    for spec_file in get_yaml(cfg_path)[0]:
       adjusted_spec_path = _adjust_path(cfg_path, spec_file)
       segment_dicts = load_spec(adjusted_spec_path)
       yield [segment_dicts[2]['start line'], segment_dicts[2]['end line'], segment_dicts] 
    
def load_cfg(cfg_path):
    return list(preload_cfg(cfg_path))
    