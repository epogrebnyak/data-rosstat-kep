import pandas as pd

predoc = ["1. Gross domestic product at current prices", "billion ruble", "YEAR\tVALUE", "2013\t61500", "2014\t64000"]
doc = "\n".join(predoc)

RS_FROM_FILE = [
       {'string':"1. Gross domestic product at current prices",
          'list':["1. Gross domestic product at current prices"],
		  'head':"1. Gross domestic product at current prices",
		  'is_data_row':False,
		  'primary_label':None,
		  'unit_label':None},
		
		{'string':"billion ruble",
          'list':["billion ruble"],
		  'head':"billion ruble",
		  'is_data_row':False,
		  'primary_label':None,
		  'unit_label':None},		  
		
		{'string':"YEAR\tVALUE",
          'list':["YEAR", "VALUE"],
		  'head':"YEAR",
		  'is_data_row':False,
		  'primary_label':None,
		  'unit_label':None},
		  
		{'string':"2013\t61500",
          'list':["2013", "61500"],
		  'head':"2013",
		  'is_data_row':True,
		  'primary_label':None,
		  'unit_label':None},

		{'string':"2014\t64000",
          'list':["2014", "64000"],
		  'head':"2014",
		  'is_data_row':True,
		  'primary_label':None,
		  'unit_label':None}
		  ]

LABELLED_RS = RS_FROM_FILE
for i in [3,4]:
    LABELLED_RS[i]['primary_label'] = "GDP"
    LABELLED_RS[i]['unit_label'] = "bln_rub"	

header_dict = {"Gross domestic product": ["GDP", "bln_rub"]}
unit_dict = {'percent change to previous year': 'yoy'}
dicts = header_dict, unit_dict 

GDP_DF = pd.DataFrame.from_items([
                                 ('GDP', [61500, 64000])
				                 ])			 
GDP_DF.index = [2013,2014]								 
 	
def doc_to_rowsystem(doc):
	return RS_FROM_FILE 

def label_rowsystem(rs, dicts):
    return LABELLED_RS
	
rs1 = doc_to_rowsystem(doc)
assert rs == RS_FROM_FILE 

rs2 = label_rowsystem(rs1, dicts)
assert rs == LABELLED_RS 



	
rs2 = label_rowsystem(rs, dicts):
assert rs2 == LABELLED_RS

