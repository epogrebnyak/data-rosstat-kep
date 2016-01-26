Todos
-----

##Future

0. update output on release of Dec 2015 data - see rs.update.py

##Critcal

0. move todos form more.txt

0. rename classes from sketch 

0. remove older folders to branches

0. rs.py L286 dump df csvs - control structure

0. RowSystem.apparent_timeseries_count():
   - # in datainfo rows count all 2014 years - if startswith "2014"
   - # add this statistics to __repr__()
   - not todо/make issue: number of variables by section. 

0. very slim frontface - output as a package for pandas - see https://github.com/epogrebnyak/rosstat-kep-data/blob/master/rs/init__.py and dataframes.KEP() + put it in output folder to enable ```from output import DFA, DFQ, DFM, VARNAMES, get_ts, get_df```

0. comment what not imported and why in toc.txt
   - add missing variables defintions
   - make list of 

0. URL wrappers - https://github.com/epogrebnyak/rosstat-kep-data/issues/92

0. end use examples (Excel,Python,R) + more end use tests
   - retrieve data, options: 
      - open Excel file (xl or xlsx)
      - git clone + or download as zip and acces locally ```from output import DFA, DFQ, DFM, VARNAMES, get_ts, get_df```
      - from url in python
      - from url in R-  
   - ... and look at it
   - state goal/hypothesis/research question 
   - clean data + calculate
   - plot and export results 
   - make conclusion (falsifiable statment, interesting to know/discuss, use in the future, decide using this information)

##Low priority

0. move to folders + make a package 

0. clean depreciated tests or make todos
   - test_mwe as test_rs2?
   - test_rs1 as fixture from plots.py?

0. dataframes.Varnames(): 

  > must order variable names by name 
  
  - add frequency column (may have letters A, Q, M in it, example: "A,Q,M", "A,M", "Q")
  - these frequencies are available from Varnames().get_varnames(self, freq = None), where freq is in 'aqm'
  - move table header from tabulate.py to Varnames
  - omit _year, _qtr, _month
  - not todo: mask some labels with extra text, possibly Segment().head_dicts[2] - third element in list

##Forget about it

- save csv dumps both to database folder and a copy to output folder 
- some slow tests + TrialDatabase() not used in tests
- clean tabulate.py	

Done
----

> in output\varnames.md I have line, which should be without 1.12 (it is defined in https://github.com/epogrebnyak/rosstat-kep-data/blob/master/data/2015/ind12/__spec.txt#L345-L347) 
```| GOV_CONSOLIDATED_DEFICIT_bln_rub             | 1.12. Äåôèöèò ( – ), ïðîôèöèò êîíñîëèäèðîâàííîãî áþäæåòà                      | ìëðä. ðóá.                             |```
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

