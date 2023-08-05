cd /d %~dp0

if EXIST %cd%\win32\Python (set PYTHON_DIR=%cd%\win32\Python) else (set PYTHON_DIR=%cd%\..\..\..\) 
%PYTHON_DIR%\python.exe -m pip install --user --upgrade numpy

set PATH=%PYTHON_DIR%;%cd%\bin;%PATH%
set PYTHONPATH=%PYTHON_DIR%\lib;%PYTHON_DIR%\DLLs



bin\visus.exe %*
