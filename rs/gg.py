
# save 'glob_dict' to db table + mask some values
def get_title(name, glob_dict):
    
    if Label(name).head in glob_dict.keys():
        return glob_dict[name]
    else:
        return FILLER
    

#from db
def yield_var_name_components(self):        
    """Yields a list containing variable name, text description and unit of measurement."""        
    for var_name in self.get_saved_full_labels():
        lab = Label(var_name)
        yield [lab.labeltext, lab.head_description, lab.unit_description]
            
            
#from rs
def get_global_header_dict():
    """______________________."""
    glob_dict = {}
    for spec in self.segments:
        for k,v in spec.header_dict.items():
            glob_dict.update({k:v[0]})             
    return glob_dict

   
        
def get_title(name, ddict=None):
    if ddict is None:
        global default_dicts
        if default_dicts is None:
            default_dicts = get_complete_dicts(CURRENT_MONTH_DATA_FOLDER)
        ddict = default_dicts
    title_abbr = get_var_abbr(name)
    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr == two_labels_list[0]:
            return title
    return FILLER
    
def get_title(name, ddict=None):
    if ddict is None:
        global default_dicts
        if default_dicts is None:
            default_dicts = get_complete_dicts(CURRENT_MONTH_DATA_FOLDER)
        ddict = default_dicts
    title_abbr = get_var_abbr(name)
    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr == two_labels_list[0]:
            return title
    return FILLER

    
UNITS_ABBR = {
# --- part from unit dicts
    'rog': 'в % к предыдущему периоду',
    'rub': 'рублей',
    'yoy': 'в % к аналог. периоду предыдущего года' ,
    'ytd': 'с начала года'б
# --- part from header dicts
    'bln_t_km': 'млрд. т-км',
    'percent': '%',
    'bln_rub': 'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'mln': 'млн. человек',
    'mln_t': 'млн. т',
    'TWh': 'млрд. кВт·ч',
    'eop': 'на конец периода',
    'bln': 'млрд.',
    'units': 'штук',
    'th': 'тыс.',
}

def get_unit(name):
    unit_abbr = get_unit_abbr(name)
    if unit_abbr in UNITS_ABBR.keys():
        return UNITS_ABBR[unit_abbr]
    else:
        return FILLER    