@echo off

set DIRNAME=.\downloads
if not exist %DIRNAME% md %DIRNAME%
set FILENAME=.\downloads\python-3.7.6-amd64.exe
set URL=https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64.exe
echo %FILENAME%
if exist %FILENAME% (
    echo installing
) else (
    echo downloading....
    powershell -Command "(new-object System.Net.WebClient).DownloadFile('%URL%','%FILENAME%')"
    echo installing....
    
)
%FILENAME%
echo finished
