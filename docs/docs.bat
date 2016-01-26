@echo off
cd..
sphinx-apidoc -o docs/source/ kep --force

cd docs
make html
start docs/build/html/index.html
