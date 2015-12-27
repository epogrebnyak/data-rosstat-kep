ip_raw_data_doc = """1.2. Индекс промышленного производства1)         / Industrial Production index1)																	
в % к соответствующему периоду предыдущего года  / percent of corresponding period of previous year																	
2014	101,7	101,1	101,8	101,5	102,1	99,8	102,1	101,4	102,4	102,8	100,4	101,5	100,0	102,8	102,9	99,6	103,9
в % к предыдущему периоду  / percent of previous period																	
2014		87,6	103,6	102,7	109,6	81,2	101,6	109,7	97,3	99,6	99,9	102,2	99,8	102,7	105,1	99,8	108,1
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year																	
2014						99,8	100,9	101,1	101,4	101,7	101,5	101,5	101,3	101,5	101,7	101,5	101,7"""

ip_spec_doc = """# Раздел 1. Специальная/дополнительная информация
# Section 1. Auxillary information
RUR_USD : read13

---
# Раздел 2. Единицы измерении
# Section 2. Units of measurement

в % к предыдущему периоду: rog
в % к соответствующему периоду предыдущего года: yoy

---
# Раздел 3. Определения переменных
# Section 3. Variable definitions
#
# Формат:
# Часть названия таблицы :
# - VAR_LABEL # sample label
# - bln_rub # sample units

#1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles

Инвестиции в основной капитал :
 - I
 - bln_rub
"""
ip_spec_dicts = {'headers':{'Инвестиции в основной капитал': ['I', 'bln_rub']},
                   'units':{'в % к предыдущему периоду': 'rog',
                            'в % к соответствующему периоду предыдущего года': 'yoy'}
                }

ip = {'raw_data_doc': ip_raw_data_doc, 'spec_doc': ip_spec_doc, 'spec_dicts': ip_spec_dicts}

from kep.file_io.common import docstring_to_file
from kep.file_io.specification import load_spec

def check_spec_and_doc_from_dict(cur_dict):
    # write cur_dict['spec_doc'] to file
    specpath = docstring_to_file(cur_dict['spec_doc'], 'spec.txt')
    # from file with cur_dict['spec_doc'] must obtain cur_dict['spec_dicts']
    dicts = load_spec(specpath)
    assert dicts[0] == cur_dict['spec_dicts']['headers']
    assert dicts[1] == cur_dict['spec_dicts']['units']

check_spec_and_doc_from_dict(ip)