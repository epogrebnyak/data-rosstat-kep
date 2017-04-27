# -*- coding: utf-8 -*-
"""File access."""

import os
import tempfile

ENCODING = 'utf8'

class File():
    """Custom reader for dirty raw CSV file."""
    
    def __init__(self, path: str):
        """Set file path, raise error if file does not exist."""
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError(path)

    def __repr__(self):
        return os.path.normpath(self.path)

    def __yield_lines__(self):
        """Iterate over CSV file by line."""
        with open(self.path, 'r', encoding=ENCODING) as f:
            for line in f:
                if line.endswith('\n'):
                    yield line[0:-1]
                else:
                    yield line

    def read_text(self):
        """Read text from file."""
        return "\n".join(self.__yield_lines__())
       

class Tempfile():
    """Mimic localfile with *content_string* content.
    
       Usage:
           
           with Tempfile(content) as f:
               <do something with f>"""

    def __init__(self, content_string):
        with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as fp:
            fp.write(content_string)
        self.path = fp.name

    def __enter__(self):
        return self.path

    def __exit__(self, type, value, traceback):
        os.remove(self.path)
        
    @property 
    def name(self):
        return self.path
    
    def close(self):
        os.remove(self.path)