# -*- coding: utf-8 -*-
"""
Apply parsing instructions to csv proxy to get streams of annual, quarterly and 
monthly datapoints. 

Point of entry:
    
    stream_by_freq(freq, raw_data, parsing_instructions), 
    
        inputs:
            *freq* must be 'a', 'q' or 'm'
            *raw_data* is a list of csv row elements
            *parsing_instructions* is a list of headers and units dictionaries    
       
        returns:
            generator of dictionaries containing datapoints           
           
"""

"""
Todo - General questions    
  1. review algorithm, comment where code surprises you
  2. (optional) suggest alternatives for algorightm.
  3. suggestions for better naming of vars, funcs
  4. where would you add tests?  
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

SPLITTER_FUNC = None

def get_parsing_instructions():
    return HEADERS, UNITS, SPLITTER_FUNC

# -----------------------------------------------------------------------------
#
# Variable label handling
#
# -----------------------------------------------------------------------------

EMPTY_LABEL = {'var':'', 'unit':''}

def view_label(lab):
    return lab['var'] + "_" + lab['unit']
   

# TODO (EP): bring back splitting label to head and unit

#------------------------------------------------------------------------------
#
# Converting non-empty rows to 'head', 'data', 'label' dictionaries
#
#------------------------------------------------------------------------------

def row_as_dict(row):
    """Convert list *row* to dictionary for convenient usage.
    
       Keys:
          'head' - string, first element in list
          'data' - list, next elements in list
          'label' - placeholder for row label like dict(var="GDP", unit="bln_rub") 
    
    Example:
    >>> row_as_dict(['2013', '15892', '17015', '18543', '19567']) == {'head': '2013', 'data': ['15892', '17015', '18543', '19567'], 'label': {'unit': '', 'var': ''}}
    True
    """
    
    return dict(head=row[0], data=row[1:], label=EMPTY_LABEL)    

def yield_rows_as_dicts(rows):
    """Yield non-empty rows as dictionaries containing 
       'head', 'data' and 'label' keys.
    """       
    for r in rows:
       # check if list is not empty and first element is not empty 
       if r and r[0]:  
            yield row_as_dict(r)

def get_year(s):
    """Extract year from string *s*.
    
    Example:
    >>> get_year('2015')
    2015
    >>> get_year('20161)')
    2016
    """
    return int(s[:4])
   
def is_year(s):
    """Check if *s* contains year number.
    
    Example:
    >>> is_year('1. Сводные показатели')
    False
    >>> is_year('20151)')
    True
    
    """
    try:
        get_year(s)
        return True
    except:
        return False

#------------------------------------------------------------------------------
#
# Assigning labels (row['label']) to rows  
#
#------------------------------------------------------------------------------

def detect(text, refs):
    """Detects if any of the strings from *refs* list of strings is present 
       in *text* string. Returns flag and first matched string from *refs* 
       list of strings.
       
       assert detect("Canada", ["ana", "bot"]) == (True, 'ana')       
       
       """
    found = ""
    flag = False
    for r in refs:
        if r in text:
            found = r
            flag = True
            break
    return flag, found


def label_rows(rows, parsing_instructions):
    
    headers, units, _ = parsing_instructions   
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

#------------------------------------------------------------------------------
#
# Splitter functions extract annual, quarterly and monthly values from data row
#
#------------------------------------------------------------------------------

    
def split_row_by_periods(row):           
    """A Q Q Q Q M*12"""
    return row[0], row[1:1+4], row[1+4:1+4+12]


def split_row_by_year_and_qtr(row):         
    """A Q Q Q Q"""
    return row[0], row[1:1+4], None    

# TODO (EP)
# more splitter funcs at https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/stream.py
# warning: must adjust key by 1 

ROW_LENGTH_TO_FUNC = { 1+4+12: split_row_by_periods, 
                          1+4: split_row_by_year_and_qtr}

#------------------------------------------------------------------------------
#
# Emitting datapoints from data row
#
#------------------------------------------------------------------------------

def get_splitter_func(row, parsing_instructions):
    """Return custom splitter func from parsing_instructions if defined.
       Otherwise, choose parsing function based on number of elements in row
       using ROW_LENGTH_TO_FUNC dictionary.
       """
    _, _, custom_splitter_func = parsing_instructions
    if custom_splitter_func:
        return custom_splitter_func
    else:
        cnt = len(row['data'])
        return ROW_LENGTH_TO_FUNC[cnt]
        
def get_datapoints(row, parsing_instructions):    
    splitter_func = get_splitter_func(row, parsing_instructions)
    row_tuple = splitter_func(row['data']) 
    return yield_dicts(row_tuple, 
                       year=get_year(row['head']), 
                       varname=view_label(row['label']))

def filter_value(x):
    # can be more complex as in code below    
    # https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/stream.py#L74-L108
    return float(x.replace(",", "."))

def yield_dicts(row_tuple, varname, year):
       
       a, qs, ms = row_tuple
           
       if a:
           yield {'freq' : 'a',
            'varname' : varname,
            'year'    : year,
            'value'   : filter_value(a)}
           
       if qs is not None:         
           for i, val in enumerate(qs):
               if val:
                  yield {'freq' : 'q',
            'varname' : varname,
            'year'    : year,
            'qtr'     : i+1,
            'value'   : filter_value(val)}
   
       if ms is not None:         
           for j, val in enumerate(ms):
               if val:
                  yield {'freq' : 'm',
            'varname' : varname,
            'year'    : year,
            'month'   : j+1,
            'value'   : filter_value(val)}    
    
#------------------------------------------------------------------------------
#
# Generating stream of datapoints from csv and parsing instructions
#
#------------------------------------------------------------------------------


def is_datarow(row):
    return is_year(row['head'])


def stream_by_freq(freq, raw_data=get_rows(), 
                         parsing_instructions=get_parsing_instructions()):
    gen = yield_rows_as_dicts(raw_data)
    rows = label_rows(gen, parsing_instructions)
    for row in filter(is_datarow, rows):
        for p in get_datapoints(row, parsing_instructions):
            if p['freq'] == freq: 
               p.pop('freq')
               yield p

#------------------------------------------------------------------------------
#
# Some testing
#
#------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    from io import StringIO
               
    dfa = pd.DataFrame(stream_by_freq('a'))               
    dfq = pd.DataFrame(stream_by_freq('q'))               
    dfm = pd.DataFrame(stream_by_freq('m'))


    DFA = pd.read_csv(StringIO(',value,varname,year\n0,71017.0,GDP_bln_rub,2013\n1,79200.0,GDP_bln_rub,2014\n2,83233.0,GDP_bln_rub,2015\n3,85881.0,GDP_bln_rub,2016\n4,101.3,GDP_rog,2013\n5,100.7,GDP_rog,2014\n6,97.2,GDP_rog,2015\n7,99.8,GDP_rog,2016\n8,99.2,IND_PROD_yoy,2015\n9,101.3,IND_PROD_yoy,2016\n')
                      , index_col = 0)
    DFQ = pd.read_csv(StringIO(',qtr,value,varname,year\n0,1,15892.0,GDP_bln_rub,2013\n1,2,17015.0,GDP_bln_rub,2013\n2,3,18543.0,GDP_bln_rub,2013\n3,4,19567.0,GDP_bln_rub,2013\n4,1,17139.0,GDP_bln_rub,2014\n5,2,18884.0,GDP_bln_rub,2014\n6,3,20407.0,GDP_bln_rub,2014\n7,4,21515.0,GDP_bln_rub,2014\n8,1,18210.0,GDP_bln_rub,2015\n9,2,19284.0,GDP_bln_rub,2015\n10,3,21294.0,GDP_bln_rub,2015\n11,4,22016.0,GDP_bln_rub,2015\n12,1,18561.0,GDP_bln_rub,2016\n13,2,19979.0,GDP_bln_rub,2016\n14,3,22190.0,GDP_bln_rub,2016\n15,1,100.6,GDP_rog,2013\n16,2,101.1,GDP_rog,2013\n17,3,101.2,GDP_rog,2013\n18,4,102.1,GDP_rog,2013\n19,1,100.6,GDP_rog,2014\n20,2,101.1,GDP_rog,2014\n21,3,100.9,GDP_rog,2014\n22,4,100.2,GDP_rog,2014\n23,1,97.2,GDP_rog,2015\n24,2,95.5,GDP_rog,2015\n25,3,96.3,GDP_rog,2015\n26,4,96.2,GDP_rog,2015\n27,1,98.8,GDP_rog,2016\n28,2,99.4,GDP_rog,2016\n29,3,99.6,GDP_rog,2016\n30,1,99.9,IND_PROD_yoy,2015\n31,2,98.3,IND_PROD_yoy,2015\n32,3,99.5,IND_PROD_yoy,2015\n33,4,99.1,IND_PROD_yoy,2015\n34,1,101.1,IND_PROD_yoy,2016\n35,2,101.5,IND_PROD_yoy,2016\n36,3,101.0,IND_PROD_yoy,2016\n37,4,101.7,IND_PROD_yoy,2016\n38,1,82.8,IND_PROD_rog,2015\n39,2,102.6,IND_PROD_rog,2015\n40,3,103.9,IND_PROD_rog,2015\n41,4,112.3,IND_PROD_rog,2015\n42,1,84.4,IND_PROD_rog,2016\n43,2,103.1,IND_PROD_rog,2016\n44,3,103.3,IND_PROD_rog,2016\n45,4,113.1,IND_PROD_rog,2016\n')
                      , index_col = 0)
    DFM = pd.read_csv(StringIO(',month,value,varname,year\n0,1,100.0,IND_PROD_yoy,2015\n1,2,98.2,IND_PROD_yoy,2015\n2,3,101.2,IND_PROD_yoy,2015\n3,4,98.2,IND_PROD_yoy,2015\n4,5,97.6,IND_PROD_yoy,2015\n5,6,99.1,IND_PROD_yoy,2015\n6,7,98.5,IND_PROD_yoy,2015\n7,8,100.2,IND_PROD_yoy,2015\n8,9,99.7,IND_PROD_yoy,2015\n9,10,98.4,IND_PROD_yoy,2015\n10,11,101.0,IND_PROD_yoy,2015\n11,12,98.1,IND_PROD_yoy,2015\n12,1,99.2,IND_PROD_yoy,2016\n13,2,103.8,IND_PROD_yoy,2016\n14,3,100.3,IND_PROD_yoy,2016\n15,4,101.0,IND_PROD_yoy,2016\n16,5,101.5,IND_PROD_yoy,2016\n17,6,102.0,IND_PROD_yoy,2016\n18,7,101.4,IND_PROD_yoy,2016\n19,8,101.5,IND_PROD_yoy,2016\n20,9,100.1,IND_PROD_yoy,2016\n21,10,101.6,IND_PROD_yoy,2016\n22,11,103.4,IND_PROD_yoy,2016\n23,12,100.2,IND_PROD_yoy,2016\n24,1,102.3,IND_PROD_yoy,2017\n25,2,97.3,IND_PROD_yoy,2017\n26,1,73.9,IND_PROD_rog,2015\n27,2,99.8,IND_PROD_rog,2015\n28,3,112.5,IND_PROD_rog,2015\n29,4,95.6,IND_PROD_rog,2015\n30,5,97.6,IND_PROD_rog,2015\n31,6,103.2,IND_PROD_rog,2015\n32,7,100.5,IND_PROD_rog,2015\n33,8,101.4,IND_PROD_rog,2015\n34,9,103.1,IND_PROD_rog,2015\n35,10,105.0,IND_PROD_rog,2015\n36,11,101.9,IND_PROD_rog,2015\n37,12,109.1,IND_PROD_rog,2015\n38,1,74.7,IND_PROD_rog,2016\n39,2,104.4,IND_PROD_rog,2016\n40,3,108.8,IND_PROD_rog,2016\n41,4,96.3,IND_PROD_rog,2016\n42,5,98.1,IND_PROD_rog,2016\n43,6,103.8,IND_PROD_rog,2016\n44,7,99.9,IND_PROD_rog,2016\n45,8,101.5,IND_PROD_rog,2016\n46,9,101.7,IND_PROD_rog,2016\n47,10,106.6,IND_PROD_rog,2016\n48,11,103.6,IND_PROD_rog,2016\n49,12,105.8,IND_PROD_rog,2016\n50,1,76.2,IND_PROD_rog,2017\n51,2,99.4,IND_PROD_rog,2017\n52,1,100.0,IND_PROD_ytd,2015\n53,2,99.1,IND_PROD_ytd,2015\n54,3,99.9,IND_PROD_ytd,2015\n55,4,99.4,IND_PROD_ytd,2015\n56,5,99.1,IND_PROD_ytd,2015\n57,6,99.1,IND_PROD_ytd,2015\n58,7,99.0,IND_PROD_ytd,2015\n59,8,99.1,IND_PROD_ytd,2015\n60,9,99.2,IND_PROD_ytd,2015\n61,10,99.1,IND_PROD_ytd,2015\n62,11,99.3,IND_PROD_ytd,2015\n63,12,99.2,IND_PROD_ytd,2015\n64,1,99.2,IND_PROD_ytd,2016\n65,2,101.5,IND_PROD_ytd,2016\n66,3,101.1,IND_PROD_ytd,2016\n67,4,101.1,IND_PROD_ytd,2016\n68,5,101.1,IND_PROD_ytd,2016\n69,6,101.3,IND_PROD_ytd,2016\n70,7,101.3,IND_PROD_ytd,2016\n71,8,101.3,IND_PROD_ytd,2016\n72,9,101.2,IND_PROD_ytd,2016\n73,10,101.2,IND_PROD_ytd,2016\n74,11,101.4,IND_PROD_ytd,2016\n75,12,101.3,IND_PROD_ytd,2016\n76,1,102.3,IND_PROD_ytd,2017\n77,2,99.7,IND_PROD_ytd,2017\n')
                      , index_col = 0)
        
                  
    assert DFA.equals(dfa)
    assert DFQ.equals(dfq)
    assert DFM.equals(dfm)
    
    
# Not todo below
    
"""
Use different *raw_data* and *parsing_instructions* from file or constants 
--------------------------------------------------------------------------
  - csv must read from file, definitions must be read from file 
  - csv and definitions may be used in tests as files or hardcoded strings

Multiple segments
-----------------
  - this is one segment of file, will have different instructions for different 
    parts of CSV file
  - see SegmentState class https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/reader.py#L29  

Custom splitter function
------------------------
  - *DONE

Generate variable descriptions:
------------------------------
describe_var("GDP_yoy") == "Валовый внутренний продукт"
describe_unit("GDP_yoy") == "изменение год к году"
split("GDP_yoy") == "GDP", "yoy"  

# Implemented in Label class in reader.label
# https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/label.py

# Another strategy - saving text labels from file 
#    def get_headlabel_description_dicts(self):
#        return dict([(x["_head"],x["_desc"]) for x in self.get_iter_from_table(self.DB_HEADLABELS)])
       
Possible checks
---------------
Need to prioritize the checks:
  - all variables from definitions are read
  - some datapoints are read and compared to hardcoded values
  - sums round up to priod data
  - rates of change are product of monthly/quarterly rates  
  - other?
  
News csv file representation (?)
--------------------------------
- now a flat stream of lines
- may be a group of tables (header + data) + sections - tables 
  organised by section  
"""
