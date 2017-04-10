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

DOC2 = """
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

def doc_to_lists(doc):
    return [r.split('\t') for r in doc.split('\n')]

raw_data2 = doc_to_lists(DOC2)

import yaml

def parse_spec_text(yaml_string):
    """Parse specification from YAML document to dictionary."""
    content = list(yaml.load_all(yaml_string))
    return { 'scope': { 'start_line':  content[0]['start line'],
                          'end_line':  content[0]['end line']},
             'reader_func': content[0]['special reader'],
             'units':   content[1],
             'table_headers': content[2]
             }
spec2 = parse_spec_text(YAML2)

