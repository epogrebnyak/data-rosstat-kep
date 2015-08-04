# -*- coding: utf-8 -*-

from word import yield_continious_rows, dump_iter_to_csv, make_headers
import os

def yield_folder(file_list):
    print()
    for p in file_list:
        print("File:", p)
        for row in yield_continious_rows(p):
            yield row
            
def dump_files_to_csv(file_list, csv):
    folder_iter = yield_folder(file_list)
    dump_iter_to_csv(folder_iter, csv) 
    return csv

def make_csv_in_stei_folder(folder)
    files = ["tab" + str(x) + ".doc" for x in range(0,5)] 
    files[0] = "tab.doc"
    file_list = [os.path.abspath(folder + fn) for fn in files]
    csv = os.path.abspath(folder + "all_tab.csv")
        
    dump_files_to_csv(file_list, csv)
    make_headers(csv)
    
if __name__ == "__main__":
    folder = "data/ind06/"
    make_csv_in_stei_folder(folder)
