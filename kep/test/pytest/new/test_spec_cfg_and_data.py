import os
import io
import pandas as pd
from pandas.util.testing import assert_frame_equal   

from kep.file_io.common import docstring_to_file
from kep.file_io.specification import load_spec
from kep.file_io.specification import load_cfg
   
# --------------------------------------------------------------------------------
#1. TEST IMPORT OF HEADERS AND UNITS DICTS FROM SPEC FILES
#

# ---- strings/docs ----
unit_definition = """в % к соответствующему периоду предыдущего года: yoy
в % к предыдущему периоду : rog
отчетный месяц в % к предыдущему месяцу : rog
отчетный месяц в % к соответствующему месяцу предыдущего года : yoy
период с начала отчетного года : ytd
\n"""

spec_ip_doc = unit_definition + """---
Индекс промышленного производства:
  - IND_PROD
  - yoy
"""

spec_3headers_doc = unit_definition + """---
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

spec_cpi_block = unit_definition +  """---
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

# ---- header and unit dicts ----

header_dicts = {
'ip'        :{'Индекс промышленного производства': ['IND_PROD', 'yoy']},
'trans'     :{'Производство транспортных средств и оборудования': ['TRANS', 'Not specified']},
'investment':{'Инвестиции в основной капитал': ['INVESTMENT', 'bln_rub']},
'cpi_block' :{'Индекс потребительских цен': ['CPI', 'rog'], 
              'непродовольственные товары': ['CPI_NONFOOD', 'rog']},  
'food_block':{'пищевые продукты, включая напитки, и табачные изделия': ['SALES_FOOD','bln_rub'],
              'непродовольственные товары': ['SALES_NONFOOD', 'bln_rub']}
}

common_unit_dict = {'в % к соответствующему периоду предыдущего года': 'yoy',
'в % к предыдущему периоду' : 'rog',
'отчетный месяц в % к предыдущему месяцу' : 'rog',
'отчетный месяц в % к соответствующему месяцу предыдущего года' : 'yoy',
'период с начала отчетного года' : 'ytd'}

unit_dicts = {
'ip'        : common_unit_dict,
'trans'     : common_unit_dict,
'investment': common_unit_dict,
'cpi_block' : common_unit_dict ,   
'food_block':{'bln rubles':'bln_rub'}
}

# ---- support functions ----

def join_header_dicts(vars):
    """Join headers dict of variables listed in *vars*."""
    headers = {}
    for key in vars:
      headers.update(header_dicts[key])
    return headers  

def compare_doc_to_spec_dicts(doc, ref_header_dict, ref_unit_dict):
    specpath = docstring_to_file(doc, 'spec.txt')
    dicts = load_spec(specpath)
    assert dicts[0] == ref_header_dict
    assert dicts[1] == ref_unit_dict    
    os.remove(specpath)

# ---- test yaml specification, import specifiction from file and compare to ref dicts ----
def test_specification_import():
    inputs = [ 
      [spec_ip_doc,       header_dicts['ip'],         unit_dicts['ip']]
    , [spec_cpi_block,    header_dicts['cpi_block'],  unit_dicts['cpi_block']]
    , [spec_food_block,   header_dicts['food_block'], unit_dicts['food_block']]
    ]

    for i in inputs:
       compare_doc_to_spec_dicts(doc=i[0], ref_header_dict=i[1], ref_unit_dict=i[2])

def test_specification_import_for_bigger_doc():
    compare_doc_to_spec_dicts(doc=spec_3headers_doc, 
                              ref_header_dict=join_header_dicts(['ip','trans','investment'])  , 
                              ref_unit_dict=common_unit_dict)
    
    
       
# -----------------------------------------------------------------------------------
# 2. TEST IMPORT OF CONFIGURATION FILE - A COMBO OF SPEC FILES
#

