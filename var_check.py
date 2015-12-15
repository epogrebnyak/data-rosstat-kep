# -*- coding: utf-8 -*-
#
# Scope of work:
# - read all variable names from spec/cfg files
# - read all variable names in database (all non-empty /  at specific frequency)
# - make and count headers (non-data rows) 
#

from kep.io.common import get_filenames, get_var_abbr
from kep.io.specification import load_cfg, load_spec
from kep.database.db import get_unique_labels

VERBOSE_FLAG = True

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

def unique(lst):
    return sorted(list(set(lst)))
assert unique([0,0]) == [0]

# -------------------------------------------------

def which_only_in_left(a,b):
    return [x for x in a if x not in b] 
def which_only_in_right(a,b):
    return which_only_in_left(b,a)
def which_in_both(a,b):
    return [x for x in a if x in b and x in a]

a = [1,2,3,4]
b = [3,4,10,100]
assert which_only_in_left(a,b) == [1,2]
assert which_only_in_right(a,b) == [10,100]
assert which_in_both(a,b) == [3,4]
assert get_duplicates(a + b) == [3,4,3,4]

# -------------------------------------------------

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
    seg = unpack_segments(segments)
    hdr = unpack_header_dict(header_dict)
    return seg, hdr
    
def get_spec_varnames(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return h    

def get_cfg_varnames(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return s
    
def get_user_defined_varnames(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return s+h

def get_overlapping_varnames_from_spec_and_cfg(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return which_in_both(s, h)

def get_tuple_of_user_defined_varname_derivatives(data_folder):
    s, h = get_spec_and_cfg_varnames(data_folder)
    return h, s, s+h, which_in_both(s, h)

def msg(text, total_list, verbose = VERBOSE_FLAG):
    unique_list = unique(total_list)
    count_msg = " ({0} total, {1} unique)".format(len(total_list), len(unique_list))
    if verbose:
        print("\n" + text + count_msg + ":\n", unique_list)
    else:
        print("\n" + text + count_msg)

def inspect_udf(data_folder):
    s, c, udf_vars, w =  get_tuple_of_user_defined_varname_derivatives(data_folder)
    msg("Varnames in spec and cfg/segments", udf_vars)
    msg("Varnames in spec", s)
    msg("Varnames in cfg/segments", c)
    msg("Overlapping varnames in spec and cfg/segments", w)

def get_db_varnames():
    return unique([get_var_abbr(x) for x in get_unique_labels()])

def get_varnames_not_in_db():
    db_vars = get_db_varnames()
    udf_vars = unique(get_user_defined_varnames(data_folder)) 
    return which_only_in_left(udf_vars,db_vars)
    
def inspect_db(data_folder):
    udf_vars = unique(get_user_defined_varnames(data_folder)) 
    msg("User-defined variables", udf_vars)
    db_vars = get_db_varnames()  
    msg("Variables in database", db_vars)  
    not_in_db = which_only_in_left(udf_vars,db_vars)
    msg("Not imported to database", not_in_db)

if __name__ == "__main__":
    data_folder = "data/2015/ind10"
    from kep.parser.csv2db import import_csv
    import_csv(data_folder)
    inspect_db(data_folder)
    print("\nTEST - following list must be empty: ", get_varnames_not_in_db())
    # assert below fails, must pass 
    # assert len(get_varnames_not_in_db()) == 0

# kep.parser.csv2db.import_csv() logic:
# - reads specification files spec and cfg <- this is inspect_db().udf_vars 
# - labels rows read from CSV file <- need check here
# - flattens rows into stream <- need check here
# - reads stream in database <- inspect_db() checks variables here

    from kep.parser.label_csv import get_labelled_rows
    from kep.parser.stream import stream_flat_data
    from kep.database.db import stream_to_database

    # def to_database(raw_data_file, spec_file, cfg_file = None):
    csv, spec, cfg = get_filenames(data_folder)
    lab_rows = get_labelled_rows(csv, spec, cfg)
    vq = 'PROD_AUTO_TRUCKS_AND_CHASSIS' # 'PROFIT'
    for x in lab_rows:
        if x[0] == vq: 
            print (x[0:5 ])
    db_rows = stream_flat_data(lab_rows)
    stream_to_database(db_rows)



# IGNORE ----------------------------------------------------------------
# NOTE: maybe check for duplicates in s or has_key
#       must pass len(lst) == len(unique(lst)), otherwise issue warning
#
#       count number of headers, proxy for total varnames
#
#       make_headers()
#------------------------------------------------------------------------