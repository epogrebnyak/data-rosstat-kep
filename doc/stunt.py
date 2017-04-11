# -*- coding: utf-8 -*-

import yaml
from collections import OrderedDict

# -----------------------------------------------------------------------------
#
# Generic transform functions
#
# -----------------------------------------------------------------------------

def doc_to_lists(doc: str) -> list:
    """Splits string by EOL and tabs, returns list of lists.
    Emulates csv.reader output. 
    
    FIXME: \n screws the doctest below
    doc_to_lists('2015\t99,2\t99,9\n2016\t101,3\t101,1')
    [['2015', '99,2', '99,9'], ['2016', '101,3', '101,1']]"""
    return [r.split('\t') for r in doc.split('\n')]


def parse_spec_text(yaml_string):
    """Parse specification from YAML document to dictionary."""
    content = list(yaml.load_all(yaml_string))
    return { 'scope': { 'start_line':  content[0]['start line'],
                          'end_line':  content[0]['end line']},
             'reader_func': content[0]['special reader'],
             'units':   content[1],
             'table_headers': content[2]
             }

# -----------------------------------------------------------------------------
#
# CSV proxy
#
# -----------------------------------------------------------------------------

doc_a = """
	Год / Year	Кварталы / Quarters			
		I	II	III	IV
1. Сводные показатели / Aggregated indicators					
1.1. Валовой внутренний продукт1) / Gross domestic product1)					
Объем ВВП, млрд.рублей /GDP, bln rubles					
2013	71017	15892	17015	18543	19567
20142)	79200	17139	18884	20407	21515
20152)	83233	18210	19284	21294	22016
20162)	85881	18561	19979	22190	
2017					
Индекс физического объема произведенного ВВП, в % / Volume index of produced GDP, percent					
2013	101,3	100,6	101,1	101,2	102,1
20142)	100,7	100,6	101,1	100,9	100,2
20152)	97,2	97,2	95,5	96,3	96,2
20162)	99,8	98,8	99,4	99,6	
2017					
"""

doc_b = """
	Год / Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
1.2. Индекс промышленного производства1) / Industrial Production index1)																	
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2015	99,2	99,9	98,3	99,5	99,1	100,0	98,2	101,2	98,2	97,6	99,1	98,5	100,2	99,7	98,4	101,0	98,1
2016	101,3	101,1	101,5	101,0	101,7	99,2	103,8	100,3	101,0	101,5	102,0	101,4	101,5	100,1	101,6	103,4	100,2
2017						102,3	97,3										
в % к предыдущему периоду / percent of previous period																	
2015		82,8	102,6	103,9	112,3	73,9	99,8	112,5	95,6	97,6	103,2	100,5	101,4	103,1	105,0	101,9	109,1
2016		84,4	103,1	103,3	113,1	74,7	104,4	108,8	96,3	98,1	103,8	99,9	101,5	101,7	106,6	103,6	105,8
2017						76,2	99,4										
период с начала отчетного года в % к соответствующему периоду предыдущего года / period from beginning of reporting year as percent of corresponding period of previous year																	
2015						100,0	99,1	99,9	99,4	99,1	99,1	99,0	99,1	99,2	99,1	99,3	99,2
2016						99,2	101,5	101,1	101,1	101,1	101,3	101,3	101,3	101,2	101,2	101,4	101,3
2017						102,3	99,7										
"""

# -----------------------------------------------------------------------------
#
# Suit 1
#
# -----------------------------------------------------------------------------

DOC = doc_a + doc_b

def get_rows1():
    return doc_to_lists(DOC)


def get_parsing_instructions1():
    HEADERS = {"Объем ВВП": dict(var="GDP", unit="bln_rub")
        , "Индекс физического объема произведенного ВВП": dict(var="GDP", unit="rog")
        , "Индекс промышленного производства": dict(var="IND_PROD", unit="")
               }
    UNITS = OrderedDict([("в % к предыдущему периоду", "rog"),
             ("период с начала отчетного года в % к соответствующему периоду предыдущего года", "ytd"),
             ("в % к соответствующему периоду предыдущего года", "yoy")])
    SPLITTER_FUNC = None
    return HEADERS, UNITS, SPLITTER_FUNC

