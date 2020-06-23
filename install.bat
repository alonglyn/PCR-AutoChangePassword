@echo off
set FILENAME=.\downloads\python-3.7.6-amd64-webinstall.exe
set URL=https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64-webinstall.exe
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

游戏账号：xanbesjgfp，游戏密码：63854566邮箱rg976355@163.com密码ie6930