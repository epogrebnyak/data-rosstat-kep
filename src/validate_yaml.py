# -*- coding: utf-8 -*-
import os
import yaml
from collections import OrderedDict
from word import dump_iter_to_csv, get_varname_filename, get_spec_filename

def ordered_load_all(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """From SO"""
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load_all(stream, OrderedLoader)

def load_as_ordered_dict(f):
    with open(f) as stream:
        z = [x for x in ordered_load_all(stream, Loader = yaml.loader.Loader)]
    return z[0], z[1], z[2]

def load_as_dict(f):        
    with open(f) as stream:
        z = [x for x in yaml.load_all(stream)]
    return z[0], z[1], z[2]
    
def yield_varnames(f):
    f = get_spec_filename(f)
    reader_dict, unit_dict, var_dict = load_as_ordered_dict(f)
    for k, v in var_dict.items():
        yield (v[0], k)

def dump_varnames_to_csv(f):
    gen = yield_varnames(f)
    outfile = get_varname_filename(f) 
    dump_iter_to_csv(gen, outfile)       

f = os.path.abspath("../data/ind06/all_tab_spec.txt")
dump_varnames_to_csv(f)

for p in yield_varnames(f):
    print(p)



# Todo:
# through var_dict to new table in db
# create  table with auto enumumeration
