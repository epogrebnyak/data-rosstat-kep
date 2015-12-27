# next:
# - check what data is used in specification testing, may also move to different folder
# - cfg file
# - data structure that is obtained when reading cfg

# also:
# - simplify yaml (two docs in it)

# --------------------------------------------------------------------------------
#1. TEST IMPORT OF HEADERS AND UNITS DICTS FROM SPEC FILES

#
#   WARNING:
#   New format of spec file applied - YAML now has two sections, not three, first (useless) section now depreciated
#   Using load_spec() for this. Must aplly in package
#   This file replaces tests in test/*/module/test_common_specification.
#

spec_ip_doc = """в % к соответствующему периоду предыдущего года: yoy
в % к предыдущему периоду : rog
период с начала отчетного года : ytd
---
Индекс промышленного производства:
  - IND_PROD
  - yoy
"""

spec_3headers_doc = """в % к соответствующему периоду предыдущего года: yoy
в % к предыдущему периоду : rog
период с начала отчетного года : ytd
---
Индекс промышленного производства:
  - IND_PROD
  - yoy

Производство транспортных средств и оборудования:
  - TRANS
  - Not specified
 
Инвестиции в основной капитал: 
  - INVESTMENT
  - bln_rub
"""

spec_cpi_block = """в % к соответствующему периоду предыдущего года: yoy
в % к предыдущему периоду : rog
период с начала отчетного года : ytd
---
Индекс потребительских цен: 
  - CPI
  - rog

непродовольственные товары:
   - CPI_NONFOOD
   - rog  
""" 

spec_food_block = """bln rubles : bln_rub
---
пищевые продукты, включая напитки, и табачные изделия :
 - SALES_FOOD
 - bln_rub
 
непродовольственные товары :
 - SALES_NONFOOD
 - bln_rub
""" 

header_dicts = {
'ip'        :{'Индекс промышленного производства': ['IND_PROD', 'yoy']},
'trans'     :{'Производство транспортных средств и оборудования': ['TRANS', 'Not specified']},
'investment':{'Инвестиции в основной капитал': ['INVESTMENT', 'bln_rub']},
'cpi_block' :{'Индекс потребительских цен': ['CPI', 'rog'], 
              'непродовольственные товары': ['CPI_NONFOOD', 'rog']},  
'food_block':{'пищевые продукты, включая напитки, и табачные изделия': ['SALES_FOOD','bln_rub'],
              'непродовольственные товары': ['SALES_NONFOOD', 'bln_rub']}
}

def join_header_dicts(vars):
    """Join headers dict of variables listed in *vars*."""
    headers = {}
    for key in vars:
      headers.update(header_dicts[key])
    return headers  

common_unit_dict = {'в % к соответствующему периоду предыдущего года': 'yoy',
'в % к предыдущему периоду' : 'rog',
'период с начала отчетного года' : 'ytd'}

unit_dicts = {
'ip'        : common_unit_dict,
'trans'     : common_unit_dict,
'investment': common_unit_dict,
'cpi_block' : common_unit_dict ,   
'food_block':{'bln rubles':'bln_rub'}
}

from kep.file_io.common import docstring_to_file
from kep.file_io.specification import load_spec
from kep.file_io.specification import load_cfg
import os

def compare_doc_to_spec_dicts(doc, ref_header_dict, ref_unit_dict):
    specpath = docstring_to_file(doc, 'spec.txt')
    dicts = load_spec(specpath)
    assert dicts[0] == ref_header_dict
    assert dicts[1] == ref_unit_dict    
    os.remove(specpath)

# test yaml specification, import from file and compare to ref dicts 
def test_specification_import():
    inputs = [ 
      [spec_ip_doc,       header_dicts['ip'],         unit_dicts['ip']]
    , [spec_3headers_doc, join_header_dicts(['ip','trans','investment']), common_unit_dict]
    , [spec_cpi_block,    header_dicts['cpi_block'],  unit_dicts['cpi_block']]
    , [spec_food_block,   header_dicts['food_block'], unit_dicts['food_block']]
    ]

    for i in inputs:
       compare_doc_to_spec_dicts(doc=i[0], ref_header_dict=i[1], ref_unit_dict=i[2])
# -----------------------------------------------------------------------------------
# 2. TEST IMPORT OF CONFIGURATION FILES

END_STRING = "EOF" 

# imagine we import *full_raw_doc* by segment. we would have a config file like *doc_cfg_file_content*:

cpi_additional_spec_filename = "cpi_spec.txt"
food_additional_spec_filename = "retail_spec.txt"

cpi_specpath = docstring_to_file(spec_cpi_block, cpi_additional_spec_filename)
food_specpath = docstring_to_file(spec_food_block, food_additional_spec_filename)

cpi_dicts  = (header_dicts['cpi_block'],  unit_dicts['cpi_block'])
food_dicts = (header_dicts['food_block'],  unit_dicts['food_block'])

doc_cfg_file_content = """- Индекс потребительских цен
- Из общего объема оборота розничной торговли
- {1}
---
- Из общего объема оборота розничной торговли
- {0}
- {2}""".format(END_STRING, cpi_additional_spec_filename, food_additional_spec_filename)
cfg_path = docstring_to_file(doc_cfg_file_content, 'cfg.txt')

