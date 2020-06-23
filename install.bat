@echo off
set FILENAME=.\downloads\python-3.7.6-webinstall.exe
echo %FILENAME%
if exist %FILENAME% (
    echo 已存在文件，直接安装
) else (
    echo 开始下载python， 请等待完成
    powershell -Command "(new-object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.7.6/python-3.7.6-webinstall.exe','.\downloads\python-3.7.6-webinstall.exe')"
    echo 完成下载，请安装
    
)
%FILENAME%
echo 完成安装， 请添加环境变量