from kep.importer.csv2db import import_csv
from kep.paths import CURRENT_MONTH_DATA_FOLDER

def update_database_to_current_month_folder():
    import_csv(CURRENT_MONTH_DATA_FOLDER)