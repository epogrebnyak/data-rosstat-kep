"""Small example of raw data and parsing specification.

data -> write temp files (FILE_CONTENT) -> folder -> RowSystem -> values 

"""

from inputs import TempfolderFile
from config import RESERVED_FILENAMES, TESTDATA_DIR
from rs import CSV, Segment, InputDefinition, RowSystem

def setup_module(module):
    write_temp_files()

def teardown_module(module):
    remove_temp_files()
    
# -------------------------------------------------------------------
#
#    Data used for min working example of end-to-end testing:
#    - CSV_TXT
#    - SPEC*_TXT 
#    - CFG_TXT
#
# -------------------------------------------------------------------


# ************* CSV_TXT  *************

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

CSV_TXT = ("\n"*5).join([raw_data_docs[key] for key in ['ip', 'trans', 'investment', 'cpi_block', 'food_block']])
  

# ************* SPEC_TXT ************* 

null_segment_definition = """# segment information
start line : null
end line : null
special reader: null
---\n"""

cpi_segment_definition = """# segment information
start line : 3.5. Индекс потребительских цен
end line : Из общего объема оборота розничной торговли
special reader: null
---\n"""

food_segment_definition = """# segment information
start line : Из общего объема оборота розничной торговли
end line : null
special reader: null
---\n"""


# -------------------
                                             
unit_definition = """в % к соответствующему периоду предыдущего года: yoy
в % к предыдущему периоду : rog
отчетный месяц в % к предыдущему месяцу : rog
отчетный месяц в % к соответствующему месяцу предыдущего года : yoy
период с начала отчетного года : ytd
---\n"""

extra_unit_definition = """bln rubles : bln_rub
---\n"""

# -------------------

header_spec_ip_trans_inv = """
### ip
Индекс промышленного производства:
  - IND_PROD
  - yoy

### trans
Производство транспортных средств и оборудования:
  - TRANS
  - Not specified

### inv
Инвестиции в основной капитал: 
  - INVESTMENT
  - bln_rub
"""

header_spec_cpi =  """
Индекс потребительских цен: 
  - CPI
  - rog

непродовольственные товары:
   - CPI_NONFOOD
   - rog  
"""

header_food_spec = """пищевые продукты, включая напитки, и табачные изделия :
 - SALES_FOOD
 - bln_rub
 
непродовольственные товары :
 - SALES_NONFOOD
 - bln_rub
"""

spec_main       = null_segment_definition + unit_definition       + header_spec_ip_trans_inv
spec_cpi_block  = cpi_segment_definition  + unit_definition       + header_spec_cpi
spec_food_block = food_segment_definition + extra_unit_definition + header_food_spec

flist = ["sp0.txt", "sp_cpi.txt",  "sp_food.txt"]

def gen_cfg_txt(filename_list):
    return "\n".join(["- {}".format(fn) for fn in filename_list])
    
CFG_TXT = gen_cfg_txt(flist)

FILE_CONTENT = {
     RESERVED_FILENAMES['csv']: CSV_TXT
   , RESERVED_FILENAMES['cfg']: CFG_TXT
   , flist[0]                 : spec_main
   , flist[1]                 : spec_cpi_block
   , flist[2]                 : spec_food_block
}

def get_rs():
    folder = write_temp_files()  
    assert folder == TESTDATA_DIR    
    return RowSystem(folder)
   
def write_temp_files(fc = FILE_CONTENT):
    """Write files for input testing."""
    for k, v in fc.items():
        z = TempfolderFile(k).save_text(v)
    return z.folder
    
def remove_temp_files(fc = FILE_CONTENT):
    """Delete input testing files."""
    for k, v in fc.items():
        TempfolderFile(k).remove()

# -------------------------------------------------------------------
#
#  Test values
#   - dicts derived from defintions (testing not performed)  
#   - annual reference values
#
# -------------------------------------------------------------------


null_segment_dict = {'special reader': None, 'start line': None, 
                                             'end line':   None}
                                             
cpi_segment_dict  = {'special reader': None, 'start line': '3.5. Индекс потребительских цен', 
                                             'end line':   'Из общего объема оборота розничной торговли'}
                                             
food_segment_dict = {'special reader': None, 'start line': 'Из общего объема оборота розничной торговли',
                                             'end line':    None}
    

common_unit_dict = {'в % к соответствующему периоду предыдущего года': 'yoy',
'в % к предыдущему периоду' : 'rog',
'отчетный месяц в % к предыдущему месяцу' : 'rog',
'отчетный месяц в % к соответствующему месяцу предыдущего года' : 'yoy',
'период с начала отчетного года' : 'ytd'}

food_block_unit_dict = {'bln rubles':'bln_rub'}

hd_ip_trans_inv = {'Индекс промышленного производства': ['IND_PROD', 'yoy'],
                   'Производство транспортных средств и оборудования': ['TRANS', 'Not specified'],
                   'Инвестиции в основной капитал': ['INVESTMENT', 'bln_rub']}

