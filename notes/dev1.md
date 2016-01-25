Todos
-----

0. move to folders + rename from sketch + make a package 

0. clean depreciated tests or make todos
   - test_mwe as test_rs2?
   - test_rs1 as fixture from plots.py?

0. dataframes.Varnames(): 
  - must order variable names by name 
  - omit _year, _qtr, _month
  - add frequency column (may have letters A, Q, M in it, example: "A,Q,M", "A,M", "Q")
  - move table header from tabulate.py to Varnames
    
0. make_headers in Rowsystem()
  - header emitters
    - header emitter 1 - emit text rows
    - header emitter 2 - re "#." counts as "assumed variable group"     
  - count "assumed variable groups"
  - write header emitter to file in self.folder
  - can coverage be calculated?
  
0. add missing variables 

0. update on release of Dec 2015 data 

### May do:
- save csv dumps both to database folder and a copy to output folder 
- some slow tests + TrialDatabase() not used in tests
- clean tabulate.py	

Project sketch
---------------

- ```reader.CurrentMonthRowSystem``` reads data from raw/dirty CSV file using parsing specification from yaml files. It also  
  saves a stream of clean database rows to sqlite database and via ```DictsAsDataframes()``` dumps end-use dataframes as CSVs.

- ```dataframes.KEP``` is end-use class that contains dataframes and data retrieval functions. ```KEP()``` is initialised 
  by reading CSV dumps. 

- ```dataframes.Publisher(KEP)``` saves Excel and graphics to output folder. 

**Comments:**

- Everything may work without sqlite database now, implemented for future development/data transfer 


```
config.py 


rs.py: """Import raw data and parsing specification, generate stream of dicts, and save it to sqlite database and csv dumps."""
\reader: inputs.py + rs.py + label.py + stream.py + word.py
     csv + yamls      --> CurrentMonthRowSystem() --> (stream of dicts) 


db.py: """Accept a stream of dicts and store it to database + read a stream of dicts from database."""
\database: db.py
   (stream of dicts)  --> Database() --> sqlite database + dataframe CSV dump 
   
     sqlite database  --> Database() --> (stream of dicts)    
  dataframe CSV dump  --> KEP()      --> end use dataframes (dfa, dfq, dfm) + varnames()


dataframes.py: """Transform a stream of dicts to pandas dataframes, read/write dataframes as csv*2."""  
\dataframes: dataframes.py + plots.py
   (stream of dicts)  --> DictsAsDataframes() --> end use dataframes (dfa, dfq, dfm)             --> dataframe CSV dump
 dataframe CSV dump   --> KEP()               --> end use dataframes (dfa, dfq, dfm) + varnames() 
KEP+Varnames+plots.py --> Publisher()         --> xls + png + pdf


\plotting: plots.py
end use dataframes (dfa, dfq, dfm) --> plots.py --> 


\tests
   \reader
   \database
   \dataframes
   \plotting
   \end_to_end
   \depreciated 
```       
                                          
Extra notes
-----------
 
Todos are on different levels:

  - local and well defined tasks, code refactoring 
  - overall program architecture, design decisions 
