# -*- coding: utf-8 -*-
import os

# Converting tables from Word files to one CSV file
from kep.converter.word import make_csv
# Parsing CSV file and uploading to database
from kep.parser.csv2db import import_csv
# Save data from database to CSV and Excel xls(x)
from kep.selector.save import db_dump
# Graphs
from kep.plots.plots import write_plots
# NOTE: dump_var_list_explained is not part of example_import.py
# Operate with variable names
from kep.selector.var_names import dump_var_list_explained

if __name__ == "__main__":
    data_folder = "data/2015/ind10/"
    
    # Create CSV file
    make_csv(data_folder)
    
    # Parse and upload CSV file to database
    import_csv(data_folder)
    
    # Export times series from database to CSV files and Excel xls(x)
    db_dump()
    
    # Create and save PDF and *.png graphs
    write_plots()
    
    # Writes list of variables
    dump_var_list_explained()