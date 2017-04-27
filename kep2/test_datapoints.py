# -*- coding: utf-8 -*-

import pandas as pd
import unittest 

from emitter import Datapoints
from parsing_definitions import ParsingDefinition
from csv_data import CSV_Reader

from files import Tempfile
	

#
# Fixtures - test strings
#

# ---------------- CSV data

csv_content_1 = """
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


csv_content_2 = """
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


csv_content_3 = """
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


# ---------------- parsing definitions (YAML) data
                                       
yaml_content_1 = """
# Раздел 1. Информация по сегментам
# Section 1. Segment information 
# segment information
start line : null
end line : null
special reader: null
---
# Раздел 2. Единицы измерении
# Section 2. Units of measurement
# rog - темп изменения к предыдущему периоду  
# yoy - темп изменения к соответствующему периоду предыдущего года  
# ytd - темп изменения за период с начала текущегогода к аппп
в % к предыдущему периоду : rog
период с начала отчетного года в % к соответствующему периоду предыдущего года : ytd
в % к соответствующему периоду предыдущего года : yoy
---
#2. Финансы / Finances
#2.1. Доходы и расходы 1) / Revenues and expenditures 1)
#2.1.1. Доходы (по данным Федерального казначейства) 2) / Revenues (data of the Federal Treasury) 2)
#Консолидированный бюджет, млрд.рублей / Consolidated budget, bln rubles
Объем ВВП : 
 - GDP
 - bln_rub
Индекс физического объема произведенного ВВП :
 - GDP
 - rog
Индекс промышленного производства :
 - IND_PROD 
"""


yaml_content_2 = """
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


def get_csv_data(content):
     # get csv data  
     with Tempfile(content_string = content) as path:
         return CSV_Reader(path).yield_dicts()		
     
    
def get_parsing_def(content):
     # get test parsing definitions
     with Tempfile(content_string = content) as path:
         return ParsingDefinition(path)	
     
    
def get_dfs(input_csv, yaml_content):    
    # get test parsing definitions
    pdef = get_parsing_def(yaml_content)
	 # get csv data     
    csv_dicts = get_csv_data(input_csv)                
    d = Datapoints(csv_dicts, pdef)    
    # added column order to match DFA, DFQ, DFM constants
    dfa = pd.DataFrame(d.emit('a'))[['value', 'varname', 'year']]
    dfq = pd.DataFrame(d.emit('q'))[['qtr', 'value', 'varname', 'year']]
    dfm = pd.DataFrame(d.emit('m'))[['month', 'value', 'varname', 'year']]
    return dfa, dfq, dfm    
    
    
