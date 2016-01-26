Todos
-----

0. move to folders + rename from sketch + make a package 

0. clean depreciated tests or make todos
   - test_mwe as test_rs2?
   - test_rs1 as fixture from plots.py?

0. rs.py L286 dump df csvs

0. dataframes.Varnames(): 
  > must order variable names by name 
  
  - add frequency column (may have letters A, Q, M in it, example: "A,Q,M", "A,M", "Q")
  - move table header from tabulate.py to Varnames
  - omit _year, _qtr, _month
  - not todo: mask some labels with extra text, possibly Segment().head_dicts[2] - third element in list
  
0. add missing variables + comment what not imported and why (duplicate) + see toc.txt

0. update on release of Dec 2015 data 
 
0. end use examples (Excel,Python,R) + more end use tests
   - retrieve data, options: 
      - open Excel file (xl or xlsx)
      - ```from kep import DFA, DFQ, DFM, VARNAMES, get_ts, get_df```
      - from url in python
      - from url in R
   - ... and look at it
   - state goal/hypothesis/research question 
   - clean data + calculate
   - plot and export results 
   - make conclusion (falsifiable statment, interesting to know/discuss, use in the future, decide using this information)

**Done**
> in output\varnames.md I have line, which should be without 1.12 (it is defined in https://github.com/epogrebnyak/rosstat-kep-data/blob/master/data/2015/ind12/__spec.txt#L345-L347) 
```| GOV_CONSOLIDATED_DEFICIT_bln_rub             | 1.12. ������� ( � ), �������� ������������������ �������                      | ����. ���.                             |```
possibly it is redefined somewhere else.

---
> rename previous folder ```kep`` to ``prekep``` + move to branch

---

> make_headers in Rowsystem()
>  + header emitters
>  + --  header emitter 1 - emit text rows possibly with modification
>  + --  header emitter 2 - re "#." counts as "assumed variable group"     
>  + count "assumed variable groups"
>  + write header emitter to file in self.folder
>  - can coverage be calculated?

**May do:**

- save csv dumps both to database folder and a copy to output folder 
- some slow tests + TrialDatabase() not used in tests
- clean tabulate.py	

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
