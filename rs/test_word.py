import os
from config import TESTDATA_DIR, RESERVED_FILENAMES
from word import make_csv

def test_make_csv():

    # tab.doc is assumed to be in TESTDATA_DIR
    # will run only on Windows with MS Word    
    
    csv = os.path.join(TESTDATA_DIR, RESERVED_FILENAMES['csv'])
    if os.path.exists(csv):
        os.remove(csv)
    make_csv(TESTDATA_DIR)
    assert 6267 == os.path.getsize(csv)
    os.remove(csv)
