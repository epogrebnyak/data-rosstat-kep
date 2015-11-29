import os

try:
    from common import get_filenames
    from label_csv import get_labelled_rows
    from stream import stream_flat_data
    from database import stream_to_database, wipe_db_tables
    from query import get_var_list, db_dump, get_dataframe
    from var_names import dump_var_list_explained
    from plots import save_plots_as_pdf
except (SystemError, ImportError): 
    from .common import get_filenames
    from .label_csv import get_labelled_rows
    from .stream import stream_flat_data
    from .database import stream_to_database, wipe_db_tables
    from .query import get_var_list, db_dump, get_dataframe
    from .var_names import dump_var_list_explained
    from .plots import save_plots_as_pdf

def to_database(raw_data_file, spec_file, cfg_file = None):
    lab_rows = get_labelled_rows(raw_data_file, spec_file, cfg_file)
    db_rows = stream_flat_data(lab_rows)
    stream_to_database(db_rows)
 
def import_csv(data_folder):
    csv, spec, cfg = get_filenames(data_folder)
    wipe_db_tables()
    to_database(csv, spec)
    #to_database(csv, spec, cfg)
    # TODO: start reading some duplicate variables with config file
    # example: 

    db_dump()    
    dump_var_list_explained()
    # TODO: add a dump of variables as in *output/varnames.md* to a separate sheet of kep.xls(x)

def write_monthly_pdf():
    PDF_FILE = 'output/monthly.pdf'
    var_names = get_var_list()    
    df = get_dataframe(var_names, "m", "1999-01")
    save_plots_as_pdf(df, PDF_FILE, 3, 2)  

if __name__ == "__main__":    
    data_folder = "../data/ind09/"
    #import_csv(data_folder)
    
    #var_names = get_var_list() 
    #print(var_names)
    #write_monthly_pdf()
    pass 

# NOTE: must merge *query* and *api2*.
