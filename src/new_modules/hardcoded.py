# -*- coding: utf-8 -*-
"""Hardcoded inputs"""

ip ="""1.2. Индекс промышленного производства1)         / Industrial Production index1)																	
в % к соответствующему периоду предыдущего года  / percent of corresponding period of previous year																	
2014	101,7	101,1	101,8	101,5	102,1	99,8	102,1	101,4	102,4	102,8	100,4	101,5	100,0	102,8	102,9	99,6	103,9
в % к предыдущему периоду  / percent of previous period																	
2014		87,6	103,6	102,7	109,6	81,2	101,6	109,7	97,3	99,6	99,9	102,2	99,8	102,7	105,1	99,8	108,1
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year																	
2014						99,8	100,9	101,1	101,4	101,7	101,5	101,5	101,3	101,5	101,7	101,5	101,7"""

parsed_ip = [
 ['PROD', 'yoy', '2014', '101,7', '101,1', '101,8', '101,5', '102,1', '99,8', '102,1', '101,4', '102,4', '102,8', '100,4', '101,5', '100,0', '102,8', '102,9', '99,6', '103,9']
,['PROD', 'rog', '2014', '', '87,6', '103,6', '102,7', '109,6', '81,2', '101,6', '109,7', '97,3', '99,6', '99,9', '102,2', '99,8', '102,7', '105,1', '99,8', '108,1']
,['PROD', 'rytd', '2014', '', '', '', '', '', '99,8', '100,9', '101,1', '101,4', '101,7', '101,5', '101,5', '101,3', '101,5', '101,7', '101,5', '101,7']
]


trans = """Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous month												
2015	31,1	126,3	139,8	83,8	94,6	115,8						
отчетный месяц в % к соответствующему месяцу предыдущего года  / reporting month as percent of corresponding month of previous year												
2015	87,2	77,6	94,8	77,8	82,2	80,1						
	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year												
2015	87,2	82,4	86,5	84,3	83,9	83,3						"""

parsed_trans = [
 ['PROD_TRANS', 'rog', '2015', '31,1', '126,3', '139,8', '83,8', '94,6', '115,8', '', '', '', '', '', '']
,['PROD_TRANS', 'yoy', '2015', '87,2', '77,6', '94,8', '77,8', '82,2', '80,1', '', '', '', '', '', '']
,['PROD_TRANS', 'rytd', '2015', '87,2', '82,4', '86,5', '84,3', '83,9', '83,3', '', '', '', '', '', '']
]

investment = """1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles																	
2014	13527,7	1863,8	2942,0	3447,6	5274,3	492,2	643,2	728,4	770,4	991,1	1180,5	1075,1	1168,5	1204,0	1468,5	1372,5	2433,3
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2014	97,3	94,7	98,1	98,5	97,2	92,7	95,5	95,3	97,4	97,3	99,3	99,1	98,4	98,1	99,2	92,2	98,9
в % к предыдущему периоду  / percent of previous period																	
2014		35,7	158,2	114,9	149,9	21,1	129,6	114,5	106,6	127,0	119,0	90,5	107,1	103,3	121,6	92,7	173,8"""

parsed_investment = [
 ['I', 'bln_rub', '2014', '13527,7', '1863,8', '2942,0', '3447,6', '5274,3', '492,2', '643,2', '728,4', '770,4', '991,1', '1180,5', '1075,1', '1168,5', '1204,0', '1468,5', '1372,5', '2433,3']
,['I', 'yoy', '2014', '97,3', '94,7', '98,1', '98,5', '97,2', '92,7', '95,5', '95,3', '97,4', '97,3', '99,3', '99,1', '98,4', '98,1', '99,2', '92,2', '98,9']
,['I', 'rog', '2014', '', '35,7', '158,2', '114,9', '149,9', '21,1', '129,6', '114,5', '106,6', '127,0', '119,0', '90,5', '107,1', '103,3', '121,6', '92,7', '173,8']
]

