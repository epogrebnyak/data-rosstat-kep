# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:07:40 2017

@author: PogrebnyakEV
"""

import os
def test_create_file(tmpdir):
    # tmpdir is defined internally in pytest
    # described here: https://docs.pytest.org/en/latest/tmpdir.html#the-tmpdir-fixture
    # see also: http://stackoverflow.com/questions/36070031/creating-a-temporary-directory-in-pytest
    p = tmpdir.join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
    #assert 0
    
