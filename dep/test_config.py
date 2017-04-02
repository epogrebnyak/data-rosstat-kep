import os
from config import CURRENT_MONTH_DATA_FOLDER, OUTPUT_DIR, PARSING_DEFINITIONS_FOLDER

def test_config():
    for p in [CURRENT_MONTH_DATA_FOLDER, OUTPUT_DIR, PARSING_DEFINITIONS_FOLDER]:
        assert os.path.exists(p)
        