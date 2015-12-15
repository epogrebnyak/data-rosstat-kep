# -*- coding: utf-8 -*-
"""Import data from Word files or raw CSV to database
Note: same as kep.update() or kep\\update.py"""

import kep 
data_folder = "data/2015/ind10"

# convert Word files to csv 
kep.make_csv(data_folder)

# parse and import csv to database
kep.import_csv(data_folder)

# save data and variable list to Excel and CSV files 
kep.db_dump()

# write plots to PDF and *.png files
kep.write_plots()
    
# run some inspection 
kep.notify_on_import_result(data_folder)    
    
# export times series from database to CSV files and Excel xls(x)
kep.db_dump()
    
# create and save PDF and *.png graphs
kep.write_plots()
    
# keprites list of variables to nmarkdown file 
dump_var_list_explained()

# all of the above also done by:
kep.update(data_folder)