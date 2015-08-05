# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 02:15:13 2015

@author: Евгений
"""

import os
import yaml
from collections import OrderedDict

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load_all(stream, OrderedLoader)

# usage example:
#ordered_load(stream, yaml.SafeLoader)

def load_as_ordered_dict(f):
    with open(f) as stream:
        z = [x for x in ordered_load(stream, Loader = yaml.loader.Loader)]
    return z[0], z[1], z[2]

def load_as_dict(f):        
    with open(f) as stream:
        z = [x for x in yaml.load_all(stream)]
    return z[0], z[1], z[2]  

f = os.path.abspath("../data/ind06/all_tab_spec.txt")
reader_dict, unit_dict, var_dict = load_as_ordered_dict(f)

# through var_dict to new table in db
# create  table with auto enumumeration


for k, v in var_dict.items():
    print(k)
