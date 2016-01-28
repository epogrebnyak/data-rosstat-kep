Development notes
=================

This project goal is to make Russian economic statistics available as online time series database, in a fashion similar to  [FRED](https://research.stlouisfed.org/fred2/), [Quandl](https://www.quandl.com/) and other database sources. Hopefully it can make quantative research on Russian economy more accessbile/reproducible and less 'black box'.

We take a publication from Rosstat as a group of MS Word files, make a raw CSV file, parse it to flat database rows stream and convert this steam to pandas and R dataframes and well as CSV, Excel files and some graphic output. 

Some day Rosstat will have an open API frondend to their data making this project irrelevant. So far it our best bet for open-source Russian economic data time series.  

Main entry
----------

Main entry point to ```kep``` package is [update.py](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/update.py). Its listing is below:

```
from pandas import pd
from kep.reader.rs import CurrentMonthRowSystem
from kep.extract.publish import Publisher
from kep.extract.dataframes import KEP

# read raw csv datafile and save data to sqlite and clean CSV dumps 
CurrentMonthRowSystem().update()

# visualise data in 'ouput' directory
Publisher().publish()

# access available data as pandas 
dfa, dfq, dfm = KEP().dfs()
```

- ```reader.CurrentMonthRowSystem``` reads data from raw and dirty CSV file using parsing specification from yaml files. ```CurrentMonthRowSystem``` also saves a stream of clean database rows to sqlite database and (via ```DictsAsDataframes()```) dumps end-use dataframes as CSVs.

- ```dataframes.Publisher(KEP)``` saves Excel, PDF and graphics files to output folder. 
 
- ```dataframes.KEP``` is a slim end-use class that contains 3 dataframes (at annual, quarter and monthly frequencies) and two data retrieval functions (```get_df``` and ```get_ts```). ```KEP``` is initialised by reading CSV dumps of dataframes. 

Additional comments
-------------------

- While everything may work without database now, ```kep.database.Database()``` wrapper around sqlite is implemented for future development and data transfer. It may be particularly useful for storing vintages of time series.

Some spaghetti:
- ```dataframes.Varnames``` class uses a dictionary of variable names obtained at ```CurrentMonthRowSystem```.  Invoking ```CurrentMonthRowSystem``` to read it is too heavy, so a dictionary is stored in sqlite database and read back from it by ```dataframes.Varnames``` - does not seem too elegant. 


Dataflow
--------

```
1. LOGIC OF DATAFLOW

   csv + yamls --> CurrentMonthRowSystem() --> KEP()       --> dfa, dfq, dfm (end use dataframes)
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
