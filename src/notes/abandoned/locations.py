
#---------------------


# locate current file config.py
CODE_FOLDER, _ = os.path.split(__file__)
# one level up
PROJECT_FOLDER, _ = os.path.split(CODE_FOLDER)
# data dir is in root folder
DATA_FOLDER = os.path.join(PROJECT_FOLDER, 'data')


#find latest data folder

def subdirectories(root_dir):
    return [f for f in os.listdir(root_dir)
           if not os.path.isfile(os.path.join(root_dir,f))]


def max_year():
    dirs = subdirectories(DATA_FOLDER)
    return max([int(f) for f in dirs if f.startswith("20")])


def max_month():
    year_dir = os.path.join(DATA_FOLDER, str(max_year()))
    dirs = subdirectories(year_dir)
    return max([int(f.replace('ind','')) for f in dirs if f.startswith("ind")])


def current_month_data_dir(year, month):
    month_dir = 'ind'+str(month).zfill(2)
    return os.path.join(DATA_FOLDER, str(year), month_dir)

CURRENT_MONTH = max_year(), max_month()
# may override manually below
# CURRENT_MONTH = 2017, 2

CURRENT_MONTH_DATA_FOLDER = current_month_data_dir(*CURRENT_MONTH)
CSV_FILENAME = 'tab.csv'
CSV_PATH = os.path.join(CURRENT_MONTH_DATA_FOLDER, CSV_FILENAME)


#---------------------
