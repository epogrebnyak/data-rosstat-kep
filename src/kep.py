# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 02:44:07 2015

@author: Евгений
"""

from doc2db.batch import csv_to_database 
import doc2db.word

p = "../data/1-07/1-07.doc"
csv_to_database(p)
