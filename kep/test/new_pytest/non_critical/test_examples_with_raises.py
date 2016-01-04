import pytest

def test_examples():
    # useful, but time-consuming

    #try:
    #    import kep_import
    #except:
    #    pytest.fail("kep_import raised an exception!")
                
    try:
        import example_use_data
    except:
        pytest.fail("example_use_data raised an exception!")