# -----------------------------------------------------------------------------
#
# Suit 2
#
# -----------------------------------------------------------------------------

doc_c = """
	Год Year	Янв. Jan.	Янв-фев. Jan-Feb	I квартал Q1	Янв-апр. Jan-Apr	Янв-май Jan-May	I полугод. 1st half year	Янв-июль Jan-Jul	Янв-авг. Jan-Aug	Янв-cент. Jan-Sent	Янв-окт. Jan-Oct	Янв-нояб. Jan-Nov
2. Финансы / Finances												
2.1. Доходы и расходы / Revenues and expenditures												
2.1.1. Доходы (по данным Федерального казначейства)1) / Revenues (data of the Federal Treasury)1)												
Консолидированный бюджет, млрд.рублей / Consolidated budget, bln rubles												
2013	24442,7	1591,7	3206,6	5401,6	7707,7	9441,5	11370,7	13574,9	15472,1	17417,5	19700,9	21570,2
20142)	26766,1	1726,3	3579,8	5960,4	8498,3	10572,3	12671,2	15108,2	17143,4	19221,4	21563,5	23439,4
2015	26922,0	1661,5	3403,0	6044,6	8704,9	10514,7	12748,6	15243,3	17316,8	19496,2	21911,1	23679,2
2016	27746,73)	1653,1	3264,7	5876,1	8330,0	10213,0	12521,5	14932,9	17197,8	19374,5	21871,0	24095,8
2017		1978,8										
	Год Year	Янв. Jan.	Янв-фев. Jan-Feb	I квартал Q1	Янв-апр. Jan-Apr	Янв-май Jan-May	I полугод. 1st I half year	Янв-июль Jan-Jul	Янв-авг. Jan-Aug	Янв-cент. Jan-Sent	Янв-окт. Jan-Oct	Янв-нояб. Jan-Nov
Удельный вес в общем объеме доходов соответствующего бюджета, в процентах / Share of revenue of corresponding budget in total revenues, percent												
"""

YAML2 = """
# Раздел 1. Информация по сегментам
# Section 1. Segment information 
# segment information
start line : 2.1.1. Доходы (по данным Федерального казначейства)
end line : Удельный вес в общем объеме доходов соответствующего бюджета
special reader: fiscal
---
# Раздел 2. Единицы измерении
# Section 2. Units of measurement
# rog - темп изменения к предыдущему периоду  
# yoy - темп изменения к соответствующему периоду предыдущего года  
# ytd - темп изменения за период с начала текущегогода к аппп
в % к соответствующему периоду предыдущего года : yoy
в % к предыдущему периоду : rog
в % к предыдущему месяцу: rog
период с начала отчетного года : ytd
отчетный месяц в % к соответствующему месяцу предыдущего года : yoy
в % к соответствующему месяцу предыдущего года : yoy
отчетный месяц в % к предыдущему месяцу : rog 
рублей / rubles : rub
млн.рублей : mln_rub
---
#2. Финансы / Finances
#2.1. Доходы и расходы 1) / Revenues and expenditures 1)
#2.1.1. Доходы (по данным Федерального казначейства) 2) / Revenues (data of the Federal Treasury) 2)
#Консолидированный бюджет, млрд.рублей / Consolidated budget, bln rubles
Консолидированный бюджет : 
 - GOV_CONSOLIDATED_REVENUE_ACCUM
 - bln_rub 
"""


def get_rows2():
    return doc_to_lists(doc_c)


def get_parsing_instructions2():
    
    d = parse_spec_text(YAML2)
    HEADERS = d['table_headers']
    UNITS = d['units']
    SPLITTER_FUNC = d['reader_func']
    return HEADERS, UNITS, SPLITTER_FUNC


#==============================================================================
#
# TODO
# Suit 3. doc_a + doc_c + doc_b + segments
#
#==============================================================================
