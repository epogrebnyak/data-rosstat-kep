# -*- coding: utf-8 -*-
### Импорт в базу данных

import kep 
data_folder = "data/2015/ind10"

# TODO:
# must stop if (1) no Word installed, (2) CSV already exists 
kep.make_csv(data_folder)

# 
kep.import_csv()

# save data and variable list to Excel, CSV files, write plots to PDF and *.png 
# TODO: separate to two commands
kep.dump_db()
