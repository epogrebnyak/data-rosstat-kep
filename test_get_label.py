# -*- coding: utf-8 -*-


txt = """Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous month												
2002	81,4	101,1	102,6	107,5	94,2	105,2	102,5	102,5	105,8	95,6	89,1	103,3
отчетный месяц в % к соответствующему месяцу предыдущего года  / reporting month as percent of corresponding month of previous year												
2002	101,4	102,2	89,2	106,9	102,0	106,8	96,8	110,0	105,4	99,4	85,1	87,9
	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year												
2015	87,2	82,4	86,5	84,3	83,9	83,3						
"""

def stub_rows():
    for row in [x.split("\t") for x in txt.split("\n")]:
        yield row

ROWS_GEN = stub_rows()

a = "Производство транспортных средств и оборудования  / Manufacture of  transport equipment												"
assert a.startswith("Производство транспортных средств и оборудования") == True

b = "период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year"

headline_dict = {
"Производство транспортных средств и оборудования":  ['PROD_TRANS', None]
 }
 
support_dict =    {
 "отчетный месяц в % к предыдущему месяцу" : 'rog',
 "отчетный месяц в % к соответствующему месяцу предыдущего года": 'yoy',
 "период с начала отчетного года" : 'ytd'
 }

from word import get_label, yield_row_with_labels
#def get_label(text, lab_dict):
#    
#    LABEL_NOT_FOUND = 0
#    
#    for pat in lab_dict.keys():
#        if text.strip().startswith(pat): 
#            return lab_dict[pat]
#    else:
#         return LABEL_NOT_FOUND
#         
#def is_year(s):
#    try:
#        int(s)
#        return True        
#    except:
#        return False
#
#def adjust_labels(line, cur_labels, dict_headline, dict_support):
#    labels = cur_labels
#    z = get_label(line, dict_headline)
#    w = get_label(line, dict_support)         
#    if z:            
#       # reset to new var          
#       labels[0], labels[1] = z            
#    elif w:
#       # change unit
#       labels[1] = w
#    else: 
#       # unknown var
#       labels = ["unknown_var", "unknown_unit"]
#    return labels    
#   
#def yield_row_with_labels(incoming_gen, dict_headline, dict_support):
#    labels = ["unknown_var", "unknown_unit"]
#    for row in ROWS_GEN:
#        if len(row[0]) > 0:
#            if not is_year(row[0]):
#                labels = adjust_labels(row[0], labels, dict_headline, dict_support)
#            else:
#                # assign label and yeild
#                yield(labels + row)

assert get_label(a, headline_dict) ==  ['PROD_TRANS', None]
assert get_label(a, support_dict) == 0 
assert get_label(b, support_dict) == "ytd"

gen = yield_row_with_labels(ROWS_GEN, headline_dict, support_dict)
assert next(gen)[0:2] == ['PROD_TRANS', 'rog']
assert next(gen)[0:2] == ['PROD_TRANS', 'yoy']
assert next(gen)[0:2] == ['PROD_TRANS', 'ytd']