from kep.quick_look import show_2016

def test_quick_look_show_2016_contains_GDP_value():
    echo = show_2016()
    assert 'GDP__bln_rub' in echo
    assert '2016' in echo 
    assert '85881.0' in echo