Folder structure:

\_package - end-to-end tests
\_modules - testing of key modules (mainly data import)
\_non_critical - less important tests (usually data retrieval and small doctests)
\_failing - test with problems, excluded from testing suit 


Comments about structure of testing suit:

a) We have tests that test all of package functionality and module levels
Package functionality is in '_package' folder, other tests in this folder for now.

b) We can run import and query/retrieval of data using:
- variables as input (testing core algorightms)
- configuaration and data files as input (testing files import too)

c) First testing option is running tets import with one specification file. 
Second option is using supplementary spec files listed in a config file. 

-----

use yield fixture

```
@pytest.yield_fixture
def yaml_docfile():
    # Create resource
    doc = """- Something looking like a yaml
- Но обязательно с русским текстом
---
key1 : with two documents
key2 : который будет глючить с кодировкой."""

    p = docstring_to_file(doc, "_test_yaml_doc.txt")

    # Execute the test passing this tuple as yaml_docfile
    yield (p, doc)

    # Cleanup resource
    os.remove("_test_yaml_doc.txt")

def test_io_fixture(yaml_docfile):
    p, doc = yaml_docfile

    assert doc == "\n".join([x[0] for x in yield_csv_rows(p)])
    y = _get_yaml(p)
    assert y[0][0] == 'Something looking like a yaml'
```

-----
using module cleanup:

```
# Here you create the variable and assign it to "module", which is the current module
def setup_module(module):
    module.a = 1

# Here you can access the variable defined in setup.
def test_a_is_1():
    assert a == 1

# Here you can perform some cleanup, for example removing files
def teardown_module(module):
    pass
```