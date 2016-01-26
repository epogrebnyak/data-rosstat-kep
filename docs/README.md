Generating documentation using Sphinx
=====================================

Installation
------------

To generate docs, you need Sphinx

    pip install sphinx

Or even better, use a development virtual environment:

    pip install -r requirements-dev.txt

How to generate docs
--------------------

1. From the root directory of the project, update auto-generated *\*.rst* files

        sphinx-apidoc -o docs/source/ kep --force

2. Make HTML using makefile

        cd docs
        make html

How to view HTML docs
---------------------

1. Run simple HTTP server

        cd docs/build/html
        python -m http.server

2. Open in browser: <http://localhost:8000/>

3. Alternatively start ```docs/build/html/index.html``` in browser.

Batch file
----------

Operations above are handled by ```docs.bat```

```
cd..
sphinx-apidoc -o docs/source/ kep --force

cd docs
make html
start docs/build/html/index.html
```
