set MY_PATH=C:\Program Files\Python37\Script
set ENV_PATH=%PATH%;%MY_PATH%
@echo ====new environment：
@echo 开始安装py包
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
@echo 开始配置
call python set_config.py

@echo 开始下载
call python download.py