# ---- strings/docs ----
# imagine we import *full_raw_doc* by segment. we would have a config file like *doc_cfg_file_content*:
END_STRING = "EOF" 
cpi_additional_spec_filename = "cpi_spec.txt"
food_additional_spec_filename = "retail_spec.txt"
doc_cfg_file_content = """- 3.5. Индекс потребительских цен
- Из общего объема оборота розничной торговли
- {1}
---
- Из общего объема оборота розничной торговли
- {0}
- {2}""".format(END_STRING, cpi_additional_spec_filename, food_additional_spec_filename)

# ---- header and unit dicts ----

cpi_dicts  = (header_dicts['cpi_block'],  unit_dicts['cpi_block'])
food_dicts = (header_dicts['food_block'],  unit_dicts['food_block'])

ref_reading_of_cfg_file  = [
   ["Индекс потребительских цен", "Из общего объема оборота розничной торговли", cpi_additional_spec_filename]
  ,["Из общего объема оборота розничной торговли", END_STRING, food_additional_spec_filename]]

ref_qualified_cfg_contents = [
  ["Индекс потребительских цен", "Из общего объема оборота розничной торговли", cpi_dicts]
 ,["Из общего объема оборота розничной торговли", END_STRING, food_dicts]]

# ---- file paths ---- 
cpi_specpath = docstring_to_file(spec_cpi_block, cpi_additional_spec_filename)
food_specpath = docstring_to_file(spec_food_block, food_additional_spec_filename)
cfg_path = docstring_to_file(doc_cfg_file_content, 'cfg.txt')

# ---- testing cfg files ---- 

def cfg_tests():
    # can cfg content be retrieved from string/doc? 
    import yaml
    assert list(yaml.load_all(doc_cfg_file_content)) == ref_reading_of_cfg_file 

    # can cfg content be retrieved from cfg file?
    from kep.file_io.specification import get_yaml
    assert get_yaml(cfg_path) == ref_reading_of_cfg_file 

    # does file with cfg string specify correct data structure?
    assert load_cfg(cfg_path) == ref_qualified_cfg_contents 
    
# -----------------------------------------------------------------------------------
# 3.1 RAW DATA (for reference)
#

