SPEC1 = ({'Gross domestic product': ['GDP', 'bln_rub']}, {'percent change from previous year': 'yoy', 'billion ruble': 'bln_rub'}, {'special reader': None, 'start line': None, 'end line': None})

LABELLED_RS = [
       {'string':"1. Gross domestic product at current prices",
          'list':["1. Gross domestic product at current prices"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
        
        {'string':"billion ruble",
          'list':["billion ruble"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},          
        
        {'string':"\tYEAR\tVALUE",
          'list':["", "YEAR", "VALUE"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': None},
          
        {'string':"2013\t61500",
          'list':["2013", "61500"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
                    
        {'string':"2014\t64000",
          'list':["2014", "64000"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
          
         {'string': "percent change from previous year - annual basis",
          'list': ["percent change from previous year - annual basis"],
          'head_label': 'GDP',
          'unit_label': 'yoy',
          'spec': SPEC1},
          
        {'string':"2013\t1.013",
          'list':["2013", "1.013"],
          'head_label':'GDP',
          'unit_label':'yoy',
          'spec': SPEC1},

        {'string':"2014\t1.028",
          'list':["2014", "1.028"],
          'head_label':'GDP',
          'unit_label':'yoy',
          'spec': SPEC1}         
]

LABELLED_WITH_SEGMENTS = [{'head_label': 'GDP',
  'list': ['1. Gross domestic product at current prices'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': '1. Gross domestic product at current prices',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['billion ruble'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': 'billion ruble',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['', 'YEAR', 'VALUE'],
  'spec': None,
  'string': '\tYEAR\tVALUE',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['2013', '61500'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': '2013\t61500',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['2014', '64000'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': '2014\t64000',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['percent change from previous year - annual basis'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None,
            'special reader': 'read_special',
            'start line': 'percent change'}),
  'string': 'percent change from previous year - annual basis',
  'unit_label': 'yoy'},
 {'head_label': 'GDP',
  'list': ['2013', '1.013'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None,
            'special reader': 'read_special',
            'start line': 'percent change'}),
  'string': '2013\t1.013',
  'unit_label': 'yoy'},
 {'head_label': 'GDP',
  'list': ['2014', '1.028'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None,
            'special reader': 'read_special',
            'start line': 'percent change'}),
  'string': '2014\t1.028',
  'unit_label': 'yoy'}]

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
}

ordered_keys = ['ip', 'trans', 'investment', 'cpi_block', 'food_block']
full_raw_doc = ("\n"*5).join([raw_data_docs[key] for key in ordered_keys])
  