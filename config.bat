set MY_PATH=C:\Program Files\Python37\Script
set ENV_PATH=%PATH%;%MY_PATH%
@echo ====new environment��
@echo ��ʼ��װpy��
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
@echo ��ʼ����
call python set_config.py

@echo ��ʼ����
call python download.py
