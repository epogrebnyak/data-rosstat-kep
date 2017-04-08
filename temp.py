# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 21:37:06 2017

@author: Евгений
"""
from pprint import pprint

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
rows = [r.split('\t') for r in DOC.split('\n')]

headers = {"Объем ВВП" : dict(var="GDP", unit="bln_rub")
, "Индекс физического объема произведенного ВВП" : dict(var="GDP", unit="rog")
, "Индекс промышленного производства" : dict(var="IND_PROD", unit="")
}

units = {"в % к предыдущему периоду" : "rog",
         "период с начала отчетного года в % к соответствующему периоду предыдущего года" : "ytd",
         "в % к соответствующему периоду предыдущего года" : "yoy"}

def yield_rows(rows):
    for r in rows:
        if r and r[0]:  
            yield dict(head=r[0], data=r, label={'var':"", 'unit':""})

#pprint([x for x in yield_rows(rows)])
   
def is_year(s):
    try:
        int(s[:4])
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

   
empty_label = {'var':"", 'unit':""}    
current_label = {'var':"", 'unit':""}

for row in yield_rows(rows):
    
    if is_year(row['head']):
        row['label'] = current_label
        print(row['head'], view_label(current_label))  
     
    else:        
        flag1, current_header = detect(row['head'], headers.keys())
        if flag1:
           current_label = headers[current_header]
        flag2, unit = detect(row['head'], units.keys())
        if flag2:
            current_label['unit'] = units[unit]
        
        row['label'] = current_label   
     
      
def view_label(lab):
    return lab['var'] + "_" + lab['unit']



def which_label_in_text(text, lab_dict):
    for pat in lab_dict.keys():
        if pat in text:
            # found matching text anywhere in line
            return lab_dict[pat]
    return None
