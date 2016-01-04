# -*- coding: utf-8 -*-
"""Import data from Word files or raw CSV to database and dump outputs."""

import kep 
data_folder = "data/2015/ind11"

kep.update_db(data_folder)
kep.update_output()