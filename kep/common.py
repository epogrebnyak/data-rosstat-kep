# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 03:35:55 2017

@author: Евгений
"""
import os

ENCODING = 'utf8' 
    
class File():

    def __init__(self, path):
        if os.path.exists(path):
            self.path = path            
        else:
            raise FileNotFoundError(path)
     
    def __yield_lines__(self):
        with open(self.path, 'r', encoding = ENCODING) as f:
            for line in f:
                if line.endswith('\n'):
                     yield line[0:-1]
                else:
                     yield line                      
                     
    def read_text(self):
        """Read text from file."""
        return "\n".join(self.__yield_lines__())