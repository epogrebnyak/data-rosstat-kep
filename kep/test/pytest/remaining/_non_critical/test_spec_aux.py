# test a function in module

from kep.file_io.specification import _adjust_path
def test__adjust_path():
    assert _adjust_path(os.path.join('temp', '_config.txt'), 'new.txt') == os.path.join('temp', 'new.txt')   

