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
             
             
def csv_file_to_dicts(filepath):
    rows = from_csv(filepath)
    for row in rows:
        if row and row[0]:
            yield dict(head=row[0], data=row[1:])   