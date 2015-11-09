try:
	from label_csv import get_labelled_rows
	from stream import stream_flat_data
	from database import stream_to_database
except:
	from .label_csv import get_labelled_rows
	from .stream import stream_flat_data
	from .database import stream_to_database

def to_database_by_spec(raw_data_file, _spec_file):
    to_database(raw_data_file, spec_file = _spec_file)

def to_database_by_cfg(raw_data_file, _cfg_file):
    to_database(raw_data_file, cfg_file= _cfg_file)
	
def to_database(raw_data_file, spec_file = None, cfg_file = None):
    lab_rows = get_labelled_rows(raw_data_file, spec_file, cfg_file)
    db_rows = stream_flat_data(lab_rows)
    stream_to_database(db_rows)


    from query import get_var_list
    from api2 import get_dataframe
    df = get_dataframe(get_var_list(), "m", "1999-01")
    save_plots_as_pdf('monthly.pdf', (3, 2), df)

if __name__ == "__main__":
    from common import infolder
    from database import wipe_db_tables
    from query import db_dump     
    data_folder = "../../data/ind06/"   
    csv  = infolder(data_folder, "tab.csv")
    spec = infolder(data_folder, "tab_spec.txt")
    wipe_db_tables
    to_database_by_spec(csv, spec)
    db_dump()

    from query import get_var_list
    from api2 import get_dataframe
    # NOTE: must merge *query* and *query*.
    from plots import save_plots_as_pdf
    df = get_dataframe(get_var_list(), "m", "1999-01")
    save_plots_as_pdf('monthly.pdf', (3, 2), df)