import pytest

def test_examples():

    # useful, but time-consuming:
    #
    #try:
    #    import kep_import
    #except:
    #    pytest.fail("kep_import raised an exception!")
                
    try:
        import kep_example
    except:
        pytest.fail("kep_example.py raised an exception!")