ref_reading_of_cfg_file  = [
   ["Индекс потребительских цен", "Из общего объема оборота розничной торговли", cpi_additional_spec_filename]
  ,["Из общего объема оборота розничной торговли", END_STRING, food_additional_spec_filename]]

ref_qualified_cfg_contents = [
  ["Индекс потребительских цен", "Из общего объема оборота розничной торговли", cpi_dicts]
 ,["Из общего объема оборота розничной торговли", END_STRING, food_dicts]]

def test__adjust_path():
    # test a function in module
    from kep.file_io.specification import _adjust_path
    assert _adjust_path(os.path.join('temp', '_config.txt'), 'new.txt') == os.path.join('temp', 'new.txt')

def cfg_tests():
    # is cfg string equavalent to its reading? 
    import yaml
    assert list(yaml.load_all(doc_cfg_file_content)) == ref_reading_of_cfg_file 

    # is file with cfg string equavalent to its reading?
    from kep.file_io.specification import get_yaml
    assert get_yaml(cfg_path) == ref_reading_of_cfg_file 

    # does file with cfg string specify correct data structure?
    assert load_cfg(cfg_path) == ref_qualified_cfg_contents 
    
# -----------------------------------------------------------------------------------
# 3. RAW DATA (for reference, as big dict with variable tags as keys)
#

raw_data_docs = { 
'ip':"""1.2. Индекс промышленного производства1)         / Industrial Production index1)																	
в % к соответствующему периоду предыдущего года  / percent of corresponding period of previous year																	
2014	101,7	101,1	101,8	101,5	102,1	99,8	102,1	101,4	102,4	102,8	100,4	101,5	100,0	102,8	102,9	99,6	103,9
в % к предыдущему периоду  / percent of previous period																	
2014		87,6	103,6	102,7	109,6	81,2	101,6	109,7	97,3	99,6	99,9	102,2	99,8	102,7	105,1	99,8	108,1
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year																	
2014						99,8	100,9	101,1	101,4	101,7	101,5	101,5	101,3	101,5	101,7	101,5	101,7"""

, 'trans': """Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous month												
2015	31,1	126,3	139,8	83,8	94,6	115,8						
отчетный месяц в % к соответствующему месяцу предыдущего года  / reporting month as percent of corresponding month of previous year												
2015	87,2	77,6	94,8	77,8	82,2	80,1						
	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year												
2015	87,2	82,4	86,5	84,3	83,9	83,3						"""

, 'investment':"""1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles																	
2014	13527,7	1863,8	2942,0	3447,6	5274,3	492,2	643,2	728,4	770,4	991,1	1180,5	1075,1	1168,5	1204,0	1468,5	1372,5	2433,3
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2014	97,3	94,7	98,1	98,5	97,2	92,7	95,5	95,3	97,4	97,3	99,3	99,1	98,4	98,1	99,2	92,2	98,9
в % к предыдущему периоду  / percent of previous period																	
2014		35,7	158,2	114,9	149,9	21,1	129,6	114,5	106,6	127,0	119,0	90,5	107,1	103,3	121,6	92,7	173,8"""
#note: both cpi_block and food_block contain "непродовольственные товары", when importing 
#      text string cpi_block + food_block must use segment specification and config file
, 'cpi_block':"""3.5. Индекс потребительских цен (на конец периода, в % к концу предыдущего периода) / Consumer Price Index (end of period, percent of end of previous period)																	
1999	136,5	116,0	107,3	105,6	103,9	108,4	104,1	102,8	103,0	102,2	101,9	102,8	101,2			
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
непродовольственные товары / non-food products																	
1999	139,2	114,0	108,6	107,2	104,9	106,2	104,0	103,2	104,0	102,7	101,6	101,9	102,4	
"""
, 'food_block':"""Из общего объема оборота розничной торговли:																	
пищевые продукты, включая напитки, и табачные изделия1), млрд.рублей / Of total volume of retail trade turnover: food products, including beverages, and tobacco1),																	
bln rubles																	
1999	866,1	186,8	204,3	222,6	252,4	60,3	60,7	65,8	66,2	68,6	69,5	71,6	74,0	77,0	79,1	79,1	94,2
2015		79,1	101,8	103,7		70,4	96,4	107,1	97,2	102,4	99,3	103,0	101,5	97,9	101,4		
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
непродовольственные товары1), млрд.рублей / non-food goods1), bln rubles																	
1999	931,3	192,2	212,2	242,0	284,9	61,5	62,2	68,5	69,2	70,3	72,7	74,2	83,6	84,2	88,0	91,1	105,8
"""
# will use end_string to capture segment that is at the end of file 
, 'end_string':END_STRING 
}

# -----------------------------------------------------------------------------------
# 4. FOR FURTHER TESTING:

ordered_keys = ['ip', 'trans', 'investment', 'cpi_block', 'food_block', 'end_string']
full_raw_doc = ("\n"*5).join([raw_data_docs[key] for key in ordered_keys])


