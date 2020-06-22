from core.bili_change import *


def notice_input(choices, text = '输入对应的编号后回车(不能有多余输入)，默认输入0'):
    '''choices是选项列表， text是开头提示文字'''
    for i,v in enumerate(choices):
        text+='\n%d:%s'%(i,choices[i])
    sel = input(text+'\n').strip()
    if not sel:
        sel = 0
    else:
        sel = int(sel)
    return sel

if __name__ == "__main__":
    files = ['data/account.txt', 'data/mail.txt', 'data/account.xlsx', 'data/mail.xlsx']
    choices = [
        '抽取B站账户',
        '抽取邮箱账户',
        '开始批量导入邮箱',
        '开始修改密码',
        '开始换绑邮箱',
        '依次进行0,1,2,3,4',
        '检查密码',
        '导出账号txt文本到指定目录',
        '生成gmail邮箱分身'
    ]
    cmd = notice_input(choices)
    if cmd == 5 or cmd == 0:
        extract_account()
    if cmd == 5 or cmd == 1:
        extract_mail()
    if cmd == 5 or cmd == 2:
        sel = notice_input(['添加全部邮箱', '仅添加账号绑定的邮箱','仅添加未绑定的邮箱'])
        input('将网易邮箱大师打开，弄到邮箱设置界面，再回来命令行敲回车。\n 然后迅速窗口切回网易邮箱大师，15s后会自动开始， 中间不能动鼠标也不能停止\n')
        time.sleep(15)
        if sel == 0 or sel == 1:
            add_all_mail(files[2])
        if sel == 0 or sel == 2:
            add_all_mail(files[3])
    if cmd == 5 or cmd == 3:
        sel = notice_input(['使用重置密码接口','使用修改密码接口'])
        change_password(files[2], sel=sel)
    if cmd == 5 or cmd == 4:
        change_mail(files[2],files[3])
    if cmd == 6:
        check_login(files[2])
    if cmd == 7:
        to_pcr()
    if cmd == 8:
        generate_gmail(files[3])