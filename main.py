from core.bili_change import *
from core.data_help import notice_input



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
        sel2 = notice_input(['0.5s','1s','3s','5s','10s'], '登录等待时间选择（默认选0）(一般默认即可比较快， 网络不好建议选3s以上）')
        print('将网易邮箱大师打开，弄到邮箱设置界面，全屏，再回来命令行选择自动启动倒计时时间')
        sel3 = notice_input(['5s','10s','15s','20s',],'倒计时时间选择(默认0)。\n 启动倒计时后， 迅速切换到网易邮箱大师界面，不动，中间不能动鼠标也不能停止直到执行完毕\n')
        time.sleep((sel3+1)*5)
        if sel == 0 or sel == 1:
            add_all_mail(files[2], time_delay=sel2)
        if sel == 0 or sel == 2:
            add_all_mail(files[3], time_delay=sel2)
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
        s = input('输入开始编号和结束编号，中间用空格隔开（默认为:1 100)\n会生成如alonglyn+100@gmail.com的分身账号\n').strip()
        if not s:
            generate_gmail(files[3])
        else:
            s = s.split(' ')
            assert(len(s)==2)
            generate_gmail(files[3],left=int(s[0]),right=int(s[1]))