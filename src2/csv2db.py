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
    data_folder = "../data/ind06/"   
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
    from plots import save_plots_as_pdf
    df = get_dataframe(get_var_list(), "m", "1999-01")
    # save_plots_as_pdf(PDF_FILE, (3, 2), df)
	
 
#------------------------------------------------------------------------------ 

 	# todo - html + png dump:
	# сделать либо: 
	# - дамп отдельных маленких картинок в .png файлы в папку output/png
	# - дамп картинок 3*2 которые сейчас генерируются в pdf туда же
	# (смотря что проще)
	# - сгенерировать html файл которые показывает эти .png 
	# - опциональное - запускать браузер для просмотра этого файла

#------------------------------------------------------------------------------ 
	
	