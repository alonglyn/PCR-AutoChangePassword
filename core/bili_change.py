from selenium import webdriver
import pandas as pd
from random import choice
import time
from core.bili_core import BiliBili,LoginException
from core.data_help import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from core.auto_mail import auto_add_mail

'''selenium启动函数'''
def lazy_capability():
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    return capa

def proxy_option():

    chromeOptions = webdriver.ChromeOptions()
    # 设置代理
    pools = get_socket_pool()
    socket = generate_socket(pools)
    chromeOptions.add_argument("--proxy-server=http://%s"%socket)

def lazy_browser():
    capa = lazy_capability()
    browser = webdriver.Chrome(desired_capabilities=capa)
    return browser


'''主要功能函数'''



def to_pcr():
    df = pd.read_excel('data/account.xlsx')
    bound = int(input('输入最后一个mana号的编号， 例如前30个号是mana号， 则输入30(默认为30)\n').strip())
    if not bound:
        bound = 30
    df1 = df.loc[0:bound]
    df2 = df.loc[bound:]
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

@with_open
def generate_gmail(df):
    while True:
        gmail = input('输入gmail邮箱，用户名不能包括.和+如alonglyn@gmail.com\n').strip()
        if mail_valid(gmail):
            break
        else:
            print('格式错误，请重新输入')
    (prefix, suffix) = gmail.split('@')
    for mid in ['.','+']:
        for i in range(len(prefix)):
            gmail_new = prefix[:i]+mid+prefix[i:]
            line = [None for _ in df.columns]
            line[0] = gmail_new+'@'+suffix
            addCol(df, 'added')
            df.loc[len(df)] = line
            df.loc[len(df)-1,'added'] = 1

@with_open
def change_password(df, sel):
    browser = webdriver.Chrome()
    addCol(df,'pwdchanged')
    bl = BiliBili(browser)
    end = False
    # print(df.head())
    try:
        for i in df.index:
            t = df.loc[i]
            if t['pwdchanged']:
                continue
            npw = generate_pw()
            # print(t)
            bl.set_info(t['username'],t['userpwd'],t['mail_add'],npw)
            try:
                if sel == 0:
                    print('使用重置密码模式')
                    bl.reset_password()
                else:
                    print('使用修改密码模式')
                    bl.change_password()
            except Exception as e:
                print(e)
                df.loc[i,'pwdchanged'] = -1
                break
            except LoginException as le:
                print(le)
                df.loc[i,'available'] = 0
                break
            else:
                df.loc[i,'userpwd'] = npw
                df.loc[i,'pwdchanged'] = 1
                df.loc[i,'available'] = 1
            
    except Exception as e:
        print('发生了其他错误')
        print(e)
    finally:
        # browser.close()
        pass

@with_open
def change_mail(df, df_mail):
    browser = webdriver.Chrome()
    bl = BiliBili(browser)
    addCol(df,'mailchanged')
    addCol(df_mail,'used')
    # print(df.head())
    try:
        for i in df.index:
            t = df.loc[i]
            if t['mailchanged']:
                continue
            try:
                bl.set_mail_df(df_mail)
                bl.set_info(t['username'],t['userpwd'],t['mail_add'])
                index_mail = bl.change_mail()
            except Exception as e:
                print(e)
                # cmd = input('发生错误是否继续?\n输入Y继续，直接输入回车结束检查错误')
                # if cmd.strip() != 'Y':
                #     break
                break
            else:
                df.loc[i,'mailchanged'] = 1
                df.loc[i,'mail_add'] = df_mail.loc[index_mail,'mail_add']
                df.loc[i,'mail_pwd'] = df_mail.loc[index_mail,'mail_pwd']
                # mailchanged
                df_mail.loc[i,'used'] = 1
    except Exception as e:
        print('发生了其他错误')
        print(e)
    finally:
        # browser.close()
        pass
@with_open
def check_login(df):
    browser = webdriver.Chrome()
    addCol(df,'available')
    bl = BiliBili(browser)

    # print(df.head())
    try:
        for i in df.index:
            t = df.loc[i]
            print(t)
            if t['available'] == 1:
                continue
            bl.set_info(t['username'],t['userpwd'],t['mail_add'])
            try:
                df.loc[i,'available'] = int(bl.check_login())
            except Exception as e:
                print(e)
            except LoginException as le:
                print(le)
                df.loc[i,'available'] = 0
                bl.logout()
                
            
    except Exception as e:
        print('发生了其他错误')
        print(e)
    finally:
        # browser.close()
        pass


@with_open
def add_all_mail(*args):
    input('将网易邮箱大师打开，弄到邮箱设置界面，再回来命令行敲回车。\n 然后迅速窗口切回网易邮箱大师，15s后会自动开始， 中间不能动鼠标也不能停止')
    time.sleep(15)
    for df in args:
        auto_add_mail(args)

def extract_account():    
    notice1 = '''
    根据账户账号密码的格式
    输入账号密码列顺序（默认0123）
    0:游戏账号
    1:游戏密码
    2:邮箱账号
    3:邮箱密码

    例如 游戏账号：pyuqwzd2esb游戏密码：qaw3sedrf邮箱账号:yz94904622@163.com邮箱密码:qh4561416
    则输入 0 1 2 3
    回车继续
    '''
    with open('data/account.txt','r') as f:
        print(f.readline())
    col_name = ['username','userpwd','mail_add','mail_pwd']
    columns = input(notice1).strip().split()
    if columns:
        assert(set(columns) == {'0','1','2','3'})
        
        
    else:
        columns = [0,1,2,3]
    columns = [col_name[int(i)] for i in columns]
    df = get_df('data/account.txt', columns)
    append_to_df(df, 'data/account.xlsx')

def extract_mail():    
    notice1 = '''
    根据账户账号密码的格式
    输入账号密码列顺序(默认0 1)
    0:邮箱账号
    1:邮箱密码

    例如 邮箱账号:yz94904622@163.com邮箱密码:qh4561416
    则输入 0 1
    回车继续
    '''
    with open('data/mail.txt','r') as f:
        print(f.readline())
    col_name = ['mail_add','mail_pwd']
    columns = input(notice1).strip().split()
    if columns:
        assert(set(columns) == {'0','1'})
        
    else:
        columns = [0,1]
    columns = [col_name[int(i)] for i in columns]


    # 抽取邮箱信息
    df = get_df('data/mail.txt', columns)
    append_to_df(df, 'data/mail.xlsx')