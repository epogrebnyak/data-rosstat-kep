import unittest
import files

class Test_TempFile_File(unittest.TestCase):
    def test_read_one_line(self):     
        with files.Tempfile("abc") as f:
            assert "abc" == files.File(f).read_text()
    
    def test_read_lines_separated_by_signle_newline(self):     
        with files.Tempfile("a\nx") as f:
            assert "a\nx" == files.File(f).read_text()    