from kep.inspection.var_check import count_entries, unique, get_complete_dicts
from kep.file_io.common import get_filenames, write_file
from kep.importer.parser.label_csv import get_nondata_rows

data_folder = "data/2015/ind10"
csv, spec, cfg = get_filenames(data_folder)
rows = get_nondata_rows(csv)
fst_elements = [r[0] for r in rows]
def is_almost_in(x, lst):
    flag = 0
    for y in lst:
       if x[0:10] in y:
           flag += 1
    return flag 
#rows_with_count = [[r, count_entries(r[0], fst_elements)] for r in rows]
def is_almost_in(x, lst):
    flag = 0
    for y in lst:
       if x[0:10] in y:
           flag += 1
    return flag 
rows_with_count = [[r, is_almost_in(r[0], fst_elements)] for r in rows]
interest = unique([x[0][0] for x in rows_with_count if x[1] > 1 and len(x[0][0]) > 1])
# error on printing to screen - Unicode
write_file("\n".join(interest),"i.txt")


#todo: failures are where too many entries (>1) of spec/cfg dictionaries are found in fst_elements

#get big specification
#see how many times header_dict keys hit fst_elements

header_dict, unit_dict = get_complete_dicts(data_folder)


  

def is_in(x, lst):
    flag = 0
    for y in lst:
       if x in y:
           flag += 1
    return flag           

keys_with_count =  [[x, is_in(x, fst_elements)] for x in sorted(list(header_dict.keys())) ]
interest2 = [x for x in keys_with_count if x[1] > 1]
write_file("\n".join([str(x[0]) + " : " + str(x[1]) for x in interest2]),"i2.txt")

# Legacy code:
#
#def make_headers(p):
#    """Makes a list of docfile table headers and footers in txt file.
#    Used to review file contents and manually make label dictionaries."""    
#    f = get_headers_filename(p)    
#    with open(f, "w") as file:
#       for row in yield_csv_rows(p):
#           if not is_year(row[0]) and len(row[0]) > 0:
#                file.write(row[0] + "\n")
#    return f 