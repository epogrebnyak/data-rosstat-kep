# -*- coding: utf-8 -*-
"""
In this demo we apply parsing instructions to csv proxy to get streams
of annual, quarterly and monthly datapoints. 

Point of entry:
    
    stream_by_freq(freq, raw_data, parsing_instructions), 
    
       inputs:
           *freq* must be 'a', 'q' or 'm'
           *raw_data* is a list of of csv strings
           *parsing_instructions* is a list of headers and units dictionaries    

What is different form actual task:
  - csv must read from file, definitions must be read from file 
  - this is one segment of file, may have different instructions for different 
    parts of CSV file
  - as a consequence - need to inject splitter fucntion in some way 
    different form ROW_LENGTH_TO_FUNC[cnt]
  - values in stream must be floats (112.3), not str ("112,3") + there is some 
    parsing of comments eg '3461)' is filtered to '346' - this can be done in 
    this file
  - (out of scope) dfa, dfq, dfm are futher transformed in getter module 

Possible checks: 
  - all variables from definitions are read
  - some datapoints are read and compared to hardcoded values
  - sums round up to priod data
  - rates of change are product of monthly/quarterly rates  
  - other?
 
 
Tasks out this demo:
    
  - generate list of variable decriptions:
      
      describe_var("GDP_yoy") == "Валовый внутренний продукт"
      describe_unit("GDP_yoy") == "изменение год к году"
      
  - will need varname splitter for this split("GDP_yoy") == "GDP", "yoy"     

"""

"""
Todo:
  - review algorighm, comment where surprises
  - suggestions for better naming of vars, funcs
  - other comments
  
"""

import pandas as pd

# -----------------------------------------------------------------------------
#
# CSV proxy
#
# -----------------------------------------------------------------------------

DOC = """
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
def get_rows():
    return [r.split('\t') for r in DOC.split('\n')]

# -----------------------------------------------------------------------------
#
# Parsing instructions 
#
# -----------------------------------------------------------------------------

HEADERS = {"Объем ВВП" : dict(var="GDP", unit="bln_rub")
, "Индекс физического объема произведенного ВВП" : dict(var="GDP", unit="rog")
, "Индекс промышленного производства" : dict(var="IND_PROD", unit="")
}

UNITS = {"в % к предыдущему периоду" : "rog",
         "период с начала отчетного года в % к соответствующему периоду предыдущего года" : "ytd",
         "в % к соответствующему периоду предыдущего года" : "yoy"}

def get_parsing_instructions():
    return HEADERS, UNITS

# -----------------------------------------------------------------------------
#
# Parsing
#
# -----------------------------------------------------------------------------

EMPTY_LABEL = {'var':'', 'unit':''}

def view_label(lab):
    return lab['var'] + "_" + lab['unit']
   

def yield_rows_as_dicts(rows):
    for r in rows:
       if r and r[0]:  
            yield dict(head=r[0], data=r[1:], label=EMPTY_LABEL)

def get_year(s):
    return int(s[:4])
   
def is_year(s):
    try:
        get_year(s)
        return True
    except:
        return False

def detect(text, refs):
    found = ""
    flag = False
    for r in refs:
        if r in text:
            found = r
            flag = True
            break
    return flag, found


def label_rows(rows, parsing_instructions):
    
    headers, units = parsing_instructions   
    current_label = EMPTY_LABEL
    
    for row in rows:
         
        if is_year(row['head']):
            row['label'] = current_label           
         
        else:            
            flag1, current_header = detect(row['head'], headers.keys())
            if flag1:
               current_label = headers[current_header]
            
            flag2, unit = detect(row['head'], units.keys())
            if flag2:
                current_label['unit'] = units[unit]
            
            row['label'] = current_label   
               
        yield row                 

    
def is_datarow(row):
    return is_year(row['head'])

def split_row_by_periods(row):           
    """A Q Q Q Q M*12"""
    return row[0], row[1:1+4], row[1+4:1+4+12]

def split_row_by_year_and_qtr(row):         
    """A Q Q Q Q"""
    return row[0], row[1:1+4], None    

    
ROW_LENGTH_TO_FUNC = { 1+4+12: split_row_by_periods, 
                          1+4: split_row_by_year_and_qtr}

def yield_dicts(row_tuple, varname, year):
       
       a, qs, ms = row_tuple
           
       if a:
           yield {'freq' : 'a',
            'varname' : varname,
            'year'    : year,
            'value'   : a}
           
       if qs is not None:         
           for i, val in enumerate(qs):
               if val:
                  yield {'freq' : 'q',
            'varname' : varname,
            'year'    : year,
            'qtr'     : i+1,
            'value'   : val}
   
       if ms is not None:         
           for j, val in enumerate(ms):
               if val:
                  yield {'freq' : 'm',
            'varname' : varname,
            'year'    : year,
            'month'   : j+1,
            'value'   : val}    

def get_datapoints(row):
    cnt = len(row['data'])
    splitter_func = ROW_LENGTH_TO_FUNC[cnt] 
    row_tuple = splitter_func(row['data']) 
    return yield_dicts(row_tuple, 
                       year=get_year(row['head']), 
                       varname=view_label(row['label']))

def stream_by_freq(freq, raw_data=get_rows(), 
                         parsing_instructions=get_parsing_instructions()):
    gen = yield_rows_as_dicts(raw_data)
    gen2 = label_rows(gen, parsing_instructions)
    for row in filter(is_datarow, gen2):
        for p in get_datapoints(row):
            if p['freq'] == freq: 
               p.pop('freq')
               yield p

if __name__ == "__main__":               
    dfa = pd.DataFrame(stream_by_freq('a'))               
    dfq = pd.DataFrame(stream_by_freq('q'))               
    dfm = pd.DataFrame(stream_by_freq('m'))