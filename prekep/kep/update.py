# -*- coding: utf-8 -*-
import os

# data import to db
from kep.importer.converter.word import make_csv
from kep.importer.csv2db import import_csv
from kep.inspection.var_check import notify_on_import_result 

# writing data as output
from kep.query.save import db_dump
from kep.query.plots import write_plots
from kep.query.var_names import dump_var_list_explained

# folder 
from kep.paths import CURRENT_MONTH_DATA_FOLDER 

def update_db(data_folder = CURRENT_MONTH_DATA_FOLDER):
    """Creates CSV and imports data to database with notification"""
    
    # Converting tables from Word files to one CSV file (if CSV file does not exist, need MS Word installation)
    make_csv(data_folder)

    # Parse and upload CSV file to database
    import_csv(data_folder)

    # Run some inspection of import results - are all variables imported?
    notify_on_import_result(data_folder) 
    
    print("Finished updating based on folder:", CURRENT_MONTH_DATA_FOLDER, "\n")


def update_output():
    """Write new files to output folder based on current content of the database."""
    # Export times series from database to CSV files and Excel xls(x)
    db_dump()    
    
    # Draw graphs and save them as in PDF file and as many .png files 
    write_plots()

    # Dump variable names to markdown file  
    # Note: may also want to see frequencies of data
    dump_var_list_explained()
    
    print("Finished writing CSV, Excel, PDF and png to output folder")   
    
    
def update(data_folder = CURRENT_MONTH_DATA_FOLDER):  
   update_db(data_folder)
   update_output()