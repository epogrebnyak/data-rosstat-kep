# -*- coding: utf-8 -*-
# for testing and new features

# Scope of work:
# - read all variable names from spec/cfg files
# - read all variable names in database (all non-empty /  at specific frequency)
# - make and count headers (non-data rows) 

def count_entries(z, list_):
    count = 0
    for x in list_:
       if z == x:
           count += 1
    return count 

assert count_entries("a", ["a","a","b"]) == 2
assert count_entries("b", ["a","a","b"]) == 1

from kep.io.common import get_filenames
from kep.io.specification import load_cfg, load_spec

data_folder = "data/2015/ind10"
csv, spec, cfg = get_filenames(data_folder)
segments = load_cfg(cfg)
header_dict, unit_dict = load_spec(p)

print (segments[0])
print (header_dict)