# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 23:43:56 2015

@author: Евгений
"""

# download dump sources from urls (not supported)

# dump source files to csv
csv = make_csv_for_source(source_file_list, file_parser_func)

# generate data strteam from source file
stream = get_data(csv, csv_reader_func, *args)

# write source to database
dump_to_database(stream, db_file)


# check updates validity (not supported)




