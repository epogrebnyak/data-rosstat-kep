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

if __name__ == "__main__":
   from common import infolder
   from database import wipe_db_tables
   from query import db_dump     
   data_folder = "../../data/ind06/"   
   csv  = infolder(data_folder, "tab.csv")
   spec = infolder("test_txt_files", "_yaml_spec_sample.txt")
   
   # --------------- Error 1: duplicates on import ---------------------------
   wipe_db_tables()
   to_database_by_spec(csv, spec)
   db_dump()
   """После этого прохода все записыватся в базу данных, и считывается из нее,
      все нормально."""
   
   #to_database_by_spec(csv, spec)
   #db_dump()   
   """После этого прохода в базе данных задваиваются данные, не проходит проверку
   Exception: Duplicate labels: I_bln_rub I_yoy Uslugi_bln_rub Uslugi_yoy
   Возмоные причины:
   - при записи данныx в базу данных не срабатывает REPLACE 
   - неверно выставлен первичный ключ базы данных
   - сам тест check_for_dups(dfa) неправильный, но это вряд ли"""
   # --------------- End Error 1 ---------------------------
   
   # --------------- Error 2: cannot parse /data/ind06/tab_spec.txt -----------
   spec = infolder(data_folder, "tab_spec.txt")
   to_database_by_spec(csv, spec)
   """почему-то не парсится /data/ind06/tab_spec.txt
    возможные пути :
        удалить все комментарии, посмотреть может где-то форматирование файла кривое
        закомментировать вообще все, и постепенно раскомментировать что было открыто        
    с более простой спецификацией test_txt_files/_yaml_spec_sample.txt выше все работает
   """
   # --------------- End Error 2 ---------------------------

      
   #cfg  = infolder(folder, "tab_cfg.txt")
   
# from common import get_raw_csv_filename, get_labelled_csv_filename, get_spec_filename
# from common import yield_csv_rows, dump_iter_to_csv

# # higher level wrapper
# def write_to_database(p):
    # gen = emit_flat_data(p)
    # stream_to_database(gen)

# try:
    # from .common import get_labelled_csv_filename, yield_csv_rows
# except:
    # from common import get_labelled_csv_filename, yield_csv_rows
    

# #------------------------------------------------------------------------------
# #  Generate stream from labelled csv file 
# #------------------------------------------------------------------------------

# def emit_flat_data(p):
    # """Emit all data from file *p*
    # p - path to csv file with var-labelled rows
    # """
    # f = get_labelled_csv_filename(p)
    # gen = yield_csv_rows(f)
    # return  stream_flat_data(gen)

# #------------------------------------------------------------------------------
# #  Convenience wrappers to make CSV with labelled rows 
# #------------------------------------------------------------------------------

# def yield_labelled_rows(p):
    # # obtain filenames
    # raw_data_file = get_raw_csv_filename(p)
    # spec_file = get_spec_filename(p)
    # # get labelled rows as iterator
    # return get_labelled_rows_by_single_specfile(raw_data_file, spec_file)

# def dump_labelled_rows_to_csv(p):
    # gen_out = yield_labelled_rows(p)
    # # obtain filename    
    # f = get_labelled_csv_filename(p)
    # # save to file
    # dump_iter_to_csv(gen_out, f)
