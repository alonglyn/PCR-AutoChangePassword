@echo off
set FILENAME=.\downloads\python-3.7.6-webinstall.exe
echo %FILENAME%
if exist %FILENAME% (
    echo �Ѵ����ļ���ֱ�Ӱ�װ
) else (
    echo ��ʼ����python�� ��ȴ����
    powershell -Command "(new-object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.7.6/python-3.7.6-webinstall.exe','.\downloads\python-3.7.6-webinstall.exe')"
    echo ������أ��밲װ
    
)
%FILENAME%
echo ��ɰ�װ�� ����ӻ�������