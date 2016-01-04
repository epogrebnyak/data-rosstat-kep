from kep.importer.csv2db import to_database
from kep.inspection.var_check import inspect_db
from kep.database.db import wipe_db_tables

#to_database(raw_data_file, spec_file, cfg_file = None):
#    lab_rows = get_labelled_rows(raw_data_file, spec_file, cfg_file)
#    db_rows = stream_flat_data(lab_rows)
#    stream_to_database(db_rows)

folder = "C:\\Users\\Евгений\\Documents\\GitHub\\rosstat-kep-data\\data\\2015\\ind10\\"
raw_data_file = folder + "tab.csv"
spec_file = folder + "spec_profit.txt" # "spec_overdue.txt" #"spec_profit.txt" # "spec_cpi.txt"

wipe_db_tables()
to_database(raw_data_file, spec_file)
lab_rows = get_labelled_rows(raw_data_file, spec_file, cfg_file)
# Inspection procedure
inspect_db(folder) 
