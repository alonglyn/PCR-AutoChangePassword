import pandas as pd
from core.data_help import write_to_file
import os


if __name__ == "__main__":
    df = pd.read_excel('data/account.xlsx')
    df1 = df.loc[0:29]
    df2 = df.loc[30:]
    while True:
        prefix = input('输入脚本需要代码所在目录绝对路径,自动生成到目标目录下，如果不输入请直接回车， 账号密码会放在本目录\n').strip()
        if not prefix:
            break
        if  os.path.isdir(prefix):
            break
        else:
            print('未找到目标目录， 请输入正确的目录或者直接回车\n')
    
    write_to_file([df1],'pcr_farm_mana.txt',prefix)
    write_to_file([df2],'pcr_farm_zb.txt',prefix)
    write_to_file([df1,df2],'pcr_farm_all.txt',prefix)
