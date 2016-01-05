# -*- coding: utf-8 -*-

from kep.file_io.common import get_filenames, get_var_abbr
from kep.file_io.specification import load_cfg, load_spec
from kep.database.db import get_unique_labels
import kep.query.var_names

# --------------------------------------------------
def get_definitions_from_folder(data_folder):
    csv, spec, cfg = get_filenames(data_folder)
    segments = load_cfg(cfg)
    header_dict, unit_dict = load_spec(spec)
    return segments, header_dict, unit_dict  

# -------------------------------------------------
def get_complete_dicts(data_folder):
    csv, spec, cfg = get_filenames(data_folder)
    return get_complete_dicts_by_filename(spec, cfg)
    
def get_complete_dicts_by_filename(spec_file, cfg_file):
    header_dict, unit_dict = load_spec(spec_file)
    segments = load_cfg(cfg_file)
    for seg in segments:
        #third element in seg (seg[2]) is a tuple of header_dict and unit_dict
        seg_header_dict = seg[2][0]
        seg_unit_dict   = seg[2][1]
        #this operation will eat up/destroy information of duplicate keys  
        header_dict.update(seg_header_dict)
        unit_dict.update(seg_unit_dict)
    return header_dict, unit_dict

# -------------------------------------------------
def get_spec_and_cfg_varnames(data_folder):
    segments, header_dict, unit_dict = get_definitions_from_folder(data_folder)
    hdr = unpack_header_dict(header_dict)
    seg = unpack_segments(segments)
    return hdr, seg
    
def get_spec_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return hdr    

def get_cfg_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return seg
    
def unpack_header_dict(header_dict):
   """Get varnames from header_dict"""
   return list(x[0] for x in header_dict.values())

def unpack_segments(segments):
   """Get varnames from segments"""
   var_list = []
   for seg in segments:
       seg_var_list =  unpack_header_dict(seg[2][0])       
       var_list.extend(seg_var_list)
   return var_list 

# ----------------- 
    
def get_user_defined_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return unique(hdr+seg)

def get_user_defined_varnames_by_filename(spec_path, cfg_path):
    segments = load_cfg(cfg_path)
    header_dict, unit_dict = load_spec(spec_path)
    hdr = unpack_header_dict(header_dict)
    seg = unpack_segments(segments)
    return unique(hdr+seg)
    
# -----------------   
    
def get_target_and_actual_varnames_by_file(spec_path, cfg_path):
    labels_in_spec = sorted(get_user_defined_varnames_by_filename(spec_path, cfg_path))
    labels_in_db   = sorted(get_db_varnames())
    return labels_in_spec, labels_in_db 

def get_target_and_actual_varnames_by_folder(data_folder):
    csv, spec_path, cfg_path = get_filenames(data_folder)    
    return get_target_and_actual_varnames_by_file(spec_path, cfg_path)    

# -----------------    
   
def msg(text, total_list, verbose = True):
    unique_list = unique(total_list)
    count_msg = " ({0} total, {1} unique)".format(len(total_list), len(unique_list))
    if verbose:
        print("\n" + text + count_msg + ":\n", unique_list)
    else:
        print(text + count_msg)
    
def inspect_user_varnames(data_folder):
    from_spec, from_cfg = get_spec_and_cfg_varnames(data_folder)
    all_user_varnames = from_spec+from_cfg
    overlap = which_in_both(from_spec, from_cfg)
    def _msg_block(verbose_flag):
        msg("1. Varnames in spec and cfg/segments", all_user_varnames, verbose_flag)
        msg("2. Varnames in spec", from_spec, verbose_flag)
        msg("3. Varnames in cfg/segments", from_cfg, verbose_flag)
        msg("4. Overlapping varnames in spec and cfg/segments", overlap, verbose_flag)
    _msg_block(True)
    print("\nSummary:")
    _msg_block(False)

# -----------------    

def inspect_db(data_folder):
    udf_vars = unique(get_user_defined_varnames(data_folder)) 
    # msg("User-defined variables", udf_vars)
    db_vars = get_db_varnames()
    msg("1. Variables in database", db_vars)
    not_in_db = which_only_in_left(udf_vars,db_vars)
    msg("2. Not imported to database", not_in_db)

def notify_on_import_result(data_folder):
    not_imported = get_varnames_not_in_db(data_folder)
    n = len(unique(get_db_varnames()))
    if len(not_imported) == 0:
        print("All user defined variables imported to database.")
    else:
        print("Not imported tо database: ", ",".join(not_imported))
    print("Total variables in database: {}".format(n)) 
    kep.query.var_names.print_varlist_two_columns()

# -----------------    
   
def get_db_varnames():
    return unique([get_var_abbr(x) for x in get_unique_labels()])

def get_varnames_not_in_db(data_folder):
    db_vars = get_db_varnames()
    udf_vars = unique(get_user_defined_varnames(data_folder)) 
    return which_only_in_left(udf_vars,db_vars)

# -------------------------------------------------

def count_entries(z, list_):
    count = 0
    for x in list_:
       if z == x:
           count += 1
    return count 

#assert count_entries("a", ["a","a","b"]) == 2
#assert count_entries("b", ["a","a","b"]) == 1

def get_duplicates(full_list):
    ix = [count_entries(x,full_list) > 1 for x in full_list]
    return [full_list[i] for i, flag in enumerate(ix) if flag]

#assert get_duplicates(["a","a","b"]) == ["a","a"]

# -------------------------------------------------

def unique(list_):
    return sorted(list(set(list_)))
#assert unique([0,0]) == [0]

# -------------------------------------------------

def which_only_in_left(a,b):
    return [x for x in a if x not in b] 
def which_only_in_right(a,b):
    return which_only_in_left(b,a)
def which_in_both(a,b):
    return [x for x in a if x in b and x in a]

#a = [1,2,3,4]
#b = [3,4,10,100]
#assert which_only_in_left(a,b) == [1,2]
#assert which_only_in_right(a,b) == [10,100]
#assert which_in_both(a,b) == [3,4]
#assert get_duplicates(a + b) == [3,4,3,4]
