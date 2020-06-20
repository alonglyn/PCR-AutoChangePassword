from core.data_help import *
from core.bili_change import change_password, change_mail, check_login
from core.auto_mail import auto_add_mail
import time
import pandas as pd

def and_event(tags, l):
    for i in l:
        if not tags[i]:
            return False
    return True
def message(choices, i):
    return '\n%d:%s'%(i,choices[i])

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



if __name__ == "__main__":
    files = ['data/account.txt', 'data/mail.txt', 'data/account.xlsx', 'data/mail.xlsx']
    
    choices = {
        0:'抽取B站账户',
        1:'抽取邮箱账户',
        2:'开始批量导入邮箱',
        3:'开始修改密码',
        4:'开始换绑邮箱',
        5:'依次进行0,1,2,3,4',
        6:'检查密码'
    }
    msg = '输入对应数字后回车'
    for k,v in choices.items():
        msg += '\n%d:%s'%(k,v)
    
    while True:
        cmd = input(msg+'\n')
        assert(cmd.strip())
        try:
            cmd = int(cmd)
        except Exception as e:
            print(e)
            print('请输入正确的格式')
        else:
            break
    df_account = pd.DataFrame()
    df_mail = pd.DataFrame()
    if cmd == 5 or cmd == 0:
        extract_account()

    if cmd == 5 or cmd == 1:
        df_mail = extract_mail()

    
    if cmd == 5 or cmd == 2:
        try:
            df_account = pd.read_excel(files[2])
            df_mail = pd.read_excel(files[3])
        except FileNotFoundError as fnfe:
            print(fnfe)
            exit(0)
        try:
            input('将网易邮箱大师打开，弄到邮箱设置界面，再回来命令行敲回车。\n 然后迅速窗口切回网易邮箱大师，15s后会自动开始， 中间不能动鼠标也不能停止')
            time.sleep(15)
            dfList = [df_account,df_mail]
            for ind in range(2):
                auto_add_mail(dfList[ind])
        except Exception as e:
            print(e)
        finally:
            df_account.to_excel(files[2],index=False)
            df_mail.to_excel(files[3],index=False)
    if cmd == 5 or cmd == 3:
        try:
            df_account = pd.read_excel(files[2])
        except FileNotFoundError as fnfe:
            print(fnfe)
            exit(0)
        try:
            sel = input('输入0使用重置密码接口\n输入1使用修改密码接口\n(两个接口对IP的限制不统一， 一个结束了可以换另一个）、\n').strip()
            assert(sel == '1' or sel == '0')
            sel=int(sel)
            change_password(df_account,sel)
        except Exception as e:
            print(e)
        finally:
            df_account.to_excel(files[2],index=False)
    if cmd == 5 or cmd == 4:
        try:
            df_account = pd.read_excel(files[2])
            df_mail = pd.read_excel(files[3])
        except FileNotFoundError as fnfe:
            print(fnfe)
            exit(0)
        try:
            change_mail(df_account,df_mail)
        except Exception as e:
            print(e)
        finally:
            df_account.to_excel(files[2],index=False)
            df_mail.to_excel(files[3],index=False)
    if cmd == 6:
        try:
            df_account = pd.read_excel(files[2])
        except FileNotFoundError as fnfe:
            print(fnfe)
            exit(0)
        try:
            check_login(df_account)
        except Exception as e:
            print(e)
        finally:
            df_account.to_excel(files[2],index=False)