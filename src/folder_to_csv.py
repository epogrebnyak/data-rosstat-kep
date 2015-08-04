# -*- coding: utf-8 -*-

from word import dump_doc_files_to_csv, make_headers
import os        

def make_csv_in_stei_folder(folder):
    """Make single csv based on all STEI .doc files in current *folder*. """
    
    files = ["tab" + str(x) + ".doc" for x in range(0,5)] 
    files[0] = "tab.doc"
    file_list = [os.path.abspath(folder + fn) for fn in files]
    csv = os.path.join(folder, "all_tab.csv")

    dump_doc_files_to_csv(file_list, csv)
    make_headers(csv)
    
if __name__ == "__main__":
    folder = os.path.abspath("../data/ind06/")
    make_csv_in_stei_folder(folder)
