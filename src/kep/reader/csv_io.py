import csv 
from kep.ini import ENCODING, CSV_FORMAT

def to_csv(rows, filepath):
    """Accept iterable of rows *rows* and write in to *csv_path*"""
    with open(filepath, 'w', encoding=ENCODING) as csvfile:
        filewriter = csv.writer(csvfile, **CSV_FORMAT)
        for row in rows:
            filewriter.writerow(row)
    return filepath


def from_csv(filepath):
    """Get iterable of rows from *csv_path*"""
    with open(filepath, 'r', encoding=ENCODING) as csvfile:
       csvreader = csv.reader(csvfile, **CSV_FORMAT)
       for row in csvreader:
             yield row  
    
         
def to_dict(row):
    """Make dictionary based on non-empty *row*"""
    if row and row[0]:
       return dict(head=row[0], data=row[1:])
    else:
       return None
    
    
def csv_file_to_dicts(filepath):
    """Yield non-empty dictionaries from CSV *filepath*"""
    raw = from_csv(filepath)
    csv_dicts = map(to_dict, raw)    
    return filter(lambda x: x is not None, csv_dicts) 


if __name__ == "__main__":
    import kep.ini as ini
    filepath = ini.get_path_csv_data()
    gen = from_csv(filepath)
    zen = csv_file_to_dicts(filepath)
    print(len(list(gen)))
    print(len(list(zen)))