raw_data_docs = { 
'ip':"""1.2. Индекс промышленного производства1)         / Industrial Production index1)																	
в % к соответствующему периоду предыдущего года  / percent of corresponding period of previous year																	
2014	101,7	101,1	101,8	101,5	102,1	99,8	102,1	101,4	102,4	102,8	100,4	101,5	100,0	102,8	102,9	99,6	103,9
в % к предыдущему периоду / percent of previous period																	
2014		87,6	103,6	102,7	109,6	81,2	101,6	109,7	97,3	99,6	99,9	102,2	99,8	102,7	105,1	99,8	108,1
	Год / Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
период с начала отчетного года в % к соответствующему периоду предыдущего года / period from beginning of reporting year as percent of corresponding period of previous year																	
2014						99,8	100,9	101,1	101,4	101,7	101,5	101,5	101,3	101,5	101,7	101,5	101,7"""

, 'trans': """Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous month												
2014	45,4	131,8	123,9	102,3	88,8	116,3	98,4	84,0	123,4	100,7	112,3	141,6
отчетный месяц в % к соответствующему месяцу предыдущего года / reporting month as percent of corresponding month of previous year												
2014	103,8	113,2	114,2	119,6	118,3	111,7	122,0	90,9	111,4	109,8	95,5	91,0
	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.
период с начала отчетного года в % к соответствующему периоду предыдущего года / period from beginning of reporting year as percent of corresponding period of previous year												
2014	103,8	108,9	111,0	113,4	114,8	114,2	114,8	111,8	111,8	111,6	110,1	108,5"""

, 'investment':"""1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles																	
2014	13527,7	1863,8	2942,0	3447,6	5274,3	492,2	643,2	728,4	770,4	991,1	1180,5	1075,1	1168,5	1204,0	1468,5	1372,5	2433,3
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2014	97,3	94,7	98,1	98,5	97,2	92,7	95,5	95,3	97,4	97,3	99,3	99,1	98,4	98,1	99,2	92,2	98,9
в % к предыдущему периоду  / percent of previous period																	
2014		35,7	158,2	114,9	149,9	21,1	129,6	114,5	106,6	127,0	119,0	90,5	107,1	103,3	121,6	92,7	173,8"""

#NOTE: both cpi_block and food_block contain "непродовольственные товары", when importing 
#      text string cpi_block + food_block must use segment specification and config file

, 'cpi_block':"""3.5. Индекс потребительских цен (на конец периода, в % к концу предыдущего периода) / Consumer Price Index (end of period, percent of end of previous period)																	
2014	111,4	102,3	102,4	101,4	104,8	100,6	100,7	101,0	100,9	100,9	100,6	100,5	100,2	100,7	100,8	101,3	102,6
в том числе: / of which:																	
продукты питания / food products																	
2014	115,7	103,7	103,5	100,4	107,4	100,9	101,1	101,7	101,3	101,5	100,7	99,8	99,5	101,1	101,3	102,3	103,7
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
алкогольные напитки / alcoholic beverages																	
2014	113,7	106,0	103,3	102,3	101,6	101,6	102,0	102,3	101,2	101,2	100,8	100,6	101,1	100,6	100,5	100,5	100,7
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
непродовольственные товары / non-food products																	
2014	108,1	101,4	101,5	101,4	103,6	100,3	100,4	100,7	100,6	100,5	100,4	100,4	100,5	100,6	100,6	100,6	102,3
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
услуги / services																	
2014	110,5	101,4	102,4	102,4	104,0	100,5	100,4	100,5	100,7	100,8	100,9	101,4	100,7	100,3	100,6	101,2	102,2
"""
, 'food_block':"""	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
Из общего объема оборота розничной торговли:																	
пищевые продукты, включая напитки, и табачные изделия1), млрд.рублей / Of total volume of retail trade turnover: food products, including beverages, and tobacco1),																	
bln rubles	
2014	12380,9	2729,6	2966,3	3140,1	3544,9	882,7	884,5	962,4	963,6	999,4	1003,3	1034,0	1061,8	1044,3	1084,6	1097,9	1362,4
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
непродовольственные товары1), млрд.рублей / non-food goods1), bln rubles																	
2014	13975,3	3063,3	3290,4	3557,2	4064,4	984,4	986,8	1092,1	1079,3	1095,6	1115,5	1158,2	1202,0	1197,0	1226,3	1245,7	1592,4
"""

# NOTE: will use *end_string* to capture segment that is at the end of file 
, 'end_string':END_STRING 

}

# -----------------------------------------------------------------------------------
# 3.2 MORE DATA FOR FURTHER TESTING:

ordered_keys = ['ip', 'trans', 'investment', 'cpi_block', 'food_block', 'end_string']
full_raw_doc = ("\n"*5).join([raw_data_docs[key] for key in ordered_keys])

# save it as temp file 
csv_path = docstring_to_file(full_raw_doc, 'csv.txt')

# save specs
# WARNING: when using 'spec.txt' - the file is overwritten somehow beofr it gets to test_full_import(). py.test fixture, perhaps?
spec_path = docstring_to_file(spec_3headers_doc, '__spec.txt')
extra_spec1 = docstring_to_file(spec_cpi_block, cpi_additional_spec_filename)
extra_spec2 = docstring_to_file(spec_food_block, food_additional_spec_filename)

# save cfg 
cfg_path = docstring_to_file(doc_cfg_file_content, '__cfg.txt')

