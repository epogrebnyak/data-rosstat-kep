"""Parse and import Rosstat KEP publication to local database and query database to get time series from it.

1. Converter
doc - > raw csv
(word.py)
2. Parser
raw csv + specification -> labelled csv -> flat stream -> database
         (load_spec.py)   (label_csv.py)  (stream.py)    (database.py)
3. Selector
database -> dfm, dfq, dfa -> get_ts(), get_df()
                      ... -> get_varnames()   
(query.py)

1. Converter
   Convert several MS Word files containing (a bit chaotic) tables to raw CSV file
   Files: word.py
   
2. Parser
   Attach labels to rows in raw CSV file, flatten data and import it to database 
   Files:
     label_csv.py, load_spec.py, stream.py	
     common.py, database.py
     csv2db.py (control file)

3. Selector
   Query database for pandas TimeSeries or DataFrame.
   Files:  query.py

4. Plotting 
   Files:  plots.py

5. Testing 
   Files: hardcoded.py, test_1.py	
     
6. Current work
   Files: temp.py  
""" 

__all__ = ["common", 
    "csv2db", 
    "database", 
    "hardcoded", 
    "label_csv", 
    "load_spec", 
    "plots", 
    "query", 
    "stream", 
    "temp", 
    "var_names", 
    "word"]
