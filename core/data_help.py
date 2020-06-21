import pandas as pd
import string
import requests
import os
import re
import functools
from random import choice
from config import password
'''配置目录'''
passchar = '_$.;!~'+string.digits+string.ascii_letters
mail_mode=r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'


'''修饰器'''
def with_open(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            df_list = [pd.read_excel(i) for i in args]
        except FileNotFoundError as fnfe:
            print(fnfe)
            exit(0)
        try:
            func(*df_list, **kw)
        except Exception as e:
            print(e)
        finally:
            for i,v in enumerate(args):
                df_list[i].to_excel(args[i],index=False)
    return wrapper


'''一些正则'''
def mail_valid(mail):
    return re.match(mail_mode,mail)


'''DataFrame'''
def df_maker(cols, idxs):
    return pd.DataFrame({c:[c+str(i) for i in idxs] for c in cols}, index=idxs)

def addCol(df,name):
    if name not in df.columns:
        df.insert(len(df.columns),name,0)

def extract(s):
    sp = re.compile('[\u4e00-\u9fa5:：，,-]+')
    return sp.sub(' ',s).strip().split()

def get_df(filename, columns):
    with open(filename) as f:
        lines = f.readlines()

    lines = [extract(line) for line in lines if line]

    return pd.DataFrame(lines, columns=columns)

def write_to_file(df_list, file_name,prefix='./',mode='w'):
    with open(os.path.join(prefix,file_name), mode) as f:
        for df in df_list:
            for i in df.index:
                f.write(df.loc[i, 'username']+'---'+df.loc[i,'userpwd']+'\n')
                # if len(df_list)==2 and i == 25:
                #     f.write(df.loc[0, 'username']+'---'+df.loc[0,'userpwd']+'\n')

def append_to_df(df, filename = ''):
    if os.path.exists(filename):
        df_origin = pd.read_excel(filename)
        df_sum = df_origin.append(df,ignore_index=True)
        df_sum.fillna(0,inplace=True)
    else:
        df_sum = df
    df_sum.to_excel(filename, index=False)




'''generate'''
def generate_pw():
    if password:
        return password
    else:
        return ''.join([choice(passchar) for _ in range(12)])

def get_socket_pool():
    pools = requests.get('http://api.wandoudl.com/api/ip?app_key=a6cec112e480cc7b8790b118dd17cb5f&pack=0&num=20&xy=1&type=1&lb=\r\n&mr=1&').text.split()
    return pools

def generate_socket(pools):
    return choice(pools)


def generate_mail(df):
    addCol(df,'used')
    for i in df.index:
        if df.loc[i,'added'] and not df.loc[i,'used']:
            return i
            # df.to_excel('mail.xlsx')
            # return df.loc[i,'mail_add']
    return -1



# get_socket_pool()

