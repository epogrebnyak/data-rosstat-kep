@echo off
REM make_docs.bat - generate simple documentation for src2 folder

SET "FOLDER=src2"

REM ----------- pydoc ----------- 

REM cleanup
del *.html

REM make individual html files 
pydoc -w ..\%FOLDER%\

REM rename them to src2.*.html - this name pattern is used in index file src2.html generated below
dir *.html /B > files.txt
for /f %%i in (files.txt) DO ren %%i src2.%%i

REM move to docs folder 
move *.html ..\docs\

REM make index file - src2.html
cd..
pydoc -w %FOLDER%

REM move to docs folder 
move %FOLDER%.html docs\

REM ----------- pycco ----------- 
cd %FOLDER%
dir *.py /B > files.txt
for /f %%i in (files.txt) DO pycco %%i -d ../docs/pycco
del files.txt
