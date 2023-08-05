cd /d %~dp0

set PYTHON_VERSION=3.7
if EXIST %cd%\win32\Python (set PYTHON_DIR=%cd%\win32\Python) else (set PYTHON_DIR=%cd%\..\..\..\) 
%PYTHON_DIR%\python.exe -m pip install --user --upgrade numpy PyQt5

set PATH=%PYTHON_DIR%;%cd%\bin;%PATH%
set PYTHONPATH=%PYTHON_DIR%\lib;%PYTHON_DIR%\DLLs

FOR /F "tokens=* USEBACKQ" %%F IN (`%PYTHON_DIR%\python.exe -c "import os,PyQt5; print(os.path.dirname(PyQt5.__file__))"`) DO (SET PyQt5_DIR=%%F)
set PATH=%PyQt5_DIR%\Qt\bin;%PATH%
set QT_PLUGIN_PATH=%PyQt5_DIR%\Qt\plugins



bin\visusviewer.exe %*
