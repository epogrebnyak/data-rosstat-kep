#
# TODO: add methods rs.head_lables() and id.head_labels()
#

def get_var_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))
assert get_var_abbr('PROD_E_TWh') == 'PROD_E' 

def get_unit_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))
assert get_unit_abbr('PROD_E_TWh') == 'TWh'

     
def unique(x):
    return sorted(list(set(x)))

# labels in rowsystem data    
def rowsystem_full_labels(rs):
    assert is_labelled(rs)
    varnames = unique(db_tuple_to_dict(t)['varname'] for t in stream_flat_data(rs))
    return sorted(varnames)    
    
def rowsystem_head_labels(rs):
    return unique([get_var_abbr(name) for name in rowsystem_full_labels(rs)])


folder = os.path.dirname(os.path.realpath(__file__))
rs = init_rowsystem_from_folder(folder)
print(rowsystem_head_labels(rs))    

    
    
# labels in definition files    
def definition_full_labels(folder):
     pass
     
def definition_full_labels(folder):
     pass

def get_user_defined_full_labels(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return unique(hdr+seg)

def get_user_defined_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return unique(hdr+seg)

def get_spec_and_cfg_varnames(data_folder):
    csv, default_spec, segments = get_folder_definitions(folder)
    header_dict = default_spec[0]
    hdr = unpack_header_dict(header_dict)
    seg = unpack_segments(segments)
    return hdr, seg
    
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
