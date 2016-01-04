# -*- coding: utf-8 -*-
"""Import data from Word files or raw CSV to database and dump outputs.
Note: same as kep.update() or kep\\update.py"""

import kep 
data_folder = "data/2015/ind11"

# 1. convert Word files to csv 
kep.make_csv(data_folder)

# 2. parse and import csv to database
kep.import_csv(data_folder)

# 3. run some inspection 
kep.notify_on_import_result(data_folder)    
    
# 4. export times series from database to CSV and Excel xls(x)
kep.db_dump()
    
# 5. create and save PDF and *.png graphs
kep.write_plots()
    
# 6. keprites list of variables to markdown file 
kep.dump_var_list_explained()

# NOTE:
# all of the above also done by:
# kep.update(data_folder)
