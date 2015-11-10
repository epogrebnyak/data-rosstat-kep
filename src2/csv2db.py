try:
	from label_csv import get_labelled_rows
	from stream import stream_flat_data
	from database import stream_to_database
except:
	from .label_csv import get_labelled_rows
	from .stream import stream_flat_data
	from .database import stream_to_database
	
def to_database(raw_data_file, spec_file, cfg_file = None):
    lab_rows = get_labelled_rows(raw_data_file, spec_file, cfg_file)
    db_rows = stream_flat_data(lab_rows)
    stream_to_database(db_rows)
    
if __name__ == "__main__":
    from common import infolder
    from database import wipe_db_tables
    from query import db_dump     
    data_folder = "../data/ind09/"   
    csv  = infolder(data_folder, "tab.csv")
    spec = infolder(data_folder, "tab_spec.txt")
    сfg = infolder(data_folder, "tab_cfg.txt")
    wipe_db_tables
    to_database(csv, spec)
	#to_database(csv, spec, cfg)
    db_dump()
    # agg a dump of variables to separate sheet and csv file.

    from query import get_var_list
    from api2 import get_dataframe
	
    PDF_FILE = 'output/monthly.pdf'
	
    # NOTE: must merge *query* and *api2*.
    from plots import save_plots_as_pdf, one_plot 
    var_names = get_var_list()
    df = get_dataframe(var_names, "m", "1999-01")
    save_plots_as_pdf(df, PDF_FILE, 3, 2)
    
    # todo-4 @DN:
    for vn in var_names:
        ts = df[[vn]]
        fig = one_plot(ts)
        filename = "output/png/" + vn + ".png"
        # записывать one_plot(ts) рисунок в filename 
        
    # todo-5 @DN:
        # сгенерировать markdown файл, в котором по 3 на строку
        # выведены все картинки var_names + ".png"       