hd_cpi_block  = {'Индекс потребительских цен': ['CPI', 'rog'], 
                 'непродовольственные товары': ['CPI_NONFOOD', 'rog']}
                 
hd_food_block = {'пищевые продукты, включая напитки, и табачные изделия': ['SALES_FOOD','bln_rub'],
                 'непродовольственные товары': ['SALES_NONFOOD', 'bln_rub']}
                 
REF_DFA_CSV = 'year,CPI_NONFOOD_rog,CPI_rog,IND_PROD_yoy,INVESTMENT_bln_rub,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub\n2014,108.1,111.4,101.7,13527.7,97.3,12380.9,13975.3\n'
REF_DFQ_CSV = 'time_index,year,qtr,CPI_NONFOOD_rog,CPI_rog,IND_PROD_rog,IND_PROD_yoy,INVESTMENT_bln_rub,INVESTMENT_rog,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub\n2014-03-31,2014,1,101.4,102.3,87.6,101.1,1863.8,35.7,94.7,2729.6,3063.3\n2014-06-30,2014,2,101.5,102.4,103.6,101.8,2942.0,158.2,98.1,2966.3,3290.4\n2014-09-30,2014,3,101.4,101.4,102.7,101.5,3447.6,114.9,98.5,3140.1,3557.2\n2014-12-31,2014,4,103.6,104.8,109.6,102.1,5274.3,149.9,97.2,3544.9,4064.4\n'
REF_DFM_CSV = 'time_index,year,month,CPI_NONFOOD_rog,CPI_rog,IND_PROD_rog,IND_PROD_yoy,IND_PROD_ytd,INVESTMENT_bln_rub,INVESTMENT_rog,INVESTMENT_yoy,SALES_FOOD_bln_rub,SALES_NONFOOD_bln_rub,TRANS_rog,TRANS_yoy,TRANS_ytd\n2014-01-31,2014,1,100.3,100.6,81.2,99.8,99.8,492.2,21.1,92.7,882.7,984.4,45.4,103.8,103.8\n2014-02-28,2014,2,100.4,100.7,101.6,102.1,100.9,643.2,129.6,95.5,884.5,986.8,131.8,113.2,108.9\n2014-03-31,2014,3,100.7,101.0,109.7,101.4,101.1,728.4,114.5,95.3,962.4,1092.1,123.9,114.2,111.0\n2014-04-30,2014,4,100.6,100.9,97.3,102.4,101.4,770.4,106.6,97.4,963.6,1079.3,102.3,119.6,113.4\n2014-05-31,2014,5,100.5,100.9,99.6,102.8,101.7,991.1,127.0,97.3,999.4,1095.6,88.8,118.3,114.8\n2014-06-30,2014,6,100.4,100.6,99.9,100.4,101.5,1180.5,119.0,99.3,1003.3,1115.5,116.3,111.7,114.2\n2014-07-31,2014,7,100.4,100.5,102.2,101.5,101.5,1075.1,90.5,99.1,1034.0,1158.2,98.4,122.0,114.8\n2014-08-31,2014,8,100.5,100.2,99.8,100.0,101.3,1168.5,107.1,98.4,1061.8,1202.0,84.0,90.9,111.8\n2014-09-30,2014,9,100.6,100.7,102.7,102.8,101.5,1204.0,103.3,98.1,1044.3,1197.0,123.4,111.4,111.8\n2014-10-31,2014,10,100.6,100.8,105.1,102.9,101.7,1468.5,121.6,99.2,1084.6,1226.3,100.7,109.8,111.6\n2014-11-30,2014,11,100.6,101.3,99.8,99.6,101.5,1372.5,92.7,92.2,1097.9,1245.7,112.3,95.5,110.1\n2014-12-31,2014,12,102.3,102.6,108.1,103.9,101.7,2433.3,173.8,98.9,1362.4,1592.4,141.6,91.0,108.5\n'

# -------------------------------------------------------------------
#
#    Testing:
#    - entered via get_rs()  
#    - uses REF_DFA_CSV, REF_DFQ_CSV, REF_DFM_CSV
#
# ---------------------------------------------------------------------
     
def test_folder_level_import_and_df_testing():
    rs = get_rs()
    assert rs.headnames() == ['CPI', 'CPI_NONFOOD', 'IND_PROD', 'INVESTMENT', 'SALES_FOOD', 'SALES_NONFOOD', 'TRANS']
    assert len(rs.not_imported()) == 0 
    assert REF_DFA_CSV == rs.data.annual_df().to_csv()
    assert REF_DFQ_CSV == rs.data.quarter_df().to_csv()
    assert REF_DFM_CSV == rs.data.monthly_df().to_csv()
    assert rs.__len__() == {'n_heads': 7, 'n_points': 199, 'n_vars': 13}
    #rs.save()    
    #kep = KEP()
    remove_temp_files()
   
if __name__ == "__main__":
    import pprint
    z = get_rs()
    print("\nRowsystem content")
    for frow in z.full_rows:
        pprint.pprint(frow)  
    print(z)
    