ft = """1.10. Внешнеторговый оборот – всего1),  млрд.долларов США / Foreign trade turnover – total1),  bln US dollars																	
1999	115,1	24,4	27,2	28,4	35,1	7,2	7,9	9,3	9,8	8,0	9,3	9,5	9,3	9,6	10,4	11,1	13,7"""

RAW_FILE = '_raw.txt'

def docstring_to_file(docstring, filename):
    with open(filename,"w") as f:
        f.write(docstring)
    return filename

def init_raw_csv_file():
    doc = "\n".join([ip,trans,investment])
    return docstring_to_file(doc, RAW_FILE)    

PARSED_RAW_FILE_AS_LIST = parsed_ip + parsed_trans + parsed_investment



# -----------------------------------------------------------------------------
# Specification dictionaries import

yaml_main = """PROD_TRANS: read12
---
в % к соответствующему периоду предыдущего года : yoy
в % к предыдущему периоду : rog
период с начала отчетного года : rytd
отчетный месяц в % к предыдущему месяцу : yoy
отчетный месяц в % к соответствующему месяцу предыдущего года : yoy
в % к соответствующему месяцу предыдущего года : yoy
отчетный месяц в % к предыдущему месяцу : rog 
в % к предыдущему периоду : rog
---
1.2. Индекс промышленного производства :
  - PROD
  - yoy
1.7. Инвестиции в основной капитал :
  - I
  - bln_rub 
Производство транспортных средств и оборудования :
  - PROD_TRANS
  - yoy"""

MAIN_YAML_FILENAME = "_spec.txt" 
  
def init_main_yaml():    
    return docstring_to_file(yaml_main, MAIN_YAML_FILENAME)
    
REF_HEADER_DICT = {'Производство транспортных средств и оборудования': ['PROD_TRANS', 'yoy'], 
'1.7. Инвестиции в основной капитал': ['I', 'bln_rub'], 
'1.2. Индекс промышленного производства': ['PROD', 'yoy']}

REF_UNIT_DICT = {'период с начала отчетного года': 'rytd', 
'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy', 
'отчетный месяц в % к предыдущему месяцу': 'rog', 
'в % к предыдущему периоду': 'rog', 
'в % к соответствующему месяцу предыдущего года': 'yoy', 
'в % к соответствующему периоду предыдущего года': 'yoy'}





REF_SEGMENT_SPEC = [# список
 
[  # первая и вторая строка сегмента
  'Производство транспортных средств и оборудования', 
  '1.7. Инвестиции в основной капитал', 
  # кортеж из словарей header dict и unit dict 
  ({'1.2. Индекс промышленного производства': ['PROD', 'yoy'], 
   'Производство транспортных средств и оборудования': ['PROD_TRANS', 'yoy'], 
   '1.7. Инвестиции в основной капитал': ['I', 'bln_rub']}, 
  {'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy', 
  'отчетный месяц в % к предыдущему месяцу': 'rog', 'в % к предыдущему периоду': 'rog', 
  'период с начала отчетного года': 'rytd', 
  'в % к соответствующему месяцу предыдущего года': 'yoy', 
  'в % к соответствующему периоду предыдущего года': 'yoy'})]
  
  ]




















ADDITIONAL_YAML_FILENAME = "_spec_1.txt"

# temporarily use same contents for additional yaml
def init_additional_yaml():    
    return docstring_to_file(yaml_main, ADDITIONAL_YAML_FILENAME)



# снчала идет общий файл,
# потом идут прочие конфиги
#    начальная строка
#    конецчная строка
#    название конфига для сегментов
# пока не разираем случай от начала файла и до конца файла
yaml_config="""_spec.txt
---
- Производство транспортных средств и оборудования
- 1.7. Инвестиции в основной капитал
- _spec_1.txt"""

CONFIG_YAML_FILENAME = "_config.txt"
def init_config_yaml():    
    return docstring_to_file(yaml_config, CONFIG_YAML_FILENAME)
    