dfa_csv = 'year,CPI_NONFOOD_rog,CPI_rog,IND_PROD_yoy,INVESTMENT_bln_rub,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub\n2014,108.1,111.4,101.7,13527.7,97.3,12380.9,13975.3\n'
dfq_csv = 'time_index,year,qtr,CPI_NONFOOD_rog,CPI_rog,IND_PROD_rog,IND_PROD_yoy,INVESTMENT_bln_rub,INVESTMENT_rog,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub\n2014-03-31,2014,1,101.4,102.3,87.6,101.1,1863.8,35.7,94.7,2729.6,3063.3\n2014-06-30,2014,2,101.5,102.4,103.6,101.8,2942.0,158.2,98.1,2966.3,3290.4\n2014-09-30,2014,3,101.4,101.4,102.7,101.5,3447.6,114.9,98.5,3140.1,3557.2\n2014-12-31,2014,4,103.6,104.8,109.6,102.1,5274.3,149.9,97.2,3544.9,4064.4\n'
dfm_csv = 'time_index,year,month,CPI_NONFOOD_rog,CPI_rog,IND_PROD_rog,IND_PROD_yoy,IND_PROD_ytd,INVESTMENT_bln_rub,INVESTMENT_rog,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub,TRANS_rog,TRANS_yoy,TRANS_ytd\n2014-01-31,2014,1,100.3,100.6,81.2,99.8,99.8,492.2,21.1,92.7,882.7,984.4,45.4,103.8,103.8\n2014-02-28,2014,2,100.4,100.7,101.6,102.1,100.9,643.2,129.6,95.5,884.5,986.8,131.8,113.2,108.9\n2014-03-31,2014,3,100.7,101.0,109.7,101.4,101.1,728.4,114.5,95.3,962.4,1092.1,123.9,114.2,111.0\n2014-04-30,2014,4,100.6,100.9,97.3,102.4,101.4,770.4,106.6,97.4,963.6,1079.3,102.3,119.6,113.4\n2014-05-31,2014,5,100.5,100.9,99.6,102.8,101.7,991.1,127.0,97.3,999.4,1095.6,88.8,118.3,114.8\n2014-06-30,2014,6,100.4,100.6,99.9,100.4,101.5,1180.5,119.0,99.3,1003.3,1115.5,116.3,111.7,114.2\n2014-07-31,2014,7,100.4,100.5,102.2,101.5,101.5,1075.1,90.5,99.1,1034.0,1158.2,98.4,122.0,114.8\n2014-08-31,2014,8,100.5,100.2,99.8,100.0,101.3,1168.5,107.1,98.4,1061.8,1202.0,84.0,90.9,111.8\n2014-09-30,2014,9,100.6,100.7,102.7,102.8,101.5,1204.0,103.3,98.1,1044.3,1197.0,123.4,111.4,111.8\n2014-10-31,2014,10,100.6,100.8,105.1,102.9,101.7,1468.5,121.6,99.2,1084.6,1226.3,100.7,109.8,111.6\n2014-11-30,2014,11,100.6,101.3,99.8,99.6,101.5,1372.5,92.7,92.2,1097.9,1245.7,112.3,95.5,110.1\n2014-12-31,2014,12,102.3,102.6,108.1,103.9,101.7,2433.3,173.8,98.9,1362.4,1592.4,141.6,91.0,108.5\n'


# -----------------------------------------------------------------------------------
# 3.3 END-TO-END 'FURTHER TESTING':

from kep.importer.csv2db import to_database
from kep.inspection.var_check import get_target_and_actual_varnames_by_file
from kep.database.db import wipe_db_tables
from kep.query.end_user import get_reshaped_dfs

def load_db_sample():
   wipe_db_tables()
   to_database(raw_data_file=csv_path, spec_file=spec_path, cfg_file=cfg_path)

def test_full_import():
    load_db_sample()
    labels_in_spec, labels_in_db = get_target_and_actual_varnames_by_file(spec_path, cfg_path)
    assert labels_in_spec == labels_in_db 
    assert labels_in_spec == ['CPI', 'CPI_NONFOOD', 'IND_PROD', 'INVESTMENT', 'SALES_FOOD', 'SALES_NONFOOD', 'TRANS']
    
def test_df_csvs():
   load_db_sample()
   dfa, dfq, dfm = get_reshaped_dfs()
   assert dfa.to_csv() == dfa_csv 
   assert dfq.to_csv() == dfq_csv 
   assert dfm.to_csv() == dfm_csv 

   
#def teardown_module(module):
#   # cleanup for files created
#   for fn in [csv_path, spec_path, cfg_path, extra_spec1, extra_spec2]:
#      if os.path.exists(fn):
#          os.remove(fn)

