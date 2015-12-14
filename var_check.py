# -*- coding: utf-8 -*-
# for testing and new features

# Scope of work:
# - read all variable names from spec/cfg files
# - read all variable names in database (all non-empty /  at specific frequency)
# - make and count headers (non-data rows) 

# -------------------------------------------------

def count_entries(z, list_):
    count = 0
    for x in list_:
       if z == x:
           count += 1
    return count 

assert count_entries("a", ["a","a","b"]) == 2
assert count_entries("b", ["a","a","b"]) == 1

def get_duplicates(full_list):
    ix = [count_entries(x,full_list) > 1 for x in full_list]
    return [full_list[i] for i, flag in enumerate(ix) if flag]

assert get_duplicates(["a","a","b"]) == ["a","a"]


# -------------------------------------------------

def which_only_in_a(a,b):
    return [x for x in a if x not in b] 
def which_only_in_b(a,b):
    return which_only_in_a(b,a)
def which_in_both(a,b):
    return [x for x in a if x in b and x in a]

a = [1,2,3,4]
b = [3,4,10,100]
assert which_only_in_a(a,b) == [1,2]
assert which_only_in_b(a,b) == [10,100]
assert which_in_both(a,b) == [3,4]
assert get_duplicates(a + b) == [3,4,3,4]

# -------------------------------------------------

from kep.io.common import get_filenames
from kep.io.specification import load_cfg, load_spec

def unpack_header_dict(header_dict):
   return list(x[0] for x in header_dict.values())

def unpack_segments(segments):
   var_list = []
   for seg in segments:
       seg_var_list =  unpack_header_dict(seg[2][0])       
       var_list.extend(seg_var_list)
   return var_list 

def get_spec_and_cfg_varnames(data_folder):
    csv, spec, cfg = get_filenames(data_folder)
    segments = load_cfg(cfg)
    header_dict, unit_dict = load_spec(spec)
    s = unpack_segments(segments)
    h = unpack_header_dict(header_dict)
    return s, h
    
def get_varnames_from_spec(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return h    

def get_varnames_from_cfg(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return s
    
def get_varnames_from_spec_and_cfg(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return s+h

def get_overlapping_varnames_from_spec_and_cfg(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return which_in_both(s, h)
    
# NOTE: maybe check for duplicates in s or has_key
#       must pass len(lst) == len(unique(lst)), otherwise issue warning
    
def unique(lst):
    return sorted(list(set(lst)))

data_folder = "data/2015/ind10"
sc = get_varnames_from_spec_and_cfg(data_folder)
c = get_varnames_from_cfg(data_folder)
s = get_varnames_from_spec(data_folder)
w = get_overlapping_varnames_from_spec_and_cfg(data_folder)

def msg(text,total_list):
    unique_list = unique(total_list)
    count_msg = " ({0} total, {1} unique):\n".format(len(total_list), len(unique_list))
    print("\n" + text + count_msg, unique_list)

msg("Varnames in spec and cfg", sc)
msg("Varnames in spec", s)
msg("Varnames in cfg", c)
msg("Overlapping varnames in spec and cfg", w)

# todo: count number of headers
#       total varnames
