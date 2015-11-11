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
 
def get_filenames(folder):
    # NOTE: bad name for join() function 
    from common import infolder
    csv  = infolder(data_folder, "tab.csv")
    spec = infolder(data_folder, "tab_spec.txt")
    сfg =  infolder(data_folder, "tab_cfg.txt")
    return csv, spec, сfg

def import_csv(data_folder):
    from database import wipe_db_tables
    from query import db_dump     
    # TODO-6 DONE: важно - вызов из новой папки не проходит Exception: Duplicate labels: TRANS_COM_bln t-km TRANS_RAILLOAD_mln_t TRANS_bln t-km
    csv, spec, cfg = get_filenames(data_folder)
    wipe_db_tables()
    to_database(csv, spec)
    #to_database(csv, spec, cfg)
    db_dump()
    # add a dump of variables to separate sheet and csv file.

def write_pdf():
    from query import get_var_list
    from api2 import get_dataframe
	
    PDF_FILE = 'output/monthly.pdf'
	
    # NOTE: must merge *query* and *api2*.
    from plots import save_plots_as_pdf 
    var_names = get_var_list()
    df = get_dataframe(var_names, "m", "1999-01")
    save_plots_as_pdf(df, PDF_FILE, 3, 2)
       
if __name__ == "__main__":
    data_folder = "../data/ind09/"
    import_csv(data_folder)
    var_names = get_var_list()
    print(var_names)
    write_pdf()

    # todo-4 @DN:
    from plots import one_plot 
    from query import get_var_list
    from api2 import get_dataframe
    df = get_dataframe(var_names, "m", "1999-01")
    var_names = get_var_list()
    for vn in var_names:
        #ts = df[[vn]]       
        #fig = one_plot(ts)
        #filename = "output/png/" + vn + ".png"
        # записывать one_plot(ts) рисунок в filename 
        pass
    
        
    # todo-5 @DN:
        # сгенерировать markdown файл, в котором по 3 на строку
        # выведены все картинки var_names + ".png"  
        
    # todo-7 - DONE:
        # в https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src2/output/monthly.pdf
        # дублируются два показателя USLUGI_bln_rub	USLUGI_yoy и Uslugi_bln_rub	Uslugi_yoy
        # непонятно почему происходит и как от этого избавиться

