import os
 
def untest_cfg_import():
    write_spec_files()
    cfg = write_cfg()    
    assert SegmentList(cfg).segments == cfg_list    
    
def cmp_spec(doc,var):
    cnt = Segment(doc)._as_load_spec 
    assert var == cnt
            
#from rowsystem.tests.testdata import spec_ip_doc, spec_ip_trans_inv_doc, spec_cpi_block, spec_food_block, header_dicts, common_unit_dict, unit_dicts, null_segment_dict, cpi_segment_dict,  food_segment_dict
#from rowsystem.tests.testdata import join_header_dicts

def untest_spec():
    cmp_spec(doc=spec_ip_doc, var=(header_dicts['ip'], unit_dicts['ip'], null_segment_dict))
    
    cmp_spec(doc=spec_ip_trans_inv_doc, 
             var=(join_header_dicts(['ip','trans','investment']),
                  common_unit_dict, null_segment_dict))
                  
    cmp_spec(doc=spec_cpi_block, 
             var=(header_dicts['cpi_block'], unit_dicts['cpi_block'], cpi_segment_dict))

    cmp_spec(doc=spec_food_block, 
             var=(header_dicts['food_block'], unit_dicts['food_block'], food_segment_dict))
