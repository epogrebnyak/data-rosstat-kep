Project sketch
---------------

- ```reader.CurrentMonthRowSystem``` reads data from raw and dirty CSV file using parsing specification from yaml files. ```CurrentMonthRowSystem``` also saves a stream of clean database rows to sqlite database and (via ```DictsAsDataframes()```) dumps end-use dataframes as CSVs.

- ```dataframes.KEP``` is a slim end-use class that contains 3 dataframes (at annual, quarter and monthly frequencies) and two data retrieval functions (```get_df``` and ```get_ts```). ```KEP()``` is initialised  by reading CSV dumps. 

- ```dataframes.Publisher(KEP)``` saves Excel, PDF and graphics files to output folder. 

- While everything may work without database now, ```Database()``` wrapper around sqlite is implemented for future development and data transfer. It may be particularly useful for storing vintages of time series.


Dataflow
--------

```
1. LOGIC OF DATAFLOW

   csv + yamls --> CurrentMonthRowSystem() --> KEP()       --> end use dataframes (dfa, dfq, dfm) + varnames
                                               Publisher() --> xls + png + pdf + (csv)
											   
2. IMPLEMENTATION

config.py 

rs.py: """Import raw data and parsing specification, generate stream of dicts, and save it to sqlite database and csv dumps."""
\reader: inputs.py + rs.py + label.py + stream.py + word.py
     csv + yamls      --> CurrentMonthRowSystem() --> (stream of dicts) 

db.py: """Accept a stream of dicts and store it to database + read a stream of dicts from database."""
\database: db.py
   (stream of dicts)  --> Database() --> sqlite database + dataframe CSV dump 
   
     sqlite database  --> Database() --> (stream of dicts)    
  dataframe CSV dump  --> KEP()      --> end use dataframes (dfa, dfq, dfm) + varnames()

dataframes.py: """Transform a stream of dicts to pandas dataframes, read/write dataframes as csv."""  
\dataframes: dataframes.py + plots.py
   (stream of dicts)  --> DictsAsDataframes() --> end use dataframes (dfa, dfq, dfm)    --> dataframe CSV dump
 dataframe CSV dump   --> KEP()               --> end use dataframes (dfa, dfq, dfm) + varnames() 
KEP+Varnames+plots.py --> Publisher()         --> xls + png + pdf

\plotting: plots.py
end use dataframes (dfa, dfq, dfm) --> plots.py --> png + pdf

\tests
   \reader
   \database
   \dataframes
   \plotting
   \end_to_end
   \depreciated 
```
