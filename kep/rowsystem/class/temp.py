import dataset 

DB_MAIN_TABLE = 'flatdata'

def test_dict_iterator():
    yield {'varname':'GDP_rub', 'year':2014, 'val':65000}
    yield {'varname':'GDP_rub', 'year':2014, 'val':62000}
    
gen = test_dict_iterator()

KEYS = next(test_dict_iterator()).keys()


def db_connect():
    sqlite_file = "kep.sqlite3"
    return dataset.connect('sqlite:///' + sqlite_file)

with db_connect() as con:
    con[DB_MAIN_TABLE].delete()
    
with db_connect() as con:
    con[DB_MAIN_TABLE].insert_many(gen)    

with db_connect() as con:
    for row in con[DB_MAIN_TABLE]:
        print ({k:row[k] for k in KEYS})   

        