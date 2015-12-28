'''
tests for kep.importer.converter

needs win32com.client for check
'''
import os
from kep.importer.converter.word import make_csv, get_csv_filename, folder_to_csv
from kep.paths import DATA_FOLDER, PROJECT_ROOT_PATH

expected_csv_filename = os.path.join(PROJECT_ROOT_PATH, 'data', '2015', 'ind10', 'tab.csv')

def test_get_csv_filename():
    assert expected_csv_filename == get_csv_filename(DATA_FOLDER)

def test_folder_to_csv():
    if os.path.isfile(expected_csv_filename):
        os.remove(expected_csv_filename)
    folder_to_csv(DATA_FOLDER)
    assert os.path.isfile(expected_csv_filename)
    os.remove(expected_csv_filename)

def test_make_csv_01_default_no_overwrite():
    if os.path.isfile(expected_csv_filename):
        os.remove(expected_csv_filename)
    make_csv(DATA_FOLDER)
    assert os.path.isfile(expected_csv_filename)

def test_make_csv_02_overwrite():
    if os.path.isfile(expected_csv_filename):
        os.remove(expected_csv_filename)
    file_csv = open(expected_csv_filename, 'w')
    file_csv.write("test_line")
    file_csv.close()
    make_csv(DATA_FOLDER)
    file_csv = open(expected_csv_filename, 'r')
    readed_line = file_csv.readline()
    assert "test_line" == readed_line

    make_csv(DATA_FOLDER, overwrite=True)
    file_csv = open(expected_csv_filename, 'r')
    readed_line = file_csv.readline()
    assert "test_line" != readed_line