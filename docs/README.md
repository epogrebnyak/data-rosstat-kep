Generating documentation using Sphinx
=====================================

Installation
------------

To generate docs, you need Sphinx

    pip install sphinx


How to generate docs
--------------------

1. Update auto-generated *\*.rst* files from code

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
