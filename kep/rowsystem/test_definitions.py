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