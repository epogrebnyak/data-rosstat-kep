import unittest
from kep.input_getter.files import File, Tempfile

class Test_TempFile_File(unittest.TestCase):
    def test_read_one_line(self):     
        with Tempfile("abc") as f:
            assert "abc" == File(f).read_text()
    
    def test_read_lines_separated_by_signle_newline(self):     
        with Tempfile("a\nx") as f:
            assert "a\nx" == File(f).read_text()    