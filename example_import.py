# -*- coding: utf-8 -*-
### Импорт в базу данных

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

# TODO: var_list not saved (?)
# TODO: more Starting (job) +  Done (job) messages.