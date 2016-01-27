@echo off
cd..
sphinx-apidoc -o docs/source/ kep --force

cd docs
call make html
start build/html/index.html
