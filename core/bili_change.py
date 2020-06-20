from selenium import webdriver
import pandas as pd
from random import choice
from core.bili_core import BiliBili,LoginException
from core.data_help import generate_pw, addCol, generate_socket, get_socket_pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

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


def change_password(df, mode = 0):
    browser = webdriver.Chrome()
    addCol(df,'pwdchanged')
    bl = BiliBili(browser)

    end = False
    print(df.head())
    try:
        for i in df.index:
            t = df.loc[i]
            if t['pwdchanged']:
                continue
            npw = generate_pw()
            print(t)
            bl.set_info(t['username'],t['userpwd'],t['mail_add'],npw)
            try:
                if mode:
                    print('使用修改密码模式')
                    bl.change_password()
                else:
                    print('使用重置密码模式')
                    bl.reset_password()
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

        
def change_mail(df, df_mail):
    browser = webdriver.Chrome()
    bl = BiliBili(browser)
    
    addCol(df,'mailchanged')
    
    addCol(df_mail,'used')

    print(df.head())
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

def check_login(df):
    browser = webdriver.Chrome()
    addCol(df,'available')
    bl = BiliBili(browser)

    print(df.head())
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