# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT_PATH = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# data source
CURRENT_MONTH_DATA_FOLDER = os.path.join(PROJECT_ROOT_PATH, 'data', '2015', 'ind10')
DATA_FOLDER = CURRENT_MONTH_DATA_FOLDER

# database file
DB_FILE = os.path.join(PROJECT_ROOT_PATH, 'kep', 'database', 'kep.sqlite')

# output
OUTPUT_DIR    = os.path.join(PROJECT_ROOT_PATH, 'output')
PDF_FILE      = os.path.join(OUTPUT_DIR, 'monthly.pdf')
MD_PATH       = os.path.join(OUTPUT_DIR, 'images.md')
PNG_FOLDER    = os.path.join(OUTPUT_DIR, 'png')

XLSX_FILE     = os.path.join(OUTPUT_DIR, 'kep.xlsx')
XLS_FILE      = os.path.join(OUTPUT_DIR, 'kep.xls')
ANNUAL_CSV    = os.path.join(OUTPUT_DIR, 'data_annual.txt')
QUARTERLY_CSV = os.path.join(OUTPUT_DIR, 'data_qtr.txt')
MONTHLY_CSV   = os.path.join(OUTPUT_DIR, 'data_monthly.txt')

VARNAMES_FILE = os.path.join(OUTPUT_DIR, 'varnames.md')

# temp folder for testing
SUBFOLDER = os.path.join(PROJECT_ROOT_PATH, 'kep', 'test', 'temp')

# inspection files (not used now)
INSPECTION_FOLDER = os.path.join(PROJECT_ROOT_PATH,'kep', 'inspection')