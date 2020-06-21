from core.bili_change import *


def notice_input(choices, text = '输入对应的编号后回车(不能有多余输入)'):
    '''choices是选项列表， text是开头提示文字'''
    for i,v in enumerate(choices):
        text+='\n%d:%s'%(i,choices[i])
    sel = input(text+'\n').strip()
    # assert(sel == '1' or sel == '0')
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
        add_all_mail(files[2],files[3])
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