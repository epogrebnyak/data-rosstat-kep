# -*- coding: utf-8 -*-
"""
"""
# IMPORT ERROR: here and below - cannot do proper import of modules from parent directory 
from src2.common import test_io

# tests below rely on hardcoded.py
from ..load_spec import test_individial_docs_and_dicts, test_in_one_doc, test_with_file
from ..label_csv import test_label_csv1, test_segment_specs, test_label_csv2
# ---------------------------------

from ..stream import test_flat_emitter
from ..database import test_database    

# for this test database must be filled with data
from ..query import test_get_df_and_ts