class TestDatapoints(unittest.TestCase):
    
    # QUESTION: use setUp() and tearDown() methods here?
    
    def test_dataframes_simple(self):
        """
        csv: csv_content_1 + csv_content_2 
        yaml: yaml_content_1
        matches: hardcoded values below
        """
        
        input_csv = csv_content_1 + csv_content_2
        yaml_content = yaml_content_1
        dfa, dfq, dfm = get_dfs(input_csv, yaml_content)
        
        assert dfa.to_csv() == ',value,varname,year\n0,71017.0,GDP_bln_rub,2013\n1,79200.0,GDP_bln_rub,2014\n2,83233.0,GDP_bln_rub,2015\n3,85881.0,GDP_bln_rub,2016\n4,101.3,GDP_rog,2013\n5,100.7,GDP_rog,2014\n6,97.2,GDP_rog,2015\n7,99.8,GDP_rog,2016\n8,99.2,IND_PROD_yoy,2015\n9,101.3,IND_PROD_yoy,2016\n'
        assert dfq.to_csv() == ',qtr,value,varname,year\n0,1,15892.0,GDP_bln_rub,2013\n1,2,17015.0,GDP_bln_rub,2013\n2,3,18543.0,GDP_bln_rub,2013\n3,4,19567.0,GDP_bln_rub,2013\n4,1,17139.0,GDP_bln_rub,2014\n5,2,18884.0,GDP_bln_rub,2014\n6,3,20407.0,GDP_bln_rub,2014\n7,4,21515.0,GDP_bln_rub,2014\n8,1,18210.0,GDP_bln_rub,2015\n9,2,19284.0,GDP_bln_rub,2015\n10,3,21294.0,GDP_bln_rub,2015\n11,4,22016.0,GDP_bln_rub,2015\n12,1,18561.0,GDP_bln_rub,2016\n13,2,19979.0,GDP_bln_rub,2016\n14,3,22190.0,GDP_bln_rub,2016\n15,1,100.6,GDP_rog,2013\n16,2,101.1,GDP_rog,2013\n17,3,101.2,GDP_rog,2013\n18,4,102.1,GDP_rog,2013\n19,1,100.6,GDP_rog,2014\n20,2,101.1,GDP_rog,2014\n21,3,100.9,GDP_rog,2014\n22,4,100.2,GDP_rog,2014\n23,1,97.2,GDP_rog,2015\n24,2,95.5,GDP_rog,2015\n25,3,96.3,GDP_rog,2015\n26,4,96.2,GDP_rog,2015\n27,1,98.8,GDP_rog,2016\n28,2,99.4,GDP_rog,2016\n29,3,99.6,GDP_rog,2016\n30,1,99.9,IND_PROD_yoy,2015\n31,2,98.3,IND_PROD_yoy,2015\n32,3,99.5,IND_PROD_yoy,2015\n33,4,99.1,IND_PROD_yoy,2015\n34,1,101.1,IND_PROD_yoy,2016\n35,2,101.5,IND_PROD_yoy,2016\n36,3,101.0,IND_PROD_yoy,2016\n37,4,101.7,IND_PROD_yoy,2016\n38,1,82.8,IND_PROD_rog,2015\n39,2,102.6,IND_PROD_rog,2015\n40,3,103.9,IND_PROD_rog,2015\n41,4,112.3,IND_PROD_rog,2015\n42,1,84.4,IND_PROD_rog,2016\n43,2,103.1,IND_PROD_rog,2016\n44,3,103.3,IND_PROD_rog,2016\n45,4,113.1,IND_PROD_rog,2016\n'
        assert dfm.to_csv() == ',month,value,varname,year\n0,1,100.0,IND_PROD_yoy,2015\n1,2,98.2,IND_PROD_yoy,2015\n2,3,101.2,IND_PROD_yoy,2015\n3,4,98.2,IND_PROD_yoy,2015\n4,5,97.6,IND_PROD_yoy,2015\n5,6,99.1,IND_PROD_yoy,2015\n6,7,98.5,IND_PROD_yoy,2015\n7,8,100.2,IND_PROD_yoy,2015\n8,9,99.7,IND_PROD_yoy,2015\n9,10,98.4,IND_PROD_yoy,2015\n10,11,101.0,IND_PROD_yoy,2015\n11,12,98.1,IND_PROD_yoy,2015\n12,1,99.2,IND_PROD_yoy,2016\n13,2,103.8,IND_PROD_yoy,2016\n14,3,100.3,IND_PROD_yoy,2016\n15,4,101.0,IND_PROD_yoy,2016\n16,5,101.5,IND_PROD_yoy,2016\n17,6,102.0,IND_PROD_yoy,2016\n18,7,101.4,IND_PROD_yoy,2016\n19,8,101.5,IND_PROD_yoy,2016\n20,9,100.1,IND_PROD_yoy,2016\n21,10,101.6,IND_PROD_yoy,2016\n22,11,103.4,IND_PROD_yoy,2016\n23,12,100.2,IND_PROD_yoy,2016\n24,1,102.3,IND_PROD_yoy,2017\n25,2,97.3,IND_PROD_yoy,2017\n26,1,73.9,IND_PROD_rog,2015\n27,2,99.8,IND_PROD_rog,2015\n28,3,112.5,IND_PROD_rog,2015\n29,4,95.6,IND_PROD_rog,2015\n30,5,97.6,IND_PROD_rog,2015\n31,6,103.2,IND_PROD_rog,2015\n32,7,100.5,IND_PROD_rog,2015\n33,8,101.4,IND_PROD_rog,2015\n34,9,103.1,IND_PROD_rog,2015\n35,10,105.0,IND_PROD_rog,2015\n36,11,101.9,IND_PROD_rog,2015\n37,12,109.1,IND_PROD_rog,2015\n38,1,74.7,IND_PROD_rog,2016\n39,2,104.4,IND_PROD_rog,2016\n40,3,108.8,IND_PROD_rog,2016\n41,4,96.3,IND_PROD_rog,2016\n42,5,98.1,IND_PROD_rog,2016\n43,6,103.8,IND_PROD_rog,2016\n44,7,99.9,IND_PROD_rog,2016\n45,8,101.5,IND_PROD_rog,2016\n46,9,101.7,IND_PROD_rog,2016\n47,10,106.6,IND_PROD_rog,2016\n48,11,103.6,IND_PROD_rog,2016\n49,12,105.8,IND_PROD_rog,2016\n50,1,76.2,IND_PROD_rog,2017\n51,2,99.4,IND_PROD_rog,2017\n52,1,100.0,IND_PROD_ytd,2015\n53,2,99.1,IND_PROD_ytd,2015\n54,3,99.9,IND_PROD_ytd,2015\n55,4,99.4,IND_PROD_ytd,2015\n56,5,99.1,IND_PROD_ytd,2015\n57,6,99.1,IND_PROD_ytd,2015\n58,7,99.0,IND_PROD_ytd,2015\n59,8,99.1,IND_PROD_ytd,2015\n60,9,99.2,IND_PROD_ytd,2015\n61,10,99.1,IND_PROD_ytd,2015\n62,11,99.3,IND_PROD_ytd,2015\n63,12,99.2,IND_PROD_ytd,2015\n64,1,99.2,IND_PROD_ytd,2016\n65,2,101.5,IND_PROD_ytd,2016\n66,3,101.1,IND_PROD_ytd,2016\n67,4,101.1,IND_PROD_ytd,2016\n68,5,101.1,IND_PROD_ytd,2016\n69,6,101.3,IND_PROD_ytd,2016\n70,7,101.3,IND_PROD_ytd,2016\n71,8,101.3,IND_PROD_ytd,2016\n72,9,101.2,IND_PROD_ytd,2016\n73,10,101.2,IND_PROD_ytd,2016\n74,11,101.4,IND_PROD_ytd,2016\n75,12,101.3,IND_PROD_ytd,2016\n76,1,102.3,IND_PROD_ytd,2017\n77,2,99.7,IND_PROD_ytd,2017\n'                         
        
    def test_dataframes_using_custom_splitter_func(self):  
        """
        csv: csv_content_3 
        yaml: yaml_content_2
        matches: hardcoded values below
        """
        input_csv = csv_content_3
        yaml_content = yaml_content_2
        dfa, dfq, dfm = get_dfs(input_csv, yaml_content)
        
        assert dfa.to_csv() == ',value,varname,year\n0,24442.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n1,26766.1,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2014\n2,26922.0,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2015\n3,27746.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2016\n'
        assert dfq.to_csv() == ',qtr,value,varname,year\n0,1,5401.6,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n1,2,11370.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n2,3,17417.5,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n3,4,24442.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n4,1,5960.4,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2014\n5,2,12671.2,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2014\n6,3,19221.4,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2014\n7,4,26766.1,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2014\n8,1,6044.6,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2015\n9,2,12748.6,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2015\n10,3,19496.2,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2015\n11,4,26922.0,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2015\n12,1,5876.1,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2016\n13,2,12521.5,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2016\n14,3,19374.5,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2016\n15,4,27746.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2016\n'
        assert dfm.to_csv().startswith(',month,value,varname,year\n0,1,1591.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n1,2,3206.6,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n2,3,5401.6,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n3,4,7707.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n4,5,9441.5,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n5,6,11370.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n6,7,13574.9,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n7,8,15472.1,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n8,9,17417.5,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n9,10,19700.9,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n10,11,21570.2,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n11,12,24442.7,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub,2013\n12,1,1726.3,GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub')
        
    def test_mixed_dataframes(self):  
        """
        Special section csv_content_3 between tables  csv_content_1 and csv_content_2
        
        csv: csv_content_1 + csv_content_3 + csv_content_2] 
        yaml: dict(default=yaml_content_1, additional=yaml_content_2)
        matches: will need to recycle test values from prvios tests
        """
        assert False
        # TODO: user interface for default and additional spec in datapoints.py
        # TODO: this test 
        
        

if __name__ == '__main__':    
    unittest.main()
    # input_csv = csv_content_1 + csv_content_2
    # yaml_content = yaml_content_1
    # dfa, dfq, dfm = get_dfs(input_csv, yaml_content)