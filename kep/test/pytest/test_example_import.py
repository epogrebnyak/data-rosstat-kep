import pytest

try:
    import example_import
except:
    pytest.fail("example_import raised an exception!")