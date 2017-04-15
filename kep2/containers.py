from config import get_default_csv_path
from csv_data import CSV_Reader

# data
csv_path = get_default_csv_path()
csv_dicts = list(CSV_Reader(csv_path).yield_dicts())

def get_year(s: str) -> int:
    """Extract year from string *s*.
    >>> get_year('2015')  # most cases
    2015
    >>> get_year('20161)') # some cells with comment
    2016
    >>> get_year('20161)2)') # some cells with two comments
    2016
    #>>> get_year('27000,1-45000,0') # will raise ValueError    
    #ValueError: 27000,1-45000,0is not a year."""
    if is_year(s):
        return int(s[:4])
    else:
        raise ValueError(s + " is not a year.")

def is_year(s: str)->bool:
    """Check if *s* contains year number.
    >>> is_year('1. Сводные показатели')
    False
    >>> is_year('20151)')
    True"""
    try:
        x = int(s[:4])
        if x > 1900 and x < 2050 and '-' not in s:
            return True
        else:
            return False
    except:
        return False

def is_numeric(s: str)->bool:
    # replace all digits and see what remains
    pass

def is_top_section_name(s: str)->bool:
    if len(s) > 3 and s[0].isdigit() and s[1] == "." and s[2] == " ":
        return True
    else:
        return False    

def echo(h: str):
    try:
        print(h)
    except UnicodeEncodeError:
        print (h[:5] + "...")
    

if __name__ == "__main__":

    #import doctest
    #doctest.testmod()

    import itertools

    text_block = {'labels':[], 'datarows':[]}
    datarows = []
    i = 0
    h_0 = ""

    for d in csv_dicts: #itertools.islice(csv_dicts):
        h = d['head']
        #if is_top_section_name(h):
        #    print(h)
        #    i = 0
        #    current_top_section = h
        if is_year(h):
            i = i + 1
            datarows.append(d)
            #print(i, h)
        else:
            text_block['labels'].append(h)            
            if i > 0:
               print(i, "data rows")            
            if is_year(h_0):
                print("--------------------------------------------------")
                # must flush to  
            echo(h)
            i = 0

        h_0 = h
